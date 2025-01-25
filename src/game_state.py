import pygame

from src import shared, utils
from src.enums import State


class GameState:
    def __init__(self) -> None:
        self.clean_up_world()
        self.entities = shared.world_map.load()

    def clean_up_world(self):
        utils.Collider.all_colliders.clear()

    def update(self):
        for entity in self.entities:
            entity.update()

    def draw(self):
        for entity in self.entities:
            entity.draw()
