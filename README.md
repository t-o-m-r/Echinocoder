This is a library for continuous encodings of multisets of vectors in $\mathbb{R}^m$.  
The number of elements in each multiset is denoted $n$.

In principle, all encoders expect only reals or real vectors and generate only reals.

The sorting encoider is efficient for any $n$ but only can work with $m=1$.
The polynomial encoders are efficient for $m=1$ or $m=2$ but in general have order $O(n m^2)$.
The (vanilla) busar encoder has order $O(m n^2)$.
The fair busar encoder has order $Binom(m+n,n)-1$.

Internally, some may use complex representations, however such routines should be considered private (unexposed) even if technically visible. This is to allow interface standardisation.


./test.py is the example/test script.

Note to self: one could complexify the Bursar's idea.
