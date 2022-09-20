from Models.Set import Set
from Models.Tile import Tile
from Models.Hand import Hand
import collections


class Player:
  """
  A Player that does something or does nothing or does something illegal
  """
  def __init__(self, name):
    self.hand = Hand([])
    self.taken_triplets = []
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
    self.riichi_tile = False
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
      self.hand.draw_tile(self.drawn_tile)
    else:
      self.drawn_tile = deck.draw_from_front()
      self.hand.draw_tile(self.drawn_tile)

  def play_tile(self):
    self.print_hand()
    while True:
      chosen_tile = input("Choose a tile: ")
      suit = chosen_tile[0]
      value = chosen_tile[1:]
      if suit not in ['m', 'p', 's', 'w', 'h']:
        print('invalid tile')
        continue
      if suit == 'w' and value not in ['e', 's', 'w', 'n']:
        print('invalid tile')
        continue
      if suit == 'h' and value not in ['r', 'g', 'w']:
        print('invalid tile')
        continue
      if (suit == 'm' or suit == 'p' or suit == 's') and value not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        print('invalid tile')
        continue
      tile = Tile(suit, value)
      if self.hand.contains(tile):
        self.discard(tile)
        self.hand.sort()
        return tile
      print('invalid tile')

  def discard(self, tile):
    self.hand.discard(tile)
    self.is_furiten()

  def is_furiten(self):
    if self.is_tenpai():
      for discard in self.discards:
        for wait in self.waits:
          if discard == wait:
            self.furiten = True
    else:
      self.furiten = False

  def can_chi(self, tile_to_take, player):
    if (self.player - 1) % 4 != player:
      return False
    possible_combinations = []
    if tile_to_take.suit_value <= 27:
      number = tile_to_take.value
      if tile_to_take.value == 'r':
        number = 5
      if tile_to_take.value != 'r':
        number = int(tile_to_take.value)
      suit = tile_to_take.suit
      if number == 1:
        possible_combinations.append([Tile(suit, '2'), Tile(suit, '3')])
      elif number == 9:
        possible_combinations.append([Tile(suit, '8'), Tile(suit, '7')])
      elif number == 2:
        possible_combinations.append([Tile(suit, '1'), Tile(suit, '3')])
        possible_combinations.append([Tile(suit, '3'), Tile(suit, '4')])
      elif number == 8:
        possible_combinations.append([Tile(suit, '7'), Tile(suit, '9')])
        possible_combinations.append([Tile(suit, '6'), Tile(suit, '7')])
      else:
        possible_combinations.append([Tile(suit, str(number + 1)), Tile(suit, str(number + 2))])
        possible_combinations.append([Tile(suit, str(number - 1)), Tile(suit, str(number + 1))])
        possible_combinations.append([Tile(suit, str(number - 2)), Tile(suit, str(number - 1))])

      for combination in possible_combinations:
        for tile in combination:
          if tile not in self.hand:
            possible_combinations.remove(combination)

      if possible_combinations.empty():
        return False
      else:
        return possible_combinations

  def chi(self, tile_to_take, possible_combinations, player):
    if len(possible_combinations) == 1:
      b = input('would you like to chi? Type y if yes, anything else if no')
      if b == 'y':
        sequence_to_take = possible_combinations[0]
        sequence_to_take.sort(key=lambda t: tile.suit_value())
        self.taken_triplets.append(Set("chi", sequence_to_take, tile_to_take, player))
        self.closed = False
        for i in sequence_to_take:
          self.discard(i)
        return True
      return False
    else:
      b = input('would you like to chi? Type y if yes, anything else if no')
      if b == 'y':
        for combination in possible_combinations:
          for tile in combination:
            possible_combinations[combination][tile] = tile.tile_to_string
        while True:
          how_to_chi = input(possible_combinations + 'how would you like to chi? Type 0 for 1st option, (1 for 2nd), '
                                                     '(2 for 3rd), b to cancel')
          if how_to_chi == 'b':
            self.chi(tile_to_take, possible_combinations, player)
          if how_to_chi.isdigit():
            if int(how_to_chi) in range(len(possible_combinations)):
              sequence_to_take = possible_combinations[0].append(tile_to_take)
              sequence_to_take.sort(key=lambda t: t.suit_value())
              self.taken_triplets.append(Set("chi", sequence_to_take, tile_to_take, player))
              self.closed = False
              for i in sequence_to_take:
                self.discard(i)
              return True
    return False

  def can_pon(self, tile_to_take):
    counter = 0
    for i in self.hand.lot:
      if i == tile_to_take:
        counter += 1
    return counter >= 2

  def pon(self, tile_to_take, player):
    result = input('would you like to pon? Type y if yes, anything else if no')
    if result == 'y':
      triplet_to_take = [tile_to_take, tile_to_take, tile_to_take]
      self.taken_triplets.append(Set("pon", triplet_to_take, tile_to_take, player))
      self.closed = False
      self.discard(tile_to_take)
      self.discard(tile_to_take)
      return True
    return False

  def can_take_kan(self, tile_to_take):
    counter = 0
    for i in self.hand.lot:
      if i == tile_to_take:
        counter += 1
    return counter >= 3

  def take_kan(self, tile_to_take, player):
    b = input('would you like to kan? Type y if yes, anything else if no')
    if b == 'y':
      q = [tile_to_take, tile_to_take, tile_to_take, tile_to_take]
      self.taken_triplets.append(Set("open_kan", q, tile_to_take, player))
      self.closed = False
      self.discard(tile_to_take)
      self.discard(tile_to_take)
      self.discard(tile_to_take)
      return True
    return False

  def can_complete_kan(self):
    possible_kans = []
    if len(self.taken_triplets) != 0:
      for s in self.taken_triplets:
        if (s.type_of_set == "pon") and (self.hand.contains(s.taken_tile)):
          possible_kans.append(s.taken_tile)
    if len(possible_kans) == 0:
      return False
    else:
      return possible_kans

  def complete_kan(self, possible_kans):
    b = input('would you like to kan? Type y if yes, anything else if no')
    if b == 'y':
      if len(possible_kans == 1):
        for s in self.taken_triplets:
          if (s.type_of_set == "pon") and (self.hand.contains(possible_kans[0])):
            s.type_of_set = "complete_kan"
            s.tiles.append(possible_kans[0])
            return True
      else:
        while True:
          how_to_kan = input(possible_kans + 'what would you like to kan? Type 0 for 1st option, (1 for 2nd), '
                                             '(2 for 3rd), b to cancel')
          if how_to_kan == 'b':
            self.self_kan(possible_kans)
          if how_to_kan.isdigit():
            if int(how_to_kan) in range(len(possible_kans)):
              for s in self.taken_triplets:
                if (s.type_of_set == "pon") and (self.hand.contains(possible_kans[how_to_kan])):
                  s.type_of_set = "complete_kan"
                  s.tiles.append(possible_kans[how_to_kan])
                  return True

  def can_self_kan(self):
    possible_kans = []
    tiles = collections.Counter(self.hand.lot)
    unique_tiles = tiles.keys()
    for i in unique_tiles:
      if tiles[i] == 4:
        possible_kans.append(i)
    if len(possible_kans) == 0:
      return False
    else:
      return possible_kans

  def self_kan(self, possible_kans):
    b = input('would you like to kan? Type y if yes, anything else if no')
    if b == 'y':
      if len(possible_kans == 1):
        q = [possible_kans[0], possible_kans[0], possible_kans[0],
             possible_kans[0]]
        self.taken_triplets.append(Set("closed kan", q, possible_kans[0], self.player))
        self.discard(possible_kans[0])
        self.discard(possible_kans[0])
        self.discard(possible_kans[0])
        return True
      else:
        while True:
          how_to_kan = input(possible_kans + 'what would you like to kan? Type 0 for 1st option, (1 for 2nd), '
                                             '(2 for 3rd), b to cancel')
          if how_to_kan == 'b':
            self.self_kan(possible_kans)
          if how_to_kan.isdigit():
              q = [possible_kans[how_to_kan], possible_kans[how_to_kan], possible_kans[how_to_kan],
                   possible_kans[how_to_kan]]
              self.taken_triplets.append(Set("closed kan", q, possible_kans[how_to_kan], self.player))
              self.discard(possible_kans[how_to_kan])
              self.discard(possible_kans[how_to_kan])
              self.discard(possible_kans[how_to_kan])
              return True
    return False

  def can_riichi(self):
    riichi_tiles = []
    if self.closed:
      for tile_to_riichi in self.hand.lot:
        self.discard(tile_to_riichi)
        if self.is_tenpai():
          riichi_tiles.append(tile_to_riichi)
        self.hand.lot.append(tile_to_riichi)
    if len(riichi_tiles) == 0:
      return False
    else:
      return riichi_tiles

  def riichi(self, riichi_tiles):
    while True:
      how_to_riichi = input(riichi_tiles + 'how to riichi? Type 0 for 1st option,(1 for 2nd), (2 for 3rd), b to cancel')
      if how_to_riichi == 'b':
        return False
      if how_to_riichi.isdigit():
        if int(how_to_riichi) in range(len(how_to_riichi)):
          self.riichi_tile = riichi_tiles[how_to_riichi]
          return True

  def can_ron(self, tile_to_win):
    if not self.furiten and tile_to_win in self.waits:
        return True

  def ron(self, tile_to_win):
    b = input('would you like to ron? Type y if yes, anything else if no')
    if b == 'y':
      self.winning_tile = tile_to_win
      return True
    else:
      return False

  def can_tsumo(self):
    if self.can_win():
      return True

  def tsumo(self):
    b = input('would you like to ron? Type y if yes, anything else if no')
    if b == 'y':
      self.winning_tile = self.hand.drawn_tile
      return True
    else:
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
      self.hand.lot.append(i)
      if self.can_win():
        self.waits.append(i)
      self.discard(i)
    if len(self.waits) > 0:
      return True
    else:
      return False

  def can_win(self):
    return self.hand.can_win()

  def can_take(self, tile_to_take, player):
    takes = []
    if self.can_chi(tile_to_take, player):
      takes.append("chi")
    if self.can_pon(tile_to_take):
      takes.append("pon")
    if self.can_take_kan(tile_to_take):
      takes.append("take_kan")
    if self.can_ron(tile_to_take):
      takes.append("ron")
    if len(takes) == 0:
      return False
    else:
      return takes

  def print_hand(self):
    for t in self.hand.lot:
      print(t.tile_to_string(), end=" ")
