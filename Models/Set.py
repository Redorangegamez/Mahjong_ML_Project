class Set(object):
    """
    A Set is represented with the type of set, tiles in the set, tile taken, and the player taken from.
    """

    def __init__(self, type_of_set, tiles, taken_tile, player):
        self.type_of_set = type_of_set
        self.tiles = tiles
        self.taken_tile = taken_tile
        self.player = player

    def type_of_set(self):
        return self.type_of_set

    def tiles(self):
        return self.tiles

    def taken_tile(self):
        return self.taken_tile

    def player(self):
        return self.player
