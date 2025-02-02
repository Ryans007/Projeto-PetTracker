from ast import Tuple
from datetime import datetime
import random
from typing import Tuple
import time
from location import Location

class Tracker():
  def __init__(self, state: bool, id: int | None = None) -> None:
    if id is None:
      self.id = random.randint(0, 500)
    else:
      self.id = id
    self.state = state
    self.last_update = None
    self.location = Location()
  
  def location_generate(self) -> Tuple[int, int]:
    while True:
      x = random.randint(0, 500)
      y = random.randint(0,500)
      
      time.sleep(30)
      self.last_update = datetime.now()
      
      self.location.update_coordinated((x,y))


