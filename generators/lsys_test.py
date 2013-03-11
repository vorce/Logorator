import lsys
import unittest
from hamcrest import *

class TestLSys(unittest.TestCase):
    def create_minimal_lsys(self):
        return lsys.LSys("", {}, 1)
    
    def test_produce_any_axiom_with_no_rules_should_give_the_axiom(self):
        ls = self.create_minimal_lsys()
        my_axiom = "axiom"
        
        command = ls.produce(my_axiom, {})
        
        assert_that(command, is_(my_axiom))
        

    def test_produce_axiom_F_rules_FplusF_should_give_FplusF(self):
        ls = self.create_minimal_lsys()
        my_axiom = "F"
        my_rules = {"F": "F+F"}
        
        command = ls.produce(my_axiom, my_rules)
        
        assert_that(command, is_(my_rules[my_axiom]))


    def test_produce_axiom_F_rules_FplusF_twice_should_give_FplusFplusFplusF(self):
        ls = self.create_minimal_lsys()
        my_axiom = "F"
        my_rules = {"F": "F+F"}
        
        command = ls.produce(ls.produce(my_axiom, my_rules), my_rules)
        
        assert_that(command, is_("F+F+F+F"))

    def test_evolve_axiom_F_rules_FplusF_twice_should_give_same_as_produce_twice(self):
        ls = self.create_minimal_lsys()
        my_axiom = "F"
        my_rules = {"F": "F+F"}
        
        command = ls.evolve(2, my_axiom, my_rules)
        
        assert_that(command, is_(ls.produce(ls.produce(my_axiom, my_rules), my_rules)))