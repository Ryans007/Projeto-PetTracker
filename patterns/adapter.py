import math

class CoordinateAdapter:
    """
    Converts two geographic coordinates (lat1, lon1) and (lat2, lon2)
    into Cartesian components (x, y) in meters.
    
    x -> East component (in meters)
    y -> North component (in meters)
    """
    def __init__(self, lat1, lon1, lat2, lon2):
        # Initialize the latitude and longitude for two points
        self.lat1 = lat1
        self.lon1 = lon1
        self.lat2 = lat2
        self.lon2 = lon2
        # Calculate the x and y components
        self.x, self.y = self._calculate_components()

    def _calculate_components(self):
        # Convert degrees to radians
        lat1_rad = math.radians(self.lat1)
        lat2_rad = math.radians(self.lat2)
        lon1_rad = math.radians(self.lon1)
        lon2_rad = math.radians(self.lon2)
        
        # Differences between the coordinates
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        # Calculate the total distance using the Haversine formula
        R = 6371000  # Earth's average radius in meters
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c  # Total distance in meters
        
        # Calculate the azimuth (direction from the north, clockwise)
        y_az = math.sin(dlon) * math.cos(lat2_rad)
        x_az = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon)
        azimuth = (math.degrees(math.atan2(y_az, x_az)) + 360) % 360

        # Decompose the distance into East (x) and North (y) components
        x = distance * math.sin(math.radians(azimuth))
        y = distance * math.cos(math.radians(azimuth))
        
        # Convert values to positive integers and reduce by a factor of 1.5
        x = int(abs(x / 1.5))
        y = int(abs(x / 1.5))
        
        return x, y

    def get_coordinates(self):
        """
        Returns the calculated x (east) and y (north) components.
        """
        return self.x, self.y
