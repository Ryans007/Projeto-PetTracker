import random
import time
import threading
from _class.location import Location

class Tracker():
    def __init__(self, state: bool, x_limit: int, y_limit: int, id: int | None = None) -> None:
        if id is None:
            self.id = random.randint(0, 500)
        else:
            self.id = id
        self.state = state
        self.last_update = None
        self.x = random.randint(1, x_limit - 2)  # Posição inicial aleatória
        self.y = random.randint(1, y_limit - 2)
        self.current_location = Location(self.x, self.y)  # Armazena a localização atual
        self._running = False  # Flag para controlar a execução da thread

    def location_generate(self) -> Location:
        direction = random.choice(['up', 'down', 'left', 'right'])
        if direction == 'up':
            self.y -= 1
        elif direction == 'down':
            self.y += 1
        elif direction == 'left':
            self.x -= 1
        elif direction == 'right':
            self.x += 1

        return Location(self.x, self.y)

    def _location_loop(self):
        """Loop que gera localizações continuamente em background."""
        while self._running:
            # Gera uma nova localização e atualiza o atributo current_location
            self.current_location = self.location_generate()
            # Aqui você pode atualizar last_update ou notificar outra parte do sistema
            self.last_update = time.time()
            # Intervalo entre atualizações (ajuste conforme necessário)
            time.sleep(0.2)

    def start_location_generation(self):
        """Inicia a thread que gera localizações continuamente."""
        self._running = True
        self._thread = threading.Thread(target=self._location_loop, daemon=True)
        self._thread.start()

    def stop_location_generation(self):
        """Para a geração contínua de localizações."""
        self._running = False
        if hasattr(self, '_thread'):
            self._thread.join()
