from src import shared, utils


class Floor:
    def __init__(self, pos) -> None:
        self.image = utils.load_image("assets/floor.png", False)
        self.collider = utils.Collider(pos=pos, size=self.image.get_size())

    def update(self):
        pass

    def draw(self):
        shared.screen.blit(self.image, shared.camera.transform(self.collider.pos))
        self.collider.draw()
