import pygame

from src import shared, utils


class Player:
    JUMP_VELOCITY = -150
    MAX_HORIZONTAL_SPEED = 40

    def __init__(self, pos) -> None:
        self.image = utils.load_image(
            "assets/player.png", alpha=True, scale=0.4, bound=True
        )
        self.collider = utils.Collider(size=self.image.get_size(), pos=pos)
        self.gravity = utils.Gravity()

    @classmethod
    def get_placeholder_img(cls) -> pygame.Surface:
        return utils.load_image("assets/player_placeholder.png", True, scale=0.4)

    @property
    def pos(self):
        return self.collider.pos

    def update(self):
        dx, dy = 0, 0
        self.gravity.update()

        if shared.kp[pygame.K_SPACE]:
            self.gravity.velocity = Player.JUMP_VELOCITY

        dy += self.gravity.velocity * shared.dt

        dx += shared.keys[pygame.K_d] - shared.keys[pygame.K_a]
        dx *= Player.MAX_HORIZONTAL_SPEED * shared.dt

        collider_data = self.collider.get_collision_data(dx, dy)
        if (
            utils.CollisionSide.BOTTOM in collider_data.colliders
            or utils.CollisionSide.TOP in collider_data.colliders
        ):
            self.gravity.velocity = 0
            dy = 0

        if (
            utils.CollisionSide.RIGHT in collider_data.colliders
            or utils.CollisionSide.LEFT in collider_data.colliders
        ):
            dx = 0

        self.collider.pos += dx, dy
        shared.camera.attach_to(self.collider.pos)

    def draw(self):
        shared.screen.blit(self.image, shared.camera.transform(self.collider.pos))
        self.collider.draw()
