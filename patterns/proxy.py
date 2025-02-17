from _class.person import Admin, User
from _class.territory import Territory

class UserProxy:
    _cache = {}
      
    @staticmethod
    def get_by_id(conn, id: int):
      if id in UserProxy._cache:
        return UserProxy._cache[id]
      user = User.get_by_id(conn, id)
      if user:
        UserProxy._cache[id] = user
      return user
    
    @staticmethod
    def delete(user: User, conn):
        user.delete(conn)
        if user.id in UserProxy._cache:
            del UserProxy._cache[user.id]
      

class AdminProxy:
    _cache = {}

    @staticmethod
    def get_by_id(conn, id: int):
        if id in AdminProxy._cache:
            return AdminProxy._cache[id]
        admin = Admin.get_by_id(conn, id)
        if admin:
            AdminProxy._cache[id] = admin
        return admin

    @staticmethod
    def save(admin: Admin, conn):
        admin.save(conn)
        if admin.id:
            AdminProxy._cache[admin.id] = admin

    @staticmethod
    def delete(admin: Admin, conn):
        admin.delete(conn)
        if admin.id in AdminProxy._cache:
            del AdminProxy._cache[admin.id]

class TerritoryProxy:
    _cache = {}

    @staticmethod
    def get_by_id(conn, id: int):
        if id in TerritoryProxy._cache:
            return TerritoryProxy._cache[id]
        territory = Territory.get_by_id(conn, id)
        if territory:
            TerritoryProxy._cache[id] = territory
        return territory

    @staticmethod
    def save(territory: Territory, conn):
        territory.save(conn)
        if territory.id:
            TerritoryProxy._cache[territory.id] = territory

    @staticmethod
    def delete(territory: Territory, conn):
        territory.delete(conn)
        if territory.id in TerritoryProxy._cache:
            del TerritoryProxy._cache[territory.id]


