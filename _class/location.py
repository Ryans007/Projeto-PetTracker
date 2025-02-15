import time
import random
from _class.territory import Territory

class Location():
  def __init__(self, x_limit: int, y_limit: int) -> None:
     self.x_limit = x_limit
     self.y_limit = y_limit
  def generate_coordenate(self) -> tuple:
      x = random.randint(1, self.x_limit - 2)  # Posição inicial aleatória
      y = random.randint(1, self.y_limit - 2)
      return (x, y)
