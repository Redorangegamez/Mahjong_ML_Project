from Models import Tile
import collections

class Hand(object):
    """
    A hand consists of a list of 1,4,7,10, or 13 tiles, and a most recently drawn tile.
    """

    def __init__(self, lot, drawn_tile):
        self.lot = lot
        self.drawn_tile = drawn_tile

    def can_win(self):                      #checks if a hand (assuming right amount of tiles (2,5,8,11,14)) is winning
        hand = self.lot + self.drawn_tile
        possible_combos = []
        for tile in self.hand:
            hand.append(tile.tile_to_string())
        tiles = collections.Counter(hand)
        unique_tiles = tiles.keys()
        if (len(unique_tiles) == 7):
            c = True
            for i in unique_tiles: #check seven pairs
                if tiles[i] != 2:
                    c = False
            if c:
                print("seven pairs wheeeee")
        return True
        for i in unique_tiles:                #removes a pair and checks if there's 4 sets of triplets left
            if tiles[i] >= 2:
                tiles[i] -= 2
                b = self.find_sets(tiles, possible_combos)
                if b:
                    return True
                tiles[i] += 2
        return False

    def find_sets(self, tiles2, possible_combos):            #finds triplets with backtracking
        tiles = tiles2
        unique_tiles = tiles.keys()
        need_to_del = []
        for i in unique_tiles:
            if tiles[i] == 0:
                need_to_del.append(i)
        for i in need_to_del:
            del tiles[i]
        unique_tiles = tiles.keys()
        p = []
        possible_sequences = []
        need_to_del = []
        if (len(tiles) == 0):
            return True
        for i in unique_tiles:                  #checks winds and dragons first (easy)
            if (i[0] == 'w') or (i[0] == 'h'):
                if tiles[i] == 3:
                    need_to_del.append(i)
                else:
                    return possible_combos
        for i in need_to_del:
            del tiles[i]

        for i in unique_tiles:                #checks for sequences next (adds possible sequences)
            number = int(i[1])
            tile = i[0]
            if tiles[i] >= 3:
                p.append([i,i,i])
            if number == 1:
                p.append([i,tile + str(number+1), tile + str(number+2)])
            elif number == 9:
                p.append([tile + str(number-2), tile + str(number-1), i])
            elif number == 2:
                p.append([i,tile + str(number+1), tile + str(number+2)])
                p.append([tile + str(number-1), i, tile + str(number+1)])
            elif number == 8:
                p.append([tile + str(number-1), i, tile + str(number+1)])
                p.append([tile + str(number-2), tile + str(number-1), i])
            else:
                p.append([i,tile + str(number+1), tile + str(number+2)])
                p.append([tile + str(number-1), i, tile + str(number+1)])
                p.append([tile + str(number-2), tile + str(number-1), i])
        for i in p:
            if i not in possible_sequences:
                possible_sequences.append(i)
        for i in reversed(possible_sequences):
            remove = False
            for j in i:
                if j not in unique_tiles:
                    remove = True
            if remove:
                possible_sequences.remove(i)
        if (len(possible_sequences) == 0):
            return possible_combos
        for i in possible_sequences:    #[[1,2,3],[2,3,4],[3,4,5]]
            temp = list(possible_combos)
            temp.append(i)
            for j in i:
                tiles[j] -= 1
            return self.find_sets(tiles, temp)

