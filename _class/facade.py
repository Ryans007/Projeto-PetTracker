from _class.territory import Territory
from _class.animal import Animal
from _class.tracker import Tracker
from _class.person import Admin, User
import random

class SystemFacade:
    def __init__(self):
        self.admins = []
        self.users = []
        self.territories = []
        self.animals = []

    def create_admin(self, name: str, email: str, celphone: str) -> Admin:
        admin = Admin(name, email, celphone)
        self.admins.append(admin)
        return admin

    def create_user(self, name: str, email: str, celphone: str, territory: Territory) -> User:
        user = User(name, email, celphone, territory)
        self.users.append(user)
        territory.add_owner(user)
        return user

    def create_territory(self, name: str, x: int, y: int) -> Territory:
        territory = Territory(name, x, y)
        self.territories.append(territory)
        return territory

    def add_animal_to_territory(self, admin: Admin, name: str, specie: str, age: int, territory: Territory, description="No Description") -> bool:
        tracker = Tracker(state=True) 
        return admin.add_animal(name, specie, age, tracker, territory, description)

    def show_territory(self, territory: Territory):
        territory.show_territory()

    def list_admins(self):
        return self.admins

    def list_users(self):
        return self.users

    def list_territories(self):
        return self.territories

    def list_animals_in_territory(self, territory: Territory):
        return territory.animals
