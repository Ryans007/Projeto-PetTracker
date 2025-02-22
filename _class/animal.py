from _class.tracker import Tracker
from _class.territory import Territory

class Animal():
  def __init__(self, name: str, specie: str, age: int, territory: Territory, description: str = "No Description", id: int | None = None) -> None:
      self.__name = name
      self.__specie = specie
      self.__age = age
      self.__description = description
      self.territory = territory
      self.tracker = Tracker(True, territory.x, territory.y)
      self.__id = id
      # Inicia a geração contínua de localizações
      self.tracker.start_location_generation()
      # Define uma localização inicial
      self.x = self.tracker.current_location.x
      self.y = self.tracker.current_location.y

  def update_position(self):
      """Método para atualizar a posição do animal com base na localização do tracker."""
      self.x = self.tracker.current_location.x
      self.y = self.tracker.current_location.y
          
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
