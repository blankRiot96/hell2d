from __future__ import annotations

import typing as t

import pygame

if t.TYPE_CHECKING:
    from src.enums import State
    from src.utils import Camera, WorldMap

# Constants
WORLD_GRAVITY = 70
MAX_FALL_VELOCITY = 300
FIRE_PIT_START_Y = 700

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
world_map: WorldMap

# Flags
