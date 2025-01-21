import pygame

from src import shared, utils
from src.enums import State
from src.floor import Floor

CAMERA_SPEED = 100


class EditorState:
    def __init__(self) -> None:
        self.world_placement_handler = utils.WorldPlacementHandler()
        self.temp = utils.load_image("assets/floor.png", False)

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
        self.scroll_camera()
        self.world_placement_handler.update(Floor, self.temp)
        self.on_game_state()

    def draw(self):
        self.world_placement_handler.draw()
        shared.world_map.draw()
