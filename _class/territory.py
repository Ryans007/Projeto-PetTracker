from bearlibterminal import terminal
import random
import time
import textwrap
from termcolor import colored
from datetime import datetime

# Class representing a territory with a name, coordinates (x, y), owner, and a list of animals
class Territory():
    def __init__(self, name: str, x: int, y: int, owner_id: int| None = None, id: int | None = None) -> None:
        self.__id = id  # Territory ID (optional)
        self.__name = name  # Name of the territory
        self.__x = x  # X-coordinate of the territory
        self.__y = y  # Y-coordinate of the territory
        self.__owner_id = owner_id  # Owner ID (optional)
        self.animals = []  # List to store animals in the territory
    
    # Getter for the territory's ID
    @property
    def id(self) -> int | None:
        return self.__id
    
    # Setter for the territory's ID
    @id.setter
    def id(self, id: int) -> None:
        self.__id = id
    
    # Getter for the territory's name
    @property
    def name(self) -> str:
        return self.__name
    
    # Setter for the territory's name
    @name.setter
    def name(self, name: str) -> None:
        self.__name = name
    
    # Getter for the territory's X-coordinate
    @property
    def x(self) -> int:
        return self.__x 
    
    # Setter for the territory's X-coordinate
    @x.setter
    def x(self, x: int) -> None:
        self.__x = x
        
    # Getter for the territory's Y-coordinate
    @property
    def y(self) -> int:
        return self.__y 
    
    # Setter for the territory's Y-coordinate
    @y.setter
    def y(self, y: int) -> None:
        self.__y = y

    # Getter for the territory's owner ID
    @property
    def owner_id(self) -> int | None:
        return self.__owner_id 
    
    # Setter for the territory's owner ID
    @owner_id.setter
    def owner_id(self, owner_id: int) -> None:
        self.__owner_id = owner_id

    # Method to add an animal to the territory
    def add_animal(self, animal) -> None:
        self.animals.append(animal)

    def show_territory(self, stop_event):
        territory_width = self.x  # Width of the territory
        territory_height = self.y  # Height of the territory
        message_area_lines = 3  # Number of lines for message display
        window_height = territory_height + message_area_lines  # Total window height

        # Adjust the window size to fit your monitor. If needed, set fixed values.
        terminal.open()
        terminal.set(f"window: size={territory_width}x{window_height}, cellsize=auto, title='{self.name}'")

        try:
            print(f"Notificações {self.name}:\n")
            while not stop_event.is_set():
                terminal.clear()

                # 1) Update the position of animals
                for animal in self.animals:
                    animal.update_position()

                # 2) Draw borders around the territory
                for x in range(territory_width):
                    terminal.put(x, 0, '#')  # Top border
                    terminal.put(x, territory_height - 1, '#')  # Bottom border
                for y in range(territory_height):
                    terminal.put(0, y, '#')  # Left border
                    terminal.put(territory_width - 1, y, '#')  # Right border

                for animal in self.animals:
                    # Check if the animal is inside the territory
                    if 1 <= animal.x < territory_width - 1 and 1 <= animal.y < territory_height - 1:
                        terminal.put(animal.x, animal.y, animal.name[0])  # Display the first letter of the animal's name
                        # If the animal was previously marked as outside, notify that it returned
                        if getattr(animal, 'ja_aviso', False):
                            print(colored(f"{animal.name} retornou ao território. Data: {datetime.fromtimestamp(animal.tracker.last_update).strftime('%d/%m/%Y %H:%M:%S.%f')[:-3]}", "green"))
                        animal.ja_aviso = False  # Reset the warning
                    else:
                        # If the animal is outside and hasn't been warned yet
                        if not getattr(animal, 'ja_aviso', False):
                            print(colored(f"{animal.name} está fora do território - X: {animal.x}, Y: {animal.y}, Data: {datetime.fromtimestamp(animal.tracker.last_update).strftime('%d/%m/%Y %H:%M:%S.%f')[:-3]}", "red"))
                            animal.ja_aviso = True  # Mark as warned

                # 4) Check which animals are inside and outside
                escaped_animals = [
                    a for a in self.animals
                    if not (1 <= a.x < territory_width - 1 and 1 <= a.y < territory_height - 1)
                ]
                inside_animals = [
                    a for a in self.animals
                    if 1 <= a.x < territory_width - 1 and 1 <= a.y < territory_height - 1
                ]

                # 5) Build status strings
                escaped_text = "Fora: " + (", ".join(a.name for a in escaped_animals) if escaped_animals else "Nenhum")
                inside_text = "Dentro: " + (", ".join(a.name for a in inside_animals) if inside_animals else "Nenhum")

                # 6) Display messages below the territory
                terminal.printf(0, territory_height,     escaped_text)  # Display escaped animals
                terminal.printf(0, territory_height + 1, inside_text)  # Display inside animals

                terminal.refresh()  # Refresh the terminal to apply changes

                # 7) Check if the user pressed 'Q' to quit
                if terminal.has_input():
                    key = terminal.read()
                    if key == terminal.TK_Q:
                        break

                time.sleep(0.2)  # Small delay for smoother updates

        except KeyboardInterrupt:
            pass  # Handle manual interruption gracefully
        finally:
            terminal.close()  # Ensure terminal closes correctly

        
    def save(self, conn):
        cursor = conn.cursor()
        try:
            if self.id is None:
                # If there's no ID, insert a new territory into the database
                cursor.execute('''
                            INSERT INTO territories (name, x, y, owner_id)
                            VALUES (?, ?, ?, ?)
                            ''', (self.name, self.x, self.y, self.owner_id))
                # Assign the last inserted ID to the object
                self.id = cursor.lastrowid
            else:
                # If an ID exists, update the existing territory record
                cursor.execute('''
                            UPDATE territories
                            SET id = ?, name = ?, x = ?, y = ?, owner_id = ?
                            WHERE id = ?
                            ''', (self.id, self.name, self.x, self.y, self.owner_id, self.id))
            # Commit the transaction to the database
            conn.commit()
        finally:
            cursor.close()  # Always close the cursor after the operation
            
    @staticmethod
    def get_by_id(conn, id: int) -> 'Territory':
        cursor = conn.cursor()
        # Retrieve a territory by its ID from the database
        cursor.execute('SELECT * FROM territories WHERE id = ?', (id,))
        row = cursor.fetchone()
        if row:
            # Return a Territory object based on the row retrieved
            return Territory(id=row[0], name=row[1], x=row[2], y=row[3], owner_id=row[4])
        # Raise an exception if no territory is found
        raise Exception("Nenhum territorio corresponde ao id")
        
    def delete(self, conn):
        if self.id is not None:
            cursor = conn.cursor()
            # Delete the territory from the database based on its ID
            cursor.execute('DELETE FROM territories WHERE id = ?', (self.id,))
            conn.commit()  # Commit the deletion
            self.id = 0  # Set the ID to 0 after deletion
            
    def __repr__(self):
        # Provide a string representation of the Territory object
        return f"Territory(id={self.id}, name={self.name}, x={self.x}, y={self.y}, owner_id={self.owner_id})"


