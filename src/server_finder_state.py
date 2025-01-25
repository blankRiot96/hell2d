import pygame
import ujson

from src import shared, utils
from src.enums import State


class ServerFinderState:
    def __init__(self) -> None:
        self.font = utils.load_font(None, 32)
        self.host_finder = utils.LocalBroadcastClient(
            discovery_port=shared.DISCOVERY_PORT
        )
        self.host_finder.start_receiving()
        self.buttons: list[utils.Button] = []

    def update(self):
        self.buttons = []
        for i, data in enumerate(self.host_finder.received_data):
            data = ujson.loads(data.decode())
            start_x = 300
            bw, bh = shared.srect.width - start_x * 2, 50
            pad = 10
            rect = pygame.Rect(start_x, 50 + (bh + pad) * i, bw, bh)
            btn = utils.Button(data["name"], rect)
            btn.update()

            if btn.just_clicked:
                shared.server_ip = data["ip"]
                shared.next_state = State.LOBBY
            self.buttons.append(utils.Button(data["name"], rect))

    def draw(self):
        for btn in self.buttons:
            btn.draw()
