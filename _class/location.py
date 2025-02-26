from _class.territory import Territory

class Location():
   def __init__(self, x: int, y: int) -> None:
         self.__x = x
         self.__y = y
   
   @property      
   def x(self) -> int:
      """Returns the x-coordinate of the location."""
      return self.__x
      
   @x.setter
   def x(self, x: int):
      """Sets the x-coordinate of the location."""
      self.__x = x
      
   @property      
   def y(self) -> int:
      """Returns the y-coordinate of the location."""
      return self.__y
      
   @y.setter
   def y(self, y: int):
      """Sets the y-coordinate of the location."""
      self.__y = y
      
   def __repr__(self) -> str:
      """Returns a string representation of the Location object."""
      return f"{type(self).__name__}({self.x!r}, {self.y!r})"
