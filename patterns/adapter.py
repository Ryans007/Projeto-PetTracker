import math

class CoordinateAdapter:
    """
    Converte duas coordenadas geográficas (lat1, lon1) e (lat2, lon2)
    em componentes cartesianas (x, y) em metros.
    
    x -> Componente Leste (em metros)
    y -> Componente Norte (em metros)
    """
    def __init__(self, lat1, lon1, lat2, lon2):
        self.lat1 = lat1
        self.lon1 = lon1
        self.lat2 = lat2
        self.lon2 = lon2
        self.x, self.y = self._calculate_components()

    def _calculate_components(self):
        # Converter graus para radianos
        lat1_rad = math.radians(self.lat1)
        lat2_rad = math.radians(self.lat2)
        lon1_rad = math.radians(self.lon1)
        lon2_rad = math.radians(self.lon2)
        
        # Diferenças entre as coordenadas
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        # Cálculo da distância total utilizando a fórmula de Haversine
        R = 6371000  # Raio médio da Terra em metros
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c  # Distância total em metros
        
        # Cálculo do azimute (sentido a partir do norte, horário)
        y_az = math.sin(dlon) * math.cos(lat2_rad)
        x_az = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon)
        azimuth = (math.degrees(math.atan2(y_az, x_az)) + 360) % 360

        # Decompor a distância nos componentes Leste (x) e Norte (y)
        x = distance * math.sin(math.radians(azimuth))
        y = distance * math.cos(math.radians(azimuth))
        
        x = int(abs(x/1.5))
        y = int(abs(x/1.5))
        
        return x, y

    def get_coordinates(self):
        """
        Retorna os componentes x (leste) e y (norte) calculados.
        """
        return self.x, self.y

