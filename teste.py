import math

def decompose_distance(lat1, lon1, lat2, lon2):
    """
    Recebe as coordenadas de dois pontos (em graus) e retorna:
      - Componente Leste (X) em metros
      - Componente Norte (Y) em metros
      - Distância total em metros
      - Azimute em graus (0° = norte, medido no sentido horário)
    """
    # 1. Converter graus para radianos
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    lon1_rad = math.radians(lon1)
    lon2_rad = math.radians(lon2)
    
    # 2. Diferenças
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # 3. Cálculo da distância usando a fórmula de Haversine
    R = 6371000  # Raio médio da Terra em metros
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c  # Distância total em metros
    
    # 4. Cálculo do azimute
    y = math.sin(dlon) * math.cos(lat2_rad)
    x = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon)
    initial_bearing = math.atan2(y, x)  # Em radianos
    # Converter para graus e normalizar para 0-360°
    bearing_deg = (math.degrees(initial_bearing) + 360) % 360
    
    # 5. Decompor a distância nos componentes
    # Note que o azimute é medido a partir do norte (sentido horário)
    d_north = distance * math.cos(math.radians(bearing_deg))
    d_east = distance * math.sin(math.radians(bearing_deg))
    
    return d_east, d_north, distance, bearing_deg

# Valores dos pontos
lat1 = -7.239255211457728
lon1 = -35.91703180629805
lat2 = -7.2404513060438465
lon2 = -35.91487237802759

# Executando a função
x, y, total_distance, bearing = decompose_distance(lat1, lon1, lat2, lon2)
print(f"Componente Leste (X): {x:.1f} m")
print(f"Componente Norte (Y): {y:.1f} m")
print(f"Distância total: {total_distance:.1f} m")
print(f"Azimute: {bearing:.1f}°")
