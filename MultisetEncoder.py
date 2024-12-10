import numpy as np

class MultisetEncoder:
    """
    This is a base class for objects which encode length-n sets of k-vectors.

    Encoders are not necessarily embedders since encoders do not need to be injective.
    All embedders are encoders, however.

    Strictly speaking wecencode "multisets" not "sets" since the containers can hold repeated objects
    and retain knowledge of the number of repeats.  However, we are sometimes guity of 
    abbreviating "multiset" to just "set".

    The set to be encoded should be inputs as a 2D numpy array with shape (n,k).
    The order of the vectors within the numpy array can be arbitrary.
    E.g. to encode a multiset containing the 2-vectors (2,2), (4,5) and (1,2) one could call
    
        encode(np.asarray([[2,2], [4,5], [1,2]]))

    or

        encode(np.asarray([[4,5], [2,2], [1,2]]))

    and both should have the same output -- at least up to numerical precision. This leeway (permission to 
    have small deviations on account of floating point precision, rather than demanding bit-for-bit identical
    embeddings) is granted to implementations in order to allow them to be faster (sometimes) than would be the
    case if they were all required to canonicalise their input sets.  Someone wanting bit-for-bit identical 
    output under permutations of input vectors could easily sort their vectors (in any way) prior to using any 
    encoder.

    All encoders return one dimensional arrays of real floats.

    In principle, a given encoder can embed sets of different sizes n and or k.  However, 
    some encoders might wish to restrict themselves to certain fixed n or k at initialisation (e.g. if 
    an embedder were to need a significant amount of n and k dependent set-up cost that it wished to do
    once only).  Thus all encoders are expected to be able to tell callers what sizes of input they can and 
    cannot embed, and how long the possible embeddings will be.  Derived classes do this by implementing the method

        size_from_n_k(n: int, k, int) -> int:

    for which:
        * a return value of >=0 is the number of reals in an encoding if sets of size (n,k) are encodable, and
        * a return value of -1 indicates that embedding for that n and k is impossible.

    """

    def encode(self, data: np.ndarray, debug=False) -> np.ndarray:
        raise NotImplementedError()

    def size_from_array(self, data: np.ndarray) -> int:
        """
        This function returns the number of reals that the encoding would contain if the set represented by "data" were to be encoded. -1 is returned if data of the supplied type is not encodable by this encder.
        """
        n,k = data.shape
        return self.size_from_n_k(n,k)

    def size_from_n_k(self, n: int, k: int) -> int:
        """
        This function returns the number of reals that the encoding would contain if a set containing n "k-vectors" were to be encoded. Derived classes implmenting this method should return -1 if they are not able to encode sets for that n and k.
        """
        raise NotImplementedError()
