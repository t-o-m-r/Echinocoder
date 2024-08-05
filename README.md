This is a library for continuous bijective encodings of multisets of vectors in $\mathbb{R}^m$.  
The number of elements of the multiset is denoted $n$.

In principle, all encoders expect only reals or real vectors and generate only reals.

* The sorting encoider is efficient for any $n$ but only can work with $m=1$.
* The polynomial encoders are efficient for $m=1$ or $m=2$ but in general have order $O(n m^2)$.
* The (vanilla) busar encoder has order $O(m n^2)$.  Indeed, the exact order is  $ORDER(m,n) = n + (m-1)*n*(n+1)/2$.
* The 'even' busar encoder has order $Binom(m+n,n)-1$.
* Note that by setting $n=2$ and encoding the multiset $\left\\{\vec x,-\vec x\right\\}$ with $\vec x$ in $R^m$ one can use the bursar encoder to encode $RP^m$ (the real projective plane of order $m$).  This $RP^m$ embedding would (for the (vanilla) bursar encoder) naively therefore be of order $2+(m-1)*2*(2+1)/2 = 2+3(m-1)$.  However, since all the terms of order 1 in the auxiliary variable $y$ always disappear, they do not need to be recorded. This removes $m$ terms, leaving only $2m-1$ needing to be recorded in the encoding for $RP^m$.  There is not currently a method to exploit this, but one should be added!   ]
* If one were to use the busar encoder when $m\ge n$ and the polynomial encoder when $n\ge m$ then one would have, in effect, a single method of order $O((mn)^{\frac 3 2})$.

Internally, some may use complex representations, however such routines should be considered private (unexposed) even if technically visible. This is to allow interface standardisation.


./test.py is the example/test script.

Note to self: one could complexify the Bursar's idea.
