from src import shared, utils
from src.enums import State
from src.player import Player


class GameState:
    def __init__(self) -> None:
        self.player = Player()
        self.floor = utils.Collider(pos=(100, 400), size=(600, 70))

    def update(self):
        self.player.update()

    def draw(self):
        self.player.draw()
        self.floor.draw()
