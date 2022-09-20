from fileinput import input

from Models import Deck, Set, Tile
import collections

class Player(object):
  """
  A Player that does something or does nothing or does something illegal
  """
  def __init__(self, name):
    self.hand = []
    self.taken_triplets = []  #a taken_triplets will be a Set()
    self.discards = []
    self.drawn_tile = ''
    self.name = name
    self.player = 0
    self.seat_wind_indicator = 'e'
    self.round_wind_indicator = 'e'
    self.points = 25000
    self.dealer = False
    self.round_dora_indicators = []
    self.waits = []
    self.no_yaku = False
    self.furiten = False
    self.fan = 0
    self.fu = 20
    self.winning_tile = None
    self.round_wind_yaku = False
    self.seat_wind_yaku = False
    self.kans = []
    self.riichi = False
    self.ippatsu = False
    self.haitei = False
    self.rinshan = False
    self.chankan = False
    self.double_riichi = False
    self.tsumo = False
    self.closed = True
    self.repeats = 0
    self.doras = []
    self.yakus = []

  def draw_tile(self, deck, was_kan):
    if was_kan:
      self.drawn_tile = deck.draw_from_back()
      self.hand.append(self.drawn_tile)
    else:
      self.drawn_tile = deck.draw_from_front()
      self.hand.append(self.drawn_tile)

  def play_tile(self):
    self.print_hand()
    while True:
      chosen_tile = input("Choose a tile: ")
      suit = chosen_tile[0]
      value = chosen_tile[1:]
      if suit not in ['m','p','s','w','h']:
        print('invalid tile')
        continue
      if suit == 'w' and value not in ['e','s','w','n']:
        print('invalid tile')
        continue
      if suit == 'h' and value not in ['r','g','w']:
        print('invalid tile')
        continue
      if (suit == 'm' or suit == 'p' or suit == 's') and value not in ['1','2','3','4','5','6','7','8','9']:
        print('invalid tile')
        continue
      tile = Tile(suit, value)
      if tile in self.hand:
        self.remove_tile(tile)
        self.hand.sort(key=lambda tile: tile.suit_value())
        return tile
      print('invalid tile')

  def remove_tile(self,tile):
    index = 0
    for i in self.hand:
      if i == tile:
        del self.hand[index]
        break
      index += 1

  def chi(self, tile_to_take, player):  #do i need to return true or can i just return false and call it a day?
    p = []
    if tile_to_take.suit_value <= 27:
      if tile_to_take.value == 'r':
        number = 5
      if tile_to_take.value != 'r':
        number = int(tile_to_take.value)
      suit = tile_to_take.suit
      if number == 1:
        p.append([Tile(suit, '2'), Tile(suit, '3')])
      elif number == 9:
        p.append([Tile(suit, '8'), Tile(suit, '7')])
      elif number == 2:
        p.append([Tile(suit, '1'), Tile(suit, '3')])
        p.append([Tile(suit, '3'), Tile(suit, '4')])
      elif number == 8:
        p.append([Tile(suit, '7'), Tile(suit, '9')])
        p.append([Tile(suit, '6'), Tile(suit, '7')])
      else:
        p.append([Tile(suit, str(number + 1)), Tile(suit, str(number + 2))])
        p.append([Tile(suit, str(number - 1)), Tile(suit, str(number + 1))])
        p.append([Tile(suit, str(number - 2)), Tile(suit, str(number - 1))])

      for i in p:
        for j in i:
          if j not in self.hand:
            p.remove(i)

      if p.empty():
        return False
      elif len(p) == 1:
        b = input('would you like to chi? Type y if yes, anything else if no')
        if b == 'y':
          q = p[0].append(tile_to_take)
          q.sort(key=lambda tile: tile.suit_value())
          self.taken_triplets.append(Set("chi", q, tile_to_take, player))
          self.closed = False
          for i in q:
            self.hand.remove_tile(i)
      else:
        b = input('would you like to chi? Type y if yes, anything else if no')
        if b == 'y':
          for i in p:
            for j in i:
              p[i].index(j) = j.tile_to_string
          while True:
            how_to_chi = input(i + 'how would you like to chi? Type 0 for 1st option, 1 for 2nd, (2 for 3rd)')
            if how_to_chi.isdigit():
              if int(how_to_chi) <= len(p):
                q = p[0].append(tile_to_take)
                q.sort(key=lambda tile: tile.suit_value())
                self.taken_triplets.append(Set("chi", q, tile_to_take, player))
                self.closed = False
                for i in q:
                  self.hand.remove_tile(i)
                break
    else:
      return False

  def pon(self, tile_to_take, player):
    counter = 0
    for i in self.hand:
      if i == tile_to_take:
        counter += 1
    if counter >= 2:
      b = input('would you like to pon? Type y if yes, anything else if no')
      if b == 'y':
        q = [tile_to_take, tile_to_take, tile_to_take]
        self.taken_triplets.append(Set("pon", q, tile_to_take, player))
        self.closed = False
        self.hand.remove_tile(tile_to_take)
        self.hand.remove_tile(tile_to_take)
    else:
      return False

  def take_kan(self, tile_to_take, player):
    counter = 0
    for i in self.hand:
      if i == tile_to_take:
        counter += 1
    if counter == 3:
      b = input('would you like to kan? Type y if yes, anything else if no')
      if b == 'y':
        q = [tile_to_take, tile_to_take, tile_to_take, tile_to_take]
        self.taken_triplets.append(Set("kan", q, tile_to_take, player))
        self.closed = False
        self.hand.remove_tile(tile_to_take)
        self.hand.remove_tile(tile_to_take)
        self.hand.remove_tile(tile_to_take)

  def self_kan(self, tile_to_take):
    if len(self.taken_triplets) != 0:
      c = False
      for s in self.taken_triplets:
        if (s.type_of_set == "pon") and (s.taken_tile == tile_to_take):
          c = True
          b = input('would you like to kan? Type y if yes, anything else if no')
          if b == 'y':
            s.type_of_set = "kan"
            s.tiles.append(tile_to_take)
    counter = 0
    for i in self.hand:
      if i == tile_to_take:
        counter += 1
    if counter == 3:
      b = input('would you like to closed kan? Type y if yes, anything else if no')
      if b == 'y':
        q = [tile_to_take, tile_to_take, tile_to_take, tile_to_take]
        self.taken_triplets.append(Set("closed kan", q, tile_to_take, self.player))
        self.hand.remove_tile(tile_to_take)
        self.hand.remove_tile(tile_to_take)
        self.hand.remove_tile(tile_to_take)
    else:
      return False

  def riichi(self, tile_to_riichi):
    if self.closed == True:
      self.remove_tile(tile_to_riichi)
      if self.is_tenpai:
        return True



    return

  def ron(self, tile_to_win):
    if not self.furiten:
      if tile_to_win in self.waits:
        b = input('would you like to ron? Type y if yes, anything else if no')
        if b == 'y':
          self.winning_tile = tile_to_win
          return True
    return False

  def tsumo(self):
    if self.can_win():
      b = input('would you like to ron? Type y if yes, anything else if no')
        if b == 'y':
          self.winning_tile = self.hand[-1]
          return True
    return False


  def is_tenpai(self):
    suits = ['p', 's', 'm']
    numbers = ['1', '2', '3', '4', '6', '7', '8', '9']
    tiles = []
    for i in suits:
      for j in numbers:
          tiles.append(Tile(i, j))
      tiles.append(Tile(i, 'r'))
    tiles.append(Tile('w', 'e'))
    tiles.append(Tile('w', 's'))
    tiles.append(Tile('w', 'w'))
    tiles.append(Tile('w', 'n'))
    tiles.append(Tile('h', 'g'))
    tiles.append(Tile('h', 'r'))
    tiles.append(Tile('h', 'w'))

    for i in tiles:
      self.hand.append(i)
      if self.can_win():
        self.waits.append(i)
      self.remove_tile(i)



  def can_win(self):                      #checks if a hand (assuming right amount of tiles (2,5,8,11,14)) is winning
    hand = []
    possible_combos = []
    for tile in self.hand:
      hand.append(tile.tile_to_string())
    tiles = collections.Counter(hand)
    unique_tiles = tiles.keys()
    for i in unique_tiles:                #removes a pair and checks if there's 4 sets of triplets left
      if tiles[i] >= 2:
        tiles[i] -= 2
        b = self.find_sets(tiles, possible_combos)
        if b:
          return True
        tiles[i] += 2
    if (len(unique_tiles) == 7):
      c = True
      for i in unique_tiles: #check seven pairs
        if tiles[i] != 2:
          c = False
      if c:
        print("seven pairs wheeeee")
        return True
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

  def print_hand(self):
    for t in self.hand:
      print(t.tile_to_string(), end=" ")
    print()

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
    yakuhai = ['rh','gh','wh']
    winds_points = [round_wind, seat_wind]
    honours = terminals + winds_and_dragons
    for i in hand: #this is so wrong wtf
      if i not in honours:
        tanyao = True
        fan += 1
    for i in unique_tiles:
      if (i in (yakuhai + winds_points)) and (tiles[i] >= 3):
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