from abc import ABCMeta, abstractmethod
import random

class User():
  def __init__(self, id: int, name: str, email: str, celphone: str) -> None:
    if id is None:
      self.__id = random.randint(10000000, 99999999)
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
    
    
class Admin(User):
  def __init__(self, id: int, name: str, email: str, celphone: str) -> None:
    super().__init__(id, name, email, celphone)
    
