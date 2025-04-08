## General TODO:

In principle the Simplex1 and Simple2 algorithms could benefit from Using Eji_lin_combs everywhere instead of Eji's at the start and then Eji_lin_combs later on as they do at present.  This would likely be irrelevant for code run time (and only a trivial memory overhead) but it may simplify some of the checks one could do (such as always having ability to do linear combinations quickly to check that certain sums are preserved).

Factor the repeated assessory functions out of the two simplex encoders.

The brute_force_decoder should probably allow for floating tolerances and near matches -- at least some of the time.

The brute force decoder leaves the first column alone and then permutes the remaining columns. The saves some time, but not as much time as COULD potetntially be saved.  E.g. if the first column has all 4s in it, no perms of the second column (in a two column scenario) would ever be needed as they are not distinct.  E.g. permuting the second column here is a waste of time if the whole thing represents a multiset of tuples rather than a list of tuples.
[(4,1),
 (4,2),
 (4,7)]
 One step in the right direction would be not to freeze (arbitrarily) the first column, as we do at present, but instead to freeze the column with the most dissimilar elements. That would leave columnsa with repeats dominating the columns whih are subject to distinct_permuations.  This would not solve everything, though. Not sure how best to proceed.

Consider writing a tool to get all the simplices for a given (n,k) and see which ones need barycentric subdivision and which ones don't.  More than this, look to see how many vertices cause the ambiguity (if that's meaningful!!) ... i.e. we want to see if it would be possible to get away with just putting a single vertex at the centre of each simplex rather than full on barycentric subdivision.

## Item 1

Note to self: one could complexify the Bursar's idea.

## Item 2

20240211a : I have just noticed that the pairwise general (m,n) encoder is "trivially" redundant (contains unnecessary information). As the printout below shows,
the encoding of

[[-2  7  7]
 [-5  1  5]
 [ 1  0  9]]

 features -6 twice and 8 twice and 21 twice, since -6 is the sum of the x-components of the vectors, and 8 is the sum of the y-components, .... and each pairwise eencoding RE-encodes this information! 
 This presumably means there are many other redundancies that are harder to spot but are hidden within.

Size (m,n)=(3,3)
About to request coding for [[-2  7]
 [-5  1]
 [ 1  0]]
Size (m,n)=(2,3)
pes 6 nop 3
About to request coding for [[-2  7]
 [-5  5]
 [ 1  9]]
Size (m,n)=(2,3)
About to request coding for [[7 7]
 [1 5]
 [0 9]]
Size (m,n)=(2,3)
ENCH Cinf_numpy_polynomial_encoder_for_array_of_reals generates [  -6.    8.   -4.  -29.    3.  -37.   -6.   21. -140.  -96.  380. -270.
    8.   21. -136.  114. -378. -252.] from [[-2  7  7]
 [-5  1  5]
 [ 1  0  9]]


