import curses
import time
import random

class Territory():
    def __init__(self, name: str, x: int, y: int, owner = str | None, id: int | None = None) -> None:
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.owner = owner
        self.animals = []

    def add_animal(self, animal) -> None:
        self.animals.append(animal)

    def show_territory(self, height: int, width: int):
        def func_to_show(stdscr):
            curses.curs_set(0)
            stdscr.nodelay(1)
            stdscr.timeout(100)
            
            territory_height = height
            territory_width = width
            status_line = territory_height + 1  # Linha para mensagens
            
            # Inicializa posições dos animais
            for animal in self.animals:
                animal.x = random.randint(1, territory_width - 2)
                animal.y = random.randint(1, territory_height - 2)
            
            while True:
                stdscr.clear()
                escaped_animals = []  # Lista de animais que escaparam
                
                # Desenha bordas do território
                for i in range(territory_height):
                    for j in range(territory_width):
                        if i == 0 or i == territory_height - 1 or j == 0 or j == territory_width - 1:
                            stdscr.addch(i, j, '#')
                
                # Desenha animais e verifica se escaparam
                for animal in self.animals:
                    # Verifica se está dentro do território
                    inside = (1 <= animal.x < territory_width-1) and (1 <= animal.y < territory_height-1)
                    
                    if inside:
                        stdscr.addstr(animal.y, animal.x, animal.name[0])
                    else:
                        escaped_animals.append(animal)
                
                # Exibe mensagem de animais que escaparam
                if escaped_animals:
                    message = "Animais fora do território: "
                    message += ", ".join([f"{animal.name} ({animal.specie})" for animal in escaped_animals])
                    stdscr.addstr(status_line, 0, message.ljust(territory_width))
                else:
                    stdscr.addstr(status_line, 0, " " * territory_width)  # Limpa linha de status
                
                # Movimenta cada animal individualmente
                for animal in self.animals:
                    direction = random.choice(['up', 'down', 'left', 'right'])
                    
                    if direction == 'up': animal.y -= 1
                    elif direction == 'down': animal.y += 1
                    elif direction == 'left': animal.x -= 1
                    elif direction == 'right': animal.x += 1
                
                stdscr.refresh()
                time.sleep(0.2)
                
                key = stdscr.getch()
                if key == ord('q'):
                    break

        curses.wrapper(func_to_show)

    def save(self, conn):
        cursor = conn.cursor()
        try:
            if self.id is None:
                cursor.execute('''
                            INSERT INTO territories (name, x, y)
                            VALUES (?, ?, ?)
                            ''', (self.name, self.x, self.y))
                self.id = cursor.lastrowid
            else:
                cursor.execute('''
                            UPDATE territories
                            SET name = ?, x = ?, y ?
                            WHERE id = ?
                            ''', (self.name, self.x, self.y, self.id))
            conn.commit()
        finally:
            cursor.close()
    @staticmethod
    def get_by_id(conn, id: int):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM territories WHERE id = ?', (id,))
        row = cursor.fetchone()
        if row:
            return Territory(id=row[0], name=row[1], x=row[2], y=row[3])
        raise Exception("Nenhum territorio corresponde ao id")
        
    def delete(self, conn):
        if self.id is not None:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM territories WHERE id = ?', (self.id,))
            conn.commit()
            self.id = None
            
    def __repr__(self):
        return f"Territory(id={self.id}, name={self.name}, x={self.x}, y={self.y})"


