import pygame

from src import shared, utils
from src.enums import State
from src.floor import Floor


class EditorState:
    def __init__(self) -> None:
        shared.camera = utils.Camera()
        self.world_placement_handler = utils.WorldPlacementHandler()
        self.temp = utils.load_image("assets/floor.png", False)

    def on_game_state(self):
        if shared.kp[pygame.K_e]:
            shared.next_state = State.GAME

    def update(self):
        self.world_placement_handler.update(Floor, self.temp)
        self.on_game_state()

    def draw(self):
        self.world_placement_handler.draw()
        shared.world_map.draw()
