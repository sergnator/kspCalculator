# объекты
class Planet:
    def __init__(self, id, name, g, atmosphere, second_space_speed, color, parent, alt):
        self.g = g
        self.atmosphere = atmosphere
        self.name = name
        self.second_space_speed = second_space_speed
        self.color = color
        self.parent = parent
        self.alt = alt
        self.id = id

    def returnname(self):
        return self.name


class ObjectOfRocket:
    pass


class RocketEngine(ObjectOfRocket):
    def __init__(self, id, name, traction, pulse, mass):
        self.name = name
        self.traction = traction
        self.pulse = pulse
        self.mass = mass


class Tank(ObjectOfRocket):
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
