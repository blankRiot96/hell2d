from os import walk

import pygame

from src import shared, utils
from src.enums import State

CAMERA_SPEED = 100


class LobbyEditorState:
    def __init__(self) -> None:
        self.world_placement_handler = utils.WorldPlacementHandler(
            world_map=shared.lobby_map, starting_keybinds_file_name="1"
        )
        self.goto_menu_btn = utils.Button("< Menu", pygame.Rect(20, 20, 140, 30))

    def scroll_camera(self):
        dx = shared.keys[pygame.K_d] - shared.keys[pygame.K_a]
        dy = shared.keys[pygame.K_s] - shared.keys[pygame.K_w]
        dv = pygame.Vector2(dx, dy)

        if dv:
            dv.normalize_ip()

        shared.camera.offset += dv * CAMERA_SPEED * shared.dt

    def update(self):
        self.goto_menu_btn.update()
        if self.goto_menu_btn.just_clicked:
            shared.next_state = State.MENU
            shared.lobby_map.dump()

        if self.goto_menu_btn.is_hovering:
            return
        self.world_placement_handler.update()
        if not self.world_placement_handler.command_bar._command_being_typed:
            self.scroll_camera()

    def draw(self):
        shared.lobby_map.draw()
        if not self.goto_menu_btn.is_hovering:
            self.world_placement_handler.draw()

        self.goto_menu_btn.draw()
