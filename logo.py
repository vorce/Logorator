import sys

class Logo(list):
    """
    A Logo is the result of any number of generators combined
    """
    
    def __init__(self, *args):
        list.__init__(self, *args)
        self._generators_by_type = self.__generator_types_map()
        self._generator_type_set = set(self._generators_by_type.keys())


    def __generator_types_map(self):
        generators_by_type = {}
        
        for generator in self:
            module_and_class = (generator.__module__, generator.__class__.__name__)
            generator_list = generators_by_type.get(module_and_class, [])
            generator_list.append(generator)
            generators_by_type[module_and_class] = generator_list
        return generators_by_type


    @classmethod
    def mix_of(cls, logo1, logo2):
        unique_gens = logo1.get_unique_generators(logo2)
        mix_gens = logo1.get_mixed_generators(logo2)
        final_gens = unique_gens + mix_gens
        
        return Logo(final_gens)


    # This is the easy part, get any generator type
    # that is only in one place and copy it/them
    def get_unique_generators(self, other):
        unique_gen_set = self._generator_type_set.symmetric_difference(
                            other._generator_type_set)
        unique_gens = []
        for gen_type in unique_gen_set:
            if gen_type in self._generators_by_type.keys():
                unique_gens += self._generators_by_type[gen_type]
            else:
                unique_gens += other._generators_by_type[gen_type]
        return unique_gens


    def get_mixed_generators(self, other):
        common_gen_set = self._generator_type_set.intersection(
                                other._generator_type_set)
        
        common_gens = []
        for gen_type in common_gen_set:
            common_gens += self._mix_generators(gen_type,
                                self._generators_by_type[gen_type],
                                other._generators_by_type[gen_type])
        return common_gens


    def _mix_generators(self, gen_type, logo1_generators, logo2_generators):
        new_gens = []
        i = 0
        (themodule, clazz) = gen_type
        
        def longest_list(list1, list2):
            return (len(list1) >= len(list2) and list1) or (list2)
        
        for gen in longest_list(logo1_generators, logo2_generators):
            if(i > (len(logo2_generators) - 1)):
                i = 0
            
            new_gen = getattr(sys.modules[themodule],
                              clazz).mix_of(gen, logo2_generators[i])  # create a new mix_of of the same class
            new_gens.append(new_gen)
            i += 1
        return new_gens