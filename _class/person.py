# type: ignore
from _class.territory import Territory  # Importing the Territory class
from _class.animal import Animal  # Importing the Animal class
from abc import ABCMeta, abstractmethod  # Importing abstract base class tools
from utils import hash_password  # Importing a utility function for password hashing
from patterns.builders import TerritoryBuilder  # Importing the TerritoryBuilder class

# Abstract base class template for a person
class PersonTemplate(metaclass=ABCMeta):
    def __init__(self, name: str, email: str, password: str, celphone: str, id: None | int = None) -> None:
        # Private attributes for storing person details
        self.__id = id
        self.__name = name
        self.__email = email
        self.__password = password
        self.__celphone = celphone
    
    # Getter and setter for 'id'
    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, id) -> None:
        self.__id = id
      
    # Getter and setter for 'name'
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name) -> None:
        self.__name = name

    # Getter and setter for 'email'
    @property
    def email(self) -> str:
        return self.__email
    
    @email.setter
    def email(self, email) -> None:
        self.__email = email    
      
    # Getter and setter for 'celphone'
    @property
    def celphone(self) -> str:
        return self.__celphone
    
    @celphone.setter
    def celphone(self, celphone) -> None:
        self.__celphone = celphone

    # Getter and setter for 'password'
    @property
    def password(self) -> str:
        return self.__password
    
    @password.setter
    def password(self, password) -> None:
        self.__password = password
    
    # Abstract method to save the person in the database
    @abstractmethod
    def save(self, conn) -> None:
        pass
    
    # Abstract method to get a person by ID from the database
    @staticmethod
    @abstractmethod
    def get_by_id(conn, id: int):
        pass
    
    # Abstract method to delete the person from the database
    @abstractmethod
    def delete(self, conn) -> None:
        pass

    # Duplicate abstract methods (save, get_by_id, delete) were present in the original code

    # String representation of the object
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.__name!r}, {self.__email!r}, {self.__celphone}, {self.__id})"

class User(PersonTemplate):
    def __init__(self, name: str, email: str, password: str, celphone: str, territory: Territory | None, id: int | None = None) -> None:
        # Initialize the User class by calling the parent constructor
        super().__init__(name, email, password, celphone, id)
        self.territory = territory  # Assign the user's territory
      
    def save(self, conn) -> None:
        """ Saves the user to the database. If the user does not have an ID, it inserts a new record;
            otherwise, it updates the existing one.
        """
        cursor = conn.cursor()
        try:
            hashed_password = hash_password(self.password)  # Hash the password before storing it
            
            if self.id is None:
                # Insert a new user into the database
                cursor.execute('''
                    INSERT INTO users (name, password, email, celphone, territory_id)
                    VALUES (?, ?, ?, ?, ?)
                ''', (self.name, hashed_password, self.email, self.celphone, self.territory.id))
                
                self.id = cursor.lastrowid  # Retrieve the last inserted ID
            else:
                # Update an existing user in the database
                cursor.execute('''
                    UPDATE users
                    SET name = ?, password = ?, email = ?, celphone = ?, territory_id = ?
                    WHERE id = ?
                ''', (self.name, hashed_password, self.email, self.celphone, self.territory.id))
            
            conn.commit()  # Commit changes to the database
        finally:
            cursor.close()  # Close the cursor to free resources
    
    @staticmethod
    def get_by_id(conn, id: int) -> 'User':
        """ Retrieves a user from the database by their ID. """
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (id,))
        row = cursor.fetchone()
        
        if row:
            # Create a User object from the retrieved row
            return User(id=row[0], name=row[1], email=row[2], password=row[3], celphone=row[4], territory=row[5])
    
    def delete(self, conn) -> None:
        """ Deletes the user from the database if they have an ID. """
        if self.id is not None:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (self.id,))
            conn.commit()  # Commit deletion
            self.id = None  # Set ID to None to indicate the user no longer exists
          
    def __repr__(self):
        """ Returns a string representation of the User object. """
        return f"{type(self).__name__}(id={self.id}, name={self.name}, email={self.email}, password={self.password}, celphone={self.celphone}, territory={self.territory})"

  
class Admin(PersonTemplate):
    def __init__(self, name: str, email: str, password: str, celphone: str, id: int | None = None) -> None:
        # Initialize the Admin class by calling the parent constructor
        super().__init__(name, email, password, celphone, id)
        self.user_list = []  # List to store users
        self.territory_list = []  # List to store territories
        self.animal_list = []  # List to store animals
      
    def add_animal(self, name: str, specie: str, age: int, territory: Territory, description: str = "No Description"):
        """ Creates a new animal and assigns it to a territory. """
        animal = Animal(name=name, specie=specie, age=age, territory=territory, description=description)
        self.animal_list.append(animal)  # Add the animal to the admin's list
        territory.add_animal(animal)  # Add the animal to the territory
        return animal
    
    def add_territory(self, name: str, x: int, y: int, conn, owner_id: int | None = None):
        """ Creates a new territory using the TerritoryBuilder and saves it to the database. """
        builder = TerritoryBuilder()
        territory = (
            builder.set_name(name)
                   .set_dimensions(x, y)
                   .set_owner(owner_id)
                   .build()
        )
        territory.save(conn)  # Save the territory to the database
        return territory
      
    def add_user(self, name: str, password: str, email: str, celphone: str, territory: Territory, id: None | int = None) -> User:
        """ Creates a new user and adds them to the admin's user list. """
        user = User(name=name, email=email, password=password, celphone=celphone, territory=territory, id=id)
        self.user_list.append(user)  # Add the user to the admin's list
        return user

    def save(self, conn) -> None:
        """ Saves the admin to the database. If the admin does not have an ID, it inserts a new record;
            otherwise, it updates the existing one.
        """
        cursor = conn.cursor()
        try:
            hashed_password = hash_password(self.password)  # Hash the password before storing it
            
            if self.id is None:
                # Insert a new admin into the database
                cursor.execute('''
                    INSERT INTO admins (name, email, password, celphone)
                    VALUES (?, ?, ?, ?)
                ''', (self.name, self.email, hashed_password, self.celphone))
                
                self.id = cursor.lastrowid  # Retrieve the last inserted ID
            else:
                # Update an existing admin in the database
                cursor.execute('''
                    UPDATE admins
                    SET name = ?, email = ?, password = ?, celphone = ?
                    WHERE id = ?
                ''', (self.name, self.email, hashed_password, self.celphone))
            
            conn.commit()  # Commit changes to the database
        finally:
            cursor.close()  # Close the cursor to free resources
        
    @staticmethod
    def get_by_id(conn, id: int):
        """ Retrieves an admin from the database by their ID. """
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admins WHERE id = ?', (id,))
        row = cursor.fetchone()
        
        if row:
            # Create an Admin object from the retrieved row
            return Admin(id=row[0], name=row[1], email=row[2], password=row[3], celphone=row[4])
          
    def delete(self, conn) -> None:
        """ Deletes the admin from the database if they have an ID. """
        if self.id is not None:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM admins WHERE id = ?', (self.id,))
            conn.commit()  # Commit deletion
            self.id = None  # Set ID to None to indicate the admin no longer exists
    
    def __repr__(self):
        """ Returns a string representation of the Admin object. """
        return f"{type(self).__name__}(id={self.id}, name={self.name}, email={self.email}, password={self.password}, celphone={self.celphone})"
