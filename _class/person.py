# type: ignore
from _class import territory
from _class.territory import Territory
from _class.animal import Animal
from _class.tracker import Tracker
import random
from abc import ABCMeta, abstractmethod
from utils import hash_password
from patterns.builders import TerritoryBuilder

class Person(metaclass=ABCMeta):
  def __init__(self, name: str, email: str, password: str, celphone: str, id: None | int = None) -> None:
    self.__id = id
    self.__name = name
    self.__email = email
    self.__password = password
    self.__celphone = celphone
  
  @property
  def id(self) -> int:
    return self.__id
  
  @id.setter
  def id(self, id) -> None:
    self.__id = id
    
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

  @property
  def password(self) -> str:
    return self.__password
  
  @password.setter
  def password(self, password) -> None:
    self.__password = password
  
  @abstractmethod
  def save(self, conn) -> None: pass
  
  @staticmethod
  @abstractmethod
  def get_by_id(conn, id: int): pass
  
  @abstractmethod
  def delete(self, conn) -> None: pass
    
  # def vizualize_animal(self) -> Location: pass
  
  # def vizualize_historic(self) -> Location: pass
  
  def __repr__(self) -> str:
    return f"{type(self).__name__}({self.__name!r}, {self.__email!r}, {self.__celphone}, {self.__id})"

class User(Person):
  def __init__(self, name: str, email: str, password: str, celphone: str, territory: Territory, id: int | None = None) -> None:
    super().__init__(name, email, password, celphone, id)
    self.territory = territory
    
  def save(self, conn) -> None:
    cursor = conn.cursor()
    try:
      hashed_password = hash_password(self.password)
      if self.id is None:
          cursor.execute('''
                        INSERT INTO users (name, password, email, celphone, territory_id)
                        VALUES (?, ?, ?, ?, ?)
                        ''', 
                        (self.name, hashed_password, self.email, self.celphone, self.territory.id))
          self.id = cursor.lastrowid
      else:
          cursor.execute('''
                      UPDATE users
                      SET name = ?, password = ?, email = ?, celphone = ?, territory_id = ?
                      WHERE id = ?
                      ''', 
                      (self.name, hashed_password, self.email, self.celphone, self.territory.id))
      conn.commit()
    finally:
      cursor.close()
  
  @staticmethod
  def get_by_id(conn, id: int) -> Person | None:
      cursor = conn.cursor()
      cursor.execute('SELECT * FROM users WHERE id = ?', (id,))
      row = cursor.fetchone()
      if row:
          return User(id=row[0], name=row[1], email=row[2], password=row[3], celphone=row[4], territory=row[5]) 
  
  def delete(self, conn) -> None:
    if self.id is not None:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (self.id,))
        conn.commit()
        self.id = None
        
  def __repr__(self):
    return f"User(id={self.id}, name={self.name}, email={self.email}, password={self.password}, celphone={self.celphone}, territory={self.territory})"
  
class Admin(Person):
  def __init__(self, name: str, email: str, password: str, celphone: str, id: int | None = None) -> None:
    super().__init__(name, email, password, celphone, id)
    self.user_list = []
    self.territory_list = []
    self.animal_list = []
    
  def add_animal(self, name: str, specie: str, age: int, territory: Territory, description: str = "No Description"):
    animal = Animal(name=name, specie=specie, age=age, territory=territory, description=description)
    self.animal_list.append(animal)
    territory.add_animal(animal)
    return animal
  
  def add_territory(self , name: str, x: int, y: int, conn):
    builder = TerritoryBuilder()
    territory = (
        builder.set_name(name)
              .set_dimensions(x, y)
              .set_owner(self.name)
              .build()
    )
    territory.save(conn)
    return territory
    
  def add_user(self, name: str, password: str, email: str, celphone: str, territory: Territory, id: None | int = None) -> User:
    user = User(name, password, email, celphone, territory, id)
    self.user_list.append(user)
    return user

  def save(self, conn) -> None:
    cursor = conn.cursor()
    try:
      hashed_password = hash_password(self.password)
      if self.id is None:
          cursor.execute('''
                        INSERT INTO admins (name, email, password, celphone)
                        VALUES (?, ?, ?, ?)
                        ''', 
                        (self.name, self.email, hashed_password, self.celphone))
          self.id = cursor.lastrowid
      else:
          cursor.execute('''
                      UPDATE admins
                      SET name = ?, email = ?, password = ?, celphone = ?
                      WHERE id = ?
                      ''', 
                      (self.name, self.email, hashed_password, self.celphone))
      conn.commit()
    finally:
      cursor.close()
      
  @staticmethod
  def get_by_id(conn, id: int) -> Person | None:
      cursor = conn.cursor()
      cursor.execute('SELECT * FROM admins WHERE id = ?', (id,))
      row = cursor.fetchone()
      if row:
          return Admin(id=row[0], name=row[1], email=row[2], password=row[3], celphone=row[4]) 
        
  def delete(self, conn) -> None:
    if self.id is not None:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM admins WHERE id = ?', (self.id,))
        conn.commit()
        self.id = None
  
  def __repr__(self):
    return f"Admin(id={self.id}, name={self.name}, email={self.email}, password={self.password}, celphone={self.celphone})"