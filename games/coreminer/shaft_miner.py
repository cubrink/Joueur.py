def shaft_mining(self, miner):
    miner.mine(miner.tile.tile_south, -1)
    miner.mine(getattr(miner.tile, self.back), -1)
    miner.build(getattr(miner.tile, self.away), 'ladder')
    miner.move(getattr(miner.tile, self.back))

