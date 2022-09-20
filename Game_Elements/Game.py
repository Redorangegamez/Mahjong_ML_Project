import random
from Models.Deck import Deck


class Game:
  def __init__(self, lop):
    random.shuffle(lop)
    self.wind_order = {0: 'e', 1: 's', 2: 'w', 3: 'n'}
    self.seat_winds = [0, 1, 2, 3]
    self.round_wind = 'e'
    for i in self.seat_winds:
      lop[self.seat_winds.index(i)].player = self.wind_order
      lop[self.seat_winds.index(i)].seat_wind_indicator = self.wind_order.get(i)
      lop[self.seat_winds.index(i)].round_wind_indicator = self.round_wind
    self.round_number = 1
    self.bonus_number = 0
    self.current_winner = 0
    self.current_loser = 0
    self.game_continues = True
    self.current_player = 0
    self.current_dealer = 0
    self.discards = [[], [], [], []]
    self.taken_triplets = [[], [], [], []]
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
        self.bonus_number += 1
      break

  def start_round(self, lop):
    deck = Deck()
    deck.deal(lop)

    for i in lop:
      i.round_dora_indicators = deck.reveal_doras(False)
    self.discards = [[], [], [], []]
    printable_discards = [[], [], [], []]
    self.current_player = self.current_dealer
    lop[self.current_player].dealer = True

    while not deck.deck_out:
      for turn_no in range(4):
        print("current player:", lop[self.current_player].name)
        print("your discards:", printable_discards)
        print("options: chi, pon, kan, ron, tsumo, riichi")
        lop[self.current_player].draw_tile(deck, False)
        if self.current_player.can_tsumo():
          if self.current_player.tsumo():
            return
        if self.current_player.can_self_kan():
          if self.current_player.self_kan(self.current_player.can_self_kan()):
            if self.current_player.can_tsumo():
              if self.current_player.tsumo():
                self.current_player.rinshan = True
                return
        next_players = [lop[(self.current_player + 1) % 4], lop[(self.current_player + 2) % 4],
                        lop[(self.current_player + 3) % 4]]
        if self.current_player.can_complete_kan():
          if self.current_player.complete_kan(self.current_player.can_complete_kan()):
            for p in next_players:
              if p.can_ron(self.current_player.hand.drawn_tile):
                if p.ron():
                  p.chankan = True
                  return
            if self.current_player.can_tsumo():
              if self.current_player.tsumo():
                self.current_player.rinshan = True
                return

        t = lop[self.current_player].play_tile()
        players_that_can_take = [next_players[0].can_take(t), next_players[1].can_take(t), next_players[2].can_take(t)]

        for i in range(3):
          if not players_that_can_take[i]:
            next_players.remove(i)
        for player in next_players:
          if player.can_ron(t):
            if player.ron(t):
              return
        for player in next_players:
          if player.can_take_kan(t):
            if player.take_kan(t):
              break
        for player in next_players:
          if player.can_pon(t):
            if player.pon(t):
              break
        for player in next_players:
          if player.can_chi(t):
            if player.chi(t, player.can_chi(t), self.current_player):
              break
        self.discards[self.current_player].append(t)
        printable_discards[self.current_player].append(t.tile_to_string())
        self.current_player = (self.current_player + 1) % 4

  def end_game(self):
    return