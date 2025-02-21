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
        # Dimensões do território e da área de mensagem
        territory_width = self.x
        territory_height = self.y  # área onde o território é desenhado
        message_area_lines = 3  # número de linhas reservadas para mensagem
        window_height = territory_height + message_area_lines
        print(self.name, self.x, self.y, self.owner_id, self.id)

        # Configura a janela do BearLibTerminal
        terminal.open()
        terminal.set(f"window: size={territory_width}x{window_height}, cellsize=auto, title='{self.name}'")

        try:
            while not stop_event.is_set():
                terminal.clear()

                # Desenha as bordas do território
                for x in range(territory_width):
                    terminal.put(x, 0, '#')
                    terminal.put(x, territory_height - 1, '#')
                for y in range(territory_height):
                    terminal.put(0, y, '#')
                    terminal.put(territory_width - 1, y, '#')

                # Desenha os animais que estão dentro do território
                for animal in self.animals:
                    if 1 <= animal.x < territory_width - 1 and 1 <= animal.y < territory_height - 1:
                        terminal.put(animal.x, animal.y, animal.name[0])

                # Computa dinamicamente quais animais estão fora e dentro do território
                escaped_animals = [
                    animal for animal in self.animals
                    if not (1 <= animal.x < territory_width - 1 and 1 <= animal.y < territory_height - 1)
                ]

                inside_animals = [
                    animal for animal in self.animals
                    if 1 <= animal.x < territory_width - 1 and 1 <= animal.y < territory_height - 1
                ]

                # Constrói as mensagens
                message_escaped = "Animais fora do território: " + ", ".join(a.name for a in escaped_animals) if escaped_animals else "Nenhum animal fora do território."
                message_inside = "Animais dentro do território: " + ", ".join(a.name for a in inside_animals) if inside_animals else "Nenhum animal dentro do território."

                # Quebra as mensagens em linhas de tamanho máximo igual à largura do território
                wrapped_escaped = textwrap.wrap(message_escaped, territory_width)
                wrapped_inside = textwrap.wrap(message_inside, territory_width)

                # Combina as mensagens, limitando ao número de linhas disponíveis
                combined_lines = wrapped_escaped + wrapped_inside
                combined_lines = combined_lines[:message_area_lines]

                # Imprime as linhas de mensagem abaixo do território
                for i in range(message_area_lines):
                    line_text = combined_lines[i] if i < len(combined_lines) else ""
                    terminal.printf(0, territory_height + i, line_text.ljust(territory_width))

                terminal.refresh()

                # Movimenta os animais aleatoriamente
                for animal in self.animals:
                    direction = random.choice(['up', 'down', 'left', 'right'])
                    if direction == 'up':
                        animal.y -= 1
                    elif direction == 'down':
                        animal.y += 1
                    elif direction == 'left':
                        animal.x -= 1
                    elif direction == 'right':
                        animal.x += 1

                # Verifica se o usuário pressionou uma tecla para sair
                if terminal.has_input():
                    key = terminal.read()
                    if key == terminal.TK_Q:  # BearLibTerminal usa TK_Q para a tecla 'q'
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


