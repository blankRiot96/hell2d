import pygame

from src import shared, utils
from src.enums import State
from src.floor import Floor
from src.player import Player


class GameState:
    def __init__(self) -> None:
        self.clean_up_world()
        self.player = Player()
        self.entities = shared.world_map.load()

    def clean_up_world(self):
        utils.Collider.all_colliders.clear()

    def on_editor_state(self):
        if shared.kp[pygame.K_e]:
            shared.next_state = State.EDITOR

    def update(self):
        self.player.update()
        self.on_editor_state()

        for entity in self.entities:
            entity.update()

    def draw(self):
        self.player.draw()

        for entity in self.entities:
            entity.draw()
