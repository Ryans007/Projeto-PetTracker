from bearlibterminal import terminal
import random
import time
import textwrap

class Territory():
    def __init__(self, name: str, x: int, y: int, owner_id: int| None = None, id: int | None = None) -> None:
        self.__id = id
        self.__name = name
        self.__x = int(238/4)
        self.__y = int(133/4)
        self.__owner_id = owner_id
        self.animals = []
    
    @property
    def id(self) -> int | None:
        return self.__id
    
    @id.setter
    def id(self, id: int) -> None:
        self.__id = id
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str) -> None:
        self.__name = name
    
    @property
    def x(self) -> int:
        return self.__x 
    
    @x.setter
    def x(self, x: int) -> None:
        self.__x = x
        
    @property
    def y(self) -> int:
        return self.__y 
    
    @y.setter
    def y(self, y: int) -> None:
        self.__y = y

    @property
    def owner_id(self) -> int | None:
        return self.__owner_id 
    
    @owner_id.setter
    def owner_id(self, owner_id: int) -> None:
        self.__owner_id = owner_id

    def add_animal(self, animal) -> None:
        self.animals.append(animal)

    def show_territory(self, stop_event):
        territory_width = self.x
        territory_height = self.y
        message_area_lines = 3
        window_height = territory_height + message_area_lines

        # Ajuste o tamanho da janela para algo que caiba no seu monitor.
        # Se precisar, coloque valores fixos, ex: "window: size=100x35"
        terminal.open()
        terminal.set(f"window: size={territory_width}x{window_height}, cellsize=auto, title='{self.name}'")

        try:
            while not stop_event.is_set():
                terminal.clear()

                # 1) Atualiza posição dos animais
                for animal in self.animals:
                    animal.update_position()

                # 2) Desenha bordas
                for x in range(territory_width):
                    terminal.put(x, 0, '#')
                    terminal.put(x, territory_height - 1, '#')
                for y in range(territory_height):
                    terminal.put(0, y, '#')
                    terminal.put(territory_width - 1, y, '#')

                # 3) Desenha animais
                for animal in self.animals:
                    # Se estiver dentro do território
                    if 1 <= animal.x < territory_width - 1 and 1 <= animal.y < territory_height - 1:
                        terminal.put(animal.x, animal.y, animal.name[0])

                # 4) Verifica quem está dentro e fora
                escaped_animals = [
                    a for a in self.animals
                    if not (1 <= a.x < territory_width - 1 and 1 <= a.y < territory_height - 1)
                ]
                inside_animals = [
                    a for a in self.animals
                    if 1 <= a.x < territory_width - 1 and 1 <= a.y < territory_height - 1
                ]

                # 5) Monta as strings de status
                escaped_text = "Fora: " + (", ".join(a.name for a in escaped_animals) if escaped_animals else "Nenhum")
                inside_text = "Dentro: " + (", ".join(a.name for a in inside_animals) if inside_animals else "Nenhum")

                # 6) Exibe as mensagens abaixo do território
                terminal.printf(0, territory_height,     escaped_text)
                terminal.printf(0, territory_height + 1, inside_text)

                terminal.refresh()

                # 7) Verifica se o usuário pressionou 'Q' para sair
                if terminal.has_input():
                    key = terminal.read()
                    if key == terminal.TK_Q:
                        break

                time.sleep(0.2)

        except KeyboardInterrupt:
            pass
        finally:
            terminal.close()
        
    def save(self, conn):
        cursor = conn.cursor()
        try:
            if self.id is None:
                cursor.execute('''
                            INSERT INTO territories (name, x, y, owner_id)
                            VALUES (?, ?, ?, ?)
                            ''', (self.name, self.x, self.y, self.owner_id))
                self.id = cursor.lastrowid
            else:
                cursor.execute('''
                            UPDATE territories
                            SET id = ?, name = ?, x = ?, y = ?, owner_id = ?
                            WHERE id = ?
                            ''', (self.id, self.name, self.x, self.y, self.owner_id, self.id))
            conn.commit()
        finally:
            cursor.close()
            
    @staticmethod
    def get_by_id(conn, id: int):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM territories WHERE id = ?', (id,))
        row = cursor.fetchone()
        if row:
            return Territory(id=row[0], name=row[1], x=row[2], y=row[3], owner_id=row[4])
        raise Exception("Nenhum territorio corresponde ao id")
        
    def delete(self, conn):
        if self.id is not None:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM territories WHERE id = ?', (self.id,))
            conn.commit()
            self.id = 0
            
    def __repr__(self):
        return f"Territory(id={self.id}, name={self.name}, x={self.x}, y={self.y}, owner_id={self.owner_id})"


