from datetime import datetime
import random
from typing import List

class Datetime(datetime):
  def __init__(self) -> None:
    super().__init__()

class Tracker():
  def __init__(self, id: int, state: bool, last_upgrade: Datetime, animal_id: int) -> None:
    pass
  def location_generate(self) -> List[int]:
    x = random.randint(0, 500)
    y = random.randint(0,500)
    
    actual_location = [x,y]
    
    return actual_location