import random
import time
import threading
from _class.location import Location

class Tracker():
    def __init__(self, state: bool, x_limit: int, y_limit: int, id: int | None = None) -> None:
        self.id = id
        self.state = state
        self.last_update = None
        self.x = random.randint(1, x_limit - 2)  # Posição inicial aleatória
        self.y = random.randint(1, y_limit - 2)
        self.current_location = Location(self.x, self.y)  # Armazena a localização atual
        self._running = False  # Flag para controle da thread de atualização
        self._saving_running = False  # Flag para controle da thread de salvamento
        self.conn = None  # Conexão com o banco de dados (será setada posteriormente)
        self.animal_name = None  # Nome do animal associado (para salvar na tabela)

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
            self.current_location = self.location_generate()
            self.last_update = time.time()
            time.sleep(0.2)  # intervalo entre atualizações (ajuste conforme necessário)

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

    def start_location_saving(self, conn, animal_name: str):
        """
        Inicia uma thread que salva a localização atual no banco de dados a cada 60 segundos.
        Recebe a conexão com o banco e o nome do animal para registrar na tabela.
        """
        self.conn = conn
        self.animal_name = animal_name
        self._saving_running = True
        self._saving_thread = threading.Thread(target=self._location_saving_loop, daemon=True)
        self._saving_thread.start()

    def _location_saving_loop(self):
        """Loop que salva a localização a cada 60 segundos."""
        while self._saving_running:
            self.last_update = time.time()
            self.location_save()
            time.sleep(60)

    def stop_location_saving(self):
        """Para a thread de salvamento de localização."""
        self._saving_running = False
        if hasattr(self, '_saving_thread'):
            self._saving_thread.join()

    def location_save(self):
        """Salva a localização atual no banco de dados."""
        if self.conn is None:
            return  # Não há conexão definida
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                '''INSERT INTO location (animal_name, x, y, time, tracker_id)
                   VALUES (?, ?, ?, ?, ?)''',
                (self.animal_name, self.current_location.x, self.current_location.y, self.last_update, self.id)
            )
            self.conn.commit()
        except Exception as e:
            print("Erro ao salvar localização:", e)
        finally:
            cursor.close()
