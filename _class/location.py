import time
import random

class Location():
  def generate_coordenate(self) -> tuple:
      x = random.randint(0, 500)
      y = random.randint(0, 500)
      return (x, y)
