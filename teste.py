import curses
import random
import time

def show_territory(largura: int, altura: int):
    def func_to_show(stdscr):
        try:
            # Configurações iniciais
            curses.curs_set(0)  # Esconde o cursor
            stdscr.nodelay(1)   # Não bloqueia a entrada
            stdscr.timeout(100) # Tempo de espera para entrada do usuário

            # Verifica se o terminal suporta o tamanho desejado
            max_altura, max_largura = stdscr.getmaxyx()
            if altura + 2 > max_altura or largura + 2 > max_largura:
                raise ValueError("Tamanho do território maior que o terminal.")

            # Posição inicial do bichinho no centro do território
            x, y = largura // 2, altura // 2

            # Loop principal
            while True:
                stdscr.clear()

                # Desenha as bordas do território
                for i in range(altura + 2):
                    for j in range(largura + 2):
                        if i == 0 or i == altura + 1 or j == 0 or j == largura + 1:
                            stdscr.addch(i, j, '#')  # Desenha as bordas
                        elif i == y and j == x:
                            stdscr.addch(i, j, "*")  # Desenha o bichinho

                # Se o bichinho sair do território
                if not (1 <= x <= largura and 1 <= y <= altura):
                    stdscr.addstr(altura + 3, 0, "O cachorro saiu do território!!!")
                else:
                    stdscr.addstr(altura + 3, 0, " " * 40)  # Apaga a mensagem caso o bichinho volte

                stdscr.refresh()

                # Movimentação aleatória dentro do território
                direction = random.choice(['up', 'down', 'left', 'right'])
                if direction == 'up' and y > 1:
                    y -= 1
                elif direction == 'down' and y < altura:
                    y += 1
                elif direction == 'left' and x > 1:
                    x -= 1
                elif direction == 'right' and x < largura:
                    x += 1

                # Aguarda um tempo antes da próxima movimentação
                time.sleep(0.2)

                # Verifica se o usuário pressionou 'q' para sair
                key = stdscr.getch()
                if key == ord('q'):
                    break
        except Exception as e:
            print(f"Erro: {e}")

    # Inicia o programa com o wrapper do curses
    curses.wrapper(func_to_show)

if __name__ == "__main__": 
    show_territory(30, 30)
