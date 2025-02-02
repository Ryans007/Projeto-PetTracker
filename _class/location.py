class Location():
  def __init__(self) -> None:
    self.coordinated = None
    
  def update_coordinated(self, coordinated): 
    self.coordinated = coordinated
    self._location_register()
  
  def _location_register(self): pass
    # Implementar envio da localização ao Banco de Dados
  def location_history(self): pass
    # Implementar o recebimento do histórico de localização do Banco de Dados
