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
        self.job_map = {id(miner): ('None', 'standby', dict()) for miner in self.player.miners}
        self.standby = lambda x: print('Standing by!')

        self.state_map = {
            'Ore_miner': {
                            'return_cargo': self.return_cargo, 
                            'return_to_mining': self.return_to_mining, 
                            'mining': self.ore_mining,
                            'return_for_upgrade': self.return_for_upgrade,
                            'emergency_return': self.emergency_return
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
            'Mega_miner':{
                            'return_cargo': self.return_cargo, 
                            'return_to_mining': self.return_to_mining, 
                            'mining': self.ore_mining,
                            'emergency_return': self.emergency_return
                          },
            'Military_offence':{
                                'blocking': self.block_hopper,
                                'bombing_run': self.bombing_run
                                },
            'Military_defence': {'standby': self.standby},
            'None': {'standby': self.standby}
        }

        self.miner_row_gen = row_generator()
        self.initial_turn = True
        self.update_set = set()

        self.spawn_mega_miner = {2: 25, 11: 27, 19: 29, 25: 29}  # miner number: job_row

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

        if self.initial_turn:
            for job_row in [21, 15]:
                self.add_miner(job='Shaft_miner', state='mining', details={'job_row': job_row, 'mega': False})
            self.initial_turn = False
        self.miner_needed()

        for miner in self.player.miners:
            if not miner or not miner.tile:
                continue
            job, state, _ = self.job_map[id(miner)]
            self.consider_upgrade(miner)
            action = self.state_map[job][state]
            while action(miner):
                job, state, _ = self.job_map[id(miner)]
                action = self.state_map[job][state]

        print("Current turn: ", self.game.current_turn)
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




    def consider_upgrade(self, miner):
        job, state, details = self.job_map[id(miner)]
        desired_lvl = 0

        if job == 'Ore_miner' or job == 'Shaft_miner':
            if details['job_row'] < 16:
                desired_lvl = 1
            else:
                desired_lvl = 2
        elif job == 'Mass_miner':
            desired_lvl = 1
        elif job == 'Military':
            desired_lvl = 3
        elif job == 'Mega_miner':
            desired_lvl = 3
        else:
            return
        
        if len(self.player.miners) > 12:
            desired_lvl = 3

        if desired_lvl > miner.upgrade_level:
            # check bank to consider upgrading
            if self.player.money >= self.game.upgrade_price * 2:
                self.update_set.add(id(miner))
                return True


    


    def miner_needed(self):
        miner = None

        if len(self.player.miners) in self.spawn_mega_miner:
            if self.player.money >= self.game.spawn_price + (3 * self.game.upgrade_price):
                # spawn Mega_miner and max upgrade
                miner = self.add_miner(job='Shaft_miner', state='mining', details={'job_row': self.spawn_mega_miner[len(self.player.miners)], 'mega': True})
                while miner.upgrade():
                    if miner.upgrade_level == self.game.max_upgrade_level:
                        print("MEGA MINER IS ALIVE!!! -> LVL ", miner.upgrade_level)
            else:
                return False
            

        # add miner if desired
        elif self.player.money >= self.game.spawn_price * (3 + 0.5*len(self.player.miners)):
            # get the levels with working miners
            jobs = []
            job_levels = []
            for miner_id in self.job_map:
                # print("In job map? : ", id(temp_miner) in self.job_map)
                jobs.append(self.job_map[miner_id][0])
                if self.job_map[miner_id][0] in ['Ore_miner', 'Shaft_miner']:
                    job_levels.append(self.job_map[miner_id][-1]['job_row'])
            try:
                print("***********************************************")
                print(job_levels)
                next_row = next(self.miner_row_gen)
                while next_row in job_levels:
                    next_row = next(self.miner_row_gen)
                    print(next_row)
                print("***********************************************")

                self.add_miner(job='Shaft_miner', state='mining', details={'job_row': next_row, 'mega': False})                
                # we want every other row to have a ore miner starting at 5 going to 29
                # start at 17
            except StopIteration:
                print("ABORT! ABORT!")
                return




        # use self.add_miner() to spawn miner
        

    def shaft_mining(self, miner):
        print("Start shaft mining")
        tile_away = lambda: getattr(miner.tile, self.away)
        tile_back = lambda: getattr(miner.tile, self.back)
        material_left = lambda x: x.ore + x.dirt


        while miner.mining_power > 0 and miner.moves > 0:
            if miner.tile.y >= self.job_map[id(miner)][-1]['job_row']:
                self.update_job_map(miner, 'Ore_miner', 'mining')
                print(f"Miner {id(miner)} has changed state to ('Ore_miner', 'mining')")
                return True

            if miner.tile.x == self.player.base_tile.x:
                # If they are aligned, don't want this
                if material_left(tile_away()):
                    miner.mine(tile_away(), -1)
                if material_left(tile_away()):
                    # Out of mining power. Done for turn
                    return False
                else:
                    # Block was mined, move there
                    miner.move(tile_away())
            
            if miner.tile.x != self.player.base_tile.x:
                # If they are not aligned. We want this
                # Check if back tile is hopper
                if tile_back().is_hopper or (tile_back().x, tile_back().y) == (self.player.base_tile.x, self.player.base_tile.y):
                    # Dump ore and buy materials
                    dump_all(miner, tile_back())

                    if miner.building_materials < self.game.ladder_cost * 6:
                        # Buy materials, if needed
                        materials_needed = (6*self.game.ladder_cost) - miner.building_materials
                        miner.buy('buildingMaterials', materials_needed)
                    
                # Build ladder above, if needed
                if miner.tile.tile_north is not None and not miner.tile.tile_north.is_ladder:
                    miner.build(miner.tile.tile_north, 'ladder')
                # Build ladder, current, if needed
                if not miner.tile.is_ladder:
                    miner.build(miner.tile, 'ladder')

                # Buy more materials, if needed
                if tile_back().is_hopper:
                    if miner.building_materials < self.game.ladder_cost * 6:
                        materials_needed = (6*self.game.ladder_cost) - miner.building_materials
                        miner.buy('buildingMaterials', materials_needed)

                # Buying/Building done, start mining

                # First mine back
                if material_left(tile_back()):
                    miner.mine(tile_back(), -1)
                if material_left(tile_back()):
                    return False

                if miner.tile.tile_south is None:
                    self.update_job_map(miner, 'Ore_miner', 'mining')
                    print(f"Miner {id(miner)} has changed state to ('Ore_miner', 'mining')")
                    return True
                if material_left(miner.tile.tile_south):
                    miner.mine(miner.tile.tile_south, -1)
                if miner.tile.tile_south is None:
                    return False
                elif material_left(miner.tile.tile_south):
                    return False
                else:
                    miner.move(miner.tile.tile_south)

            if miner.tile.y >= self.job_map[id(miner)][-1]['job_row']:
                self.update_job_map(miner, 'Ore_miner', 'mining')
                print(f"Miner {id(miner)} has changed state to ('Ore_miner', 'mining')")
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

        # miner starts at spawn
        # move to row 2
        # if shielding, become a Ore_miner 
            # use generator to assign job row


        pass





    # TODO: add break condition when tile is None somewhere in ore mining job
    # TODO: when moving away or back, check for ladder


    def return_cargo(self, miner):
        print("in return cargo")
        # TODO: make sure you can walk forward - place ladder or dirt as needed

        # return miner to cargo - moving back to cargo
        tile_away = lambda: getattr(miner.tile, self.away)
        tile_back = lambda: getattr(miner.tile, self.back)

        # check if miner is on hopper
        if miner.tile.is_hopper:
            # dump all cargo
            dump_all(miner, miner.tile)
            # buy meterials until you have 3x required amount
            while miner.building_materials < ((3+miner.upgrade_level)*self.game.support_cost):
                miner.buy('buildingMaterials', self.game.support_cost)
            self.update_job_map(miner, 'Ore_miner', 'return_for_upgrade')
            return True
        # the tile back is the hopper
        elif tile_back().is_hopper:
            # dump all cargo
            dump_all(miner, tile_back())
            # buy materials until you have 3x required amount
            while miner.building_materials < ((3+miner.upgrade_level)*self.game.support_cost):
                miner.buy('buildingMaterials', self.game.support_cost)
            self.update_job_map(miner, 'Ore_miner', 'return_for_upgrade')
            return True
        # move back to find hopper
        else:
            if tile_back() is not None:
                # check for missing tile beneth tile back
                if self.walkable(tile_back()):
                    miner.move(tile_back())
                else:
                    self.update_job_map(miner, 'Ore_miner', 'emergency_return')
                    return True
        
        return False
        

    def return_to_mining(self, miner):
        print("in return to mining")
        # TODO: make sure you can walk forward - place ladder or dirt as needed
        # TODO: make sure you go back to desired rung

        # return miner to mining - moving away as far as possible
        tile_away = lambda: getattr(miner.tile, self.away)
        tile_back = lambda: getattr(miner.tile, self.back)

        # move vertical up the ladder until the desired row is met
        while miner.tile.y < self.job_map[id(miner)][-1]['job_row']:
            if miner.tile.tile_north is not None and is_tile_empty(miner.tile.tile_north):
                if not miner.tile.tile_north.is_ladder:
                    if tile_back() is not None and tile_back().is_hopper:
                        miner.buy('buildingMaterials', self.game.ladder_cost*1)
                    miner.build(miner.tile.tile_north, 'ladder')
                if not miner.move(miner.tile.tile_north):
                    return False
            else:
                return False


        if tile_away() is not None and not is_tile_empty(tile_away()):
            self.update_job_map(miner, 'Ore_miner', 'mining')
            return True
        
        if tile_away() is not None:
            if is_tile_empty(tile_away()):
                miner.move(tile_away())

        return False


    def ore_mining(self, miner):
        # mine away if possible
        tile_away = lambda: getattr(miner.tile, self.away)
        tile_back = lambda: getattr(miner.tile, self.back)

        # check if state needs to be changed
        
        # if cargo full
        if self.current_cargo(miner) == miner.current_upgrade.cargo_capacity or miner.building_materials < self.game.support_cost:
            # go to state "return to cargo"
            self.update_job_map(miner, 'Ore_miner', 'return_cargo')
            return True

        # if no tile away
        if tile_away() is not None and is_tile_empty(tile_away()):
            # go to state "return to mining"
            self.update_job_map(miner, 'Ore_miner', 'return_to_mining')
            return True

        if not is_tile_empty(tile_away()):
            miner.mine(tile_away(), -1)
            # TODO
            # check if support needs to be placed
            tile = self.game.get_tile_at(tile_away().x, tile_away().y-1)
            if not self.is_supported(tile) and miner.building_materials > self.game.support_cost:
                print("Building support!")
                miner.build(tile_away(), 'support')
                miner.move(tile_away())
        
        return False
    


    # TODO: add case where miner can't move left and needs to dump stuff
    def emergency_return(self, miner):

        tile_away = lambda: getattr(miner.tile, self.away)
        tile_back = lambda: getattr(miner.tile, self.back)

        # state called when the miner gets stuck trying to return return cargo
        if not is_tile_empty(tile_back()):
            # get amount of material to clear
            material_needed_to_remove = tile_size(tile_back())
            # dump that amout of material behind
            while miner.bombs + miner.dirt + miner.ore > material_needed_to_remove:
                if not miner.dump(tile_away(), 'dirt', -1):
                    if not miner.dump(tile_away(), 'ore', 1):
                        break
            if miner.bombs + miner.dirt + miner.ore > material_needed_to_remove:
                # if miner has no items and still can't carry all
                while miner.mining_power and not is_tile_empty(tile_back()):
                    if miner.mine(tile_back(), -1):
                        miner.dump(tile_away(), 'dirt', -1)
                        miner.dump(tile_away(), 'ore', -1)
        
        if is_tile_empty(tile_back()):
            miner.move(tile_back())

        # check if next tile back is the chute
        if tile_back().is_hopper:
            self.update_job_map(miner, 'Ore_miner', 'return_cargo')
            return True
        
        return False


    def return_for_upgrade(self, miner):
        if id(miner) not in self.update_set:
            if self.job_map[id(miner)][0] == 'Ore_miner':
                self.update_job_map(miner, 'Ore_miner', 'return_to_mining')
            return True

        print("returning for upgrades")


        # TODO: make sure you can walk forward - place ladder or dirt as needed

        # return miner to cargo - moving back to cargo
        tile_away = lambda: getattr(miner.tile, self.away)
        tile_back = lambda: getattr(miner.tile, self.back)

        if tile_back() is not None:
            # check if miner is on hopper
            if miner.tile.is_hopper:
                miner.upgrade()
                self.update_set.discard(id(miner))
                if self.job_map[id(miner)][0] == 'Ore_miner':
                    self.update_job_map(miner, 'Ore_miner', 'return_to_mining')
                return True

            # the tile back is the hopper
            elif tile_back().is_hopper:
                miner.move(tile_back())
                miner.upgrade()
                self.update_set.discard(id(miner))
                if self.job_map[id(miner)][0] == 'Ore_miner':
                    self.update_job_map(miner, 'Ore_miner', 'return_to_mining')
                return True
            # move back to find hopper
            else:
                # check for missing tile beneth tile back
                if self.walkable(tile_back()):
                    miner.move(tile_back())
                else:
                    self.update_set.discard(id(miner))
                    self.update_job_map(miner, self.job_map[id(miner)][0], 'emergency_return')
                    return True
        
        return False




    def block_hopper(self, miner):
        # return miner to cargo - moving back to cargo
        tile_away = lambda: getattr(miner.tile, self.away)
        tile_back = lambda: getattr(miner.tile, self.back)

        self.update_job_map(miner, 'Military_offence', 'bombing_run')



    def bombing_run(self, miner):
        # return miner to cargo - moving back to cargo
        tile_away = lambda: getattr(miner.tile, self.away)
        tile_back = lambda: getattr(miner.tile, self.back)

        # have mine run accross top of the map placing ladders until space before opponent hopper
        


        self.update_job_map(miner, 'Military_offence', 'block_hopper')


    





    def is_supported(self, tile):
        # tile is the tile to see if it will fall
        if is_tile_empty(tile):
            return True
        # consider y-1
        tiles = [self.game.get_tile_at(x, tile.y+1) for x in [tile.x-1, tile.x, tile.x+1]]
        tiles = [t for t in tiles if t is not None]
        return any((t.is_support for t in tiles))

    def current_cargo(self, miner):
        return miner.dirt + miner.ore + miner.building_materials + (miner.bombs * self.game.bomb_size)
        
    def walkable(self, tile):
        # return true if miner can move, otherwise false
        if tile.is_ladder:
            return True
        tile_to_check = self.game.get_tile_at(tile.x, tile.y+1)
        if tile_to_check is None:
            return True # You are on the bottom of the map
        if not is_tile_empty(tile_to_check):
            return True
        return False
    
    def safe_dump(self, tile):
        # tile is the tile to walk to
        # need to check if it will be supported

        # check 2 tiles down
        if not is_tile_empty(self.game.get_tile_at(tile.x, tile.y+2)):
            return True
        #check the side tiles 1 tile down to see if both are supported
        tiles = [self.game.get_tile_at(tile.x-1, tile.y+1), self.game.get_tile_at(tile.x+1, tile.y+1)]
        if all([temp_tile is not None for temp_tile in tiles]):
            if all([self.is_supported(temp_tile) for temp_tile in tiles]):
                return True

        return False



    def update_job_map(self, miner, job, state, details=None):
        if id(miner) not in self.job_map:
            self.job_map[id(miner)] = ('None', 'standby', dict())
        if details is None:
            details = self.job_map[id(miner)][-1]
        self.job_map[id(miner)] = (job, state, details)


    def add_miner(self, job='None', state='standby', details=dict()):
        prev = set((id(miner) for miner in self.player.miners))
        self.player.spawn_miner()
        new_miner_id = set((id(miner) for miner in self.player.miners)).difference(prev).pop()
        miner = [m for m in self.player.miners if id(m) == new_miner_id][0]
        self.update_job_map(miner, job, state, details=details)
        print(f'New miner id = {new_miner_id}')
        return miner





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

def tile_size(tile):
    # return the size of the tile
    return len(tile.bombs) + tile.dirt + tile.ore

def row_generator(start=17, stride=2):
    curr = start
    yield start
    stride_idx = 1
    while 4 < curr < 30:
        curr = start + stride*stride_idx
        yield curr
        curr = start - stride*stride_idx
        yield curr
        stride_idx += 1
        curr = start + stride*stride_idx



    # <<-- /Creer-Merge: functions -->>