#!/usr/bin/env python 

"""
The purpose of this script is to provide a method that will attempt a brute force decoding of any array encoder which outputs "input_data" within its metadata assuming that all it has to do is re-order ascending_data(input_data).

Note that this is not a true decoder, as it does not confirm that the encoding could generate the ascending_data. However, any encoder could pacakge ascending_data alongside any other encoding without increasing its order beyond (nk) if already (nk) .... 
"""

import numpy as np
import C0HomDeg1_simplicialComplex_embedder_2_for_array_of_reals_as_multiset as simplex2
import tools

embedder = simplex2.Embedder()

data = np.array([[1,2,3],
                 [4,-5,6],
                 [-7,8,9]])

encoding, (n,k), metadata = embedder.embed(data)

print(f"data = {data}")
print(f"ecoding = {encoding}")
print(f"metadata = {metadata}")

def canonical_form(data):
    return tools.sort_np_array_rows_lexicographically(data)

# See if we can attempt brute force decode:
if "ascending_data" in metadata:
    # yes, it seems we can try
    ascending_data = metadata["ascending_data"]
    print(f"ascending data = {ascending_data}")

    if "input_data" in metadata:
        assert np.equal(ascending_data, tools.ascending_data(metadata["input_data"])).all()

    bad_matches = set()
    good_matches = set()
    canonical = canonical_form(data)

    for hypothesis in tools.permute_columns_except_first(ascending_data):
        #print("Might be:")
        #print(hypothesis)
        encoding_of_hypothesis, _, _ = embedder.embed(hypothesis)

        if (encoding_of_hypothesis == encoding).all(): # Ought to worry about rounding
            print("\n\nWe found an exact encoding match between")
            print(data)
            print("and")
            print(hypothesis)
            canonical_hypothesis = canonical_form(hypothesis)

            ch = tuple(tuple(i) for i in canonical_hypothesis.tolist())

            if (canonical == canonical_hypothesis).all():
                good_matches.add(ch)
                print("This is a GOOD DESIRED match.")
            else:
                bad_matches.add(ch)
                print("This match is BAD.")
            print(f"So far: #GOOD={len(good_matches)} and #BAD={len(bad_matches)}.") 

    print(f"At end: GOOD={good_matches} and BAD={bad_matches}.") 
    print(f"At end: #GOOD={len(good_matches)} and #BAD={len(bad_matches)}.") 

    assert len(bad_matches) == 0 
    assert len(good_matches) == 1



        







