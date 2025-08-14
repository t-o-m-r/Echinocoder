#import itertools
import math
from vertex_matches import (
    generate_all_vertex_match_signatures,
    generate_all_vertex_matches,
)

from distinct_permutations_with_leftovers import distinct_permutations_with_leftovers as distinct_permutations
from distinct_partitions_with_start import distinct_partitions_with_start as distinct_partitions
from bi_range import bi_range_with_maxes
from equivalent_places import Equivalent_Places

def generate_all_useful_vertex_matches(
    M, # M=number of bad bats
    k, # k=dimension of space 
    permute = True,
    ):
    yield from generate_all_vertex_matches(M=M, k=k, permute=permute)


def generate_all_useful_vertex_matches_given_perming_places(
        M, # M=number of bad bats
        k, # k=dimension of space (supply k if you want to calculate only useful matches, otherwise omit)
        perming_places = 0, # permutations take place within the first "perming_places" places, otherwise not.
        ):
    yield from generate_all_vertex_matches_given_perming_places(M, k=k, perming_places=perming_places)

def generate_all_vertex_matches_given_perming_places(
        M, # M=number of bad bats
        k=None, # k=dimension of space (supply k if you want to calculate only useful matches, otherwise omit)
        perming_places = 0, # permutations take place within the first "perming_places" places, otherwise not.
        ):

        if M<0:
            raise ValueError(f"M should be a non-negative integer but is {M}.")

        if perming_places<0 or perming_places>M:
            raise ValueError(f"perming_places should be in [0,{M}]  but is {perming_places}.")

        non_perming_places = M-perming_places

        for number_of_ones, number_of_minus_ones, number_of_zeros in generate_all_vertex_match_signatures(M,k=k):

            for perming_ones, non_perming_ones in bi_range_with_maxes(number_of_ones, max_first=perming_places, max_second=non_perming_places):
                for perming_minus_ones, non_perming_minus_ones in bi_range_with_maxes(number_of_minus_ones, max_first = perming_places-perming_ones, max_second=non_perming_places - non_perming_ones):
                    perming_zeros = perming_places - (perming_ones + perming_minus_ones)
                    non_perming_zeros = number_of_zeros - perming_zeros

                    assert perming_zeros >=0
                    assert non_perming_zeros >=0

                    perming_part = (-1,)*perming_minus_ones + (0,)*perming_zeros + (1,)*perming_ones # Note numerical order!
                    non_perming_part = (-1,)*non_perming_minus_ones + (0,)*non_perming_zeros + (1,)*non_perming_ones # Note numerical order!

                    for perm in distinct_permutations(perming_part):
                        yield perm + non_perming_part


                  
def demo():
    M=4
    for perming_places in range(5):
        print(f"All matches, given M={M} bad bats, for perming_places={perming_places}")
        for i,match in enumerate(generate_all_vertex_matches_given_perming_places(M=M, perming_places=perming_places)):
           print(f"   {i+1}:    {match}")
        print()
    k=2
    for perming_places in range(5):
        print(f"All USEFUL matches in k={k} dimensions, given M={M} bad bats, for perming_places={perming_places}")
        for i,match in enumerate(generate_all_useful_vertex_matches_given_perming_places(k=k, M=M, perming_places=perming_places)):
           print(f"   {i+1}:    {match}")
        print()

if __name__ == "__main__":
    demo()

