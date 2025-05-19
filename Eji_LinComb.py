import hashlib
import numpy as np
from typing import Self
from dataclasses import dataclass
from injection import hash_to_64_bit_reals_in_unit_interval
from Maximal_Simplex_Vertex import Maximal_Simplex_Vertex
from tools import sort_np_array_rows_lexicographically


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

