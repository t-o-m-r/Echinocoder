from distinct_permutations import distinct_permutations

class X:
    def __init__(self, name): self.name = name
    def __repr__(self): return f"X({self.name!r})"

a = X('a')
b = X('b')
c = X('c')

def test_things():
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

if __name__ == "__main__":
    test_things()

