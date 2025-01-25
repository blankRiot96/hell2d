import pygame

from src import shared, utils


class Floor:
    PLACEHOLDER_IMG_PATH = "assets/floor.png"

    def __init__(self, pos) -> None:
        self.image = utils.load_image("assets/floor.png", False)
        self.collider = utils.Collider(pos=pos, size=self.image.get_size())

    @classmethod
    def get_placeholder_img(cls) -> pygame.Surface:
        return utils.load_image("assets/floor.png", True)

    @property
    def pos(self):
        return self.collider.pos

    def update(self):
        pass

    def draw(self):
        shared.screen.blit(self.image, shared.camera.transform(self.collider.pos))


class Rose:
    PLACEHOLDER_IMG_PATH = "assets/rose.png"

    def __init__(self, pos) -> None:
        self.image = utils.load_image("assets/rose.png", True)
        self.collider = utils.Collider(pos=pos, size=self.image.get_size())

    @classmethod
    def get_placeholder_img(cls) -> pygame.Surface:
        return utils.load_image("assets/rose.png", True)

    @property
    def pos(self):
        return self.collider.pos

    def update(self):
        pass

    def draw(self):
        shared.screen.blit(self.image, shared.camera.transform(self.collider.pos))


class Sunflower:
    PLACEHOLDER_IMG_PATH = "assets/sunflower.png"

    def __init__(self, pos) -> None:
        self.image = utils.load_image("assets/sunflower.png", True)
        self.collider = utils.Collider(pos=pos, size=self.image.get_size())

    @classmethod
    def get_placeholder_img(cls) -> pygame.Surface:
        return utils.load_image("assets/sunflower.png", True)

    @property
    def pos(self):
        return self.collider.pos

    def update(self):
        pass

    def draw(self):
        shared.screen.blit(self.image, shared.camera.transform(self.collider.pos))
