import email
from _class import territory
from _class.territory import Territory
from _class.animal import Animal
from _class.tracker import Tracker
from _class.person import Admin, User
#import random
import sqlite3
from utils import hash_password

from database.database import database_init

class SystemFacade:
    def __init__(self):        
        database_init()
        self.conn = sqlite3.connect('pettracker.db')
        self.cursor = self.conn.cursor()
        self.admin = None
        
    def create_admin(self, name: str, email: str, password: str,celphone: str):
        try:
            self.admin=Admin(name=name, email=email, password=password, celphone=celphone)
            self.admin.save(self.conn)
            return self.admin
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Erro ao criar admin: {e}")
            return None

    def create_user(self, name: str, password: str, email: str, celphone: str, territory: Territory) -> User | None:
        try:
            if self.admin is not None:
                user = self.admin.add_user(name, password, email, celphone, territory)
                user.save(self.conn)
                return user
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Erro ao criar usuário: {e}")
            return None

    def update_user(self, id:int, name: str, password: str, email: str, celphone: str, territory: Territory):
        user = self.get_user_by_id(id)
        if user:
            if name:
                user.name = name
            if password:
                user.password = password
            if email:
                user.email = email
            if celphone:
                user.celphone = celphone
            user.save(self.conn)
        
    def get_user_by_id(self, id: int):
        return User.get_by_id(self.conn, id)
    
    def delete_user(self, id: int):
        user = self.get_user_by_id(id)
        if user:
            user.delete(self.conn)
            
    def create_territory(self, name: str, x: int, y: int) -> Territory | None:
        try:
            territory = Territory(name=name, x=x, y=y)
            territory.save(self.conn)
            return territory
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Erro ao criar território: {e}")
            return None
        
    def get_territory_by_id(self, id: int):
        return Territory.get_by_id(self.conn, id)
    
    def update_territory(self, id: int, name: str, x: int, y: int):
        territory = self.get_territory_by_id(id)
        if territory:
            if name:
                territory.name = name
            if x:
                territory.x = x
            if y:
                territory.y = y
            territory.save(self.conn)
            
    def delete_territory(self, id: int):
        territory = self.get_territory_by_id(id)
        if territory:
            territory.delete(self.conn)
           
    def delete_animal(self, id: int):
        self.cursor.execute('''
        DELETE FROM animals WHERE id = ?                    
        ''', (id,))
        self.conn.commit()
        
    def add_animal_to_territory(self, name: str, specie: str, age: int, territory_id: int, description="No Description"):
        self.cursor.execute('''
        INSERT INTO animals (name, specie, age, description, territory_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, specie, age, description, territory_id))
        self.conn.commit()

    def list_admins(self):
        self.cursor.execute('SELECT * FROM admins')
        return self.cursor.fetchall()

    def list_users(self):
        self.cursor.execute('SELECT * FROM users')
        rows = self.cursor.fetchall()
        return [User(id=row[0], name=row[1], email=row[2], password=row[3], celphone=row[4],territory=row[5]) for row in rows]

    def list_territories(self):
        self.cursor.execute('SELECT * FROM territories')
        rows = self.cursor.fetchall()
        return [Territory(id=row[0], name=row[1], x=row[2], y=row[3]) for row in rows]
    
    def list_animais(self):
        self.cursor.execute('SELECT * From animals')
        return self.cursor.fetchall()

    def list_animals_in_territory(self, territory_id: int):
        self.cursor.execute('SELECT * FROM animals WHERE territory_id = ?', (territory_id,))
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()

    @staticmethod
    def show_territory(largura: int, altura: int):
        Territory.show_territory(largura, altura)        

    def get_admin_by_email(self, email: str):
        self.cursor.execute("SELECT * FROM admins WHERE email = ?", (email,))
        return self.cursor.fetchone()
    def get_user_by_email(self, email: str):
        self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return self.cursor.fetchone()
    