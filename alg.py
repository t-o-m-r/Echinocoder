import numpy
import numpy as np
from itertools import pairwise
from collections import namedtuple
from tools import invert_perm
import hashlib

Eji = namedtuple("Eji", ["j", "i"])



def encode(data: np.ndarray, debug=False) -> np.ndarray:
    if debug:
        print(f"data is {data}")

    n,k = data.shape
    flattened_data = [ ( data[j][i], Eji(j,i) ) for j in range(n) for i in range(k) ]

    sorted_data = sorted( flattened_data, key = lambda x : -x[0])
    difference_data = [ (x[0]-y[0], x[1]) for x,y in pairwise(sorted_data) ]

    if debug:
        print(f"sorted flattened data is")
        [print(bit) for bit in sorted_data]

        print(f"difference data is")
        [print(bit) for bit in difference_data]

    # Create a vector to contain the encoding:
    encoding = np.zeros(2*n*k, dtype=np.float64)

    # Populate the last element of the encoding with the smallest element of the initial data
    encoding[-1] = sorted_data[-1][0]

    j_order = first_occurrences_numpy(np.asarray([ eji.j for _,eji in sorted_data ]))
    perm = invert_perm(j_order)

    if debug:
        print(f"the j's appear in this order {j_order}")
        print(f"inverse perm of j_order is  {perm}")

    canonical_difference_data = [ (delta, Eji(perm[j], i) ) for delta, (j,i) in difference_data ]

    if debug:
        print(f"canonical difference data is:")
        [print(bit) for bit in canonical_difference_data]

    cumulated_canonical_difference_data_1 = [ (delta, set([  eji for (_, eji) in canonical_difference_data[0:i+1] ]))  for i, (delta, _) in enumerate(canonical_difference_data)]
    if debug:
        print(f"cumulated canonical difference data (version 1) is:")
        [print(bit) for bit in cumulated_canonical_difference_data_1]

    # Calculate same thing but in a different representation
    cumulated_canonical_difference_data_2 = [ ( delta, eji_set_to_np_array(eji_set, n, k) ) for (delta, eji_set) in cumulated_canonical_difference_data_1 ]
    if debug:
        print(f"cumulated canonical difference data (version 2) is:")
        [print(bit) for bit in cumulated_canonical_difference_data_2]

    bigN = 2 * (n * k - 1) + 1
    difference_point_pairs = [(delta, eji_set_array_to_point_in_unit_hypercube(eji_set_array, bigN) ) for (delta, eji_set_array) in cumulated_canonical_difference_data_2]

    if debug:
        print(f")difference point pairs are:")
        [print(bit) for bit in difference_point_pairs]

    first_half_of_encoding = sum([delta * point for delta, point in difference_point_pairs]) + np.zeros(bigN)
    if debug:
        print(f"first bit of encoding is: {first_half_of_encoding}")

    encoding[:bigN] = first_half_of_encoding

    if debug:
        print(f"encoding is {encoding}")

    return encoding


def eji_set_to_np_array(eji_set, n, k):
    ans = np.zeros(shape=(n, k))
    for (j, i) in eji_set:
        ans[j][i] = 1
    return ans

def hash_to_128_bit_md5_int(md5):
    return int.from_bytes(md5.digest(), 'big') # 128 bits worth.

def hash_to_64_bit_reals_in_unit_interval(md5):
    """
    An md5 sum is 64 bits long so we get two such reals.
    N.B. This hash is of self._eji_counts only -- i.e. it ignores self._index.
    For the purposes to which this hash will be used, that is believed to be apporopriate.
    """

    x = hash_to_128_bit_md5_int(md5)
    bot_64_bits = x & 0xffFFffFFffFFffFF
    top_64_bits = x >> 64
    return np.float64(top_64_bits)/(1 << 64), np.float64(bot_64_bits)/(1 << 64)

def eji_set_array_to_point_in_unit_hypercube(eji_set_array, dimension):
    m = hashlib.md5()
    m.update(eji_set_array)
    ans = []
    for i in range(dimension):
        m.update(i.to_bytes())
        real_1, _ = hash_to_64_bit_reals_in_unit_interval(m) # TODO: make use of real_2 as well to save CPU
        ans.append(real_1)
    return np.asarray(ans)



def first_occurrences_numpy(x):
    _, indices = np.unique(x, return_index=True)  # Get the first occurrence indices
    sorted_indices = np.sort(indices)  # Sort these indices to maintain original order
    return x[sorted_indices]

def tost():
        import numpy as np

        calculated = first_occurrences_numpy(np.array([2, 3, 3, 4, 2, 1, 4, 0, 3, 2, 3, 4]))
        expected = numpy.array([2, 3, 4, 1, 0])
        np.testing.assert_array_equal(calculated, expected)

        calculated = first_occurrences_numpy(np.array([2,2,0,2,1,3,0,2,1,0,2,3,0,2,1,3,0,2,]))
        expected = numpy.array([2, 0, 1, 3])
        np.testing.assert_array_equal(calculated, expected)



def run_unit_tests():
    tost()

if __name__ == "__main__":
    run_unit_tests()

    input = np.asarray([[4,2],[-3,5],[8,9],[2,7]])
    output = encode(input)

    print("Encoding:")
    print(f"{input}")
    print("leads to:")
    print(f"{output}")
