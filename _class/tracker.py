import random
import time
import threading
from _class.location import Location
from termcolor import colored
from database.database import Database

class Tracker():
    def __init__(self, state: bool, x_limit: int, y_limit: int, id: int | None = None) -> None:
        # Initializing Tracker object with initial state, x and y limits, and optional ID
        self.id = id  # Optional ID of the tracker
        self.state = state  # State of the tracker (active/inactive)
        self.last_update = None  # Timestamp of the last location update
        self.x_limit = x_limit  # Max X boundary for movement
        self.y_limit = y_limit  # Max Y boundary for movement
        # Generate random initial position within the boundaries
        self.x = random.randint(1, x_limit - 2)
        self.y = random.randint(1, y_limit - 2)
        self.current_location = Location(self.x, self.y)  # Store the current location as a Location object
        self._running = False  # Flag to control the location generation thread
        self._saving_running = False  # Flag to control the saving thread
        self.conn = None  # Placeholder for the database connection, to be set later
        self.animal_id : int | None = None  # ID of the associated animal (to save in the database)

    def location_generate(self) -> Location:
        """Generate a new location based on random movement direction."""
        direction = random.choice(['up', 'down', 'left', 'right'])
        if direction == 'up':
            self.y -= 1
        elif direction == 'down':
            self.y += 1
        elif direction == 'left':
            self.x -= 1
        elif direction == 'right':
            self.x += 1

        return Location(self.x, self.y)  # Return updated location as a Location object

    def _location_loop(self):
        """Loop that continuously generates locations in the background."""
        while self._running:
            self.current_location = self.location_generate()  # Update current location
            self.last_update = time.time()  # Record the time of the update
            time.sleep(0.2)  # Interval between location updates (adjustable)

    def start_location_generation(self):
        """Start the thread that continuously generates locations."""
        self._running = True
        # Start a background thread to handle continuous location updates
        self._thread = threading.Thread(target=self._location_loop, daemon=True)
        self._thread.start()

    def stop_location_generation(self):
        """Stop the continuous location generation."""
        self._running = False  # Set the running flag to false
        if hasattr(self, '_thread'):
            self._thread.join()  # Wait for the location generation thread to finish


    def start_location_saving(self, conn, animal_name: str):
        """
        Starts a thread that saves the current location to the database every 60 seconds.
        Receives the database connection and the animal's name to register in the table.
        """
        self.conn = conn  # Store the database connection
        self.animal_name = animal_name  # Store the animal's name
        self._saving_running = True  # Flag to control the saving loop
        self._saving_thread = threading.Thread(target=self._location_saving_loop, daemon=True)
        self._saving_thread.start()  # Start the thread for saving location

    def _location_saving_loop(self):
        """Loop that saves the location every interval, stopping if the tracker record no longer exists."""
        while self._saving_running:
            # Check if the tracker still exists in the database
            db = Database()
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id FROM tracker WHERE id = ?", (self.id,))
            row = cur.fetchone()
            cur.close()
            conn.close()

            if not row:
                # If the tracker is not found, stop the saving thread
                # print("Tracker not found in DB. Stopping location saving thread.")
                self.stop_location_saving()  # Stop the location saving loop
                break

            # Update the last update time
            self.last_update = time.time()

            # Save the current location and wait for the appropriate interval
            self.location_save()
            # Choose sleep time based on position (inside or outside territory limits)
            if not (1 <= self.current_location.x < self.x_limit - 1 and 1 <= self.current_location.y < self.y_limit - 1):
                time.sleep(15)  # Sleep 15 seconds if outside territory
            else:
                time.sleep(30)  # Sleep 30 seconds if inside territory

    def stop_location_saving(self):
        """Stops the location saving thread."""
        self._saving_running = False  # Stop the saving loop
        # Ensure the saving thread exists and is not the current thread before joining.
        if hasattr(self, '_saving_thread') and threading.current_thread() != self._saving_thread:
            self._saving_thread.join()  # Wait for the saving thread to finish

    def location_save(self):
        """Save the current location to the database."""
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            # Insert current location into the location table
            cursor.execute('''
                INSERT INTO location (animal_name, x, y, time, tracker_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.animal_name, self.current_location.x, self.current_location.y, self.last_update, self.id))
            conn.commit()
        except Exception as e:
            print("Error:", e)  # Print error message if something goes wrong
        finally:
            cursor.close()  # Close the cursor
            conn.close()  # Close the connection

    def save(self, conn) -> None:
        """Save the tracker information (like animal_id) to the database."""
        cursor = conn.cursor()
        try:
            if self.id is None:
                # Insert a new tracker record if it doesn't exist
                cursor.execute('''
                            INSERT INTO tracker (animal_id)
                            VALUES (?)
                            ''', 
                            (self.animal_id,))
                self.id = cursor.lastrowid  # Get the newly inserted row ID
            else:
                # Update an existing tracker record
                cursor.execute('''
                            UPDATE tracker 
                            SET animal_id = ?
                            WHERE id = ?
                            ''', 
                            (self.animal_id, self.id))
            conn.commit()  # Commit changes to the database
        finally:
            cursor.close()  # Close the cursor

    def __repr__(self) -> str:
        """Returns a string representation of the Tracker object."""
        return f"{type(self).__name__}({self.state!r}, {self.x_limit!r}, {self.y_limit!r})"
