from _class.tracker import Tracker
from _class.territory import Territory

class Animal():
    def __init__(self, name: str, specie: str, age: int, territory: Territory, description: str = "No Description", id: int | None = None) -> None:
        self.__name = name
        self.__specie = specie
        self.__age = age
        self.__description = description
        self.territory = territory
        # Creates a tracker with boundaries defined by the territory
        self.tracker = Tracker(True, territory.x, territory.y)
        self.__id = id
        # Starts continuous location generation
        self.tracker.start_location_generation()
        # Sets the initial location based on the tracker
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
        """Updates the animal's position based on the tracker location."""
        self.x = self.tracker.current_location.x
        self.y = self.tracker.current_location.y

    def save(self, conn):
        """
        Saves the animal's data to the database.
        After saving, starts the location saving thread in the Tracker.
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
        # Starts periodic location saving through the Tracker
        self.tracker.start_location_saving(self.conn, self.__name)

    @staticmethod
    def get_by_id(conn, id: int):
        """Retrieves an animal from the database by its ID."""
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM animals WHERE id = ?', (id,))
        row = cursor.fetchone()
        if row:
            animal = Animal(id=row[0], name=row[1], specie=row[2], age=row[3], description=row[4], territory=Territory.get_by_id(conn,row[5]))
            animal.tracker_id = row[6]
            return animal
        raise Exception("No animal matches the given ID")

    def delete(self, conn):
        """Deletes the animal from the database if it has a valid ID."""
        if self.__id is not None:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM animals WHERE id = ?', (self.__id,))
            conn.commit()
            self.__id = None

    def __repr__(self) -> str:
        """Returns a string representation of the Animal object."""
        return f"{type(self).__name__}({self.name!r}, {self.specie!r}, {self.age}, {self.__id}, {self.description}, {self.territory})"
