import random


class Generator:
    """
    Basic generator contract/interface
    """
    def __init__(self):
        self.params = {}
        self.seed = {}


    def g_int_range(self, m):
        while True:
            yield random.randint(0, m)


    def g_boolean_range(self):
        while True:
            yield [True, False][random.randint(0, 1)]


    def g_int_span(self, a, b):
        while True:
            yield random.randint(a, b)


    def g_float_span(self, a, b):
        while True:
            yield (random.random() * (b - a)) + a


    def g_double_range(self):
        while True:
            yield random.random()


    def g_color_range(self):
        return self.g_int_range(255)


    def g_list_item(self, lst):
        while True:
            yield lst[random.randint(0, len(lst) - 1)]


    def g_constant(self, c):
        while True:
            yield c


    def dump(self):
        return str(self.seed)


    @classmethod
    def mix_of(cls, gen1, gen2):
        mix_gen = cls()
        
        for seed in gen1.seed:
            if seed == '__generator__':
                continue
            mix_gen.seed[seed] = (gen1.seed[seed] + gen2.seed[seed]) / 2
        return mix_gen