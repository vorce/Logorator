import unittest
import generator
from hamcrest import *

class TestGenerator(unittest.TestCase):
    def new_range_generator(self, maxrange):
        return generator.Generator().g_int_range(maxrange)


    def new_color_generator(self):
        return generator.Generator().g_color_range()


    def new_constant_generator(self, constant):
        return generator.Generator().g_constant(constant)


    def test_int_range_generator_holds_contract(self):
        g = self.new_range_generator(10)
        result = [ g.next() for _ in range(500) ]
        assert_that(result, is_not(has_item(greater_than(10))))
        assert_that(result, is_not(has_item(less_than(0))))


    def test_color_range_generator_holds_contract(self):
        g = self.new_color_generator()
        result = [ g.next() for _ in range(500) ]
        assert_that(result, is_not(has_item(greater_than(255))))
        assert_that(result, is_not(has_item(less_than(0))))


    def test_constant_generator_holds_contract(self):
        g = self.new_constant_generator("test")
        result = [ g.next() for _ in range(500) ]
        assert_that(result, only_contains("test"))


if __name__ == '__main__':
    unittest.main()

