import unittest
from hamcrest import *
import polygen
import lsysgen

class PolygenTest(unittest.TestCase):
    def test_triangle_should_have_4_point_pairs(self):
        poly_gen = polygen.PolyGen()
        triangle_sides = 3
        
        triangle_points = poly_gen.ngon(0, 0, 10, triangle_sides)
        number_of_point_pairs = len(triangle_points) / 2

        assert_that(number_of_point_pairs, is_(4))


    def test_nonrotated_triangle_first_point_pair_should_be_next_to_origin(self):
        poly_gen = polygen.PolyGen()
        triangle_sides = 3
        origin_x = 0.0
        origin_y = 0.0
        side_len = 10.0
        
        triangle_points = poly_gen.ngon(origin_x, origin_y,
                                        side_len, triangle_sides)
        first_point_pair = triangle_points[:2]
        expected_point_pair = [origin_x + side_len, origin_y]
        
        assert_that(first_point_pair, is_(expected_point_pair))


    def test_rectangle_should_have_5_point_pairs(self):
        poly_gen = polygen.PolyGen()
        rectangle_sides = 4
        
        rectangle_points = poly_gen.ngon(0, 0, 10, rectangle_sides)
        number_of_point_pairs = len(rectangle_points) / 2

        assert_that(number_of_point_pairs, is_(5))


# TODO
class LSysGenTest(unittest.TestCase):
    pass