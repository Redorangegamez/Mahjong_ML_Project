from Models import Tile
import collections


class Hand:
    """
    A hand consists of a list of 1,4,7,10, or 13 tiles, and a most recently drawn tile.
    """

    def __init__(self, lot, drawn_tile=False):
        self.lot = lot
        self.drawn_tile = drawn_tile

    def draw_tile(self, drawn_tile):
        self.drawn_tile = drawn_tile
        self.lot.append(drawn_tile)

    def sort(self):
        self.lot.sort(key=lambda tile: tile.suit_value())

    def discard(self, tile):
        index = 0
        for i in self.lot:
            if i == tile:
                del self.lot[index]
                break
            index += 1

    def contains(self, tile):
        return tile in self.lot

    def can_win(self):
        if len(self.lot == 13):
            return "error"
        self.sort()
        hand = []
        possible_combos = []
        terminals = ["m1", "m9", "p1","p9", "s1","s9","wn","ws","we","ww", "dg","dr","dw"]
        for tile in self.lot:
            hand.append(tile.tile_to_string())
        tiles = collections.Counter(hand)
        unique_tiles = tiles.keys()
        if len(unique_tiles) == 7:
            c = True
            for i in unique_tiles: #check seven pairs
                if tiles[i] != 2:
                    c = False
            if c:
                print("seven pairs wheeeee")
                return True
        if len(unique_tiles) == 13:
            for i in unique_tiles:
                if tiles[i] == 2:
                    hand.remove(i)
            for i in range(len(hand)):
                if hand[i] != terminals[i]:
                    return False
            print("thirteen orphans wheeee")
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

    def sort(self):
        return sorted(self.lot, key=lambda tile: tile.suit_value())

    """
    def count_hand(hand, round_wind, seat_wind, winning_tile,
                   taken_triplets, kans, riichi, ippatsu, haitei, rinshan, chankan,
                   double_riichi, tsumo, closed, repeats, doras):  #takes a winning hand (includes takes not kans)
        #kans are a tuple with the tile and closed boolean
        tiles = collections.Counter(hand)
        unique_tiles = tiles.keys()
    
        fan = 0
        tanyao = False
        Green = False
        Red = False
        White = False
        roundwind = False
        seatwind = False
        riichi = riichi
        ippatsu = ippatsu
        tsumo = tsumo
        haitei = False
        houtei = False
        rinshan = rinshan
        chankan = chankan
        double_riichi = double_riichi
        chiitoi = False
    
    
    
        if riichi:
            fan += 1
        if ippatsu:
            fan+= 1
        if tsumo and closed:
            fan += 1
        if haitei:
            if tsumo:
                haitei = True
            else:
                houtei = True
            fan += 1
        if rinshan:
            fan += 1
        if chankan:
            fan += 1
        if double_riichi:
            fan += 2
    
        manzu = ['1m','2m','3m','4m','5m','6m','7m','8m','9m']
        souzu = ['1s','2s','3s','4s','5s','6s','7s','8s','9s']
        pinzu = ['1p','2p','3p','4p','5p','6p','7p','8p','9p']
        terminals = ['1s','9s','1p','9p','1m','9m']
        winds = ['ew','sw','ww','nw']
        dragons = ['rh','gh','wh']
        winds_points = [round_wind, seat_wind]
        honours = terminals + winds + dragons
        for i in hand: #this is so wrong wtf
            if i not in honours:
                tanyao = True
                fan += 1
        for i in unique_tiles:
            if (i in (dragons + winds_points)) and (tiles[i] >= 3):
                if i == round_wind:
                    roundwind = True
                    fan += 1
                elif i == seat_wind:
                    seatwind = True
                    fan += 1
                elif i == 'rh':
                    Red = True
                    fan += 1
                elif i == 'gh':
                    Green = True
                    fan += 1
                elif i == 'wh':
                    White = True
                    fan += 1
        if (len(unique_tiles) == 7):
            c = True
            for i in unique_tiles: #check seven pairs
                if tiles[i] != 2:
                    c = False
            if c:
                chiitoi = True
                fan += 2
    
        for i in hand:
            if i in doras:
                fan += 1  
    """