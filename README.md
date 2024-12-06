# Echinocoder

This is a library contains functions which are able to perform:

  * Embeddings of real [symmetric product spaces](https://en.wikipedia.org/wiki/Symmetric_product_(topology)), $SP^n(\mathbb R^m)$.  These are continuous bijective mappings of multisets of size $n$ containing vectors in $\mathbb{R}^m$ into $\mathbb R^k$ for some $k$.

  * Embeddings of $\mathbb R^m$ in which $\vec x\in\mathbb R^n$ is identified with $-\vec x$.  I am not sure what these are really supposed to be called. This libarary currently calls them [real projective spaces](https://en.wikipedia.org/wiki/Real_projective_space) but that might be an abuse of terminology.

Most embedders work only reals or real vectors and generate only real embeddings as that's the whole purpose of the libarary. However, some embedders will accept complex numbers as inputs and can generate complex numbers as outputs.  Where this is the case it is not always documented. Some of the embedders which can process complex inputs and outputs are nonetheless used (in Complex mode) as steps in the implementation of other embedders.  The capacity for some embedders to process complex numbers such routines should be considered private (unexposed) even if technically visible. This is to allow interface standardisation.

## $SP^n(\mathbb R^m)$ -- i.e. multiset embedders:

* The [Simplicial Complex](https://en.wikipedia.org/wiki/Simplicial_complex) embedder works for any $n$ and $m$ and embeds into $2 n m+1$ reals. ([embedder source](C0HomDeg1_simplicialComplex_embedder_1_for_array_of_reals_as_multiset.py)) 
* The sorting embedder is efficient (i.e. embeds into $nm$ reals) for any $n$ but only can work with $m=1$. ([embedder source](C0_sorting_embedder_for_list_of_reals_as_multiset.py))
* The polynomial embedders are efficient (i.e. embed into $nm$ reals) for $m=1$ or $m=2$ but in general have order $O(n m^2)$. (embedder sources ([for multisets of vectors](Cinf_numpy_polynomial_embedder_for_array_of_reals_as_multiset.py)) and ([for multisets of reals](Cinf_numpy_polynomial_embedder_for_list_of_reals_as_multiset.py)))
* The (vanilla) busar embedder has order $O(m n^2)$.  Indeed, the exact order is  $ORDER(m,n) = n + (m-1) n (n+1)/2$. ([embedder source](Cinf_sympy_bursar_embedder_for_array_of_reals_as_multiset.py))
* The 'even' busar embedder has order $Binom(m+n,n)-1$. While this embedder is very inefficient, it does not treat any components in the $m$-space differently than any other.  ([embedder source](Cinf_sympy_bursar_embedder_for_array_of_reals_as_multiset.py))
* If one were to use the busar embedder when $m\ge n$ and the polynomial embedder when $n\ge m$ then one would have, in effect, a single method of order $O((mn)^{\frac 3 2})$. [Check this statement! It is probably not true!]

## Obsolete/Retired/Historical embedders:
* This early (nonlinear) [Simplicial Complex](https://en.wikipedia.org/wiki/Simplicial_complex) embedder works for any $n$ and $m$ and embeds into $4 n m+1$ reals. ([embedder source](Historical/C0_numpy_simplicialComplex_embedder_for_array_of_reals_as_multiset.py))  In principle it could embed into just $2 n m + 1$ reals.  However, and implementation choice which is expected to make the outputs more stable leads to the number of outputs being $4 n m + 1$ instead.

## What this library is calling $RP(\mathbb R^m)$ ([real projective space](https://en.wikipedia.org/wiki/Real_projective_space)) embedders:

* By setting $n=2$ and embedding the multiset $\left\\{\vec x,-\vec x\right\\}$ with $\vec x$ in $R^m$ one can use the bursar embedder to embed something this library calls $RP^m$ (which is possibly an abuse of the notation for real projective space of order $m$).  This $RP^m$ embedding would (for the (vanilla) bursar embedder) naively therefore be of size $2+(m-1)2(2+1)/2 = 2+3(m-1)$.  However, since all $m$ terms of order 1 in the auxiliary variable $y$ always disappear for multisets of this sort, the coefficients of those terms do not need to be recorded. This leaves only $2m-1$ reals needing to be recorded in the embedding for $RP^m$.  A method named [Cinf_numpy_regular_embedder_for_list_of_realsOrComplex_as_realOrComplexprojectivespace](Cinf_numpy_regular_embedder_for_list_of_realsOrComplex_as_realOrComplexprojectivespace.py) implements this method. It is order $2n-1$ when $n>0$.
* A small optimisation of the above method (implemented as [Cinf_numpy_complexPacked_embedder_for_list_of_reals_as_realprojectivespace](Cinf_numpy_complexPacked_embedder_for_list_of_reals_as_realprojectivespace.py))  reduces the by one when $n>0$ and $n$ is even.


## Testing/examples

[example.py](example.py) is a simple example showing how one of the embedders could be used.

[test.py](test.py) excercises some of the embedders. If they all work the script should end with a message saying something like 

"----------------------------------------------------------------------
Ran 1 test in 0.165s

OK
"

[test_PKH_alg.py](test_PKH_alg.py) contains another set of unit tests, mainly intended to exercise the Simplicial Complex embedder.

## References:

Neither the [Don Davis papers](https://www.lehigh.edu/~dmd1/toppapers.html) nor [Don Davis immersion list](https://www.lehigh.edu/~dmd1/imms.html) has been used to create this library. Both may, however, be useful references and sources of other references, so some are cached in the [DOCS](DOCS) directory.
