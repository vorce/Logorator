import unittest
from hamcrest import *
from logo import Logo
import polygen
import textgen
import lsysgen

class TestLogo(unittest.TestCase):
    def create_logo(self, gens):
        return Logo(gens)
    
    def test_empty_logo_is_empty_list(self):
        lg = Logo()
        
        assert_that(lg, is_([]))
        
    def test_get_item_from_logo_should_return_item_initialized_with(self):
        poly_gen = polygen.PolyGen()
        
        gl = self.create_logo([ poly_gen ])
        
        assert_that(gl[0], is_(poly_gen))
        
    def test_mix_of_two_logos_with_one_polygen_each_should_contain_one_new_polygen(self):
        l1 = self.create_logo([ polygen.PolyGen() ])
        l2 = self.create_logo([ polygen.PolyGen() ])
        
        mixed = Logo.mix_of(l1, l2)
        
        assert_that("Mixed logo does not have one generator",
                    len(mixed), is_(1))
        assert_that("Mixed logo's first generator is not a PolyGen",
                    mixed[0], is_(instance_of(polygen.PolyGen)))
        assert_that("Mixed logo's first generator is one of the original PolyGens",
                    mixed[0], is_not(is_in([l1, l2])))
        
    def test_mix_of_two_logos_with_one_different_gen_each_should_contain_two_unchanged_gens(self):
        poly_gen = polygen.PolyGen()
        text_gen = textgen.TextGen()
        l1 = self.create_logo([ poly_gen ])
        l2 = self.create_logo([ text_gen ])
        
        l3 = Logo.mix_of(l1, l2)
        
        assert_that(len(l3), is_(2))
        assert_that(l3, contains_inanyorder(poly_gen, text_gen))
        
    def test_mix_two_textgens_and_one_polygen_should_get_one_mixed_textgen_and_one_unchanged_polygen(self):
        poly_gen = polygen.PolyGen()
        text_gen1 = textgen.TextGen()
        text_gen2 = textgen.TextGen()
        l1 = self.create_logo([ poly_gen, text_gen1 ])
        l2 = self.create_logo([ text_gen2 ])
        
        mixed = Logo.mix_of(l1, l2)
        
        # Many asserts, but we want to be strict here
        # The mixed Logo shall:
        # * Only have two elements.
        # * Contain the original poly_gen.
        # * Not contain any of the original text_gens
        # * Contain one TextGen
        assert_that("Mixed Logo does not have two generators",
                    len(mixed), is_(2))
        assert_that("Mixed Logo does not contain the original PolyGen",
                    mixed, has_item(poly_gen))
        assert_that("Mixed Logo contains the original TextGens",
                    mixed, is_not(has_items([text_gen1, text_gen2])))
        assert_that("Mixed Logo does not contain a TextGen",
                    mixed, has_item(instance_of(textgen.TextGen)))
    
    # TODO Fix my name
    def test_multiple_generator_logos_mixed_should_adhere_to_rules(self):
        l1 = Logo([lsysgen.LSysGen(), polygen.PolyGen(),
                   polygen.PolyGen(), polygen.PolyGen()])
        
        l2 = Logo([polygen.PolyGen(), polygen.PolyGen(),
                   lsysgen.LSysGen()])

        l3 = Logo.mix_of(l1, l2)
        assert_that(len(l3), is_(4))