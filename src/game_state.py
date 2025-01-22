import pygame

from src import shared, utils
from src.enums import State


class GameState:
    def __init__(self) -> None:
        self.clean_up_world()
        self.entities = shared.world_map.load()

    def clean_up_world(self):
        utils.Collider.all_colliders.clear()

    def on_editor_state(self):
        if shared.kp[pygame.K_e]:
            shared.next_state = State.EDITOR

    def update(self):
        self.on_editor_state()

        for entity in self.entities:
            entity.update()

    def draw(self):
        for entity in self.entities:
            entity.draw()
