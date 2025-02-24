import sqlite3
import os

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        script_dir = os.path.dirname(__file__)
        db_path = os.path.join(script_dir, 'pettracker.db')
        self.db_path = db_path
        self.conn = self._create_connection()
        self._create_tables()

    def _create_connection(self):
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL;")
        return conn

    def _create_tables(self):
        cursor = self.conn.cursor()

        # tabela de admins
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            celphone TEXT NOT NULL
        )
        ''')

        # tabela de usuários
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            celphone TEXT NOT NULL UNIQUE,
            territory_id INTEGER
        )
        ''')

        # tabela de territorios
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS territories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            x INTEGER NOT NULL,
            y INTEGER NOT NULL,
            owner_id INT
        )
        ''')

        # tabela de animais
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS animals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specie TEXT NOT NULL,
            age INTEGER NOT NULL,
            description TEXT,
            territory_id INTEGER,
            tracker_id INTEGER
        )
        ''')

        # tabela de localização
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS location (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_name TEXT NOT NULL,
            x INTEGER,
            y INTEGER,
            time INTEGER,
            tracker_id INTEGER,
            FOREIGN KEY (tracker_id) REFERENCES tracker(id)
        );
        ''')

        # tabela de rastreadores
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracker (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_id INTEGER,
            FOREIGN KEY (animal_id) REFERENCES animals(id)
        );
        ''')

        self.conn.commit()

    def get_connection(self):
        return self._create_connection()

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self._instance = None

# Inicialização do banco de dados
if __name__ == "__main__":
    db = Database()
    db.get_connection()