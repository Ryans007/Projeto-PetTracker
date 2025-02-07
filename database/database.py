import sqlite3
import os

def database_init():
    try:
        script_dir = os.path.dirname(__file__)
        db_path = os.path.join(script_dir, 'pettracker.db')
        conn = sqlite3.connect("pettracker.db")
        cursor = conn.cursor()

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
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            celphone TEXT NOT NULL UNIQUE,
            territory_id INTEGER,
        )
        ''')
        
        # tabela de territorios
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS territories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            x INTEGER NOT NULL,
            y INTEGER NOT NULL,
                       
            owner_id INTEGER
        )
        ''')

        #tabela de animais
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

        conn.commit()
    except Exception as e:
        print(f"Erro ao criar o banco de dados: {e}")
        conn.close()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    database_init()