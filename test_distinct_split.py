from distinct_split import distinct_split

def test_distinct_split():

    def tuple_of_strings_converter(tup_of_strings):
        return tuple( ( tuple(ch for ch in s) for s in tup_of_strings)  )

    test_programme = [
       ( "make", 5, tuple(), # There are no valid splits
                      tuple_of_strings_converter
        ),
       ( "make", 2, (
                      ("ma", "ke"), # Note that the other way around ("ke", "ma") appears later too. That is intentional.
                      ("mk", "ae"),
                      ("me", "ak"),
                      ("ak", "me"),
                      ("ae", "mk"),
                      ("ke", "ma"),
                     ), tuple_of_strings_converter
        ),
       ( "make", 4, (
                      ("make", ""), 
                     ), tuple_of_strings_converter
        ),
       ( "make", 0, (
                      ("", "make"), 
                     ), tuple_of_strings_converter
        ),
       ( "happy", 2, (
                      ("ha", "ppy"),
                      ("hp", "apy"),
                      ("hy", "app"),
                      ("ap", "hpy"),
                      ("ay", "hpp"),
                      ("pp", "hay"),
                      ("py", "hap"),
                     ), tuple_of_strings_converter
        ),
    ]
  
    
    for data, n, expected, converter in test_programme:
       result_list = distinct_split(data, n)
       print(f"Initially got {result_list}")
       result_list = tuple(result_list)
       if converter is not None:
           expected = tuple(map( converter, expected ))

       print(f"got {result_list}")
       print(f"expected {expected}")
       assert set(result_list) == set(expected)
       assert len(result_list) == len(expected)
