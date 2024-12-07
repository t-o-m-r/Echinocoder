import numpy as np
import inspect

class LineNo:
    def __str__(self):
        return str(inspect.currentframe().f_back.f_lineno)

__line__ = LineNo()

def expand_complex_to_real_pairs(np_array):
    """
    This function expands numpy arrays of complex numbers into arrays which are twice as long but which have real parts separated from complex parts.
    E.g.:   [3+4i, 4+2i] -> [3, 4, 4, 2]
    Its inverse is "real_pairs_to_complex_zip".
    """

    a = np_array.real
    b = np_array.imag
    c = np.empty((a.size+b.size,), dtype=a.dtype)
    c[0::2] = a
    c[1::2] = b
    return c

def real_pairs_to_complex_zip(np_array):
    """
    This function zips adjacent reals in an array of length n into complex numbers in an array of length floor(n/2).
    E.g.:  [3, 4, 4, 2] -> [3+4i, 4+2i]
    or:    [3, 4, 4,  ] -> [3+4i, 4   ]
    Its inverse is "expand_complex_to_real_pairs".
    """
    reals = np_array[0::2]
    imags = np_array[1::2]
    if len(imags)<len(reals):
        imags = np.append(imags, [0])
    print("input ",np_array)
    print("reals ",reals)
    print("images ",imags)
    return reals+1j*imags

def invert_perm(perm):
    """given [3, 0, 1, 2] should generate [1, 2, 3, 0]"""
    return sorted(range(len(perm)), key=perm.__getitem__)

def sort_each_np_array_row(array: np.ndarray) -> np.ndarray:
    """
    Sort the elements of each row into numerical order.
    For example:
                  np.array([[1, 0, 2],
                            [0, 5, 2],
                            [3, 0, 8]])
    sorts to:     
                  np.array([[0, 1, 2],
                            [0, 2, 5],
                            [0, 3, 8]])
    """
    return np.sort(array)

def sort_np_array_rows_lexicographically(array: np.ndarray) -> np.ndarray:
    """
    Permutes rows of a numpy array (individual rows are preserved) so that the rows end up in lexicographical order.
    E.g.:
                  np.array([[1, 0, 2],
                            [0, 5, 2],
                            [3, 0, 8]])
    sorts to:     
                  np.array([[0, 5, 2],
                            [1, 0, 2],
                            [3, 0, 8]])
    """
    return array[np.lexsort(array.T[::-1])]

