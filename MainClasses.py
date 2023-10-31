
#объекты
class Planet:
    """класс планет"""

    def __init__(self, id, name, g, atmosphere, secondspacespeed, color, parent, alt):
        self.g = g
        self.atmosphere = atmosphere
        self.name = name
        self.secondspacespeed = secondspacespeed
        self.color = color
        self.parent = parent
        self.alt = alt
        self.id = id

    def returnname(self):
        return self.name

class ObjectOfRocket:
    """класс отвечает за все объекты"""
    pass


class RocketEngine(ObjectOfRocket):
    """класс отвечает за все объекты типа двигатели"""

    def __init__(self, id, name, traction, pulse, mass):
        self.name = name
        self.traction = traction
        self.pulse = pulse
        self.mass = mass


class Tank(ObjectOfRocket):
    """Топлевные баки"""

    def __init__(self, id, name, mass):
        self.name = name
        self.mass = mass

# исключения
class ExceptionGroupKSP(Exception):
    def __init__(self, message='Необработанная ошибка'):
        self.message = message

    def __str__(self):
        return f'{self.message}'


class ErrorParts(ExceptionGroupKSP):
    pass


class ErrorPlanets(ExceptionGroupKSP):
    pass


class NegativeValue(ErrorPlanets):
    pass
