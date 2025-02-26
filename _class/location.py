from _class.territory import Territory

class Location():
   def __init__(self, x: int, y: int) -> None:
         self.__x = x
         self.__y = y
   
   @property      
   def x(self) -> int:
      return self.__x
      
   @x.setter
   def x(self, x: int):
      self.__x = x
      
   @property      
   def y(self) -> int:
      return self.__y
      
   @y.setter
   def y(self, y: int):
      self.__y = y
      
   def __repr__(self) -> str:
      return f"{type(self).__name__}({self.x!r}, {self.y!r})"