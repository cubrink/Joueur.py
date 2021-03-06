# Game: Send hordes of the undead at your opponent while defending yourself against theirs to win.

# DO NOT MODIFY THIS FILE
# Never try to directly create an instance of this class, or modify its member variables.
# Instead, you should only be reading its variables and calling its functions.

from typing import Dict, List, Optional
from joueur.base_game import BaseGame

# import game objects
from games.necrowar.game_object import GameObject
from games.necrowar.player import Player
from games.necrowar.tile import Tile
from games.necrowar.tower import Tower
from games.necrowar.tower_job import TowerJob
from games.necrowar.unit import Unit
from games.necrowar.unit_job import UnitJob

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here
# <<-- /Creer-Merge: imports -->>

class Game(BaseGame):
    """The class representing the Game in the Necrowar game.

    Send hordes of the undead at your opponent while defending yourself against theirs to win.
    """

    def __init__(self):
        """Initializes a Game with basic logic as provided by the Creer code generator.
        """
        BaseGame.__init__(self)

        # private attributes to hold the properties so they appear read only
        self._current_player = None
        self._current_turn = 0
        self._game_objects = {}
        self._gold_income_per_unit = 0
        self._island_income_per_unit = 0
        self._mana_income_per_unit = 0
        self._map_height = 0
        self._map_width = 0
        self._max_turns = 100
        self._players = []
        self._river_phase = 0
        self._session = ""
        self._tiles = []
        self._time_added_per_turn = 0
        self._tower_jobs = []
        self._towers = []
        self._unit_jobs = []
        self._units = []

        self.name = "Necrowar"

        self._game_object_classes = {
            'GameObject': GameObject,
            'Player': Player,
            'Tile': Tile,
            'Tower': Tower,
            'TowerJob': TowerJob,
            'Unit': Unit,
            'UnitJob': UnitJob
        }

    @property
    def current_player(self) -> 'games.necrowar.player.Player':
        """games.necrowar.player.Player: The player whose turn it is currently. That player can send commands. Other players cannot.
        """
        return self._current_player

    @property
    def current_turn(self) -> int:
        """int: The current turn number, starting at 0 for the first player's turn.
        """
        return self._current_turn

    @property
    def game_objects(self) -> Dict[str, 'games.necrowar.game_object.GameObject']:
        """dict[str, games.necrowar.game_object.GameObject]: A mapping of every game object's ID to the actual game object. Primarily used by the server and client to easily refer to the game objects via ID.
        """
        return self._game_objects

    @property
    def gold_income_per_unit(self) -> int:
        """int: The amount of gold income per turn per unit in a mine.
        """
        return self._gold_income_per_unit

    @property
    def island_income_per_unit(self) -> int:
        """int: The amount of gold income per turn per unit in the island mine.
        """
        return self._island_income_per_unit

    @property
    def mana_income_per_unit(self) -> int:
        """int: The Amount of gold income per turn per unit fishing on the river side.
        """
        return self._mana_income_per_unit

    @property
    def map_height(self) -> int:
        """int: The number of Tiles in the map along the y (vertical) axis.
        """
        return self._map_height

    @property
    def map_width(self) -> int:
        """int: The number of Tiles in the map along the x (horizontal) axis.
        """
        return self._map_width

    @property
    def max_turns(self) -> int:
        """int: The maximum number of turns before the game will automatically end.
        """
        return self._max_turns

    @property
    def players(self) -> List['games.necrowar.player.Player']:
        """list[games.necrowar.player.Player]: List of all the players in the game.
        """
        return self._players

    @property
    def river_phase(self) -> int:
        """int: The amount of turns it takes between the river changing phases.
        """
        return self._river_phase

    @property
    def session(self) -> str:
        """str: A unique identifier for the game instance that is being played.
        """
        return self._session

    @property
    def tiles(self) -> List['games.necrowar.tile.Tile']:
        """list[games.necrowar.tile.Tile]: All the tiles in the map, stored in Row-major order. Use `x + y * mapWidth` to access the correct index.
        """
        return self._tiles

    @property
    def time_added_per_turn(self) -> int:
        """int: The amount of time (in nano-seconds) added after each player performs a turn.
        """
        return self._time_added_per_turn

    @property
    def tower_jobs(self) -> List['games.necrowar.tower_job.TowerJob']:
        """list[games.necrowar.tower_job.TowerJob]: A list of every tower type / job.
        """
        return self._tower_jobs

    @property
    def towers(self) -> List['games.necrowar.tower.Tower']:
        """list[games.necrowar.tower.Tower]: Every Tower in the game.
        """
        return self._towers

    @property
    def unit_jobs(self) -> List['games.necrowar.unit_job.UnitJob']:
        """list[games.necrowar.unit_job.UnitJob]: A list of every unit type / job.
        """
        return self._unit_jobs

    @property
    def units(self) -> List['games.necrowar.unit.Unit']:
        """list[games.necrowar.unit.Unit]: Every Unit in the game.
        """
        return self._units

    def get_tile_at(self, x: int, y: int) -> Optional['games.necrowar.tile.Tile']:
        """Gets the Tile at a specified (x, y) position.

        Args:
            x (int): An integer between 0 and the map_width.
            y (int): An integer between 0 and the map_height.

        Returns:
            games.necrowar.tile.Tile or None: The Tile at (x, y) or None if out of bounds.
        """
        if x < 0 or y < 0 or x >= self.map_width or y >= self.map_height:
            # out of bounds
            return None

        return self.tiles[x + y * self.map_width]

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you want to add any client side logic (such as state checking functions) this is where you can add them
    # <<-- /Creer-Merge: functions -->>
