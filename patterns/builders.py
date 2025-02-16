from _class.territory import Territory

class TerritoryBuilder:
    def __init__(self):
        self.territory = Territory(name="", x=0, y=0,)
    
    def set_name(self, name: str):
        self.territory.name = name
        return self
    
    def set_dimensions(self, x: int, y: int):
        self.territory.x = x
        self.territory.y = y
        return self
    
    def set_owner(self, owner: str | None = None) -> 'TerritoryBuilder':
        self.territory.owner = owner # type: ignore
        return self
    
    def build(self):
        return self.territory