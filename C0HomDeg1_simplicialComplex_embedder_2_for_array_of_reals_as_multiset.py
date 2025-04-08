# Based on OneNote -> Research -> Symmetries -> ERM - SIMPLEX EMBED #3 

import numpy as np
from itertools import pairwise
from collections import namedtuple
from tools import sort_np_array_rows_lexicographically, sort_each_np_array_column
from tools import ascending_data as ascending_data_from_tools
import hashlib
from dataclasses import dataclass, field
from typing import Self
from MultisetEmbedder import MultisetEmbedder
from typing import Any

Eji = namedtuple("Eji", ["j", "i"])

class Embedder(MultisetEmbedder):

    def embed_kOne(self, data: np.ndarray, debug=False) -> (np.ndarray, Any):
        metadata = None
        return MultisetEmbedder.embed_kOne_sorting(data), metadata

    def embed_generic(self, data: np.ndarray, debug=False) -> (np.ndarray, Any):
        assert MultisetEmbedder.is_generic_data(data) # Precondition
        if debug:
            print(f"data is {data}")
    
        n,k = data.shape

        """
        In some multi-line comments in this method we show intermediate
        values that would result from

                 data = [[ 4  2  3]
                         [-3  5  1]
                         [ 8  9  2]
                         [ 2  7  2]] 

        for which

                n=4,    k=3.

        as "data" describes  four vectors (n=4) in three dimensions (k=3).
        """

        # The following "ascending data" has the x-components in ascending order, the y-components in asceding order,
        # and so on. This has broken up the vectors.  I.e. the j=1 vector in ascending_data is not likely to
        # be any of the vectors in the input (unless the data was already sorted appropriately).
        # You can think of "ascending data" as representing all the things we want to encode EXCEPT the associations
        # which link every element of each vector up in the right way.
        ascending_data = ascending_data_from_tools(data)

        # We need to extract the smallest x, the smallest y, the smallest z (and so on) as these form some of the
        # outputs of the embedding.
        min_elements = ascending_data[0]
        if debug:
            print("min_elements is ")
            print(min_elements)
            """for our example data min_elements is [-3  2  1]"""

        flattened_data_separated_by_cpt = [ [ ( data[j][i], Eji(j,i) ) for j in range(n) ] for i in range(k) ]
        sorted_data_separated_by_cpt = [sorted(cpt, key = lambda x : -x[0]) for cpt in flattened_data_separated_by_cpt]
        if debug:
            print("sorted_data_separated_by_cpt is ")
            _ = [print(bit) for bit in sorted_data_separated_by_cpt]
            """ for our example data
            sorted_data_separated_by_cpt is 
    [(np.int64(8), Eji(j=2, i=0)), (np.int64(4), Eji(j=0, i=0)), (np.int64(2), Eji(j=3, i=0)), (np.int64(-3), Eji(j=1, i=0))]
    [(np.int64(9), Eji(j=2, i=1)), (np.int64(7), Eji(j=3, i=1)), (np.int64(5), Eji(j=1, i=1)), (np.int64(2), Eji(j=0, i=1))]
    [(np.int64(3), Eji(j=0, i=2)), (np.int64(2), Eji(j=2, i=2)), (np.int64(2), Eji(j=3, i=2)), (np.int64(1), Eji(j=1, i=2))]
            """

        difference_data_by_cpt = [[ (x[0]-y[0], x[1]) for x,y in pairwise(cpt) ] for cpt in sorted_data_separated_by_cpt]
        if debug:
            print("difference data is")
            _ = [print(bit) for bit in difference_data_by_cpt]
            """
            difference data is
    [(np.int64(4), Eji(j=2, i=0)), (np.int64(2), Eji(j=0, i=0)), (np.int64(5), Eji(j=3, i=0))]
    [(np.int64(2), Eji(j=2, i=1)), (np.int64(2), Eji(j=3, i=1)), (np.int64(3), Eji(j=1, i=1))]
    [(np.int64(1), Eji(j=0, i=2)), (np.int64(0), Eji(j=2, i=2)), (np.int64(1), Eji(j=3, i=2))]
            """
        difference_data_with_MSVs_by_cpt = [[
            (delta, Maximal_Simplex_Vertex(set([eji for (_, eji) in cpt[0:i + 1]]))) for i, (delta, _) in enumerate(cpt)]
            for cpt in difference_data_by_cpt]
        if debug:
            print("difference data with MSVs by cpt:")
            _ = [print(bit) for bit in difference_data_with_MSVs_by_cpt]
            """
            difference data with MSVs by cpt:
            [(np.int64(4), Maximal_Simplex_Vertex(_vertex_set={Eji(j=2, i=0)})),
               (np.int64(2), Maximal_Simplex_Vertex(_vertex_set={Eji(j=2, i=0), Eji(j=0, i=0)})),
                 (np.int64(5), Maximal_Simplex_Vertex(_vertex_set={Eji(j=2, i=0), Eji(j=3, i=0), Eji(j=0, i=0)}))]
            [(np.int64(2), Maximal_Simplex_Vertex(_vertex_set={Eji(j=2, i=1)})),
               (np.int64(2), Maximal_Simplex_Vertex(_vertex_set={Eji(j=3, i=1), Eji(j=2, i=1)})),
                 (np.int64(3), Maximal_Simplex_Vertex(_vertex_set={Eji(j=3, i=1), Eji(j=1, i=1), Eji(j=2, i=1)}))]
            [(np.int64(1), Maximal_Simplex_Vertex(_vertex_set={Eji(j=0, i=2)})), 
               (np.int64(0), Maximal_Simplex_Vertex(_vertex_set={Eji(j=0, i=2), Eji(j=2, i=2)})),
                 (np.int64(1), Maximal_Simplex_Vertex(_vertex_set={Eji(j=0, i=2), Eji(j=3, i=2), Eji(j=2, i=2)}))]
            """

        # Now flatten the difference data:
        difference_data_with_MSVs = [bit for cpt in difference_data_with_MSVs_by_cpt for bit in cpt]
        if debug:
            print("difference data with MSVs:")
            _ = [print(bit) for bit in difference_data_with_MSVs]
            """
            difference data with MSVs:
            (np.int64(4), Maximal_Simplex_Vertex(_vertex_set={Eji(j=2, i=0)}))
            (np.int64(2), Maximal_Simplex_Vertex(_vertex_set={Eji(j=2, i=0), Eji(j=0, i=0)}))
            (np.int64(5), Maximal_Simplex_Vertex(_vertex_set={Eji(j=2, i=0), Eji(j=3, i=0), Eji(j=0, i=0)}))
            (np.int64(2), Maximal_Simplex_Vertex(_vertex_set={Eji(j=2, i=1)}))
            (np.int64(2), Maximal_Simplex_Vertex(_vertex_set={Eji(j=3, i=1), Eji(j=2, i=1)}))
            (np.int64(3), Maximal_Simplex_Vertex(_vertex_set={Eji(j=3, i=1), Eji(j=1, i=1), Eji(j=2, i=1)}))
            (np.int64(1), Maximal_Simplex_Vertex(_vertex_set={Eji(j=0, i=2)}))
            (np.int64(0), Maximal_Simplex_Vertex(_vertex_set={Eji(j=0, i=2), Eji(j=2, i=2)}))
            (np.int64(1), Maximal_Simplex_Vertex(_vertex_set={Eji(j=0, i=2), Eji(j=3, i=2), Eji(j=2, i=2)}))
            """

        # Now begin process of barycentric subdivision.
        # First step is sorring the differences into numerical order:

        sorted_difference_data_with_MSVs = sorted(difference_data_with_MSVs, key=lambda x: -x[0] )
        if debug:
            print("sorted difference data with MSVs:")
            _ = [print(bit) for bit in sorted_difference_data_with_MSVs]
            """
            sorted difference data with MSVs:
            (np.int64(5), Maximal_Simplex_Vertex(_vertex_set={Eji(j=2, i=0), Eji(j=3, i=0), Eji(j=0, i=0)}))
            (np.int64(4), Maximal_Simplex_Vertex(_vertex_set={Eji(j=2, i=0)}))
            (np.int64(3), Maximal_Simplex_Vertex(_vertex_set={Eji(j=3, i=1), Eji(j=1, i=1), Eji(j=2, i=1)}))
            (np.int64(2), Maximal_Simplex_Vertex(_vertex_set={Eji(j=2, i=0), Eji(j=0, i=0)}))
            (np.int64(2), Maximal_Simplex_Vertex(_vertex_set={Eji(j=2, i=1)}))
            (np.int64(2), Maximal_Simplex_Vertex(_vertex_set={Eji(j=3, i=1), Eji(j=2, i=1)}))
            (np.int64(1), Maximal_Simplex_Vertex(_vertex_set={Eji(j=0, i=2)}))
            (np.int64(1), Maximal_Simplex_Vertex(_vertex_set={Eji(j=0, i=2), Eji(j=3, i=2), Eji(j=2, i=2)}))
            (np.int64(0), Maximal_Simplex_Vertex(_vertex_set={Eji(j=0, i=2), Eji(j=2, i=2)}))
            """

        deltas_in_current_order = [delta for delta, _ in sorted_difference_data_with_MSVs]
        msvs_in_current_order = [msv for _,msv in sorted_difference_data_with_MSVs]
    
        expected_number_of_vertices = n * k - k
        assert len(deltas_in_current_order) == expected_number_of_vertices
        assert len(msvs_in_current_order) == expected_number_of_vertices
    
        # The coordinates in the barycentric subdivided daughter simplex are differences of the current deltas,
        # which are up-weighted by a linear factor to (1) preserve their sum so that (2) normalised barycentric
        # coordinates transform into identically normalised barycentric coordinates, and so (3) this makes each
        # component approximately identically distributed.
        difference_data_in_subdivided_simplex = [ (  (i+1)*(deltas_in_current_order[i]-
                 (deltas_in_current_order[i+1] if i+1<expected_number_of_vertices else 0)),
                            Eji_LinComb(n, k, msvs_in_current_order[:i+1])) for i in range(expected_number_of_vertices)]
        if debug:
            print("difference data in barycentrically subdivided simplex:")
            _ = [print(bit) for bit in difference_data_in_subdivided_simplex]
            """
            difference data in barycentrically subdivided simplex:
(np.int64(1), Eji_LinComb(_index=np.uint16(1), _eji_counts=array([ [1, 0, 0],
                                                                   [0, 0, 0],
                                                                   [1, 0, 0],
                                                                   [1, 0, 0]], dtype=uint16)))
(np.int64(2), Eji_LinComb(_index=np.uint16(2), _eji_counts=array([ [1, 0, 0],
                                                                   [0, 0, 0],
                                                                   [2, 0, 0],
                                                                   [1, 0, 0]], dtype=uint16)))
(np.int64(3), Eji_LinComb(_index=np.uint16(3), _eji_counts=array([ [1, 0, 0],
                                                                   [0, 1, 0],
                                                                   [2, 1, 0],
                                                                   [1, 1, 0]], dtype=uint16)))
(np.int64(0), Eji_LinComb(_index=np.uint16(4), _eji_counts=array([ [2, 0, 0],
                                                                   [0, 1, 0],
                                                                   [3, 1, 0],
                                                                   [1, 1, 0]], dtype=uint16)))
(np.int64(0), Eji_LinComb(_index=np.uint16(5), _eji_counts=array([ [2, 0, 0],
                                                                   [0, 1, 0],
                                                                   [3, 2, 0],
                                                                   [1, 1, 0]], dtype=uint16)))
(np.int64(6), Eji_LinComb(_index=np.uint16(6), _eji_counts=array([ [2, 0, 0],
                                                                   [0, 1, 0],
                                                                   [3, 3, 0],
                                                                   [1, 2, 0]], dtype=uint16)))
(np.int64(0), Eji_LinComb(_index=np.uint16(7), _eji_counts=array([ [2, 0, 1],
                                                                   [0, 1, 0],
                                                                   [3, 3, 0],
                                                                   [1, 2, 0]], dtype=uint16)))
(np.int64(8), Eji_LinComb(_index=np.uint16(8), _eji_counts=array([ [2, 0, 2],
                                                                   [0, 1, 0],
                                                                   [3, 3, 1],
                                                                   [1, 2, 1]], dtype=uint16)))
(np.int64(0), Eji_LinComb(_index=np.uint16(9), _eji_counts=array([ [2, 0, 3],
                                                                   [0, 1, 0],
                                                                   [3, 3, 2],
                                                                   [1, 2, 1]], dtype=uint16)))
            """



        if debug:
            # Do a check: the following linear combination should be our original set:
            part_1_lin_comb = sum( coeff * (eji_lin_comb._eji_counts /eji_lin_comb._index)
                                    for coeff, eji_lin_comb in difference_data_in_subdivided_simplex )
            part_2_lin_comb = np.tile(min_elements, (n,1)) # Offsets due to min elements
            print(f"part_1_lin_comb is\n{part_1_lin_comb}")
            print(f"part_2_lin_comb is\n{part_2_lin_comb}")
            checksum = part_1_lin_comb+part_2_lin_comb
            print(f"checksum is\n{checksum}")
            print(f"while the original data (which should match checksum) is\n{data}")
            """
            part_1_lin_comb is
            [[ 7.  0.  2.]
             [ 0.  3.  0.]
             [11.  7.  1.]
             [ 5.  5.  1.]]
            part_2_lin_comb is
            [[-3  2  1]
             [-3  2  1]
             [-3  2  1]
             [-3  2  1]]
            checksum is
            [[ 4.  2.  3.]
             [-3.  5.  1.]
             [ 8.  9.  2.]
             [ 2.  7.  2.]]
            while the original data (which should match checksum) is
            [[ 4  2  3]
             [-3  5  1]
             [ 8  9  2]
             [ 2  7  2]]
             """
    
        canonical_difference_data = [(delta, msv.get_canonical_form()) for (delta, msv) in difference_data_in_subdivided_simplex]
        if debug:
            print("canonical difference data is:")
            _ = [print(bit) for bit in canonical_difference_data]
            """
            canonical difference data is:
(np.int64(1), Eji_LinComb(_index=np.uint16(1), _eji_counts=array([ [0, 0, 0],
                                                                   [1, 0, 0],
                                                                   [1, 0, 0],
                                                                   [1, 0, 0]], dtype=uint16)))
(np.int64(2), Eji_LinComb(_index=np.uint16(2), _eji_counts=array([ [0, 0, 0],
                                                                   [1, 0, 0],
                                                                   [1, 0, 0],
                                                                   [2, 0, 0]], dtype=uint16)))
(np.int64(3), Eji_LinComb(_index=np.uint16(3), _eji_counts=array([ [0, 1, 0],
                                                                   [1, 0, 0],
                                                                   [1, 1, 0],
                                                                   [2, 1, 0]], dtype=uint16)))
(np.int64(0), Eji_LinComb(_index=np.uint16(4), _eji_counts=array([ [0, 1, 0],
                                                                   [1, 1, 0],
                                                                   [2, 0, 0],
                                                                   [3, 1, 0]], dtype=uint16)))
(np.int64(0), Eji_LinComb(_index=np.uint16(5), _eji_counts=array([ [0, 1, 0],
                                                                   [1, 1, 0],
                                                                   [2, 0, 0],
                                                                   [3, 2, 0]], dtype=uint16)))
(np.int64(6), Eji_LinComb(_index=np.uint16(6), _eji_counts=array([ [0, 1, 0],
                                                                   [1, 2, 0],
                                                                   [2, 0, 0],
                                                                   [3, 3, 0]], dtype=uint16)))
(np.int64(0), Eji_LinComb(_index=np.uint16(7), _eji_counts=array([ [0, 1, 0],
                                                                   [1, 2, 0],
                                                                   [2, 0, 1],
                                                                   [3, 3, 0]], dtype=uint16)))
(np.int64(8), Eji_LinComb(_index=np.uint16(8), _eji_counts=array([ [0, 1, 0],
                                                                   [1, 2, 1],
                                                                   [2, 0, 2],
                                                                   [3, 3, 1]], dtype=uint16)))
(np.int64(0), Eji_LinComb(_index=np.uint16(9), _eji_counts=array([ [0, 1, 0],
                                                                   [1, 2, 1],
                                                                   [2, 0, 3],
                                                                   [3, 3, 2]], dtype=uint16)))
            """

        assert n*k - k == expected_number_of_vertices
        bigN = 2*(n - 1)*k + 1 # Size of the space into which the simplices are embedded.
        # bigN does not count any min elements, which would be extra.
        difference_point_pairs = [(delta, eji_lin_com.hash_to_point_in_unit_hypercube(bigN)) for (delta, eji_lin_com) in canonical_difference_data]
        if debug:
            print("difference point pairs are:")
            _ = [print(bit) for bit in difference_point_pairs]
    
        second_part_of_embedding = sum([delta * point for delta, point in difference_point_pairs]) + np.zeros(bigN)
        if debug:
            print(f"second bit of embedding is: {second_part_of_embedding}")
    
        # Create a vector to contain the embedding:
        length_of_embedding = self.size_from_n_k(n,k)
    
        assert length_of_embedding == bigN + k
        assert bigN == 2*(n - 1)*k + 1
        assert length_of_embedding == 2*n*k + 1 - k  # bigN + 2
        assert len(min_elements) == k

        embedding = np.zeros(length_of_embedding, dtype=np.float64)
    
        # Populate the first part of the embedding with the smallest elements of the initial data.
        embedding[:k] = min_elements
        # Populate other half of the embedding:
        embedding[k:bigN + k] = second_part_of_embedding

        if debug:
            print(f"embedding is {embedding}")
            print(f"embedding has length {length_of_embedding}")
    
        metadata = { "ascending_data" : ascending_data, "input_data" : data, }
        return embedding, metadata
    
    def size_from_n_k_generic(self, n: int, k: int) -> int:
        return 2*n*k + 1 - k
    
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
    calculated = np.array([2, 3, 4, 1, 0])
    expected = np.array([2, 3, 4, 1, 0])
    np.testing.assert_array_equal(calculated, expected)

def run_unit_tests():
    tost() # Renamed from test -> tost to avoid pycharm mis-detecting / mis-running unit tests!

if __name__ == "__main__":
    run_unit_tests()

    some_input = np.asarray([[4,2,3],[-3,5,1],[8,9,2],[2,7,2]])
    embedder = Embedder()
    output = embedder.embed(some_input, debug=True)

    print("Embedding:")
    print(f"{some_input}")
    print("leads to:")
    print(f"{output}")
