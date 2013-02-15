class Generator:
    """
    Basic generator contract/interface
    """
    def __init__(self, pos):
        self.pos = pos
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

    def g_int_const(self, c):
        return self._g_const(c)

    def g_float_const(self, c):
        return self._g_const(c)

    def _g_const(self, c):
        while True:
            yield c

    def dump(self):
        return str(self.seed)

    def render(self):
        raise NotImplementedException("Should implement this")

    def save_seed(self, filename):
        raise NotImplementedException("Should implement this")

    def load_seed(self, filename):
        raise NotImplementedException("Should implement this")
