from more_itertools import distinct_combinations


def distinct_partitions(iterable, splitting):
    
    """
    Yield distinct unordered partitions according to sizes given in (ordered!) splitting.
    splitting shall be a tuple of non-negative integers whose sum shall be the length of the iterable.

    E.g. the result for

        distinct_split( "hello", (2,3) )

    should be
        (
            (('h', 'a'), ('p', 'p', 'y')),
            (('h', 'p'), ('a', 'p', 'y')),
            (('h', 'y'), ('a', 'p', 'p')),
            (('a', 'p'), ('h', 'p', 'y')),
            (('a', 'y'), ('h', 'p', 'p')),
            (('p', 'p'), ('h', 'a', 'y')),
            (('p', 'y'), ('h', 'a', 'p')),
        )

    """

    items = tuple(iterable)  # fixed-size storage
    #print(f"DISTINCT SPLIT got items={items} splitting={splitting}")

    if len(items) != sum(splitting):
        raise ValueError()

    #print(f"DISTINCT SPLIT testing len splitting")

    if len(splitting) == 1:
        ans = (tuple(iterable),)
        #print(f"About to yield and then stop after {ans}")
        yield ans
        return 

    assert len(splitting)>1
   
    #print(f"About run over combs of size {splitting[0]} in {items}")
  
    for comb in distinct_combinations(items, splitting[0]):
        first_group = tuple(comb)
        #print(f"first_group is {first_group}")

        # Build complement without storing all seen
        remaining_items = list(items)
        for c in first_group:
            remaining_items.remove(c)  # safe: remove one occurrence per element in comb

        #print(f"XXXXX About to consider {remaining_items} in {splitting[1:]}")
        for other_groups in distinct_partitions(remaining_items, splitting[1:]):
            #print(f"About to yield {first_group} and {other_groups}")
            yield (first_group,) + other_groups

""" BAD: Memory grows with length of number of combinations:
def distinct_split(iterable, n):
    # Yield distinct unordered partitions of iterable into sizes n and len(iterable)-n.
    items = list(iterable)
    seen = set()
    for comb in combinations(range(len(items)), n):
        group1 = tuple(items[i] for i in comb)
        group2 = tuple(items[i] for i in range(len(items)) if i not in comb)

        # Sort within each group according to original positions (WLOG)
        # Also ensure partition is unordered by always storing smaller lexicographic first
        g1 = tuple(group1)
        g2 = tuple(group2)
        part = tuple(sorted((g1, g2)))
        
        # Deduplicate identical multisets
        if part not in seen:
            seen.add(part)
            yield g1, g2
"""

def demo():
    print("distinct_partitions.py demo:")
    print()
    data = "happy"
    splitting = (2,2)
    print(f"distinct_partitions({data}, {splitting}) gives:")
    for split in distinct_partitions(data, splitting):
        print(f"{split}")

if __name__ == "__main__":
    demo()
