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

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


# исключения
class ExceptionGroupKSP(Exception):
    def __init__(self, message='Необработанная ошибка'):
        self.message = message

    def __str__(self):
        return f'{self.message}'


class ErrorPlanets(ExceptionGroupKSP):
    pass


class NegativeValue(ErrorPlanets):
    pass


class IncorrectInput(ExceptionGroupKSP):
    pass


class NoAnyoneSelect(IncorrectInput):
    pass


class DifferentParent(IncorrectInput):
    pass

class SamePlanet(IncorrectInput):
    pass
