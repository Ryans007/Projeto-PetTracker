from _class.territory import Territory

class TerritoryBuilder:

    """
    A builder class responsible for creating and configuring Territory objects.
    """

    def __init__(self):
        """
        Initializes the builder with default values for a Territory instance.
        """
        self.territory = Territory(name="", x=0, y=0, owner_id=None)
    
    def set_name(self, name: str):
        """
        Assigns a name to the Territory.

        :param name: The new name for the Territory.
        :return: Self, to allow method chaining.
        """
        self.territory.name = name
        return self
    
    def set_dimensions(self, x: int, y: int):
        """
        Specifies the x and y coordinates of the Territory.

        :param x: The x-coordinate to be set.
        :param y: The y-coordinate to be set.
        :return: Self, to allow method chaining.
        """
        self.territory.x = x
        self.territory.y = y
        return self
    
    def set_owner(self, owner_id: int ) -> 'TerritoryBuilder':
        """
        Sets the owner_id of the Territory.

        :param owner_id: The unique identifier of the owner.
        :return: Self, to allow method chaining.
        """
        self.territory.owner_id = owner_id 
        return self
    
    def build(self):
        """
        Finalizes and returns a configured Territory instance.

        :return: A fully built Territory object.
        """
        return self.territory