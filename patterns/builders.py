from _class.territory import Territory

class TerritoryBuilder:
    def __init__(self):
        self.territory = Territory(name="", x=0, y=0, owner_id=None)
    
    def set_name(self, name: str):
        self.territory.name = name
        return self
    
    def set_dimensions(self, x: int, y: int):
        self.territory.x = x
        self.territory.y = y
        return self
    
    def set_owner(self, owner_id: int ) -> 'TerritoryBuilder':
        self.territory.owner_id = owner_id 
        return self
    
    def build(self):
        return self.territory