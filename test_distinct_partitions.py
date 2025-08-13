from distinct_partitions_v1_no_start import distinct_partitions_v1_no_start
from itertools import zip_longest

def test_distinct_partitions():

    def tuple_of_strings_converter(tup_of_strings):
        return tuple( ( tuple(ch for ch in s) for s in tup_of_strings)  )

    test_programme = [
        ( "make", (2,2), (
                      ("ma", "ke"), # Note that the other way around ("ke", "ma") appears later too. That is intentional.
                      ("mk", "ae"),
                      ("me", "ak"),
                      ("ak", "me"),
                      ("ae", "mk"),
                      ("ke", "ma"),
                     ), tuple_of_strings_converter, "set",
        ),
        ( "make", (4,0), (
                      ("make", ""), 
                     ), tuple_of_strings_converter, "set",
        ),
        ( "make", (0,4), (
                      ("", "make"), 
                     ), tuple_of_strings_converter, "set",
        ),
        ( "happy", (2,3), (
                      ("ha", "ppy"),
                      ("hp", "apy"),
                      ("hy", "app"),
                      ("ap", "hpy"),
                      ("ay", "hpp"),
                      ("pp", "hay"),
                      ("py", "hap"),
                     ), tuple_of_strings_converter, "set",
        ),
        ( "happy", (2,3), (
                      (('h', 'a'), ('p', 'p', 'y')),
                      (('h', 'p'), ('a', 'p', 'y')),
                      (('h', 'y'), ('a', 'p', 'p')),
                      (('a', 'p'), ('h', 'p', 'y')),
                      (('a', 'y'), ('h', 'p', 'p')),
                      (('p', 'p'), ('h', 'a', 'y')),
                      (('p', 'y'), ('h', 'a', 'p')),
                          ), None, "exact",
        ),
        ( "Spain", (2,3), (
            (('S', 'p'), ('a', 'i', 'n')),
            (('S', 'a'), ('p', 'i', 'n')),
            (('S', 'i'), ('p', 'a', 'n')),
            (('S', 'n'), ('p', 'a', 'i')),
            (('p', 'a'), ('S', 'i', 'n')),
            (('p', 'i'), ('S', 'a', 'n')),
            (('p', 'n'), ('S', 'a', 'i')),
            (('a', 'i'), ('S', 'p', 'n')),
            (('a', 'n'), ('S', 'p', 'i')),
            (('i', 'n'), ('S', 'p', 'a')),
                          ), None, "exact",
        ),
        ( "happy", (2,1,2), (
(('h', 'a'), ('p',), ('p', 'y')),
(('h', 'a'), ('y',), ('p', 'p')),
(('h', 'p'), ('a',), ('p', 'y')),
(('h', 'p'), ('p',), ('a', 'y')),
(('h', 'p'), ('y',), ('a', 'p')),
(('h', 'y'), ('a',), ('p', 'p')),
(('h', 'y'), ('p',), ('a', 'p')),
(('a', 'p'), ('h',), ('p', 'y')),
(('a', 'p'), ('p',), ('h', 'y')),
(('a', 'p'), ('y',), ('h', 'p')),
(('a', 'y'), ('h',), ('p', 'p')),
(('a', 'y'), ('p',), ('h', 'p')),
(('p', 'p'), ('h',), ('a', 'y')),
(('p', 'p'), ('a',), ('h', 'y')),
(('p', 'p'), ('y',), ('h', 'a')),
(('p', 'y'), ('h',), ('a', 'p')),
(('p', 'y'), ('a',), ('h', 'p')),
(('p', 'y'), ('p',), ('h', 'a')),
                          ), None, "exact",
        ),
        ( "Spain", (2,1,2), (
(('S', 'p'), ('a',), ('i', 'n')),
(('S', 'p'), ('i',), ('a', 'n')),
(('S', 'p'), ('n',), ('a', 'i')),
(('S', 'a'), ('p',), ('i', 'n')),
(('S', 'a'), ('i',), ('p', 'n')),
(('S', 'a'), ('n',), ('p', 'i')),
(('S', 'i'), ('p',), ('a', 'n')),
(('S', 'i'), ('a',), ('p', 'n')),
(('S', 'i'), ('n',), ('p', 'a')),
(('S', 'n'), ('p',), ('a', 'i')),
(('S', 'n'), ('a',), ('p', 'i')),
(('S', 'n'), ('i',), ('p', 'a')),
(('p', 'a'), ('S',), ('i', 'n')),
(('p', 'a'), ('i',), ('S', 'n')),
(('p', 'a'), ('n',), ('S', 'i')),
(('p', 'i'), ('S',), ('a', 'n')),
(('p', 'i'), ('a',), ('S', 'n')),
(('p', 'i'), ('n',), ('S', 'a')),
(('p', 'n'), ('S',), ('a', 'i')),
(('p', 'n'), ('a',), ('S', 'i')),
(('p', 'n'), ('i',), ('S', 'a')),
(('a', 'i'), ('S',), ('p', 'n')),
(('a', 'i'), ('p',), ('S', 'n')),
(('a', 'i'), ('n',), ('S', 'p')),
(('a', 'n'), ('S',), ('p', 'i')),
(('a', 'n'), ('p',), ('S', 'i')),
(('a', 'n'), ('i',), ('S', 'p')),
(('i', 'n'), ('S',), ('p', 'a')),
(('i', 'n'), ('p',), ('S', 'a')),
(('i', 'n'), ('a',), ('S', 'p')),
                          ), None, "exact",
        ),
        ( "Spain", (2,3), (
            (('S', 'p'), ('a', 'i', 'n')),
            (('S', 'a'), ('p', 'i', 'n')),
            (('S', 'i'), ('p', 'a', 'n')),
            (('S', 'n'), ('p', 'a', 'i')),
            (('p', 'a'), ('S', 'i', 'n')),
            (('p', 'i'), ('S', 'a', 'n')),
            (('p', 'n'), ('S', 'a', 'i')),
            (('a', 'i'), ('S', 'p', 'n')),
            (('a', 'n'), ('S', 'p', 'i')),
            (('i', 'n'), ('S', 'p', 'a')),
                          ), None, "exact",
        ),
        ( "make", (5,), (
                      ("", "make"), 
                     ), tuple_of_strings_converter, "throws",
        ),
        ( "make", (5,-1), (
                      ("", "make"), 
                     ), tuple_of_strings_converter, "throws",
        ),
        ( "make", (-1), (
                      ("", "make"), 
                     ), tuple_of_strings_converter, "throws",
        ),
        ( "make", "a", (
                      ("", "make"), 
                     ), tuple_of_strings_converter, "throws",
        ),
    ]

  
    
    for data, n, expected, converter, typ in test_programme:
        print('================')
        if typ=="throws":
            try:
               distinct_partitions_v1_no_start(data, n)
               assert True
            except:
               assert False
            continue

        result_exact = distinct_partitions_v1_no_start(data, n)
        result_list = tuple(distinct_partitions_v1_no_start(data, n))
        if converter is not None:
            expected = tuple(map( converter, expected ))

        if typ=="exact":
            for i,j in zip_longest(result_exact, expected):
                print(f"Hoping {i} == {j}")
                assert i==j
            continue

        if typ=="set":
            print(f"got {result_list}")
            print(f"expected {expected}")
            assert set(result_list) == set(expected)
            assert len(result_list) == len(expected)
            continue

        assert False
