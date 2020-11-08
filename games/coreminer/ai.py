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
                            'return_cargo': self.return_cargo, 
                            'return_to_mining': self.return_to_mining, 
                            'mining': self.ore_mining
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


        print("Current turn: ", self.game.current_turn)

        for miner in self.player.miners:
            if not miner or not miner.tile:
                continue
            job, state = self.job_map[id(miner)]
            action = self.state_map[job][state]
            while action(miner):
                job, state = self.job_map[id(miner)]
                action = self.state_map[job][state]
            # consider_upgrade(miner)
            # action(miner)

            print("(x, y) = ", miner.tile.x, miner.tile.y)
            print("(dirt, ore) = ", miner.dirt, miner.ore)

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





    def is_supported(self, tile):
        if is_tile_empty(tile):
            return True
        
        # consider y-1
        tiles = [self.game.get_tile_at(x, tile.y+1) for x in [tile.x-1, tile.x, tile.x+1]]
        tiles = [t for t in tiles if t is not None]
        return any((t.is_support for t in tiles))








    def shaft_mining(self, miner):
        print("Start shaft mining")
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
                    if miner.tile.y == 25:
                        miner.move(tile_away())
                        self.job_map[id(miner)] = ('Ore_miner', 'mining')
                        print("Miner {id(miner)} has changed state to ('Ore_miner', 'mining')")
                        return True
                else:
                    return

        if miner.tile.y == 25:
            miner.move(tile_away())
            self.job_map[id(miner)] = ('Ore_miner', 'mining')
            print("Miner {id(miner)} has changed state to ('Ore_miner', 'mining')")
            return True



        return False
    


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
    # TODO: when moving away or back, check for ladder
    # def mine_row(self, miner):

    #     """
    #     Mining
    #     Return cargo
    #     return to mining

    #     """




    #     tile_away = lambda: getattr(miner.tile, self.away)
    #     tile_back = lambda: getattr(miner.tile, self.back)
        
    #     # Not standing on hopper
    #     if tile_back() is not None and tile_back().is_hopper and not miner.tile.is_ladder:
    #         miner.buy('buildingMaterials', self.game.support_cost)
    #         miner.build(miner.tile, 'ladder')
        
    #     # Standing on hopper
    #     if miner.tile.is_hopper:
    #         if not is_tile_empty(tile_away()):
    #             miner.mine(tile_away(), -1)
    #         if is_tile_empty(tile_away()):
    #             miner.buy('buildingMaterials', self.game.support_cost)
    #             miner.build(miner.tile, 'ladder')


    #     # while miner can move or mine
    #     while miner.moves != 0 and miner.mining_power != 0:
    #         # if cargo is full or not enough material for support
    #         if self.current_cargo(miner) == miner.current_upgrade.cargo_capacity or miner.building_materials < self.game.support_cost:
    #             # check if miner is on hopper
    #             if miner.tile.is_hopper:
    #                 # dump all cargo
    #                 dump_all(miner, miner.tile)
    #                 # buy meterials until you have 2x required amount
    #                 while miner.building_materials < (2*self.game.support_cost):
    #                     miner.buy('buildingMaterials', self.game.support_cost)
    #             # move back until miner can drop cargo
    #             elif tile_back().is_hopper:
    #                 # dump all cargo
    #                 dump_all(miner, tile_back())
    #                 # buy materials until you have 2x required amount
    #                 while miner.building_materials < ((3+miner.upgrade_level)*self.game.support_cost):
    #                     miner.buy('buildingMaterials', self.game.support_cost)
    #             else:
    #                 if tile_back() is not None:
    #                     miner.move(tile_back())
    #         # elif cargo not full and no block away -> move away
    #         elif self.current_cargo(miner) < miner.current_upgrade.cargo_capacity and is_tile_empty(tile_away()):
    #             if tile_away() is not None:
    #                 miner.move(tile_away())
    #             # if above or below is ore and miner can place dirt
    #             if miner.tile.tile_north is not None:
    #                 if miner.tile.tile_north.ore != 0:
    #                     # mine ore and replace with dirt
    #                     miner.mine(miner.tile.tile_north, -1)
    #                 if is_tile_empty(miner.tile.tile_north):
    #                     miner.dump(miner.tile.tile_north, 'dirt', 1)
    #         # elif mine
    #         # if tile_away contains no dirt or ore
    #         elif not is_tile_empty(tile_away()):
    #             miner.mine(tile_away(), -1)
    #             # check if support needs to be placed
    #             tile = self.game.get_tile_at(tile_away().x, tile_away().y-1)
    #             if not self.is_supported(tile) and miner.building_materials > self.game.support_cost:
    #                 miner.build(tile_away(), 'support')
        
    #     # return cargo




    def return_cargo(self, miner):
        # return miner to cargo - moving back to cargo
        tile_away = lambda: getattr(miner.tile, self.away)
        tile_back = lambda: getattr(miner.tile, self.back)

        # check if miner is on hopper
        if miner.tile.is_hopper:
            # dump all cargo
            dump_all(miner, miner.tile)
            # buy meterials until you have 3x required amount
            while miner.building_materials < ((2+miner.upgrade_level)*self.game.support_cost):
                miner.buy('buildingMaterials', self.game.support_cost)
            self.job_map[id(miner)] = ('Ore_miner', 'return_to_mining')
            return True
        # move back until miner can drop cargo
        elif tile_back().is_hopper:
            # dump all cargo
            dump_all(miner, tile_back())
            # buy materials until you have 3x required amount
            while miner.building_materials < ((2+miner.upgrade_level)*self.game.support_cost):
                miner.buy('buildingMaterials', self.game.support_cost)
            self.job_map[id(miner)] = ('Ore_miner', 'return_to_mining')
            return True
        else:
            if tile_back() is not None:
                miner.move(tile_back())
        
        return False
        


    def return_to_mining(self, miner):
        # return miner to mining - moving away as far as possible
        tile_away = lambda: getattr(miner.tile, self.away)
        tile_back = lambda: getattr(miner.tile, self.back)

        if tile_away() is not None and not is_tile_empty(tile_away()):
            self.job_map[id(miner)] = ('Ore_miner', 'mining')
            return True
        
        if tile_away() is not None:
            miner.move(tile_away())
        # if above or below is ore and miner can place dirt
        if miner.tile.tile_north is not None:
            if miner.tile.tile_north.ore != 0:
                # mine ore and replace with dirt
                miner.mine(miner.tile.tile_north, -1)
            if is_tile_empty(miner.tile.tile_north):
                miner.dump(miner.tile.tile_north, 'dirt', 1)

        return False


    def ore_mining(self, miner):
        # mine away if possible
        tile_away = lambda: getattr(miner.tile, self.away)
        tile_back = lambda: getattr(miner.tile, self.back)

        # check if state needs to be changed
        
        # if cargo full
        if self.current_cargo(miner) == miner.current_upgrade.cargo_capacity:
            # go to state "return to cargo"
            self.job_map[id(miner)] = ('Ore_miner', 'return_cargo')
            return True

        # if no tile away
        if tile_away() is not None and is_tile_empty(tile_away()):
            # go to state "return to mining"
            self.job_map[id(miner)] = ('Ore_miner', 'return_to_mining')
            return True

        if not is_tile_empty(tile_away()):
            miner.mine(tile_away(), -1)
            # check if support needs to be placed
            tile = self.game.get_tile_at(tile_away().x, tile_away().y-1)
            if not self.is_supported(tile) and miner.building_materials > self.game.support_cost:
                miner.build(tile_away(), 'support')
            miner.move(tile_away())
        
        return False






    def current_cargo(self, miner):
        return miner.dirt + miner.ore + miner.building_materials + (miner.bombs * self.game.bomb_size)
        





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