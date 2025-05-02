#!/usr/bin/env python

"""
We work with (multu)sets of $n$ vectors in $k$-dimensions.

Encoding dots are done with $m$ directions: $D=\{\vec d_1, \vec d_2, ... , \vec d_m\}$

There are $M$ vectors ($M=ceil(m/(k-1)$) which are orthogonal to the vectors in $D$ (these are the $M$ bad-bats): $B=\{\vec q_1, \vec q_2, \cdots, \vec q_M\}$. E.g. $\vec q_1 \cdot m_i = 0$ for all $i\in \{ 1, 2, \cdots, k-1 \}$.

The (multi)sets $E$ and $O$ have even and odd sums of the elements of $B$:

$E=\{ \vec 0, \vec q_1 + \vec q_2, \cdots \}$
$O=\{  \vec q_1, \vec q_2, \cdots, \vec q_2 + \vec q_5 + \vec q_9, \cdots \}$

We can represent elements of E and O (and their later trimmed version) by a set of dimension-M vectors (one for each free parameter) whose components show us how much of each cpt is to be used.

E.g. if the coefficients are lambda_1, lambda_2, ... \lambda_M which are buried inside each of the q_i .... i.e.:

     \vec q_1 = \lambda_1(parameter_1) \vec Q_1
     \vec q_2 = \lambda_2(parameter_4) \vec Q_2
     \vec q_3 = \lambda_3(parameter 1) \vec Q_3
     \vec q_4 = \lambda_4(parameter 1) \vec Q_4
     \vec q_5 = \lambda_5(parameter 2) \vec Q_5
     \vdots

then the vector

    5 q_1 + 2 q_2 + 3 q_3 - 8 q_4 + 9 q_5

would be represented by

    v_{param 1} = [  5,  0,  3, -8,  0, ... ]
    v_{param 2} = [  0,  0,  0,  0,  9, ... ]
    v_{param 3} = [  0,  0,  0,  0,  0, ... ]
    v_{param 4} = [  0,  2,  0,  0,  0, ... ]
    v_{param 5} = [  0,  0,  0,  0,  0, ... ]
    \vdots

which we could put into a matrix V_{ij}, with index i being the parameter, and index j being the occurrence count of vec q_j.

With such a format in mind, we could identify whether two different linear combinations(A and B) could be made equal by checking whether their difference (A-B) has at least k+1 non-zero rows ... and in that case 

"""

import numpy as np
from itertools import combinations

# Set small dimensions for illustration
t, M, k = 4, 3, 1

# Create dummy data for n
# Shape: (2, t, M) => (2, 4, 3)
# A = n[0], B = n[1]
n = np.array([
    [  # A: Two example matrices of shape (4,3)
        [ [1, 0, 0],
          [0, 1, 0],
          [0, 0, 1],
          [1, 1, 1] ],

        [ [1, 2, 3],
          [4, 5, 6],
          [7, 8, 9],
          [0, 0, 0] ]
    ],
    [  # B: Two example matrices of shape (4,3)
        [ [1, 0, 0],
          [0, 0, 0],
          [0, 0, 1],
          [1, 1, 0] ],

        [ [1, 1, 1],
          [1, 1, 1],
          [1, 1, 1],
          [0, 0, 0] ]
    ]
])

# Transpose to get shape (2, 2, 4, 3) (2 matrices in A and B)
n = np.transpose(n, (0, 2, 3, 1))  # Now n has shape (2, 2, 4, 3)
n = n.reshape(2, 2, 4, 3)  # (2 groups: A and B) x (2 matrices each) x (4 rows) x (3 columns)

# Now extract matrices from A and B by indexing
n = n[:, :, :, :]  # Already shaped properly

# Generator function as defined earlier
def generate_variants(n, k):
    A = n[0]  # shape (num_A, t, M)
    B = n[1]  # shape (num_B, t, M)

    for a in A:
        for b in B:
            d = a - b  # shape (t, M)
            non_zero_row_indices = np.where(~np.all(d == 0, axis=1))[0]

            if len(non_zero_row_indices) < k + 1:
                continue

            for rows_to_keep in combinations(non_zero_row_indices, k + 1):
                variant = np.zeros_like(d)
                variant[list(rows_to_keep)] = d[list(rows_to_keep)]
                yield variant

# Run and print results
for i, variant in enumerate(generate_variants(n, k)):
    print(f"Variant {i+1}:\n{variant}\n")

