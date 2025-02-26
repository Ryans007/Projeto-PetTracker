from _class.person import Admin, User
from _class.territory import Territory

class UserProxy:
    _cache = {}  # Cache to store User objects for quick access
      
    @staticmethod
    def get_by_id(conn, id: int) -> User:
        # Check if the user is already in the cache
        if id in UserProxy._cache:
            return UserProxy._cache[id]
        # Fetch the user from the database if not in cache
        user = User.get_by_id(conn, id)
        if user:
            UserProxy._cache[id] = user  # Add the user to the cache
        return user
    
    @staticmethod
    def save(user: User, conn):
        # Save the user to the database
        user.save(conn)
        if user.id:
            UserProxy._cache[user.id] = user  # Update the cache with the saved user
            
    @staticmethod
    def delete(user: User, conn):
        # Delete the user from the database
        user.delete(conn)
        if user.id in UserProxy._cache:
            del UserProxy._cache[user.id]  # Remove the user from the cache
      

class AdminProxy:
    _cache = {}  # Cache to store Admin objects for quick access

    @staticmethod
    def get_by_id(conn, id: int):
        # Check if the admin is already in the cache
        if id in AdminProxy._cache:
            return AdminProxy._cache[id]
        # Fetch the admin from the database if not in cache
        admin = Admin.get_by_id(conn, id)
        if admin:
            AdminProxy._cache[id] = admin  # Add the admin to the cache
        return admin

    @staticmethod
    def save(admin: Admin, conn):
        # Save the admin to the database
        admin.save(conn)
        if admin.id:
            AdminProxy._cache[admin.id] = admin  # Update the cache with the saved admin

    @staticmethod
    def delete(admin: Admin, conn):
        # Delete the admin from the database
        admin.delete(conn)
        if admin.id in AdminProxy._cache:
            del AdminProxy._cache[admin.id]  # Remove the admin from the cache


class TerritoryProxy:
    _cache = {}  # Cache to store Territory objects for quick access

    @staticmethod
    def get_by_id(conn, id: int):
        # Check if the territory is already in the cache
        if id in TerritoryProxy._cache:
            return TerritoryProxy._cache[id]
        # Fetch the territory from the database if not in cache
        territory = Territory.get_by_id(conn, id)
        if territory:
            TerritoryProxy._cache[id] = territory  # Add the territory to the cache
        return territory

    @staticmethod
    def save(territory: Territory, conn):
        # Save the territory to the database
        territory.save(conn)
        if territory.id:
            TerritoryProxy._cache[territory.id] = territory  # Update the cache with the saved territory

    @staticmethod
    def delete(territory: Territory, conn):
        # Delete the territory from the database
        territory.delete(conn)
        if territory.id in TerritoryProxy._cache:
            del TerritoryProxy._cache[territory.id]  # Remove the territory from the cache