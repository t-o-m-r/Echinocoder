from distinct_permutations import distinct_permutations

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
                for i, part in enumerate(distinct_permutations(data, r=r, output_leftovers=output_leftovers)):
                    if r is None:
                        print(f"{i+1}:   {data} contains {part}")
                    else:
                        print(f"{i+1}:   {data} contains length={r} part {part}")
                print()

def test_things():
    test_programme= [
        {"data" : [1,2,2,3], "r" : 2, "output_leftovers" : False, "expected" : [
            (1,2), (2,1), (2,2),
            (1,3), (2,3),
            (3,1), (3,2), 
        ]},
        {"data" : [1,2,2,3], "r" : None, "output_leftovers" : False, "expected" : [
            (1,2,2,3), (2,1,2,3), (2,2,1,3), 
            (1,2,3,2), (2,1,3,2), (2,2,3,1), 
            (1,3,2,2), (2,3,1,2), (2,3,2,1), 
            (3,1,2,2), (3,2,1,2), (3,2,2,1), 
        ]},
    ]

    for d in test_programme:
        expected_sorted = sorted(d["expected"])
        got =  sorted(list(distinct_permutations(d["data"], r=d["r"], output_leftovers=d["output_leftovers"])))
        assert got == expected_sorted


if __name__ == "__main__":
    test_things()
    demo()

