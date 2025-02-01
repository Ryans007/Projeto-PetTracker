from abc import ABCMeta, abstractmethod
from xmlrpc.client import boolean


class Person(metaclass=ABCMeta):
  def __init__(self) -> None:
    self.__cpf = "Not CPF"
    self.__name = "Not name"
    self.__email = "Not email"
    self.__celphone = "Not celular"
    self.__password = "Not password"
    
  @property
  def cpf(self) -> str:
    return self.__cpf

  @property
  def name(self) -> str:
    return self.__name  
  
  @property
  def email(self) -> str:
    return self.__email   
     
  @property
  def celphone(self) -> str:
    return self.__celphone   
  
  @property
  def password(self) -> str:
    return self.__password   
  
  @cpf.setter
  def cpf(self, cpf: str) -> None:
    self.__cpf = cpf

  @name.setter
  def name(self, name: str) -> None:
    self.__name = name    
  
  @email.setter
  def email(self, email: str) -> None:
    self.__email = email    
  
  @celphone.setter
  def celphone(self, celphone: str) -> None:
    self.__celphone= celphone   
    
  @password.setter
  def password(self, password: str) -> None:
    self.__password= password 
  
  @abstractmethod  
  def register(self, cpf: str, name:str, email: str, celphone: str, password: str) -> boolean: pass
  
  @abstractmethod
  def login(self, email: str, senha: str) -> boolean: pass
    
    
class User(Person):
  def __init__(self) -> None:
    super().__init__()
      
  def register(self, cpf: str, name:str, email: str, celphone: str, password: str) -> boolean:
    self.cpf = cpf 
    self.name = name
    self.email = email
    self.celphone = celphone
    self.password = password