from ast import Tuple
from datetime import datetime
import random
from typing import Tuple
import time
from _class.location import Location

class Tracker():
  def __init__(self, state: bool, x_limit: int, y_limit: int, id: int | None = None) -> None:
    if id is None:
      self.id = random.randint(0, 500)
    else:
      self.id = id
    self.state = state
    self.last_update = None
    self.location = Location(x_limit, y_limit)
  
  def location_generate(self) -> tuple:
    while True:
      return self.location.generate_coordenate()
  def tracker_delay(self) -> None:
    time.sleep(30)

  

