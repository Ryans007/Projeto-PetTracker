class Territory():
  def __init__(self, name: str, x1: int, x2: int, y1: int, y2: int, owner = None) -> None:
    self.name = name
    self.x1 = x1
    self.x2 = x2
    self.y1 = y1 
    self.y2 = y2
    self.owner = owner
    self.animals = []
    
  def add_owner(self, owner) -> None:
    self.owner = owner
    
  def add_animal(self, animal) -> None:
    self.animals.append(animal)

if __name__ == "__main__": 
  print(104*"*")  
  for _ in range(20):
    print("*", 100*" ", "*")
  print(104*"*")
  


