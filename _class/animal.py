class Animal():
  def __init__(self, name: str, id: int, specie: str, age: int, tracker, territory, description: str = "No Description") -> None:
    self.name = name
    self.specie = specie
    self.age = age
    self.description = description
    self.territory = territory
    self.tracker = tracker
    self.id = id
  
  