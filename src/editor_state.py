import pygame

from src import shared, utils
from src.enums import State
from src.firepit import FirePit

CAMERA_SPEED = 100


class EditorState:
    def __init__(self) -> None:
        self.firepit = FirePit()
        self.world_placement_handler = utils.WorldPlacementHandler(
            starting_keybinds_file_name="1", bottom_bounds=shared.FIRE_PIT_START_Y
        )

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
        self.firepit.update()
        self.world_placement_handler.update()
        if not self.world_placement_handler.command_bar._command_being_typed:
            self.scroll_camera()
            shared.camera.bound()
            self.on_game_state()

    def draw(self):
        self.firepit.draw()
        shared.world_map.draw()
        self.world_placement_handler.draw()
