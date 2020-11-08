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
        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        self.away = "tile_east" if self.player.base_tile.x == 0 else "tile_west"
        self.back = "tile_east" if self.player.base_tile.x != 0 else "tile_west"

        self.jobs = [
            'Ore_miner',
            'Mass_miner',
            'Shaft_miner',
            'Military',
            'None'
        ]
        self.job_map = {id(miner): ('None', 'Standby') for miner in self.player.miners}
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
                            'mining': self.shaft_mining
                          },
            'Gold_digger':{
                            'return_cargo': self.standby, 
                            'return_to_mining': self.standby, 
                            'mining': self.standby
                          },
            'Military': {'Standby': self.standby},
            'None': {'Standby': self.standby}
        }

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
        print("Final value: ", self.player.value)
        print("Final money: ", self.player.money)
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
            prev = set((id(miner) for miner in self.player.miners))
            self.player.spawn_miner()
            new_miner_id = set((id(miner) for miner in self.player.miners)).difference(prev).pop()
            self.job_map[new_miner_id] = ('Shaft_miner', 'mining')
            print(f'New miner id = {new_miner_id}')


        for miner in self.player.miners:
            if not miner or not miner.tile:
                continue
            job, state = self.job_map[id(miner)]
            action = self.state_map[job][state]
            action(miner)

















            
            # self.shaft_mining(miner)
            # print("Turn: ",self.game.current_turn)
            # print(f'Miner {id(miner)}: (Job, state) = {self.job_map[id(miner)]}')
            # print("Correct function? ", action == self.shaft_mining)
            # print(action)
            # print(self.shaft_mining)

            print("(x, y) = ", miner.tile.x, miner.tile.y)
            print("(dirt, ore) = ", miner.dirt, miner.ore)

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

    def support_needed(self, miner_mining, tile_to_remove):
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
            temp_tile = self.game.get_tile_at(miner_coordinates[0]-1, miner_coordinates[1])
        elif direction == -1:            # left
            temp_tile = self.game.get_tile_at(miner_coordinates[0]+1, miner_coordinates[1])
        else:
            temp_tile = None
        
        if temp_tile:
            if temp_tile.dirt or temp_tile.ore:
                return False
        
        # check to see if 3 blockes above block will be unsupported

        tile_check_list = [
            self.game.get_tile_at(miner_coordinates[0]-1, miner_coordinates[1]+1),
            self.game.get_tile_at(miner_coordinates[0], miner_coordinates[1]+1),
            self.game.get_tile_at(miner_coordinates[0]+1, miner_coordinates[1]+1)
            ]
        return all([temp_tile.dirt or temp_tile.ore for temp_tile in tile_check_list])



    def shaft_mining(self, miner):
        print("Start shaft mining")
        print("base x:", self.player.base_tile.x)
        tile_away = lambda: getattr(miner.tile, self.away)
        tile_back = lambda: getattr(miner.tile, self.back)
        material_left = lambda x: x.ore + x.dirt

        while miner.mining_power > 0 and miner.moves > 0:
            # If miner.tile.x != self.player.base_tile.x:
            #       mine back
            #       move back
            # If miner.tile.x == self.player.base_tile.x
            #       not mined away
            #           mine away
            #           sell materials
            #           build ladder
            #       else 
            #           mine down
            #       
            if miner.tile.x != self.player.base_tile.x:
                # If not alligned, mine back
                miner.mine(tile_back(), -1)
                if (tile_back().dirt + tile_back().ore > 0):
                    # out of mining power
                    return
                else:
                    if tile_back() is not None:
                        miner.move(tile_back())
            else:
                # Try mining away
                if material_left(tile_away()) > 0:
                    miner.mine(tile_away(), -1)
                    if (tile_away().dirt + tile_away().ore > 0):
                        # out of mining power
                        return
                # Add ladder, if needed
                if miner.tile.is_hopper:
                    miner.dump(miner.tile, 'ore', -1)
                    miner.dump(miner.tile, 'dirt',-1)
                if not tile_away().is_ladder:
                    miner.buy('buildingMaterials', 5)
                    miner.build(tile_away(), 'ladder')

                # Nothing to mine laterally, mine down, if possible
                if miner.tile.tile_south is not None:
                    miner.mine(miner.tile.tile_south, -1)
                    if material_left(miner.tile.tile_south) > 0:
                        return
                    miner.move(miner.tile.tile_south)
                else:
                    return


        return
    


    # TODO
    def mass_mining(self, miner):
        # mine all the top layers of the map
        
        tile_away = lambda: getattr(miner.tile, self.away)
        tile_back = lambda: getattr(miner.tile, self.back)

        # initial routine
        if miner.tile.y == 0 and (miner.tile.x in [0, 29]):
            miner.move(tile_away())

            while miner.moves != 0:
                if miner.tile.y < 2:
                    # check for ladder
                    if miner.tile.tile_south is not None:
                        if miner.tile.tile_south.is_ladder():
                            miner.move(miner.tile.tile_south)
                if miner.tile.y == 2:
                    # check for safety barrier

                    if tile_away().shielding != 0:            # safety barrier set
                        if miner.tile.tile_south is not None:
                            miner.move(miner.tile.tile_south)
                    else:
                        #start mining the top 2 rows
                        self.mine_top_2_rows(miner)
                if miner.tile.y > 2:
                    if miner.tile.tile_south is not None:
                        miner.move(miner.tile.tile_south)

        

    def mine_top_2_rows(self, miner):
        # mine the top 2 rows of the map
        # position for the start of this function should be (1,2) or (28,2)
        pass

    # TODO: add break condition when tile is None
    def mine_row(self, miner):
        tile_away = lambda: getattr(miner.tile, self.away)
        tile_back = lambda: getattr(miner.tile, self.back)

        # additional case: what to do when the miner doesn't have enough material
        #                  to place a support
        # while miner can move or mine
            # if cargo is full or not enough material for support
                # move back until miner can drop cargo
                    # drop cargo
                    # buy materials for supports
            # elif cargo not full and no block away -> move away
                # if above or below is ore and miner can place dirt
                    # mine ore and replace with dirt
                # move away
            # elif mine
                # mine away (-1)
                # if tile_away contains no dirt or ore
                    # check if support needs to be placed
        
        # while miner can move or mine
        while miner.moves != 0 and miner.mining != 0:
            # if cargo is full or not enough material for support
            if self.current_cargo(miner) == miner.current_upgrade.cargo_capacity or miner.building_materials < self.game.support_cost:
                # move back until miner can drop cargo
                if tile_away().is_hopper:
                    # dump all cargo
                    dump_all(miner, tile_back())
                    # buy materials until you have 2x required amount
                    while miner.building_materials < (2*self.game.support_cost):
                        miner.buy('buildingMaterials', self.game.support_cost)
                else:
                    if tile_back() is not None:
                        miner.move(tile_back())
            # elif cargo not full and no block away -> move away
            elif self.current_cargo(miner) < miner.current_upgrade.cargo_capacity and is_tile_empty(tile_away()):
                if tile_away() is not None:
                    miner.move(tile_away())


               
            








    def current_cargo(self, miner):
        return miner.dirt + miner.ore + miner.buildingMaterials + (miner.bombs * self.game.bombSize)
        





def miner_max_cargo(miner):
    return miner.upgrade_level

def dump_all(miner, chute):
    # dump all cargo
    miner.dump(chute, 'dirt', -1)
    miner.dump(chute, 'ore', -1)
    miner.dump(chute, 'bomb', -1)

def is_tile_empty(tile_to_check):
    # check if the tile is empty
    return tile_to_check.dirt == 0 and tile_to_check.ore == 0




    # <<-- /Creer-Merge: functions -->>