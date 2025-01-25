import typing as t

from src import shared, utils
from src.editor_state import EditorState
from src.enums import State
from src.floor import Floor, Rose, Sunflower
from src.game_state import GameState
from src.lobby_editor_state import LobbyEditorState
from src.lobby_state import LobbyState
from src.menu_state import MenuState
from src.player import ClientSpawnPoint
from src.server_finder_state import ServerFinderState


class StateLike(t.Protocol):
    def update(self): ...

    def draw(self): ...


class StateManager:
    def __init__(self) -> None:
        self.state_dict: dict[State, t.Type[StateLike]] = {
            State.GAME: GameState,
            State.EDITOR: EditorState,
            State.MENU: MenuState,
            State.LOBBY: LobbyState,
            State.SERVER_FINDER: ServerFinderState,
            State.LOBBY_EDITOR: LobbyEditorState,
        }

        shared.camera = utils.Camera(
            bottom_bounds=shared.FIRE_PIT_START_Y
            + utils.load_image("assets/firepit.png", True, bound=True).get_height()
        )

        entities = [Floor, ClientSpawnPoint, Rose, Sunflower]
        shared.world_map = utils.WorldMap("assets/map.json", entities)
        shared.lobby_map = utils.WorldMap("assets/lobby_map.json", entities)

        shared.next_state = State.MENU
        self.set_state()

    def set_state(self):
        self.state_obj: StateLike = self.state_dict[shared.next_state]()  # type: ignore HEHHEHE
        shared.next_state = None

    def update(self):
        self.state_obj.update()
        if shared.next_state is not None:
            self.set_state()

    def draw(self):
        self.state_obj.draw()

    def cleanup(self):
        if hasattr(self.state_obj, "cleanup"):
            self.state_obj.cleanup()  # type: ignore
