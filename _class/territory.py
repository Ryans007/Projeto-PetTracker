from bearlibterminal import terminal
import random
import time
import textwrap

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

    def show_territory(self, stop_event):
        # Dimensões do território e da área de mensagem
        territory_width = self.x
        territory_height = self.y  # área onde o território é desenhado
        message_area_lines = 3  # número de linhas reservadas para mensagem
        window_height = territory_height + message_area_lines

        # Configura a janela do BearLibTerminal
        terminal.open()
        terminal.set(f"window: size={territory_width}x{window_height}, cellsize=auto, title='Território'")

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


