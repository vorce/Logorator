import unittest
import generator

class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = generator.Generator()

    def test_int_range_generator_holds_contract(self):
        g = self.gen.g_int_range(10)
        for i in range(500):
            result = g.next()
            self.assertTrue(result <= 10)


    def test_color_range_generator_holds_contract(self):
        g = self.gen.g_color_range()
        for i in range(500):
            result = g.next()
            self.assertTrue(result <= 255)

    def test_constant_generator_holds_contract(self):
        g = self.gen.g_constant("test")
        for i in range(500):
            result = g.next()
            self.assertTrue(result == "test")


if __name__ == '__main__':
    unittest.main()

