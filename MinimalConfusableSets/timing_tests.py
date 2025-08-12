import time
import math
from vertex_matches import (
      generate_all_vertex_matches_given_equivalent_places_IMPLEMENTATION_A, 
      generate_all_vertex_matches_given_equivalent_places_IMPLEMENTATION_B,
)
from equivalent_places import Equivalent_Places

def demo():

    iterations = 100

    for equivalent_places in (
            Equivalent_Places(equivalents_with_singletons=( (0,7,),(1,4,5,6),(2,3,9,), (8,),  )),
            Equivalent_Places(size=10, equivalents_without_singletons=( (0,7,),(1,4,5,6),(2,3,9,),   )),
            Equivalent_Places(size=12, equivalents_without_singletons=( (0,7,),(1,4,5,6),(2,3,9,),   )),
            Equivalent_Places(size=14, equivalents_without_singletons=( (0,7,),(1,4,5,6),(2,3,9,),   )),
           ):
      print()
      print("=======================================")
      print()
      for method in (generate_all_vertex_matches_given_equivalent_places_IMPLEMENTATION_A, generate_all_vertex_matches_given_equivalent_places_IMPLEMENTATION_B):
        t0 = time.time()
        for i in range(iterations):
            count = sum(1 for _ in method(equivalent_places = equivalent_places))
        t1 = time.time()

        total = t1-t0

        print(f"{total} seconds for {iterations} iterations of {method} on {equivalent_places}. Each found {count} matches.")

if __name__ == "__main__":
    demo()

