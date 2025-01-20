import functools
import sys
import time
import typing as t
from enum import Enum, auto
from pathlib import Path
from types import new_class

import pygame

from src import shared


class WorldEntity:
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

    def __init__(self) -> None:
        # self.chunks: dict[tuple[int, int], list[WorldEntity]] = {}
        self.entities: list[WorldEntity] = []

    def to_real_entities(self):
        return [entity.entity_type(entity.pos) for entity in self.entities]

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

    def on_place(self):
        clicked = False
        for event in shared.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True

        if not clicked:
            return

        shared.world_map.entities.append(
            WorldEntity(
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

    def attach_to(self, pos):
        self.offset.x += (pos[0] - self.offset.x - (shared.srect.width // 2)) * 0.08
        self.offset.y += (pos[1] - self.offset.y - (shared.srect.height // 2)) * 0.08

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

    def get_collision_sides(self, dx, dy) -> set[CollisionSide]:
        """Returns empty set if no collision"""

        sides = set()
        for collider in Collider.all_colliders:
            if collider is self:
                continue

            c = lambda x, y: self.rect.move(x, y).colliderect(collider.rect)

            if c(dx, 0) and dx < 0:
                new_pos = collider.rect.right + 1
                if new_pos > self.pos.x:
                    self.pos.x = new_pos

                sides.add(CollisionSide.LEFT)
            elif c(dx, 0) and dx > 0:
                new_pos = collider.pos.x - self.size[0] - 1
                if new_pos < self.pos.x:
                    self.pos.x = new_pos

                sides.add(CollisionSide.RIGHT)

            if c(0, dy) and dy < 0:
                new_pos = collider.rect.bottom
                if new_pos > self.pos.y:
                    self.pos.y = new_pos

                sides.add(CollisionSide.TOP)
            elif c(0, dy) and dy > 0:
                new_pos = collider.pos.y - self.size[1]
                if new_pos < self.pos.y:
                    self.pos.y = new_pos

                sides.add(CollisionSide.BOTTOM)

        return sides

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
