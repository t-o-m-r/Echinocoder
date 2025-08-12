from more_itertools import distinct_combinations


def distinct_split(iterable, n):
    """Yield distinct unordered partitions into sizes n and len(iterable)-n."""
    items = tuple(iterable)  # fixed-size storage
    m = len(items) - n
    for comb in distinct_combinations(items, n):
        # Build complement without storing all seen
        remaining = list(items)
        for c in comb:
            remaining.remove(c)  # safe: remove one occurrence per element in comb
        group1 = tuple(comb)
        group2 = tuple(remaining)

        yield group1, group2

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
    for a, b in distinct_split("happy", 2):
        print(f"{a} --- {b}")

if __name__ == "__main__":
    demo()
