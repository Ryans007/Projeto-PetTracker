import time
import random
import threading

class Rastreador:
    def __init__(self):
        self.location = Localizacao()

    def location_generate(self) -> None:
        while True:
            time.sleep(2)  # Espera 2 segundos
            coordenadas = self.location.generate_coordenate()
            print(f"Coordenadas geradas: {coordenadas}")

class Localizacao:
    def generate_coordenate(self) -> tuple:
        x = random.randint(0, 500)
        y = random.randint(0, 500)
        return (x, y)

# Cria uma instância do rastreador
rastreador = Rastreador()

# Inicia a thread para gerar localizações
thread = threading.Thread(target=rastreador.location_generate, daemon=True)
thread.start()

# O restante do programa continua executando normalmente
print("Programa principal rodando...")
for i in range(10):
    print(f"Executando outra tarefa {i}")
    time.sleep(1)