class Tile(object):
    """
    Tile is represented as tuple with properties 'suit' and 'value' (both strings).
    Tile can be evaluated if playable.
    """

    def __init__(self, s, v):
      self.suit = s
      self.value = v

    def suit_value(self):
      suit = self.suit
      value = self.value
      if (value == 'r') and (suit == 'm'):
        result = 5
      elif (value == 'r') and (suit == 'p'):
        result = 14
      elif (value == 'r') and (suit == 's'):
        result = 23
      elif (suit == 'w') or (suit == 'h'):
        if value == 'e':
          result = 28
        elif value == 's':
          result = 29
        elif value == 'w' and suit == 'w':
          result = 30
        elif value == 'n':
          result = 31
        elif value == 'g':
          result = 32
        elif value == 'r':
          result = 33
        else:
          result = 34
      else:
        result = int(value)
        if self.suit == "p":
          result += 9
        elif self.suit == "s":
          result += 18
      return result

    def tile_to_string(self):
      return self.suit + self.value

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.suit == other.suit and self.value == other.value
        return False