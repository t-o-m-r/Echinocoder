from distinct_permutations_with_leftovers import distinct_permutations_with_leftovers

class X:
    def __init__(self, name): self.name = name
    def __repr__(self): return f"X({self.name!r})"

a = X('a')
b = X('b')
c = X('c')

def demo():
    for data in (
         [1,2,2,3],
         ["S","p","e","e","d","o"],
         [a,b,b,c],
         ):
        for output_leftovers in False, True:
            for r in None, 2:
                if output_leftovers:
                    print("Will compute leftovers:")
                else:
                    print("Will not compute leftovers:")
                for i, part in enumerate(distinct_permutations_with_leftovers(data, r=r, output_leftovers=output_leftovers)):
                    if r is None:
                        print(f"{i+1}:   {data} contains {part}")
                    else:
                        print(f"{i+1}:   {data} contains length={r} part {part}")
                print()

def test_things():
    test_programme= [
        {"data" : [1,2,2,3], "r" : -1, "output_leftovers" : False, "expected" : [] },
        {"data" : [1,2,2,3], "r" : -1, "output_leftovers" : True, "expected" : [] },
        {"data" : [1,2,2,3], "r" : 5, "output_leftovers" : False, "expected" : [] },
        {"data" : [1,2,2,3], "r" : 5, "output_leftovers" : True, "expected" : [] },
        {"data" : [1,2,2,3], "r" : 0, "output_leftovers" : False, "expected" : [
          tuple(),
        ]},
        {"data" : [1,2,2,3], "r" : 0, "output_leftovers" : True, "expected" : [
          (tuple(), (1,2,2,3)), # Compare with order of leftovers in next test. 
        ]},
        {"data" : [1,2,2,3], "r" : 0, "output_leftovers" : True, "expected" : [
          (tuple(), (3,2,1,2)), # Compare with order of leftovers in last test. [Testing here that our unit test doesn't demand particular order within any leftovers!]
        ]},
        {"data" : [1,2,2,3], "r" : 1, "output_leftovers" : False, "expected" : [
          (1,),
          (2,),
          (3,),
        ]},
        {"data" : [1,2,2,3], "r" : 1, "output_leftovers" : True, "expected" : [
          ((1,), (2,2,3)),
          ((2,), (1,2,3)),
          ((3,), (1,2,2)),
        ]},
        {"data" : [1,2,2,3], "r" : 2, "output_leftovers" : False, "expected" : [
          (1, 2),
          (1, 3),
          (2, 1),
          (2, 2),
          (2, 3),
          (3, 1),
          (3, 2),
        ]},
        {"data" : [1,2,2,3], "r" : 2, "output_leftovers" : True, "expected" : [
            ((1,2), (2,3)),
            ((1,3), (2,2)),
            ((2,1), (2,3)),
            ((2,2), (1,3)),
            ((2,3), (1,2)),
            ((3,1), (2,2)),
            ((3,2), (1,2)),
        ]},
        {"data" : [3,2,1,2], "r" : 2, "output_leftovers" : True, "expected" : [ # Note change to order of data in this test vs last test.
            ((1,2), (2,3)),
            ((1,3), (2,2)),
            ((2,1), (2,3)),
            ((2,2), (1,3)),
            ((2,3), (1,2)),
            ((3,1), (2,2)),
            ((3,2), (1,2)),
        ]},
        # a, b and c are not sortable. So the next few tests check action on non-sortable things
        {"data" : [a,b,b,c], "r" : 1, "output_leftovers" : False, "expected" : [
            (a,),
            (b,),
            (c,),
        ]},
        {"data" : [a,b,b,c], "r" : 1, "output_leftovers" : True, "expected" : [
            ((a,), (b,b,c)),
            ((b,), (a,b,c)),
            ((c,), (a,b,b)),
        ]},
        {"data" : [a,b,b,c], "r" : 2, "output_leftovers" : False, "expected" : [
            (a,b),
            (a,c),
            (b,a),
            (b,b),
            (b,c),
            (c,a),
            (c,b),
        ]},
        {"data" : [a,b,b,c], "r" : 2, "output_leftovers" : True, "expected" : [
            ((a,b), (b,c)),
            ((a,c), (b,b)),
            ((b,a), (b,c)),
            ((b,b), (a,c)),
            ((b,c), (a,b)),
            ((c,a), (b,b)),
            ((c,b), (a,b)),
        ]},
        {"data" : [a,b,b,c], "r" : 3, "output_leftovers" : True, "expected" : [
            ((a,b,b), (c,)),
            ((a,b,c), (b,)),
            ((a,c,b), (b,)),
            ((b,a,b), (c,)),
            ((b,a,c), (b,)),
            ((b,b,a), (c,)),
            ((b,b,c), (a,)),
            ((b,c,a), (b,)),
            ((b,c,b), (a,)),
            ((c,a,b), (b,)),
            ((c,b,a), (b,)),
            ((c,b,b), (a,)),
        ]},
        {"data" : [1,2,2,3], "r" : None, "output_leftovers" : False, "expected" : [
            (1,2,2,3),
            (1,2,3,2),
            (1,3,2,2),
            (2,1,2,3),
            (2,1,3,2),
            (2,2,1,3),
            (2,2,3,1),
            (2,3,1,2),
            (2,3,2,1),
            (3,1,2,2),
            (3,2,1,2),
            (3,2,2,1),
        ]},
        {"data" : [1,2,2,3], "r" : 4, "output_leftovers" : False, "expected" : [
            (1,2,2,3),
            (1,2,3,2),
            (1,3,2,2),
            (2,1,2,3),
            (2,1,3,2),
            (2,2,1,3),
            (2,2,3,1),
            (2,3,1,2),
            (2,3,2,1),
            (3,1,2,2),
            (3,2,1,2),
            (3,2,2,1),
        ]},
        {"data" : [1,2,2,3], "r" : 4, "output_leftovers" : True, "expected" : [
            ((1,2,2,3), ()),
            ((1,2,3,2), ()),
            ((1,3,2,2), ()),
            ((2,1,2,3), ()),
            ((2,1,3,2), ()),
            ((2,2,1,3), ()),
            ((2,2,3,1), ()),
            ((2,3,1,2), ()),
            ((2,3,2,1), ()),
            ((3,1,2,2), ()),
            ((3,2,1,2), ()),
            ((3,2,2,1), ()),
        ]},
        # Try on a string:
        {"data" : "cat", "r" : None, "output_leftovers" : True, "expected" : [
            (("a","c","t"), ()),
            (("a","t","c"), ()),
            (("c","a","t"), ()),
            (("c","t","a"), tuple()), # Just for fun!
            (("t","a","c"), ()),
            (("t","c","a"), ()),
        ]},
        # Try on a string:
        {"data" : "moo", "r" : 2, "output_leftovers" : True, "expected" : [
            (("m","o"), ("o",)),
            (("o","m"), ("o",)),
            (("o","o"), ("m",)),
        ]},
    ]

    def sanitize(data, output_leftovers):
        from collections import Counter
        if output_leftovers:
            return list([(tup, Counter(leftovers)) for tup, leftovers in data])
        else:
            return list(data)
                
    for d in test_programme:
        got = list(distinct_permutations_with_leftovers(d["data"], r=d["r"], output_leftovers=d["output_leftovers"]))
        expected = d["expected"]
        from itertools import zip_longest
        print("got, expected")
        for i, (g,e) in enumerate(zip_longest(got, expected)):
            print(f"    {i}: ({g==e})   {g}   {e}")
        print()

        got = sanitize(got, d["output_leftovers"])
        expected = sanitize(expected, d["output_leftovers"])
        assert got == expected


if __name__ == "__main__":
    test_things()
    demo()

