class Weather:
    def __init__(self, city, weather, description, minima, maxima, id=None):
        self.city = city
        self.weather = weather
        self.description = description
        self.minima = minima
        self.maxima = maxima
        self.id = id
