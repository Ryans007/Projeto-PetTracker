import curses
import time
import random

class Territory():
  def __init__(self, name: str, x: int, y: int, owner = None) -> None:
    self.name = name
    self.x = x
    self.y = y
    self.owner = owner
    self.animals = []
    
  def add_owner(self, owner) -> None:
    self.owner = owner
    
  def add_animal(self, animal) -> None:
    self.animals.append(animal)

  @staticmethod
  def show_territory(height: int, width: int):
    def func_to_show(stdscr):
        try:
            curses.curs_set(0)
            stdscr.nodelay(1)
            stdscr.timeout(100)
            
            territory_height = height
            territory_width = width
            
            x, y = territory_width // 2, territory_height // 2
            
            while True:
                stdscr.clear()
                
                for i in range(territory_height):
                    for j in range(territory_width):
                        if i == 0 or i == territory_height - 1 or j == 0 or j == territory_width - 1:
                            stdscr.addch(i, j, '#')
                        elif i == y and j == x:
                            stdscr.addch(i, j, "*")
                
                inside_territory = (0 <= x < territory_width and 0 <= y < territory_height)
                
                if not inside_territory:
                    stdscr.addstr(territory_height + 1, 0, "O cachorro saiu do territorio!!!")
                else:
                    stdscr.addstr(territory_height + 1, 0, " " * 30)
                
                stdscr.refresh()
                
                direction = random.choice(['up', 'down', 'left', 'right'])
                if direction == 'up':
                    y -= 1
                elif direction == 'down':
                    y += 1
                elif direction == 'left':
                    x -= 1
                elif direction == 'right':
                    x += 1
                
                time.sleep(0.2)
                
                key = stdscr.getch()
                if key == ord('q'):
                    break
        except Exception:
            print("Tamanho do territorio maior que o terminal")
    
    curses.wrapper(func_to_show)
    
  


