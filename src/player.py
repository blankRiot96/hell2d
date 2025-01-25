import random
import typing as t
from dataclasses import asdict, dataclass

import pygame
import ujson
from pygame.transform import scale

from src import shared, utils


@dataclass
class CharacterData:
    name: str
    hair: str
    face: str
    outfit: str

    def to_json(self) -> str:
        return ujson.dumps(asdict(self))

    @classmethod
    def from_json(cls, json_str) -> t.Self:
        return cls(**ujson.loads(json_str))


class OutfitManager:
    def __init__(
        self,
        hair="default_hair",
        face="default_face",
        outfit="default_outfit",
        scale: float = 1.0,
    ) -> None:
        self.hair = utils.load_image(
            f"assets/{hair}.png", True, bound=True, scale=scale
        )
        self.face = utils.load_image(
            f"assets/{face}.png", True, bound=True, scale=scale
        )
        self.outfit = utils.load_image(
            f"assets/{outfit}.png", True, bound=True, scale=scale
        )

        itenary = [self.hair, self.face, self.outfit]
        width = max(img.get_width() for img in itenary)
        height = sum(img.get_height() for img in itenary)

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)

        acc_y = 0
        for image in itenary:
            image_rect = image.get_rect(centerx=width / 2)
            self.image.blit(image, (image_rect.x, acc_y))
            acc_y += image.get_height()

    def update(self):
        pass

    def draw(self, rect):
        shared.screen.blit(self.image, shared.camera.transform(rect))


class ClientSpawnPoint:
    points: list[pygame.Vector2] = []

    def __init__(self, pos) -> None:
        ClientSpawnPoint.points.append(pygame.Vector2(pos))

    @classmethod
    def get_placeholder_img(cls) -> pygame.Surface:
        return utils.load_image("assets/player_placeholder.png", True, scale=0.4)

    def update(self):
        pass

    def draw(self):
        pass

    @classmethod
    def create_device_player(cls):
        spawn_point = random.choice(cls.points)
        shared.player = Player(spawn_point)


class OtherClientHandler:
    def __init__(self) -> None:
        self.clients = []
        self.colliders = []

        self.name_font = utils.load_font(None, 24)

    def update(self):
        data = shared.client.received_data.decode()
        self.colliders.clear()
        if data:
            self.clients = ujson.loads(data)
            for client in self.clients:
                collider = utils.Collider(
                    size=client["size"], pos=client["pos"], temp=True
                )
                self.colliders.append(collider)
                utils.Collider.temp_colliders.append(collider)

    def draw(self):
        for collider, client in zip(self.colliders, self.clients):
            character_data = CharacterData.from_json(client["character_data"])
            outfit = OutfitManager(
                hair=character_data.hair,
                face=character_data.face,
                outfit=character_data.outfit,
                scale=0.4,
            )
            outfit.draw(collider.rect)

            name_surf = self.name_font.render(character_data.name, True, "tomato")
            name_rect = name_surf.get_rect(
                midbottom=pygame.Vector2(collider.rect.midtop) - (0, 10)
            )

            shared.screen.blit(name_surf, shared.camera.transform(name_rect))


class Player:
    JUMP_VELOCITY = -150
    MAX_HORIZONTAL_SPEED = 40

    def __init__(self, pos) -> None:
        self.outfit = OutfitManager(
            hair=shared.character_data.hair,
            face=shared.character_data.face,
            outfit=shared.character_data.outfit,
            scale=0.4,
        )
        self.collider = utils.Collider(size=self.outfit.image.get_size(), pos=pos)
        self.gravity = utils.Gravity()

        self.name_surf = utils.load_font(None, 24).render("You", True, "seagreen")
        self.name_rect = self.name_surf.get_rect()

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
        if self.collider.pos.y > 1000:
            self.collider.pos = random.choice(ClientSpawnPoint.points).copy()
        self.name_rect.midbottom = pygame.Vector2(self.collider.rect.midtop) - (0, 10)

        shared.client.send(
            ujson.dumps(
                {
                    "pos": [self.collider.pos.x, self.collider.pos.y],
                    "size": self.collider.size,
                    "character_data": shared.character_data.to_json(),
                }
            ).encode()
        )
        shared.camera.attach_to(self.collider.pos)

    def draw(self):
        shared.screen.blit(self.name_surf, shared.camera.transform(self.name_rect))
        self.outfit.draw(self.collider.rect)
