from distinct_combinations_with_start import distinct_combinations_with_start as LESTER # Supports "start".
from more_itertools import distinct_combinations as ITERTOOLS # Does not support "start".
from itertools import zip_longest
from itertools import chain

class X:
    def __init__(self, name): self.name = name
    def __repr__(self): return f"X({self.name!r})"

a = X('a')
b = X('b')
c = X('c')

def test_things():
    for data, start in (
         ((1,2,2,3), (2,)),
         (("S","p","e","e","d","o"),  ("p", "d", "o")),
         (("Christopher"),  tuple("hrhr")),
         ((a,b,c,b,c),    (c,)),
         ((a,b,b,c),    (b,b)),
         ((a,b,b,c),    (b,b)),
         ):
         r = len(start)
         print("==============================")
         print(f"Starting test with data={data}, r={r} and start (where used) of {start}.")
         print("==============================")
         start_pos = None
         for i, (lesters, itertoolss) in enumerate(zip_longest(LESTER(data, r), ITERTOOLS(data, r))):
             print(f"{i}:         {lesters} {'==' if lesters==itertoolss else '!='} {itertoolss}")
             if lesters == start and start_pos == None:
                start_pos = i
             assert lesters==itertoolss
         print("Match confirmed!")
         assert start_pos is not None
         print(f"Start pos determined to be {start_pos}.")
         for i, (lesters, itertoolss) in enumerate(zip_longest(chain(iter([None,]*start_pos),LESTER(data, r, start=start)), ITERTOOLS(data, r))):
             if i < start_pos:
                 print(f"{i}:         {lesters} ...  {itertoolss}")
             else:
                 print(f"{i}:         {lesters} {'==' if lesters==itertoolss else '!='} {itertoolss}")
                 assert lesters==itertoolss


### def test_order():
###     """ The tuples shall be rendered in numerical order. Here we test this ordering. """
### 
###     
###     for gen in (
###           distinct_permutations("Spain"),
###           distinct_permutations_with_leftovers("hello"),
###           distinct_permutations("Spain", r=3),
###           distinct_permutations_with_leftovers("hello", r=3),
###           distinct_permutations("Spain", r=-3),
###           distinct_permutations_with_leftovers("hello", r=-3),
###           ):
###         print(f"\nNew Order Test")
###         last_perm = None,
###         first = True
###         for perm in gen:
###             print(f"order test saw perm={perm}")
###             # Only check_order progression when within a given signature:
###             if not first:
###                 # Check_order!
###                 assert last_perm < perm
###             last_perm = perm
###             first = False

if __name__ == "__main__":
    test_things()
