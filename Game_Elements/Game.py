import random

from Models import Deck, Hand
from Game_Elements import Player

class Game(object):
  def __init__(self, lop):
    random.shuffle(lop)
    self.wind_order = {0:'e',1:'s',2:'w',3:'n'}
    self.seat_winds = [0,1,2,3]
    self.round_wind = 'e'
    for i in self.seat_winds:
      lop[self.seat_winds.index(i)].player = self.wind_order
      lop[self.seat_winds.index(i)].seat_wind_indicator = self.wind_order.get(i)
      lop[self.seat_winds.index(i)].round_wind_indicator = self.round_wind
    self.round_number = 1
    self.current_winner = 0
    self.game_continues = True
    self.current_player = 0
    self.current_dealer = 0
    self.discards = [[],[],[],[]]
    self.taken_triplets = [[],[],[],[]]
    while True:
      self.start_round(lop)
      if lop[self.current_winner].seat_wind_indicator != 'e':
        if self.round_number == 4:
          if self.round_wind == 'e':
            self.round_wind == 's'
            for p in lop:
              p.round_wind_indicator == self.round_wind
          elif self.round_wind == 's':
            break
        self.round_number += 1
        for i in self.seat_winds:
          i = (i + 1) % 4
          lop[self.seat_winds.index(i)].seat_wind_indicator = self.wind_order.get(i)
      else:
        for i in self.seat_winds:
          lop[self.seat_winds.index(i)].repeats += 1
      break

  def start_round(self, lop):
    deck = Deck()
    deck.deal(lop)

    for i in lop:
      i.round_dora_indicators = deck.reveal_doras(False)
    self.discards = [[],[],[],[]]
    printable_discards = [[],[],[],[]]
    self.current_player = self.current_dealer
    lop[self.current_player].dealer = True

    while True:
      for turn_no in range(4):
        print("current player:", lop[self.current_player].name)
        print("your discards:", printable_discards)
        print("options: chi, pon, kan, ron, tsumo, riichi")
        lop[self.current_player].draw_tile(deck, False)
        t = lop[self.current_player].play_tile()
        if self.can_take(t, lop, self.current_player):
          return
        else:
          self.discards[self.current_player].append(t)
          printable_discards[self.current_player].append(t.tile_to_string())
          self.current_player = (self.current_player + 1) % 4

    #print(self.end_game())

  def can_take(self, tile, lop, player):
    return False

  def end_game(self):
    return