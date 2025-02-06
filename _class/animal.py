
class Animal():
  def __init__(self, name: str, id: int, specie: str, age: int, tracker, territory, description: str = "No Description") -> None:
    self.__name = name
    self.__specie = specie
    self.__age = age
    self.__description = description
    self.territory = territory
    self.tracker = tracker
    self.__id = id

  @property
  def name(self) -> str:
    return self.__name
  
  @name.setter
  def name(self, name) -> None:
    self.__name = name

  @property
  def specie(self) -> str:
    return self.__specie
  
  @specie.setter
  def specie(self, specie) -> None:
    self.__specie = specie

  @property
  def age(self) -> int:
    return self.__age
  
  @age.setter
  def age(self, age) -> None:
    self.__age = age

  @property
  def description(self) -> str:
    return self.__description
  
  @description.setter
  def description(self, description) -> None:
    self.__description = description

  @property
  def id(self) -> int:
    return self.__id
  
  @id.setter
  def id(self, id) -> None:
    self.__id = id
  
    

  
  