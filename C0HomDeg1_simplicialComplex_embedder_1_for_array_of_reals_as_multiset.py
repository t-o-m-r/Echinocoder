import numpy as np
from itertools import pairwise
from collections import namedtuple
from tools import invert_perm, sort_np_array_rows_lexicographically
import hashlib
from dataclasses import dataclass, field
from typing import Self
from MultisetEmbedder import MultisetEmbedder

Eji = namedtuple("Eji", ["j", "i"])

class Embedder(MultisetEmbedder):

    def embed_kOne(self, data: np.ndarray, debug=False) -> np.ndarray:
        return MultisetEmbedder.embed_kOne_sorting(data)



    def embed_generic(self, data: np.ndarray, debug=False) -> np.ndarray:
        assert MultisetEmbedder.is_generic_data(data) # Precondition
        if debug:
            print(f"data is {data}")
    
        n,k = data.shape
        flattened_data = [ ( data[j][i], Eji(j,i) ) for j in range(n) for i in range(k) ]
        sorted_data = sorted( flattened_data, key = lambda x : -x[0])
    
        if debug:
            print("sorted flattened data is")
            _ = [print(bit) for bit in sorted_data]
    
        min_element = sorted_data[-1][0]
        max_element = sorted_data[0][0]
    
        difference_data = [ (x[0]-y[0], x[1]) for x,y in pairwise(sorted_data) ]
    
        if debug:
            print("difference data is")
            _ = [print(bit) for bit in difference_data]
    
        difference_data_with_MSVs = [
            (delta, Maximal_Simplex_Vertex(set([eji for (_, eji) in difference_data[0:i + 1]]))) for i, (delta, _) in enumerate(difference_data)]
    
        if debug:
            print("difference data with MSVs:")
            _ = [print(bit) for bit in difference_data_with_MSVs]
    
        sorted_difference_data_with_MSVs = sorted(difference_data_with_MSVs, key=lambda x: -x[0] )
        if debug:
            print("sorted difference data with MSVs:")
            _ = [print(bit) for bit in sorted_difference_data_with_MSVs]
    
        # Barycentrically subdivide:
        deltas_in_current_order = [delta for delta, _ in sorted_difference_data_with_MSVs]
        msvs_in_current_order = [msv for _,msv in sorted_difference_data_with_MSVs]
    
        expected_number_of_vertices = n * k - 1
        assert len(deltas_in_current_order) == expected_number_of_vertices
        assert len(msvs_in_current_order) == expected_number_of_vertices
    
    
        # The coordinates in the barycentric subdivided daughter simplex are differences of the current deltas,
        # which are up-weighted by a linear factor to make them approximately identically distributed.
        difference_data_in_subdivided_simplex = [ (  (i+1)*(deltas_in_current_order[i]-(deltas_in_current_order[i+1] if i+1<expected_number_of_vertices else 0)),  Eji_LinComb(n, k, msvs_in_current_order[:i+1])) for i in range(expected_number_of_vertices)]
    
        if debug:
            print("difference data in Barycentrically subdivided simplex:")
            _ = [print(bit) for bit in difference_data_in_subdivided_simplex]
    
        canonical_difference_data = [(delta, msv.get_canonical_form()) for (delta, msv) in difference_data_in_subdivided_simplex]
        if debug:
            print("canonical difference data is:")
            _ = [print(bit) for bit in canonical_difference_data]
    
        #j_order = first_occurrences_numpy(np.asarray([ eji.j for _,eji in sorted_data ]))
        #perm = invert_perm(j_order)
    
        #if debug:
        #    print(f"the j's appear in this order {j_order}")
        #    print(f"inverse perm of j_order is  {perm}")
    
        #canonical_difference_data = [ (delta, Eji(perm[j], i) ) for delta, (j,i) in difference_data ]
    
        #if debug:
        #    print(f"canonical difference data is:")
        #    [print(bit) for bit in canonical_difference_data]
    
        #cumulated_canonical_difference_data_1 = [ (delta, Maximal_Simplex_Vertex(set([  eji for (_, eji) in canonical_difference_data[0:i+1] ])))  for i, (delta, _) in enumerate(canonical_difference_data)]
        #if debug:
        #    print(f"cumulated canonical difference data (version 1) is:")
        #    [print(bit) for bit in cumulated_canonical_difference_data_1]
    
        # HERE
    
    
        # Calculate same thing but in a different representation
        #cumulated_canonical_difference_data_2 = [ ( delta, eji_set_to_np_array(eji_set, n, k) ) for (delta, eji_set) in cumulated_canonical_difference_data_1 ]
        #if debug:
        #    print(f"cumulated canonical difference data (version 2) is:")
        #    [print(bit) for bit in cumulated_canonical_difference_data_2]
    
        assert n*k - 1 == expected_number_of_vertices
        bigN = 2 * (n*k - 1) + 1 # Size of the space into which the simplices are embedded.
        # bigN does not count any min and max elements, which would be extra.
        difference_point_pairs = [(delta, eji_lin_com.hash_to_point_in_unit_hypercube(bigN)) for (delta, eji_lin_com) in canonical_difference_data]
        if debug:
            print("difference point pairs are:")
            _ = [print(bit) for bit in difference_point_pairs]
    
        first_half_of_embedding = sum([delta * point for delta, point in difference_point_pairs]) + np.zeros(bigN)
        if debug:
            print(f"first bit of embedding is: {first_half_of_embedding}")
    
    
    
        # Create a vector to contain the embedding:
        length_of_embedding = self.size_from_n_k(n,k)
    
        assert length_of_embedding == bigN + 2
        assert bigN == 2 * (n*k - 1) + 1
        assert length_of_embedding == 2 * (n*k - 1) + 1 + 2  # bigN + 2
        assert length_of_embedding == 2 * n * k + 1 # bigN + 2 expanded out.
    
        embedding = np.zeros(length_of_embedding, dtype=np.float64) # +2 for max_element and min_element .... TODO don't always need max_element!
    
        # Populate first half of the embedding:
        embedding[:bigN] = first_half_of_embedding
        # Populate the last element of the embedding with the smallest element of the initial data.
        embedding[-1] = min_element # TODO: Don't do this if nk==0, as nothing to record in that case.
        # Populate the second last element of the embedding with the largest element of the initial data.
        embedding[-2] = max_element # TODO: Don't do this if nk<=1, as min_element is enough in that case.
    
        if debug:
            print(f"embedding is {embedding}")
            print(f"embedding has length {length_of_embedding}")
    
        return embedding
    
    def size_from_n_k_generic(self, n: int, k: int) -> int:
        return 2*n*k + 1
    
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

@dataclass
class Maximal_Simplex_Vertex:
    _vertex_set: set[Eji] = field(default_factory=set)

    def __len__(self) -> int:
        return len(self._vertex_set)

    def __iter__(self):
        return iter(self._vertex_set)

    def get_canonical_form(self):
        """Mod out by Sn for this single vertex, ignoring any others."""
        # Method: sort the Eji by the i index, then populate the j's in order.
        sorted_eji_list = sorted(list(self._vertex_set), key=lambda eji: eji.i)
        renumbered_eji_list = [ Eji(j=j, i=eji.i) for j,eji in enumerate(sorted_eji_list)]
        return Maximal_Simplex_Vertex(set(renumbered_eji_list))

    def check_valid(self):
        # every j index in the set must appear at most once
        j_vals = { eji.j for eji in self._vertex_set }
        assert len(j_vals) == len(self._vertex_set)

    def get_permuted_by(self, perm):
        return Maximal_Simplex_Vertex({Eji(perm[eji.j], eji.i) for eji in self._vertex_set})

@dataclass
class Eji_LinComb:
    INT_TYPE = np.uint16 # uint16 should be enough as the eij_counts will not exceed n*k which can therefore reach 65535

    _index : INT_TYPE
    _eji_counts : np.ndarray

    def index(self) -> INT_TYPE:
        """How many things were added together to make this Linear Combination."""
        return self._index

    def hash_to_point_in_unit_hypercube(self, dimension):
        m = hashlib.md5()
        m.update(self._eji_counts)
        #print("self._index is")
        #print(self._index)
        # self._index.nbytes returns the number of bytes in self._index as self._index is of a numpy type which provides this
        m.update(np.array([self._index])) # creating an array with a single element is a kludge to work around difficulties of using to_bytes on np_integers of unknown size
        ans = []
        for i in range(dimension):
            m.update(i.to_bytes(8))  # TODO: This 8 says 8 byte integers
            real_1, _ = hash_to_64_bit_reals_in_unit_interval(m)  # TODO: make use of real_2 as well to save CPU
            ans.append(real_1)
        return np.asarray(ans)

    def __init__(self, n: int, k: int, list_of_Maximal_Simplex_Vertices: list[Maximal_Simplex_Vertex] | None = None):
        self._index = Eji_LinComb.INT_TYPE(0)
        self._eji_counts = np.zeros((n, k), dtype=Eji_LinComb.INT_TYPE, order='C')
        if list_of_Maximal_Simplex_Vertices:
            for msv in list_of_Maximal_Simplex_Vertices: self.add(msv)

    def _setup_debug(self, index: int, eji_counts: np.ndarray): # Really just for unit tests. Don't use in main alg code.
        self._index = Eji_LinComb.INT_TYPE(index)
        self._eji_counts = np.asarray(eji_counts, dtype=Eji_LinComb.INT_TYPE, order='C')

    def add(self, msv: Maximal_Simplex_Vertex):
        self._index += 1
        for j, i in msv: self._eji_counts[j, i] += 1


    def __eq__(self, other: Self):
        return self._index == other._index and np.array_equal(self._eji_counts, other._eji_counts)

    def __ne__(self, other: Self):
        return not self.__eq__(other)

    def get_canonical_form(self) -> Self:
        ans = Eji_LinComb.__new__(Eji_LinComb)
        ans._index = self._index
        ans._eji_counts = sort_np_array_rows_lexicographically(self._eji_counts)
        return ans



def tost(): # Renamed from test -> tost to avoid pycharm mis-detecting / mis-running unit tests!
    calculated = first_occurrences_numpy(np.array([2, 3, 3, 4, 2, 1, 4, 0, 3, 2, 3, 4]))
    expected = np.array([2, 3, 4, 1, 0])
    np.testing.assert_array_equal(calculated, expected)

    calculated = first_occurrences_numpy(np.array([2,2,0,2,1,3,0,2,1,0,2,3,0,2,1,3,0,2,]))
    expected = np.array([2, 0, 1, 3])
    np.testing.assert_array_equal(calculated, expected)



def run_unit_tests():
    tost() # Renamed from test -> tost to avoid pycharm mis-detecting / mis-running unit tests!

if __name__ == "__main__":
    run_unit_tests()

    some_input = np.asarray([[4,2],[-3,5],[8,9],[2,7]])
    embedder = Embedder()
    output = embedder.embed(some_input, debug=True)

    print("Embedding:")
    print(f"{some_input}")
    print("leads to:")
    print(f"{output}")
