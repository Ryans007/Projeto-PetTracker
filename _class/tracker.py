from ast import Tuple
from datetime import datetime
import random
from typing import Tuple
import time
from _class.location import Location

class Tracker():
  def __init__(self, state: bool, id: int | None = None) -> None:
    if id is None:
      self.id = random.randint(0, 500)
    else:
      self.id = id
    self.state = state
    self.last_update = None
    self.location = Location()
  
  def location_generate(self) -> None:
    while True:
      time.sleep(2)
      print(self.location.generate_coordenate())

  

