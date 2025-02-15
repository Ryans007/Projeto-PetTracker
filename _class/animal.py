from _class.tracker import Tracker
from _class.territory import Territory
import threading
import time
import random

class Animal():
  def __init__(self, name: str, specie: str, age: int, territory: Territory, description: str = "No Description", id: int | None = None) -> None:
    self.__name = name
    self.__specie = specie
    self.__age = age
    self.__description = description
    self.territory = territory
    self.tracker = Tracker(True)
    self.__id = id
    self.x = random.randint(1, territory.x - 2)  # Posição inicial aleatória
    self.y = random.randint(1, territory.y - 2)

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
  
  def save(self, conn):
      cursor = conn.cursor()
      try:
          if self.__id is None:
              cursor.execute('''
                          INSERT INTO animals (name, specie, age, description, territory_id)
                          VALUES(?, ?, ?, ?, ?)
                          ''', (self.name, self.specie, self.age, self.description, self.territory.id))
              self.id = cursor.lastrowid
          else:
              cursor.execute('''
                          UPDATE animals
                          SET name = ?, specie = ?, age = ?, description = ?, territory_id = ?
                          WHERE id = ?
                          ''', (self.name, self.specie, self.age, self.description, self.territory.id, self.id))
          conn.commit()    
      finally:
          cursor.close()
      
  @staticmethod
  def get_by_id(conn, id: int):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM animals WHERE id = ?', (id,))
    row = cursor.fetchone()
    if row:
      return Animal(id=row[0], name=row[1], specie=row[2], age=row[3], territory=row[4], description=row[5])
    raise Exception("Nenhum animal corresponde ao id")
   
  def delete(self, conn):
    if self.id is not None:
      cursor = conn.cursor()
      cursor.execute('DELETE FROM animals WHERE id = ?', (self.id,))
      conn.commit()
      self.id = None 

if __name__ == "__main__": pass
  # territory = Territory("IFPB", 50, 60)
  # animal = Animal("Rogerio", 1, "Cachorro", 12)
  # territory.add_animal(animal)
  
  # animal_thread = threading.Thread(target=animal.tracker.location_generate, daemon=True)
  # animal_thread.start()
  
  # print(territory.show_territory(13,13))
  # O restante do programa continua executando normalmente
