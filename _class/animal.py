from _class.tracker import Tracker
from _class.territory import Territory

class Animal():
    def __init__(self, name: str, specie: str, age: int, territory: Territory, description: str = "No Description", id: int | None = None) -> None:
        self.__name = name
        self.__specie = specie
        self.__age = age
        self.__description = description
        self.territory = territory
        # Cria o tracker com os limites definidos pelo território
        self.tracker = Tracker(True, territory.x, territory.y)
        self.__id = id
        # Inicia a geração contínua de localizações
        self.tracker.start_location_generation()
        # Define a localização inicial com base no tracker
        self.x = self.tracker.current_location.x
        self.y = self.tracker.current_location.y
        self.tracker_id = self.tracker.id

        self.conn = None
        
    @property
    def id(self) -> int | None:
      return self.__id

    @id.setter
    def id(self, id: int) -> None:
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
  

    def update_position(self):
        """Atualiza a posição do animal com base na localização do tracker."""
        self.x = self.tracker.current_location.x
        self.y = self.tracker.current_location.y

    def save(self, conn):
        """
        Salva os dados do animal no banco de dados.
        Após salvar os dados, inicia a thread de salvamento de localização no Tracker.
        """
        self.conn = conn
        cursor = conn.cursor()
        try:
            if self.__id is None:
                cursor.execute(
                    '''INSERT INTO animals (name, specie, age, description, territory_id, tracker_id)
                       VALUES(?, ?, ?, ?, ?, ?)''',
                    (self.name, self.specie, self.age, self.description, self.territory.id, self.tracker.id)
                )
                self.__id = cursor.lastrowid
            else:
                cursor.execute(
                    '''UPDATE animals
                       SET name = ?, specie = ?, age = ?, description = ?, territory_id = ?, tracker_id = ?
                       WHERE id = ?''',
                    (self.name, self.specie, self.age, self.description, self.territory.id, self.tracker.id, self.id)
                )
            conn.commit()
        finally:
            cursor.close()
        # Inicia o salvamento periódico da localização através do Tracker
        self.tracker.start_location_saving(self.conn, self.__name)

    @staticmethod
    def get_by_id(conn, id: int):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM animals WHERE id = ?', (id,))
        row = cursor.fetchone()
        if row:
            animal = Animal(id=row[0], name=row[1], specie=row[2], age=row[3], description=row[4], territory=Territory.get_by_id(conn,row[5]))
            animal.tracker_id = row[6]
            return animal
        raise Exception("Nenhum animal corresponde ao id")

    def delete(self, conn):
        if self.__id is not None:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM animals WHERE id = ?', (self.__id,))
            conn.commit()
            self.__id = None
