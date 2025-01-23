import pygame

from src import shared, utils


class FirePit:
    """Burning pit of hell, die if you fall into it"""

    def __init__(self) -> None:
        self.image = utils.load_image("assets/firepit.png", True, bound=True)
        self.fire_width = self.image.get_width()
        self.n_repeat = (shared.srect.width // self.image.get_width()) + 1

    def update(self):
        pass

    def draw(self):
        for i in range(self.n_repeat):
            shared.screen.blit(
                self.image,
                shared.camera.transform(
                    (
                        i * self.fire_width + shared.camera.offset.x,
                        shared.FIRE_PIT_START_Y,
                    )
                ),
            )
