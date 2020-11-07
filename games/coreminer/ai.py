# This is where you build your AI for the Coreminer game.

from typing import List
from joueur.base_ai import BaseAI

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here
# <<-- /Creer-Merge: imports -->>

class AI(BaseAI):
    """ The AI you add and improve code inside to play Coreminer. """

    @property
    def game(self) -> 'games.coreminer.game.Game':
        """games.coreminer.game.Game: The reference to the Game instance this AI is playing.
        """
        return self._game # don't directly touch this "private" variable pls

    @property
    def player(self) -> 'games.coreminer.player.Player':
        """games.coreminer.player.Player: The reference to the Player this AI controls in the Game.
        """
        return self._player # don't directly touch this "private" variable pls

    def get_name(self) -> str:
        """This is the name you send to the server so your AI will control the player named this string.

        Returns:
            str: The name of your Player.
        """
        # <<-- Creer-Merge: get-name -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        return "Quuz" # REPLACE THIS WITH YOUR TEAM NAME
        # <<-- /Creer-Merge: get-name -->>

    def start(self) -> None:
        """This is called once the game starts and your AI knows its player and game. You can initialize your AI here.
        """


        self.jobs = [
            'Ore_miner',
            'Mass_miner',
            'Shaft_miner',
            'Military',
            'None'
        ]
        self.job_map = {miner: 'None' for miner in self.miners}

        self.standby = lambda: True

        self.state_map = {
            'Ore_miner': {
                            'return_cargo': self.standby, 
                            'return_to_mining': self.standby, 
                            'mining': self.standby
                          },
            'Mass_miner': {
                            'return_cargo': self.standby, 
                            'return_to_mining': self.standby, 
                            'mining': self.standby
                          },
            'Shaft_miner':{
                            'return_cargo': self.standby, 
                            'return_to_mining': self.standby, 
                            'mining': self.standby
                          },
            'Military': {'Standby': self.standby},
            'None': {'Standby': self.standby}
        }



        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your start logic
        
        # <<-- /Creer-Merge: start -->>

    def game_updated(self) -> None:
        """This is called every time the game's state updates, so if you are tracking anything you can update it here.
        """
        # <<-- Creer-Merge: game-updated -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your game updated logic
        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won: bool, reason: str) -> None:
        """This is called when the game ends, you can clean up your data and dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why your AI won or lost.
        """
        # <<-- Creer-Merge: end -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your end logic
        # <<-- /Creer-Merge: end -->>
    def run_turn(self) -> bool:
        """This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your turn, False means to keep your turn going and re-call this function.
        """
        # <<-- Creer-Merge: runTurn -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # Put your game logic here for runTurn

        # If we have no miners and can afford one, spawn one
        if len(self.player.miners) < 1 and self.player.money >= self.game.spawn_price:
            self.player.spawn_miner()

        for miner in self.player.miners:
            miner.mine(miner.tile.tile_south, -1)
            miner.mine(miner.tile.tile_east, -1)
            miner.move(miner.tile.tile_east)

        # # For each miner
        # for miner in self.player.miners:
        #     if not miner or not miner.tile:
        #         continue

        #     self.went_back = False
        #     # Move to tile next to base
        #     if miner.tile.is_base:
        #         if miner.tile.tile_east:
        #             self.goto = 'tile_east'
        #             self.goback = 'tile_west'
        #             print("move east")
        #             # miner.move(miner.tile.tile_east)
        #         else:
        #             print("move west")
        #             self.attr = 'tile_west'
        #             self.goback = 'tile_east'
        #             # miner.move(miner.tile.tile_west)
            
        #     if miner.tile.y == 0:
        #         miner.mine(miner.tile.tile_south, -1)
        #     else:
        #         if not self.went_back:
        #             if (miner.dirt + miner.ore) >= miner.current_upgrade.cargo_capacity:
        #                 while miner.moves and not self.went_back:
        #                     miner.move(getattr(miner.tile, self.goback))
        #             else:
        #                 miner.mine(getattr(miner.tile, self.goto), -1)
        #                 miner.move(getattr(miner.tile, self.goto))
        #         else:
        #             pass



            print(miner.tile.x, miner.tile.y)
            print(miner.dirt, miner.ore)

            # # Sell all materials
            # sellTile = self.game.get_tile_at(self.player.base_tile.x, miner.tile.y)
            # if sellTile and sellTile.owner == self.player:
            #     miner.dump(sellTile, "dirt", -1)
            #     miner.dump(sellTile, "ore", -1)

            # eastTile = miner.tile.tile_east
            # westTile = miner.tile.tile_west

            # # Mine east and west tiles, hopper side first
            # if eastTile.x == self.player.base_tile.x:
            #     if eastTile:
            #         miner.mine(eastTile, -1)
            #     if westTile:
            #         miner.mine(westTile, -1)
            # else:
            #     if westTile:
            #         miner.mine(westTile, -1)
            #     if eastTile:
            #         miner.mine(eastTile, -1)

            # # Check to make sure east and west tiles are mined
            # if (eastTile and eastTile.ore + eastTile.dirt == 0) and (westTile and westTile.ore + westTile.dirt == 0):
            #     # Dig down
            #     if miner.tile.tile_south:
            #         miner.mine(miner.tile.tile_south, -1)
            
        return True
        # <<-- /Creer-Merge: runTurn -->>

    def find_path(self, start: 'games.coreminer.tile.Tile', goal: 'games.coreminer.tile.Tile') -> List['games.coreminer.tile.Tile']:
        """A very basic path finding algorithm (Breadth First Search) that when given a starting Tile, will return a valid path to the goal Tile.

        Args:
            start (games.coreminer.tile.Tile): The starting Tile to find a path from.
            goal (games.coreminer.tile.Tile): The goal (destination) Tile to find a path to.

        Returns:
            list[games.coreminer.tile.Tile]: A list of Tiles representing the path, the the first element being a valid adjacent Tile to the start, and the last element being the goal.
        """

        if start == goal:
            # no need to make a path to here...
            return []

        # queue of the tiles that will have their neighbors searched for 'goal'
        fringe = []

        # How we got to each tile that went into the fringe.
        came_from = {}

        # Enqueue start as the first tile to have its neighbors searched.
        fringe.append(start)

        # keep exploring neighbors of neighbors... until there are no more.
        while len(fringe) > 0:
            # the tile we are currently exploring.
            inspect = fringe.pop(0)

            # cycle through the tile's neighbors.
            for neighbor in inspect.get_neighbors():
                # if we found the goal, we have the path!
                if neighbor == goal:
                    # Follow the path backward to the start from the goal and
                    # # return it.
                    path = [goal]

                    # Starting at the tile we are currently at, insert them
                    # retracing our steps till we get to the starting tile
                    while inspect != start:
                        path.insert(0, inspect)
                        inspect = came_from[inspect.id]
                    return path
                # else we did not find the goal, so enqueue this tile's
                # neighbors to be inspected

                # if the tile exists, has not been explored or added to the
                # fringe yet, and it is pathable
                if neighbor and neighbor.id not in came_from and (
                    neighbor.is_pathable()
                ):
                    # add it to the tiles to be explored and add where it came
                    # from for path reconstruction.
                    fringe.append(neighbor)
                    came_from[neighbor.id] = inspect

        # if you're here, that means that there was not a path to get to where
        # you want to go; in that case, we'll just return an empty path.
        return []

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you need additional functions for your AI you can add them here
    # <<-- /Creer-Merge: functions -->>


    def support_needed(miner_mining, tile_to_remove):
        # check to see if a support block needs to be placed before you mine the block
        # this check shouldn't matter if the entire block will not be mined. 

        # step 2
        # determine which direction you are mining
        miner_coordinates = (miner_mining.tile.x, miner_mining.tile.y)
        # determine direction the miner is mining
        #  1 = right
        # -1 = left
        direction = tile_to_remove.y - miner_coordinates[0]

        # check to see if the block in the opposite direction has been mined
        if direction == 1:                  # right
            temp_tile = game.get_tile_at(miner_coordinates[0]-1, miner_coordinates[1])
        else if direction == -1:            # left
            temp_tile = game.get_tile_at(miner_coordinates[0]+1, miner_coordinates[1])
        else:
            temp_tile = None
        
        if temp_tile:
            if temp_tile.dirt or temp_tile.ore:
                return false
        
        # check to see if 3 blockes above block will be unsupported

        tile_check_list = [
            game.get_tile_at(miner_coordinates[0]-1, miner_coordinates[1]+1),
            game.get_tile_at(miner_coordinates[0], miner_coordinates[1]+1),
            game.get_tile_at(miner_coordinates[0]+1, miner_coordinates[1]+1)
            ]
        return all([temp_tile.dirt or temp_tile.ore for temp_tile in tile_check_list]):




