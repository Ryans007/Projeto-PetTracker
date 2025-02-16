from bearlibterminal import terminal
import random
import time
import textwrap

class Animal:
    def __init__(self, x, y, name, specie):
        self.x = x
        self.y = y
        self.name = name
        self.specie = specie

def main():
    # Dimensões do território e da área de mensagem
    territory_width = 40
    territory_height = 20        # área onde o território é desenhado
    message_area_lines = 3       # número de linhas reservadas para mensagem
    window_height = territory_height + message_area_lines

    # Configura a janela do BearLibTerminal
    terminal.open()
    terminal.set(f"window: size={territory_width}x{window_height}, cellsize=auto, title='Território'")

    # Cria alguns animais com posições iniciais dentro do território
    animals = [
        Animal(random.randint(1, territory_width-2), random.randint(1, territory_height-2), "Leão", "Panthera leo"),
        Animal(random.randint(1, territory_width-2), random.randint(1, territory_height-2), "Tigre", "Panthera tigris"),
        Animal(random.randint(1, territory_width-2), random.randint(1, territory_height-2), "Urso", "Ursus arctos"),
        Animal(random.randint(1, territory_width-2), random.randint(1, territory_height-2), "Elefante", "Loxodonta"),
        Animal(random.randint(1, territory_width-2), random.randint(1, territory_height-2), "Girafa", "Giraffa")
    ]

    try:
        while True:
            terminal.clear()

            # Desenha as bordas do território
            for x in range(territory_width):
                terminal.put(x, 0, '#')
                terminal.put(x, territory_height-1, '#')
            for y in range(territory_height):
                terminal.put(0, y, '#')
                terminal.put(territory_width-1, y, '#')

            # Desenha os animais que estão dentro do território
            for animal in animals:
                if 1 <= animal.x < territory_width-1 and 1 <= animal.y < territory_height-1:
                    terminal.put(animal.x, animal.y, animal.name[0])

            # Computa dinamicamente quais animais estão fora do território
            escaped_animals = [
                animal for animal in animals 
                if not (1 <= animal.x < territory_width-1 and 1 <= animal.y < territory_height-1)
            ]

            # Constrói a mensagem de animais fora do território
            if escaped_animals:
                message = "Animais fora do território: " + ", ".join(a.name for a in escaped_animals)
            else:
                message = "Nenhum animal fora do território."

            # Quebra a mensagem em linhas de tamanho máximo igual à largura do território
            wrapped_lines = textwrap.wrap(message, territory_width)
            # Exibe somente as primeiras linhas, conforme o espaço reservado
            wrapped_lines = wrapped_lines[:message_area_lines]

            # Imprime as linhas de mensagem abaixo do território
            for i in range(message_area_lines):
                line_text = wrapped_lines[i] if i < len(wrapped_lines) else ""
                terminal.printf(0, territory_height + i, line_text.ljust(territory_width))

            terminal.refresh()

            # Movimenta os animais aleatoriamente
            for animal in animals:
                direction = random.choice(['up', 'down', 'left', 'right'])
                if direction == 'up':
                    animal.y -= 1
                elif direction == 'down':
                    animal.y += 1
                elif direction == 'left':
                    animal.x -= 1
                elif direction == 'right':
                    animal.x += 1

            time.sleep(0.2)
    except KeyboardInterrupt:
        pass
    finally:
        terminal.close()

if __name__ == "__main__":
    main()
