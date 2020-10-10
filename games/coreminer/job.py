# Job: Information about a Unit's job.

# DO NOT MODIFY THIS FILE
# Never try to directly create an instance of this class, or modify its member variables.
# Instead, you should only be reading its variables and calling its functions.

from games.coreminer.game_object import GameObject

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here
# <<-- /Creer-Merge: imports -->>

class Job(GameObject):
    """The class representing the Job in the Coreminer game.

    Information about a Unit's job.
    """

    def __init__(self):
        """Initializes a Job with basic logic as provided by the Creer code generator."""
        GameObject.__init__(self)

        # private attributes to hold the properties so they appear read only
        self._cargo_capacity = []
        self._health = []
        self._mining_power = []
        self._moves = []
        self._title = ""

    @property
    def cargo_capacity(self):
        """The amount of cargo capacity this Unit starts with per level.

        :rtype: list[int]
        """
        return self._cargo_capacity

    @property
    def health(self):
        """The amount of starting health this Job has per level.

        :rtype: list[int]
        """
        return self._health

    @property
    def mining_power(self):
        """The amount of mining power this Unit has per turn per level.

        :rtype: list[int]
        """
        return self._mining_power

    @property
    def moves(self):
        """The number of moves this Job can make per turn per level.

        :rtype: list[int]
        """
        return self._moves

    @property
    def title(self):
        """The Job title. 'miner' or 'bomb'.

        :rtype: str
        """
        return self._title



    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you want to add any client side logic (such as state checking functions) this is where you can add them
    # <<-- /Creer-Merge: functions -->>
