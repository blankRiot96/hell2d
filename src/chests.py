import pygame

from src import shared, utils


class Chest:
    """Chest that pops out random items to pick up"""

    PLACEHOLDER_IMG_PATH = "assets/chest.png"

    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.image = utils.load_image("assets/chest.png", False)

    @classmethod
    def get_placeholder_img(cls) -> pygame.Surface:
        return utils.load_image("assets/chest.png", True)

    def update(self):
        pass

    def draw(self):
        shared.screen.blit(self.image, shared.camera.transform(self.pos))
