import random
import socket

import pygame
import ujson

from src import shared, utils
from src.player import ClientSpawnPoint, OtherClientHandler


class LobbyState:
    def __init__(self) -> None:
        self.clean_up_world()
        self.setup_network()
        self.entities = shared.lobby_map.load()
        ClientSpawnPoint.create_device_player()
        self.other_client_handler = OtherClientHandler()

    def setup_network(self):
        if shared.is_host:
            DEVICE_IP = socket.gethostbyname(socket.gethostname())
            data = {"name": shared.character_data.name, "ip": DEVICE_IP}
            utils.LocalBroadcastServer(
                discovery_port=shared.DISCOVERY_PORT,
                broadcast_data=ujson.dumps(data).encode(),
            ).start()

            shared.server_ip = socket.gethostbyname(socket.gethostname())
            self.server = utils.UDPServer(shared.GAME_PORT)
            self.server.start()

        shared.client = utils.UDPClient(shared.server_ip, shared.GAME_PORT)
        shared.client.start()
        self.font = utils.load_font(None, 32)

    def clean_up_world(self):
        utils.Collider.temp_colliders.clear()
        utils.Collider.all_colliders.clear()
        ClientSpawnPoint.points.clear()

    def update(self):
        utils.Collider.temp_colliders.clear()

        for entity in self.entities:
            entity.update()

        self.other_client_handler.update()
        shared.player.update()

    def draw(self):
        self.other_client_handler.draw()
        shared.player.draw()
        for entity in self.entities:
            entity.draw()

        shared.screen.blit(self.font.render("Lobby", True, "white"), (100, 100))
