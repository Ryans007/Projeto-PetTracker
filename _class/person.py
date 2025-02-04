from _class.territory import Territory
from _class.animal import Animal
from _class.tracker import Tracker
import random

class Person():
  def __init__(self, name: str, email: str, celphone: str, id: None | int = None) -> None:
    if id is None:
      self.__id = random.randint(0, 500)
    else:
      self.__id = id
    self.__name = name
    self.__email = email
    self.__celphone = celphone
  
  @property
  def name(self) -> str:
    return self.__name
  
  @name.setter
  def name(self, name) -> None:
    self.__name = name

  @property
  def email(self) -> str:
    return self.__email
  
  @email.setter
  def email(self, email) -> None:
    self.__email = email    
    
  @property
  def celphone(self) -> str:
    return self.__celphone
  
  @celphone.setter
  def celphone(self, celphone) -> None:
    self.__celphone = celphone
    
  # def vizualize_animal(self) -> Location: pass
  
  # def vizualize_historic(self) -> Location: pass
  
  def __repr__(self) -> str:
    return f"{type(self).__name__}({self.__name!r}, {self.__email!r}, {self.__celphone}, {self.__id})"

class User(Person):
  def __init__(self, name: str, email: str, celphone: str, territory: Territory, id: None | int = None) -> None:
    super().__init__(name, email, celphone, id)
    self.territory = territory
  
class Admin(Person):
  def __init__(self, name: str, email: str, celphone: str, id: int | None = None) -> None:
    super().__init__(name, email, celphone, id)
    self.user_list = []
    
  def add_animal(self, name: str, specie: str, age: int, tracker: Tracker, territory: Territory, description: str = "No Description") -> bool:
    animal = Animal(name, specie, age, tracker, territory, description)
    if animal:
      territory.add_animal(animal)
      print("Animal adicionado com sucesso!!!")
      return True
    print("Falha ao adicionar o animal!!!")
    return False
    
  def add_user(self, name: str, email: str, celphone: str, territory: Territory, id: None | int = None) -> bool:
    user = User(name, email, celphone, territory, id)
    if user:
      self.user_list.append(user)
      territory.add_owner(user)
      print("Usúario adicionado com sucesso!!!")
      return True
    print("Falha ao adicionar o usúario!!!")
    return False

  