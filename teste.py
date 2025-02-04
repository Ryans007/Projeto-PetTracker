from ast import Raise
from email.policy import default
import time
from typing import final

if __name__ == "__main__": 
  # print(104*"*")  
  # for _ in range(20):
  #   print("*", 100*" ", "*")
  # print(104*"*")
  
  
  import curses
  import time
  import random

  def main(stdscr):
    try:
      # Configurações iniciais
      curses.curs_set(0)  # Esconde o cursor
      stdscr.nodelay(1)   # Não bloqueia a entrada
      stdscr.timeout(100) # Tempo de espera para a entrada do usuário

      # Defina o tamanho do território manualmente
      territorio_altura = 10
      territorio_largura = 10

      # Posição inicial do caractere '*' no centro do território
      x, y = territorio_largura // 2, territorio_altura // 2

      # Loop principal
      while True:
          stdscr.clear()

          # Desenha as bordas do território
          for i in range(territorio_altura):
              for j in range(territorio_largura):
                  if i == 0 or i == territorio_altura - 1 or j == 0 or j == territorio_largura - 1:
                      stdscr.addch(i, j, '#')  # Desenha as bordas
                  elif i == y and j == x:
                      stdscr.addch(i, j, '*')  # Desenha o bichinho
          
          dentro_do_territorio = (0 <= x < territorio_largura and 0 <= y < territorio_altura)
          
          if not dentro_do_territorio:
            stdscr.addstr(territorio_altura + 1, 0, "O cachorro saiu do territorio!!!")
          else:
            # Limpa a mensagem se o bichinho voltar ao território
            stdscr.addstr(territorio_altura + 1, 0, " " * 30)
            
          # Resto do código (movimentação, etc.)
          stdscr.refresh()

          # Movimentação aleatória
          direction = random.choice(['up', 'down', 'left', 'right'])
          if direction == 'up':                             
              y -= 1
          elif direction == 'down':
              y += 1
          elif direction == 'left':
              x -= 1
          elif direction == 'right':
              x += 1
          
          """
              Linha 0: ####################  <- Parede de cima
            Linha 1: #                  #
            Linha 2: #        *         #  <- Bichinho aqui (y = 2)
            Linha 3: #                  #
            Linha 4: #                  #
            Linha 5: #                  #
            Linha 6: #                  #
            Linha 7: #                  #
            Linha 8: #                  #
            Linha 9: ####################  <- Parede de baixo
          
          """
          

          # Espera um pouco antes de mover novamente
          time.sleep(0.2)

          # Verifica se o usuário pressionou uma tecla para sair
          key = stdscr.getch()
          if key == ord('q'):
              break
    except Exception:
      print("Tamanho do territorio maior que o terminal")
      
  # Inicia o programa
  curses.wrapper(main)
  
