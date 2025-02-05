import sqlite3

def database_init():
    conn = sqlite3.connect("pettracker.db")
    cursor = conn.cursor()

    #tabela de admins
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        celphone TEXT NOT NULL
                   )
                   ''')
    
    #tabela de animais
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS territories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        x INTEGER NOT NULL,
        y INTEGER NOT NULL,
        owner_id INTEGER
    )
    ''')

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
    conn.close()

if __name__ == "__main__":
    database_init()