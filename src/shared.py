from __future__ import annotations

import typing as t

import pygame

if t.TYPE_CHECKING:
    from src.enums import State
    from src.player import CharacterData, Player
    from src.utils import Camera, UDPClient, WorldMap

# Constants
WORLD_GRAVITY = 70
MAX_FALL_VELOCITY = 300
FIRE_PIT_START_Y = 700
DISCOVERY_PORT = 5001
GAME_PORT = 6969

# Canvas
screen: pygame.Surface
srect: pygame.Rect
camera: Camera

# Events
events: list[pygame.event.Event]
mouse_pos: pygame.Vector2
mouse_press: tuple[int, ...]
keys: list[bool]
mjp: list[bool]
mjr: list[bool]
kp: list[bool]
kr: list[bool]
dt: float
clock: pygame.Clock

# States
next_state: State | None

# Objects
player: Player
client: UDPClient
world_map: WorldMap
lobby_map: WorldMap
character_data: CharacterData

# Flags
is_window_closed = False
is_host = False

# Junk
server_ip: str
