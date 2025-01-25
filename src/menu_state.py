import random

import pygame

from src import shared, utils
from src.enums import State
from src.player import CharacterData


class MenuState:
    def __init__(self) -> None:
        bw, bh = 300, 40
        pad = 30
        y_offset = -100
        self.buttons = [
            utils.Button(
                text,
                pygame.Rect(
                    shared.srect.centerx - bw / 2,
                    (shared.srect.centery - bh / 2) + y_offset + (bh + pad) * y,
                    bw,
                    bh,
                ),
            )
            for y, text in enumerate(
                [
                    "Character Select",
                    "Join Game",
                    "Host Game",
                    "Edit Lobby Map",
                    "Edit Game Map",
                ]
            )
        ]
        shared.character_data = CharacterData(
            name=f"guest_{random.randint(1, 69)}",
            hair="default_hair",
            face="default_face",
            outfit="default_outfit",
        )

    def update(self):
        for btn in self.buttons:
            if btn.text == "Join Game" and btn.just_clicked:
                shared.next_state = State.SERVER_FINDER
            elif btn.text == "Host Game" and btn.just_clicked:
                shared.is_host = True
                shared.next_state = State.LOBBY
            elif btn.text == "Edit Lobby Map" and btn.just_clicked:
                shared.next_state = State.LOBBY_EDITOR
            elif btn.text == "Edit Game Map" and btn.just_clicked:
                shared.next_state = State.EDITOR

            btn.update()

    def draw(self):
        for btn in self.buttons:
            btn.draw()
