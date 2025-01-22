from __future__ import annotations

import functools
import sys
import time
import typing as t
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path

import pygame
import ujson

from src import shared


class ItemSelector:
    """Lets you select an item"""

    PADDING = 20
    BOX_PADDING = 5

    def __init__(
        self, topleft, items: dict[str, pygame.Surface], item_scale=1.0, colors=None
    ) -> None:
        if colors is None:
            colors = {
                "bg": (100, 100, 100),
                "box": (50, 50, 50),
                "hover": (100, 100, 0),
            }

        self.colors = colors
        self.pos = pygame.Vector2(topleft)
        self.items = items
        self.currently_selected_item = list(items)[0]

        self.is_being_interacted_with = False
        self.scale_items(item_scale)
        self.create_background_image()

    def scale_items(self, item_scale):
        if item_scale != 1:
            for item_name, image in self.items.items():
                self.items[item_name] = pygame.transform.scale_by(image, item_scale)

    def create_background_image(self):
        total_width = ItemSelector.BOX_PADDING + ItemSelector.PADDING
        max_height = 0
        for item in self.items.values():
            total_width += (
                item.get_width() + ItemSelector.PADDING + ItemSelector.BOX_PADDING
            )
            if item.get_height() > max_height:
                max_height = item.get_height()

        self.bg = pygame.Surface(
            (total_width, max_height + 4 * ItemSelector.BOX_PADDING)
        )
        self.bg.fill(self.colors["bg"])

    def update(self):
        pass

    def draw(self):
        self.is_being_interacted_with = False
        shared.screen.blit(self.bg, self.pos)

        acc_x = 0
        for item_name, item_image in self.items.items():
            rect = pygame.Rect(
                self.pos.x + acc_x + ItemSelector.PADDING,
                self.pos.y + ItemSelector.BOX_PADDING,
                item_image.get_width() + 2 * ItemSelector.BOX_PADDING,
                self.bg.get_height() - (2 * ItemSelector.BOX_PADDING),
            )

            if rect.collidepoint(shared.mouse_pos):
                self.is_being_interacted_with = True
                color = self.colors["hover"]

                if shared.mjp[0]:
                    self.currently_selected_item = item_name
            else:
                color = self.colors["box"]

            pygame.draw.rect(shared.screen, color, rect)
            shared.screen.blit(
                item_image,
                (
                    self.pos.x
                    + acc_x
                    + ItemSelector.BOX_PADDING
                    + ItemSelector.PADDING,
                    self.pos.y + 2 * ItemSelector.BOX_PADDING,
                ),
            )

            acc_x += (
                item_image.get_width() + ItemSelector.BOX_PADDING + ItemSelector.PADDING
            )


class MapItem:
    """Placeholder for the real entities"""

    def __init__(self, pos, entity_type, image) -> None:
        self.pos = pygame.Vector2(pos)
        self.image = image
        self.rect = self.image.get_rect(topleft=self.pos)
        self.entity_type = entity_type

    def draw(self):
        shared.screen.blit(self.image, shared.camera.transform(self.pos))


class WorldMap:
    """The entire world, categorized in a map."""

    def __init__(self, file_path: str | Path, entity_classes: list[t.Type]) -> None:
        # self.chunks: dict[tuple[int, int], list[WorldEntity]] = {}

        self.file_path = file_path
        self.entity_classes = entity_classes
        self.reverse_entity_class_map = {
            entity_type.__name__: entity_type for entity_type in self.entity_classes
        }

        self.load_map_items()

    def load_map_items(self):
        self.entities: list[MapItem] = []

        with open(self.file_path) as f:
            schema = ujson.load(f)

        for class_name, position in schema:
            cls = self.reverse_entity_class_map[class_name]
            image = cls.get_placeholder_img()
            self.entities.append(MapItem(position, cls, image))

    def dump(self, file_path: str | Path) -> None:
        jsonable_map = [
            [entity.entity_type.__name__, (entity.pos.x, entity.pos.y)]
            for entity in self.entities
        ]

        with open(file_path, "w") as f:
            ujson.dump(jsonable_map, f, indent=2)

    def load(self) -> list:
        entities = []
        with open(self.file_path) as f:
            json_map = ujson.load(f)
            for entity_class, entity_pos in json_map:
                entity = self.reverse_entity_class_map[entity_class](entity_pos)
                entities.append(entity)

        return entities

    def draw(self):
        for entity in self.entities:
            entity.draw()


class PlacementMode(Enum):
    FREE = auto()
    GRID = auto()


class WorldPlacementHandler:
    """Handles the placement of entities into the world"""

    def __init__(self) -> None:
        self.mode = PlacementMode.FREE

        self.current_entity_pos = pygame.Vector2()
        self.current_entity_type = None
        self.current_entity_image = pygame.Surface((50, 50))

        self._last_placed_pos = pygame.Vector2(0, 0)

    def on_place(self):
        clicked = False

        potential_center = self.current_entity_pos + (
            pygame.Vector2(self.current_entity_image.get_size()) / 2
        )
        if shared.mouse_press[0] and (
            abs(self._last_placed_pos.x - potential_center.x) > 50
            or abs(self._last_placed_pos.y - potential_center.y) > 30
        ):
            clicked = True

        for event in shared.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True

        if not clicked:
            return

        self._last_placed_pos = pygame.Vector2(
            self.current_entity_image.get_rect(topleft=self.current_entity_pos).center
        )
        shared.world_map.entities.append(
            MapItem(
                self.current_entity_pos,
                self.current_entity_type,
                self.current_entity_image,
            )
        )

    def update(self, current_entity_type, current_entity_image):
        if self.mode == PlacementMode.FREE:
            self.current_entity_pos = shared.mouse_pos + shared.camera.offset

        self.current_entity_type = current_entity_type
        self.current_entity_image = current_entity_image.copy()
        self.current_entity_image.set_alpha(150)

        self.on_place()

    def draw(self):
        shared.screen.blit(
            self.current_entity_image, shared.camera.transform(self.current_entity_pos)
        )


class Camera:
    def __init__(self) -> None:
        self.offset = pygame.Vector2()

    def attach_to(self, pos, smoothness_factor=0.08):
        self.offset.x += (
            pos[0] - self.offset.x - (shared.srect.width // 2)
        ) * smoothness_factor
        self.offset.y += (
            pos[1] - self.offset.y - (shared.srect.height // 2)
        ) * smoothness_factor

    def transform(self, pos) -> pygame.Vector2 | pygame.Rect | pygame.FRect:
        if isinstance(pos, pygame.Rect) or isinstance(pos, pygame.FRect):
            return pos.move(*-self.offset)
        return pygame.Vector2(pos[0] - self.offset.x, pos[1] - self.offset.y)


def get_asset_path(path):
    if hasattr(sys, "_MEIPASS"):
        return Path(getattr(sys, "_MEIPASS")) / path
    return path


@functools.lru_cache
def load_image(
    path: str,
    alpha: bool,
    bound: bool = False,
    scale: float = 1.0,
    smooth: bool = False,
) -> pygame.Surface:
    img = pygame.image.load(get_asset_path(path))
    if scale != 1.0:
        if smooth:
            img = pygame.transform.smoothscale_by(img, scale)
        else:
            img = pygame.transform.scale_by(img, scale)
    if bound:
        img = img.subsurface(img.get_bounding_rect()).copy()
    if alpha:
        return img.convert_alpha()
    return img.convert()


@functools.lru_cache
def load_font(name: str | None, size: int) -> pygame.Font:
    return pygame.Font(get_asset_path(name), size)


class Gravity:
    """Applies gravity"""

    def __init__(self) -> None:
        self.velocity = 0.0

    def update(self):
        self.velocity += shared.WORLD_GRAVITY * shared.dt
        if self.velocity > shared.MAX_FALL_VELOCITY:
            self.velocity = shared.MAX_FALL_VELOCITY


class CollisionSide(Enum):
    RIGHT = auto()
    LEFT = auto()
    TOP = auto()
    BOTTOM = auto()


@dataclass
class CollisionData:
    colliders: dict[CollisionSide, Collider]


class Collider:
    """Have as attribute to entity"""

    all_colliders: list[t.Self] = []

    def __init__(self, pos, size) -> None:
        self.pos = pygame.Vector2(pos)
        self.size = size
        Collider.all_colliders.append(self)

    @property
    def rect(self) -> pygame.FRect:
        return pygame.FRect(self.pos, self.size)

    def get_collision_data(self, dx, dy) -> CollisionData:
        """Returns datapacket containing collisiondata"""

        colliders = defaultdict(list)
        possible_x = []
        possible_y = []

        for collider in Collider.all_colliders:
            if collider is self:
                continue

            is_colliding_x = self.rect.move(dx, 0).colliderect(collider.rect)
            is_colliding_y = self.rect.move(0, dy).colliderect(collider.rect)

            side = None
            if is_colliding_x and dx < 0:
                possible_x.append(collider.rect.right)
                side = CollisionSide.LEFT
            elif is_colliding_x and dx > 0:
                possible_x.append(collider.pos.x - self.size[0])
                side = CollisionSide.RIGHT

            if is_colliding_y and dy < 0:
                possible_y.append(collider.rect.bottom)
                side = CollisionSide.TOP
            elif is_colliding_y and dy > 0:
                possible_y.append(collider.pos.y - self.size[1])
                side = CollisionSide.BOTTOM

            if side is not None:
                colliders[side].append(collider)

        if possible_x:
            if dx < 0:
                self.pos.x = max(possible_x)
            else:
                self.pos.x = min(possible_x)

        if possible_y:
            if dy < 0:
                self.pos.y = max(possible_y)
            else:
                self.pos.y = min(possible_y)

        x_index = possible_x.index(self.pos.x) if possible_x else None
        y_index = possible_y.index(self.pos.y) if possible_y else None

        snapped = {}

        for side in (CollisionSide.LEFT, CollisionSide.RIGHT):
            if x_index is not None and colliders[side]:
                snapped[side] = colliders[side][x_index]

        for side in (CollisionSide.TOP, CollisionSide.BOTTOM):
            if y_index is not None and colliders[side]:
                snapped[side] = colliders[side][y_index]

        return CollisionData(colliders=snapped)

    def draw(self):
        pygame.draw.rect(
            shared.screen, "red", shared.camera.transform(self.rect), width=1
        )


class Timer:
    """
    Class to check if time has passed.
    """

    def __init__(self, time_to_pass: float):
        self.time_to_pass = time_to_pass
        self.start = time.perf_counter()

    def reset(self):
        self.start = time.perf_counter()

    def tick(self) -> bool:
        if time.perf_counter() - self.start > self.time_to_pass:
            self.start = time.perf_counter()
            return True
        return False
