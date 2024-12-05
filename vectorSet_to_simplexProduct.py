#!/usr/bin/env python3

from sys import version_info
import numpy
import tools
from typing import Self
from itertools import pairwise
import numpy as np
import unittest
from dataclasses import dataclass, field
from typing import Union
import hashlib

def encode(data: Union[np.ndarray, 'Position_within_Simplex_Product'],
           use_n2k2_optimisation=False, input_is_in_DeltakToN=False) -> np.ndarray:
    """
    By default, this function takes as input a length-n list of k-vectors (i.e. points in (R^k)^n)
    to encode in a perutation invariant way in R^(2nk+1).

    E.g. to encode the three two-vectors [1,2], [4,2] and [2,0] one might supply it with

        data = np.array([[1,2], [4,2], [2,0]]).

    However, if the flag "input_is_in_DkToN" is set to true, or if the input is
    detected as being of type "Position_within_Simplex_Product", the input is assumed to be already mapped into
    simplex coordinates for a space which is an n-fold product of k-simplices.  This feature is to allow
    simple unit tests.

    Args:
        data in  (R^k)^n (or in  (Delta^k)^n in some cases)
        use_n2k2_optimisation = a flag to request interpretation as (Delta^k)^n

    Returns:
        embedding in R^(nk+1)
    """

def vector_to_simplex_point(vec):
    k = len(vec)
    vec = np.array(vec)
    return 1.0/(k*(1.0+np.power(2.0,vec))) # TODO: This somewhat crude parameterisation does not use the WHOLE
    # of the simplex -- so it's a bit wasteful. It also has terrible dynamic range problems and even unit issues.
    # Might want to address all of these points with a better mapping.

def vectors_to_delta(vecs : np.ndarray, method):
    """
    The type hints intend to suggest that this will be called with a numpy array (intended to be 2D)
    so it ought to be guaranteed that all vectors within in the array have the same length.  Nonetheless,
    there is currently a test below that checks this just in case people supply a list of lists. If that
    check causes slowness, then it could be removed and people could be just forced to send in numpy arrays.
    """
    n=len(vecs)
    if n==0:
        # The list is empty, so return a null list:
        return Position_within_Simplex_Product([list() for i in range(n)])
    # "vecs" is not empty -- so the set of vectors contains at least one vector -- whose size we can query..
    k = len(vecs[0])
    delta = np.zeros((n,k),)
    for j in range(n):
        vec = vecs[j]
        simplex_point = vector_to_simplex_point(vec)
        k_this = len(vec)
        if k != k_this:
            raise Exception("Vectors supplied to vectors_to_delta are not all the same dimension!")
        for i in range(k):
            delta[j,i]=simplex_point[i]
    return Position_within_Simplex_Product(delta)

