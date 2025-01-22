import itertools

import pygame

from src import shared, utils
from src.enums import State

CAMERA_SPEED = 100


class EditorState:
    def __init__(self) -> None:
        self.item_selector = utils.ItemSelector(
            topleft=(10, 10),
            items={
                cls.__name__: cls.get_placeholder_img()
                for cls in shared.world_map.entity_classes
            },
            item_scale=0.75,
        )
        self.world_placement_handler = utils.WorldPlacementHandler()

    def on_game_state(self):
        if shared.kp[pygame.K_e]:
            shared.world_map.dump("assets/map.json")
            shared.next_state = State.GAME

    def scroll_camera(self):
        dx = shared.keys[pygame.K_d] - shared.keys[pygame.K_a]
        dy = shared.keys[pygame.K_s] - shared.keys[pygame.K_w]
        dv = pygame.Vector2(dx, dy)

        if dv:
            dv.normalize_ip()

        shared.camera.offset += dv * CAMERA_SPEED * shared.dt

    def update(self):
        self.item_selector.update()
        self.scroll_camera()

        if not self.item_selector.is_being_interacted_with:
            cls = shared.world_map.reverse_entity_class_map[
                self.item_selector.currently_selected_item
            ]
            self.world_placement_handler.update(cls, cls.get_placeholder_img())
        self.on_game_state()

    def draw(self):
        self.item_selector.draw()
        if not self.item_selector.is_being_interacted_with:
            self.world_placement_handler.draw()
        shared.world_map.draw()
