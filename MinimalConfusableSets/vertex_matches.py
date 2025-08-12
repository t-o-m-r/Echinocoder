#import itertools
import math
from distinct_permutations_with_leftovers import distinct_permutations_with_leftovers as distinct_permutations
from distinct_partitions import distinct_partitions
from bi_range import bi_range_with_maxes
from equivalent_places import Equivalent_Places

"""
Vertex matches have an even number of +1 and and odd number of -1 entries, and others zero. Their total number of entries is M, the numnber of bad bats.

"Useful" vertex matches have at least k+1 non-zero entries (because all sums of <=k linearly dependent non-zero things in k-dimes are non-zero).

A "canonical" vertex match is one where all the ones come before all the minus ones which come before all the zeros WITHIN any positions which are otherwise equivalent. . E.g., of all position are equivalent, then (1,1,-1,-1,-1,0) is a canonical match.

Sometimes it is not worth permuting vertex matches over every bad bat because other matches in the existing context may not yet have broken any symmetries between the bats.

E.g. if the first two places are different to each other (and to any other place) but the last four places are all equivalent to each other, then one need only consider these orderings of the letters "Speedo" in that context:

    Sp.eedo
    Se.pedo
    Sd.peeo
    So.peed

    pS.eedo
    pe.Sedo
    pd.Seeo
    po.Seed

    eS.pedo
    ep.pedo
    ee.pedo  # Yes, this group has five on account of the double "e" !
    ed.pedo
    eo.Sped

    dS.peeo
    dp.Seep
    de.Speo
    do.Spee

    oS.peed
    op.Seed
    oe.Sped
    od.Spee
"""


def _smallest_odd_number_greater_than_or_equal_to(x):
    return 2*math.ceil((x+1)/2)-1 

def generate_all_vertex_match_signatures(
    M, #number of bad bats
    k = None, # k=dimension of space (supply k if you want to calculate only useful matches, otherwise omit)
    ):
    """
    The signature of a caonoical match is how many ones, minus ones and zeros it has.
    We yield triplets of numbers in that order.

    Vertex matches have M entries in total, comprising an even number of +1 and and odd number of -1 entries, and others zero.

    "Useful" vertex matches have at least k+1 non-zero entries (because all sums of <=k linearly dependent non-zero things in k-dimes are non-zero).
    """
    for number_of_ones in range(0, M+1, 2):

        if k is not None:
            # In this case we need 
            #         number_of_ones + number_of_minus_ones > k  and   number_of_minus_ones >= 1
            # so
            #         number_of_minus_ones > k - number_of_ones   and number_of_minus_ones >= 1
            # so
            #         number_of_minus_ones >= k - number_of_ones + 1 and number_of_minus_ones >=1
            # so
            #         number_of_minus_ones >= max(k - number_of_ones + 1, 1)
            start_for_number_of_minus_ones =  max(1, _smallest_odd_number_greater_than_or_equal_to(k - number_of_ones + 1))
        else:
            start_for_number_of_minus_ones = 1

        for number_of_minus_ones in range(start_for_number_of_minus_ones, M+1-number_of_ones, 2):
            # In an alternative (but slower) implementation, one could always have start_for_number_of_minus_ones=1 but then 
            # uncomment the next two lines:
            # if k is not None and (number_of_ones + number_of_minus_ones <= k):
            #      continue
            number_of_zeros = M-number_of_ones-number_of_minus_ones
            yield number_of_ones, number_of_minus_ones, number_of_zeros

def generate_all_vertex_matches(
        M, # M=number of bad bats
        k=None, # k=dimension of space (supply k if you want to calculate only useful matches, otherwise omit)
        permute = True,
        ):
        """
        M should be a non-negative integer. It specifies how long each generated tuple will be. (The number of bad bats!)

        k, if not None, should be the dimension of space.  Supply k if you want to generate only the useful matches for that spatial dimension.

        This method generates all tuples with the following properties:

           * the tuple has length M,
           * the tuple has an even number of ones,
           * the tuple has an odd number of minus ones,
           * the tuple is composed only of ones, minus ones and zeros, and
           * if k is not None, then the tuple shall have AT LEAST k+1 non-zero entries.
        
        By default, each tuple is yielded in every possible distinct ordering of its elements. However, this perming can be disabled by setting permute=False. This will result in each tuple being yielded once only in a canonical form (all ones followed by all minus ones followed by all zeros).
        """

        for number_of_ones, number_of_minus_ones, number_of_zeros in generate_all_vertex_match_signatures(M, k=k):

            ones = (1,)*number_of_ones
            minus_ones = (-1,)*number_of_minus_ones
            zeros = (0,)*number_of_zeros

            if permute:
                for match in distinct_permutations( ones + minus_ones + zeros):
                    yield match
            else:
                yield ones + minus_ones + zeros

def generate_all_useful_vertex_matches(
    M, # M=number of bad bats
    k, # k=dimension of space 
    permute = True,
    ):
    yield from generate_all_vertex_matches(M=M, k=k, permute=permute)


def generate_all_vertex_matches_given_equivalent_places_IMPLEMENTATION_A(
    equivalent_places : Equivalent_Places,
    # M=None, # M = number of bad bats. (Can be derived from equivalent_places, so no longer supplied)
    k=None, # k=dimension of space (supply k if you want to calculate only useful matches, otherwise omit)
    ):

    M = equivalent_places.size
    if int(M) != M or M<0:
        raise RuntimeError("Equivalent_Places is not behaving!")

    if M==0:
        return

    assert M>0

    ##############################################
    def _generate_dicts_for(e_places, signature):
        #print(f"GENERATE_DICTS_FOR e_places={e_places} signature={signature}.")
        # Caller must guarantee e_places is non-empty, M>0 and signature consistent with e_places
        tot = sum(signature)
        assert e_places
        number_of_ones, number_of_minus_ones, number_of_zeros = signature
        assert tot == sum(len(e_place) for e_place in e_places)
    
        perming_places = len(e_places[0])
        non_perming_places = tot - perming_places
    
        # Recursion will stop when non_perming_places reaches 0 .... which should be the same as wheb e_places is length 1.
        # Let's check the above statement.
        assert (non_perming_places > 0 and len(e_places) > 1) or (non_perming_places == 0 and len(e_places)==1)
    
        #print(f"ones bi_range {list(bi_range_with_maxes(number_of_ones, max_first=perming_places, max_second=non_perming_places))}")
        for perming_ones, non_perming_ones in bi_range_with_maxes(number_of_ones, max_first=perming_places, max_second=non_perming_places):
            #print(f"minus ones bi_range {list(bi_range_with_maxes(number_of_minus_ones, max_first=perming_places-perming_ones, max_second=non_perming_places - non_perming_ones))}")
            for perming_minus_ones, non_perming_minus_ones in bi_range_with_maxes(number_of_minus_ones, max_first = perming_places-perming_ones, max_second=non_perming_places - non_perming_ones):
                perming_zeros = perming_places - (perming_ones + perming_minus_ones)
                non_perming_zeros = number_of_zeros - perming_zeros
    
    
                #print(f"PERMING_SIG = {perming_ones, perming_minus_ones, perming_zeros}")
                #print(f"NON_PERMING_SIG = {non_perming_ones, non_perming_minus_ones, non_perming_zeros}")
                assert perming_zeros >=0
                assert non_perming_zeros >=0
    
                perming_part = (1,)*perming_ones + (-1,)*perming_minus_ones + (0,)*perming_zeros
                assert len(perming_part) == len(e_places[0])
    
                perming_part_dict = dict(zip(e_places[0], perming_part))
    
                if non_perming_places == 0:
                    yield perming_part_dict
                else:
                    new_signature = (non_perming_ones, non_perming_minus_ones, non_perming_zeros)
                    for non_perming_part_dict in _generate_dicts_for(e_places[1:], new_signature):
                       yield perming_part_dict | non_perming_part_dict
    ##############################################


    e_places = equivalent_places._equivalent_places_with_singletons
    for signature in generate_all_vertex_match_signatures(M,k=k):


        for d in _generate_dicts_for(e_places, signature):
            yield tuple(d[i] for i in range(M))

def generate_all_vertex_matches_given_equivalent_places_IMPLEMENTATION_B(
        equivalent_places : Equivalent_Places,
        # M=None, # M = number of bad bats. (Can be derived from equivalent_places, so no longer supplied)
        k=None, # k=dimension of space (supply k if you want to calculate only useful matches, otherwise omit)
        ):

    M = equivalent_places.size
    if int(M) != M or M<0:
        raise RuntimeError("Equivalent_Places is not behaving!")

    if M==0:
        return

    assert M>0

    e_places = equivalent_places._equivalent_places_with_singletons
    splitting = tuple( len(group) for group in e_places ) 

    workspace = [None]*M

    for vertex_match in generate_all_vertex_matches(M=M, k=k, permute=False):
        for partition in distinct_partitions(vertex_match, splitting):
            assert len(partition) == len(e_places)
            for payload_group, pos_group in zip(partition, e_places):
                assert len(payload_group) == len(pos_group)
                for payload, pos in zip(payload_group, pos_group):
                    assert 0 <= pos < M
                    assert payload in (+1, -1, 0)
                    workspace[pos] = payload
            yield tuple(workspace)

def generate_all_vertex_matches_given_equivalent_places(
        equivalent_places : Equivalent_Places,
        # M=None, # M = number of bad bats. (Can be derived from equivalent_places, so no longer supplied)
        k=None, # k=dimension of space (supply k if you want to calculate only useful matches, otherwise omit)
        ):
    #return generate_all_vertex_matches_given_equivalent_places_IMPLEMENTATION_A(equivalent_places, k=k)
    return generate_all_vertex_matches_given_equivalent_places_IMPLEMENTATION_B(equivalent_places, k=k)

def demo():
    M=4
    print(f"All matches given M={M} bad bats are:")
    for i, match in enumerate(generate_all_vertex_matches(k=None, M=M)):
       print(f"   {i+1}:    {match}")
    print()

    k=2

    print(f"All useful matches in k={k} dimensions, given M={M} bad bats, but ignoring permutations are:")
    for i,match in enumerate(generate_all_vertex_matches(k=k, M=M, permute=False)):
       print(f"   {i+1}:    {match}")
    print()



    for equivalent_places in ( Equivalent_Places(size=M, none_equivalent=True), ):
        print(f"All USEFUL matches in k={k} dimensions, given M={M} bad bats, for equivalent_places={equivalent_places}")
        for i,match in enumerate(generate_all_vertex_matches_given_equivalent_places(k=k, equivalent_places=equivalent_places)):
           print(f"   {i+1}:    {match}")
        print()

    for equivalent_places in ( Equivalent_Places(size=M, none_equivalent=True), ):
        print(f"All matches given M={M} bad bats, for equivalent_places={equivalent_places}")
        for i,match in enumerate(generate_all_vertex_matches_given_equivalent_places(k=None, equivalent_places=equivalent_places)):
           print(f"   {i+1}:    {match}")
        print()

    print("timing tests are now in timing_tests.py")

if __name__ == "__main__":
    demo()

