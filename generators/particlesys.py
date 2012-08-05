"""
A particle system framework meant to be used by
logorator generators.
"""

class Particle:
    """
    An idividual particle moving about
    """
    def __init__(self, position, velocity, acceleration):
        self._pos = position
        self._vel = velocity
        self._acc = acceleration

    def update(self):
        pass

    def render(self, func = None):
        if func == None:
            pass
        else:
            func(self)

class Emitter:
    """
    Emits a number of Particles, in a direction
    """
    def __init__(self, position, direction):
        self._pos = position
        self._dir = direction
        self._particles = []

    def update(self):
        # Additional logic for moving an emitter?
        for p in self._particles:
            p.update()

    def render(self, func = None):
        for p in self._particles:
            p.render(func)


class ParticleSystem:
    """
    Contains a number of Emitters, and some optional additional
    parameters such as gravity
    """
    def __init__(self):
        self._emitters = []

    def add_emitter(self, position, direction):
        self._emitters.append(Emitter(position, direction))


