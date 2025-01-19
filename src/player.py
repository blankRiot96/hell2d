import pygame

from src import shared, utils


class Player:
    JUMP_VELOCITY = -150
    MAX_HORIZONTAL_SPEED = 40

    def __init__(self) -> None:
        self.image = utils.load_image(
            "assets/player.png", alpha=True, scale=0.4, bound=True
        )
        self.collider = utils.Collider(size=self.image.get_size(), pos=(200, 0))
        self.gravity = utils.Gravity()

    def update(self):
        dx, dy = 0, 0
        self.gravity.update()

        if shared.kp[pygame.K_SPACE]:
            self.gravity.velocity = Player.JUMP_VELOCITY

        dy += self.gravity.velocity * shared.dt

        dx += shared.keys[pygame.K_d] - shared.keys[pygame.K_a]
        dx *= Player.MAX_HORIZONTAL_SPEED * shared.dt

        sides = self.collider.get_collision_sides(dx, dy)
        if utils.CollisionSide.BOTTOM in sides:
            self.gravity.velocity = 0
            dy = 0
        if {utils.CollisionSide.LEFT, utils.CollisionSide.RIGHT} <= sides:
            dx = 0

        self.collider.pos += dx, dy
        shared.camera.attach_to(self.collider.pos)

    def draw(self):
        shared.screen.blit(self.image, shared.camera.transform(self.collider.pos))
