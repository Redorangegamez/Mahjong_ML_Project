import random
from Models import Tile


class Deck(object):
    """
  Deck consists of list of tiles. Is initialized with standard list of tiles.
  Deck can be shuffled, drawn from.
  """

    def __init__(self):
        self.tiles = []
        self.dead_wall = []
        self.doras = [-5, -6, -7, -8, -9, -10, -11, -12]
        self.kan_count = 0
        self.build()
        self.shuffle()

    def build(self):
        suits = ['p', 's', 'm']
        numbers = ['1', '2', '3', '4', '6', '7', '8', '9']
        for i in suits:
            for j in numbers:
                t = Tile(i,j)
                self.tiles.append(t)
                self.tiles.append(Tile(i, j))
                self.tiles.append(Tile(i, j))
                self.tiles.append(Tile(i, j))
            self.tiles.append(Tile(i, 'r'))
            self.tiles.append(Tile(i, '5'))
            self.tiles.append(Tile(i, '5'))
            self.tiles.append(Tile(i, '5'))
        for i in range(4):
            self.tiles.append(Tile('w', 'e'))
            self.tiles.append(Tile('w', 's'))
            self.tiles.append(Tile('w', 'w'))
            self.tiles.append(Tile('w', 'n'))
            self.tiles.append(Tile('h', 'g'))
            self.tiles.append(Tile('h', 'r'))
            self.tiles.append(Tile('h', 'w'))

    def shuffle(self):
        random.shuffle(self.tiles)

    def deal(self, lop):
        for i in range(4):
            s = self.tiles[slice(13 * i, 13 * (i + 1))]
            s.sort(key=lambda tile: tile.suit_value())
            lop[i].hand = s
        self.tiles = self.tiles[52:]
        self.dead_wall = self.tiles[-14:]

    def reveal_doras(self, riichi_win_bool):
        ds = []
        uras = []
        for i in range(self.kan_count + 1):
            ds.append(self.dead_wall[self.doras[2 * i]])
            uras.append(self.dead_wall[self.doras[1 + 2 * i]])
        if riichi_win_bool:
            for i in (ds + uras):
                print(i.tile_to_string() + ' ')
            return ds + uras
        else:
            for i in ds:
                print(i.tile_to_string() + ' ')
            return ds

    def draw_from_front(self):
        drawn_tile = self.tiles[0]
        self.tiles = self.tiles[1:]
        return drawn_tile

    def draw_from_back(self):
        self.kan_count += 1
        drawn_tile = self.dead_wall[-1]
        self.dead_wall = self.tiles[-1] + self.dead_wall
        self.tiles = self.tiles[:-1]
        for i in self.doras:
            i += 1
        return drawn_tile
