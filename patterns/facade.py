from _class.territory import Territory
from _class.animal import Animal
from _class.person import Admin, User
from database.database import Database
from patterns.proxy import TerritoryProxy, UserProxy
from patterns.adapter import CoordinateAdapter
import sqlite3

class SystemFacade:
    _instance = None  # Singleton instance for SystemFacade

    def __new__(cls):
        # Ensure only one instance of SystemFacade is created (Singleton pattern)
        if cls._instance is None:
            cls._instance = super(SystemFacade, cls).__new__(cls)
            cls._instance._initialize()  # Initialize the instance
        return cls._instance

    def _initialize(self):
        # Initialize database connection and other attributes
        self.db = Database()  # Create a database instance
        self.conn = self.db.get_connection()  # Get the database connection
        self.cursor = self.conn.cursor()  # Create a cursor for database operations
        self.admin = None  # Initialize admin attribute as None

    def get_territory_by_id(self, id: int):
        # Retrieve a territory by its ID using the TerritoryProxy
        return TerritoryProxy.get_by_id(self.conn, id)

    def get_user_by_id(self, id: int) -> User:
        # Retrieve a user by their ID using the UserProxy
        return UserProxy.get_by_id(self.conn, id)

    def create_admin(self, name: str, email: str, password: str, celphone: str):
        try:
            # Create a new Admin object and save it to the database
            self.admin = Admin(name=name, email=email, password=password, celphone=celphone)
            self.admin.save(self.conn)  # Save the admin to the database
            return self.admin  # Return the created admin
        except sqlite3.Error as e:
            # Rollback the transaction in case of an error and print the error message
            self.conn.rollback()
            print(f"Erro ao criar admin: {e}")
            return None  # Return None if an error occurs

    def create_territory(self, name: str, lat1: float, long1: float, lat2: float, long2: float) -> Territory | None:
        try:
            # Check if an admin is logged in
            if self.admin is not None:
                # Use CoordinateAdapter to convert latitude and longitude to coordinates
                adapter = CoordinateAdapter(lat1, long1, lat2, long2)
                x, y = adapter.get_coordinates()  # Get the converted coordinates
                # Create a new territory using the admin's method
                territory = self.admin.add_territory(name=name, x=x, y=y, conn=self.conn)
                return territory  # Return the created territory
        except sqlite3.Error as e:
            # Rollback the transaction in case of an error and print the error message
            self.conn.rollback()
            print(f"Erro ao criar território: {e}")
            return None  # Return None if an error occurs

    def update_territory(self, id: int, name: str, x: int, y: int, owner_id: int):
        # Retrieve the territory by its ID
        territory = self.get_territory_by_id(id)
        if territory:
            # Update the territory's attributes if new values are provided
            if name:
                territory.name = name
            if x:
                territory.x = x
            if y:
                territory.y = y
            # Save the updated territory to the database
            territory.save(self.conn)

    def delete_territory(self, id: int):
        # Retrieve the territory by its ID
        territory = self.get_territory_by_id(id)
        if territory:
            # Remove the territory association from users
            self.cursor.execute("UPDATE users SET territory_id = NULL WHERE territory_id = ?", (id,))

            # Delete the territory from the database
            territory.delete(self.conn)
            
            # Retrieve all animal IDs associated with the territory
            self.cursor.execute("SELECT id FROM animals WHERE territory_id = ?", (id,))
            animal_ids = [row[0] for row in self.cursor.fetchall()]
            
            if animal_ids:
                # Delete all trackers associated with the animals
                for animal_id in animal_ids:
                    self.cursor.execute("DELETE FROM tracker WHERE animal_id = ?", (animal_id,))
                
                # Delete all animals associated with the territory
                self.cursor.execute("DELETE FROM animals WHERE territory_id = ?", (id,))
            
            # Commit the changes to the database
            self.conn.commit()

    def create_user(self, name: str, password: str, email: str, celphone: str, territory_id) -> User | None:
        try:
            # Check if an admin is logged in
            if self.admin is not None:
                # Create a new user using the admin's method and associate it with a territory
                user = self.admin.add_user(name=name, password=password, email=email, celphone=celphone, territory=self.get_territory_by_id(territory_id))
                # Retrieve the associated territory
                territorie_associeted = self.get_territory_by_id(territory_id)
                # Save the user to the database using the UserProxy
                UserProxy.save(user, self.conn)
                if territorie_associeted:
                    # Set the user as the owner of the territory and save the territory
                    territorie_associeted.owner_id = user.id
                    territorie_associeted.save(self.conn)
                return user  # Return the created user
        except sqlite3.Error as e:
            # Rollback the transaction in case of an error and print the error message
            self.conn.rollback()
            print(f"Erro ao criar usuário: {e}")
            return None  # Return None if an error occurs

    def update_user(self, id: int, name: str, password: str, email: str, celphone: str, territory: Territory):
        # Retrieve the user by their ID
        user: User = self.get_user_by_id(id)
        if user:
            # Update the user's attributes if new values are provided
            if name:
                user.name = name
            if password:
                user.password = password
            if email:
                user.email = email
            if celphone:
                user.celphone = celphone
            # Save the updated user to the database using the UserProxy
            UserProxy.save(user, self.conn)

    def delete_user(self, id: int):
        # Retrieve the user by their ID
        user = self.get_user_by_id(id)
        if user:
            # Delete the user from the database using the UserProxy
            UserProxy.delete(user, self.conn)
            # Remove the user's ownership from all territories
            self.cursor.execute('''
            UPDATE territories
            SET owner_id = NULL
            WHERE owner_id = ?;                 
            ''', (id,))
            # Commit the changes to the database
            self.conn.commit()

    def delete_animal(self, id: int):
        # Delete the animal from the database by its ID
        self.cursor.execute('''
        DELETE FROM animals WHERE id = ?                    
        ''', (id,))
        self.conn.commit()  # Commit the changes to the database

        # Delete the tracker associated with the animal
        self.cursor.execute('''
        DELETE from tracker WHERE                    
        animal_id = ?''', (id,))
        self.conn.commit()  # Commit the changes to the database

    def add_animal_to_territory(self, name: str, specie: str, age: int, territory_id: int, description="No Description"):
        try:
            # Check if an admin is logged in
            if self.admin is not None:
                # Create a new animal using the admin's method and associate it with a territory
                animal = self.admin.add_animal(name=name, specie=specie, age=age, territory=self.get_territory_by_id(territory_id), description=description)
                # Save the animal to the database
                animal.save(self.conn)
                # Set the tracker's animal_id to the newly created animal's ID and save the tracker
                animal.tracker.animal_id = animal.id
                animal.tracker.save(self.conn)
                # Save the animal again to ensure all changes are persisted
                animal.save(self.conn)
                return animal  # Return the created animal
        except sqlite3.Error as e:
            # Rollback the transaction in case of an error and print the error message
            self.conn.rollback()
            print(f"Erro ao criar usuário: {e}")
            return None  # Return None if an error occurs

    def list_admins(self):
        # Execute a query to fetch all admins from the database
        self.cursor.execute('SELECT * FROM admins')
        # Return all rows from the query result
        return self.cursor.fetchall()

    def list_users(self):
        # Execute a query to fetch all users from the database
        self.cursor.execute('SELECT * FROM users')
        rows = self.cursor.fetchall()  # Fetch all rows from the query result
        # Create a list of User objects from the fetched rows
        return [User(id=row[0], name=row[1], email=row[2], password=row[3], celphone=row[4], territory=row[5]) for row in rows]

    def list_territories(self):
        # Execute a query to fetch all territories from the database
        self.cursor.execute('SELECT * FROM territories')
        rows = self.cursor.fetchall()  # Fetch all rows from the query result
        # Create a list of Territory objects from the fetched rows
        return [Territory(id=row[0], name=row[1], x=row[2], y=row[3], owner_id=row[4]) for row in rows]

    def list_animais(self):
        # Execute a query to fetch all animals from the database
        self.cursor.execute('SELECT * From animals')
        return self.cursor.fetchall()  # Return all rows from the query result

    def list_animals_in_territory(self, territory_id: int):
        # Execute a query to fetch all animals in a specific territory
        self.cursor.execute('SELECT * FROM animals WHERE territory_id = ?', (territory_id,))
        rows = self.cursor.fetchall()  # Fetch all rows from the query result
        animals = []  # Initialize an empty list to store Animal objects
        for row in rows:
            # Retrieve the territory associated with the animal
            territory = self.get_territory_by_id(row[5])  # Assuming territory_id is at index 5
            # Create an Animal object and add it to the list
            animal = Animal(id=row[0], name=row[1], specie=row[2], age=row[3], territory=territory, description=row[4])
            animals.append(animal)
        return animals  # Return the list of Animal objects

    def list_animals_in_territory_user(self, user_id: int):
        # Retrieve the user by their ID
        user = self.get_user_by_id(user_id)
        # Execute a query to fetch all animals in the user's associated territory
        self.cursor.execute('SELECT * FROM animals WHERE territory_id = ?', (user.territory,))
        rows = self.cursor.fetchall()  # Fetch all rows from the query result
        animals = []  # Initialize an empty list to store Animal objects
        for row in rows:
            # Retrieve the territory associated with the animal
            territory = self.get_territory_by_id(row[5])  # Assuming territory_id is at index 5
            # Create an Animal object and add it to the list
            animal = Animal(id=row[0], name=row[1], specie=row[2], age=row[3], territory=territory, description=row[4])
            animals.append(animal)
        return animals  # Return the list of Animal objects

    def close_connection(self):
        # Close the database connection
        self.conn.close()

    def show_territory_admin(self, territory_id: int, stop_event):
        cursor = self.conn.cursor()  # Create a new cursor for database operations
        try:
            # Retrieve the territory by its ID
            territory = self.get_territory_by_id(territory_id)
            if territory:
                # Fetch animals associated with the territory
                animals = self.list_animals_in_territory(territory_id)
                # Clear existing animals and add the new ones
                territory.animals = animals
                # Display the territory with its animals
                territory.show_territory(stop_event)
        finally:
            cursor.close  # Close the cursor

    def show_territory_null(self):
        # Execute a query to fetch territories with no owner (owner_id is NULL)
        self.cursor.execute('''SELECT * 
                            FROM territories WHERE owner_id IS NULL
                            ''')
        rows = self.cursor.fetchall()  # Fetch all rows from the query result
        # Create a list of Territory objects from the fetched rows
        return [Territory(id=row[0], name=row[1], x=row[2], y=row[3], owner_id=row[4]) for row in rows]

    def show_territory_user(self, user_id: int, stop_event):
        # Execute a query to fetch territories owned by the specified user
        self.cursor.execute('''SELECT * 
                            FROM territories t 
                            JOIN users u ON t.owner_id = ?''', (user_id,))
        rows = self.cursor.fetchall()  # Fetch all rows from the query result
        for row in rows:
            # Create a Territory object from the fetched row
            territory = Territory(id=row[0], name=row[1], x=row[2], y=row[3], owner_id=row[4])
            if territory:
                if territory.id is not None:
                    # Fetch animals associated with the territory
                    animals = self.list_animals_in_territory(territory.id)
                    territory.animals = animals
                    # Display the territory with its animals
                    territory.show_territory(stop_event)
                else:
                    # Raise an exception if the territory ID is invalid
                    raise Exception("Erro ao buscar território: ID inexistente!!!")

    def show_location_history(self, animal_id: int):
        # Retrieve the animal by its ID
        animal = Animal.get_by_id(self.conn, animal_id)

        # Execute a query to fetch location history for the animal's tracker
        self.cursor.execute('''SELECT * FROM location
                            where tracker_id = ?  
                            ''', (animal.tracker_id,))

        # Return all rows from the query result
        return self.cursor.fetchall()
        
    def get_admin_by_email(self, email: str):
        # Execute a query to fetch an admin by their email
        self.cursor.execute("SELECT * FROM admins WHERE email = ?", (email,))
        # Return the first row from the query result (or None if no match is found)
        return self.cursor.fetchone()

    def get_user_by_email(self, email: str):
        # Execute a query to fetch a user by their email
        self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        # Return the first row from the query result (or None if no match is found)
        return self.cursor.fetchone()

    def delete_location_history(self):
        # Execute a query to delete all records from the location table
        self.cursor.execute("DELETE FROM location")
        # Commit the changes to the database
        self.conn.commit()

    def close(self):
        # Close the database connection
        self.db.close_connection()