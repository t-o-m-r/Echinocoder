#import itertools
import math

def bi_range(n):
    """
    Whereas range(n) iterates over 0,1,2,3,...,n-1 ... bi_range(n) iterates over non-negative pairs of integers which sum to n.
    The first integer grows, while the second integer shrinks.
    For example, range(4) would iterate over
        (0,4), (1,3), (2,2), (3,1), (4,0).
    """
    for i in range(n+1):
        yield i, n-i

def bi_range_with_maxes_crude(n, max_first, max_second):
    """
    Whereas range(n) iterates over 0,1,2,3,...,n-1 ... bi_range(n) iterates over non-negative pairs of integers which sum to n.
    The first integer grows, while the second integer shrinks.
    The first integer may not exceed max_first, while the second may not exceed max_second.
    For example, range(4, 2,3) would iterate over
         (1,3), (2,2)
    which starts at the max_second contraint, and goes to the max_first constraint.
    If the sum of both maxes is less than the total n, there will be no valid iterator positions. So:
    """
   
    for i in range(n+1):
       if i>max_first or n-i>max_second:
           continue # TODO! Slow Fix!
       yield i, n-i

def bi_range_with_maxes(n, max_first, max_second):
    """
    Whereas range(n) iterates over 0,1,2,3,...,n-1 ... bi_range(n) iterates over non-negative pairs of integers which sum to n.
    The first integer grows, while the second integer shrinks.
    The first integer may not exceed max_first, while the second may not exceed max_second.
    For example, range(5, 2,3) would iterate over
         (1,3), (2,2)
    which starts at the max_second contraint, and goes to the max_first constraint.
    If the sum of both maxes is less than the total n, there will be no valid iterator positions. So:

    0 <= a <= A
    0 <= b <= B
    0 <= a+b = N

    so 

    0 <= a <= A
    0 <= N-a <= B

    so

    0 <= a <= A
    0 >= a-N >= -B

    so

    0 <= a <= A
    N >= a >= N-B

    so

    0 <= a <= A
    N-B <= a <= N

    so

    max(0, N-B) <= a <= min(A,N)

    """
  
    if n<0 or max_first<0 or max_second<0:
        # No valid iterator positions can be returned.
        return
    
    for a in range(max(0, n-max_second), min(max_first, n)+1):
        yield a, n-a
