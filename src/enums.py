from enum import Enum, auto


class State(Enum):
    GAME = auto()
    EDITOR = auto()
    MENU = auto()
    LOBBY = auto()
    SERVER_FINDER = auto()
    LOBBY_EDITOR = auto()
