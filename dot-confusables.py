#!/usr/bin/python

"""
We work with (multu)sets of $n$ vectors in $k$-dimensions.

Encoding dots are done with $m$ directions: $D=\{\vec d_1, \vec d_2, ... , \vec d_m\}$

There are $M$ vectors ($M=ceil(m/(k-1)$) which are orthogonal to the vectors in $D$ (these are the $M$ bad-bats): $B=\{\vec q_1, \vec q_2, \cdots, \vec q_M\}$. E.g. $\vec q_1 \cdot m_i = 0$ for all $i\in \{ 1, 2, \cdots, k-1 \}$.

The (multi)sets $E$ and $O$ have even and odd sums of the elements of $B$:

$E=\{ \vec 0, \vec q_1 + \vec q_2, \cdots \}$
$O=\{  \vec q_1, \vec q_2, \cdots, \vec q_2 + \vec q_5 + \vec q_9, \cdots \}$


"""
