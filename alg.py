#!/opt/local/bin/python3

# Patrick Kennedy-Hunt
# Christopher Lester

# THIS SHOULD BE RE-WRITTEN AS 0-based not 1-based AS IT CURRENTLY IS!
import numpy as np

def tuple_rank(tup, k):
    """ Purpose of this function is to map a supplied tuple to its position in this list:
    (), (1), (2), ... ,(k), (1,1), (1,2), ... , (1,k), (2,2), (2,3), ... ,(2,k), (3,3), ... ,(3,k),..., (k,k), (1,1,1), (1,1,2), (1,1,3), ... , (1,1,k),(1,2,2),(1,2,3),...(2,2,2),(2,2,3),...,(k,k,k),(1,1,1,1),...,(k,k,k,k),...

    Expected output:

    k = 3
    print(tuple_rank((), k))        # Expected output: 0
    print(tuple_rank((1,), k))      # Expected output: 1
    print(tuple_rank((3,), k))      # Expected output: 3
    print(tuple_rank((1,1,), k))    # Expected output: 4
    print(tuple_rank((3,3,), k))    # Expected output: 9
    print(tuple_rank((1,1,1), k))   # Expected output: 10
    """

    from math import comb

    # Convert the tuple to 0-based indexing
    tup = [x - 1 for x in tup]

    rank = 0
    n = len(tup)

    # Count all tuples of lengths less than the current tuple's length
    for length in range(n):
        rank += comb(k + length -1 , length)


    # Now, for the current tuple of length n, compute the lexicographical rank
    prev = 0
    for i in range(n):
        for val in range(prev, tup[i]):
            rank += comb(n - i + k - 1 - (val + 1), n - i - 1)
        prev = tup[i]

    return rank

def unit_test_tuple_rank():
    fails = 0;

    fails += 0 != tuple_rank((), 1)
    fails += 0 != tuple_rank((), 10)
    fails += 0 != tuple_rank((), 100)
    fails += 0 != tuple_rank((), 1000)

    fails += 10 != tuple_rank((1,1,1), 3)
    fails += 15 != tuple_rank((1,1,1), 4)
    fails += 21 != tuple_rank((1,1,1), 5)

    fails += 0 != tuple_rank((),2)
    fails += 1 != tuple_rank((1,),2)
    fails += 2 != tuple_rank((2,),2)
    fails += 3 != tuple_rank((1,1,),2)
    fails += 4 != tuple_rank((1,2,),2)
    fails += 5 != tuple_rank((2,2,),2)
    fails += 6 != tuple_rank((1,1,1,),2)
    fails += 7 != tuple_rank((1,1,2,),2)
    fails += 8 != tuple_rank((1,2,2,),2)
    fails += 9 != tuple_rank((2,2,2,),2)
    fails += 10 != tuple_rank((1,1,1,1,),2)

    fails += 0 != tuple_rank((),3)
    fails += 1 != tuple_rank((1,),3)
    fails += 2 != tuple_rank((2,),3)
    fails += 3 != tuple_rank((3,),3)
    fails += 4 != tuple_rank((1,1,),3)
    fails += 5 != tuple_rank((1,2,),3)
    fails += 6 != tuple_rank((1,3,),3)
    fails += 7 != tuple_rank((2,2,),3)
    fails += 8 != tuple_rank((2,3,),3)
    fails += 9 != tuple_rank((3,3,),3)
    fails += 10 != tuple_rank((1,1,1,),3)
    fails += 11 != tuple_rank((1,1,2,),3)
    fails += 12 != tuple_rank((1,1,3,),3)
    fails += 13 != tuple_rank((1,2,2,),3)
    fails += 14 != tuple_rank((1,2,3,),3)
    fails += 15 != tuple_rank((1,3,3,),3)
    fails += 16 != tuple_rank((2,2,2,),3)
    fails += 17 != tuple_rank((2,2,3,),3)
    fails += 18 != tuple_rank((2,3,3,),3)
    fails += 19 != tuple_rank((3,3,3,),3)
    fails += 20 != tuple_rank((1,1,1,1,),3)
    fails += 21 != tuple_rank((1,1,1,2,),3)
    fails += 22 != tuple_rank((1,1,1,3,),3)
    fails += 23 != tuple_rank((1,1,2,2,),3)
    fails += 24 != tuple_rank((1,1,2,3,),3)
    fails += 25 != tuple_rank((1,1,3,3,),3)
    fails += 26 != tuple_rank((1,2,2,2,),3)
    fails += 27 != tuple_rank((1,2,2,3,),3)
    fails += 28 != tuple_rank((1,2,3,3,),3)
    fails += 29 != tuple_rank((1,3,3,3,),3)
    fails += 30 != tuple_rank((2,2,2,2,),3)
    fails += 31 != tuple_rank((2,2,2,3,),3)
    fails += 32 != tuple_rank((2,2,3,3,),3)
    fails += 33 != tuple_rank((2,3,3,3,),3)
    fails += 34 != tuple_rank((3,3,3,3,),3)
    fails += 35 != tuple_rank((1,1,1,1,1,),3)

    if fails>0:
        raise Exception("tuple_rank fails unit test")



def ell(c, k):
    # Every c is a (possibly empty) list (or set) of (j,i) pairs, with j in [1,n] and i in [1,k].
    # Even if c is a python list (and so is ordered) it is representing an unordered mathematical object (set).
    #
    # We need to map every possible c to a natural number ... but inputs c differing only by a permutation of the j's among n elements must map to the same number (i.e. must collide) and all other collisions are forbidden. That is to say ell is supposed to be a function on C mod S(n).
    #
    # E.g. we must have all these equal:
    #
    #     ell( [(1,5),(2,42),(3,100), 8] 
    #     ell( [(7,5),(1,42),(3,100), 8]
    #     ell( [(3,5),(1,42),(3,100), 8]
    #
    # but 
        
    k_vals = [vertex[1] for vertex in c]
    k_vals.sort()  # This divides out S(n)
    return tuple_rank(k_vals, k)


def map_Delta_k_to_the_n_to_c_dc_pairs(#n=3,k=3,  # Only need n and/or k if doing "original initialisation" of x_with_coeffs 
         delta = dict(), # Each key in the dict is an (j,i) tuple representing Patrick's e^j_i with j in [1,n] and i in [i,k].  The associated value is the coefficient of that e^j_i basis vector in the associated element of (\Delta_k)^n.
        # e.g delta = {  
        #     (1,1) : 0.5, (1,2) : 0.2, (1,3) : 0.1,    #a point in the 1st simplex
        #     (2,3) : 0.25,                             #a point in the 2nd simplex 
        #     (3,1) : 0.1,                              #a point in the 3rd simplex
        #   }, 
        ):

    c_dc_pairs = []

    print("delta",delta)

    if False:
        # Original initialisation. If using this pass n and k to the algorithm

        # Set up initial value of x based on n, k and delta.
        # This is the only place where n or k is used.

        x_with_coeffs = {  (j,k):delta.get((j,k),0)  for j in range(1,n+1) } 
    else:

        # n-and-k-independent initialisation
        if delta:
           j_vals = {j for (j,i) in delta.keys() }
           largest_j = max(j_vals)
           largest_i_for_j = {  j:max([ i for (jj,i) in delta.keys() if jj == j ])   for j in j_vals }
           x_with_coeffs = {  (j,largest_i_for_j[j]):delta[(j,largest_i_for_j[j])]  for j in j_vals } 
        else:
           x_with_coeffs = dict()


    while x_with_coeffs:
        print("Iteration! =====")
        print("delta",delta)
        print("x_with_coeffs",x_with_coeffs)

        e = min(x_with_coeffs, key=x_with_coeffs.get)
        dx = x_with_coeffs[e]
        z=e[0] # z is the j-val of the element of x with the smallest coefficient
        print("smallest: e=",e,"coeff=",dx, "z=",z)

        if dx<0:
            # dx should never be negative.
            print("ERROR: or unexpected numerical precision concern since dx=",dx,"<0.")
            raise Exception("IMPLEMENTATION ERROR")

        if dx>0:
            # Grow the c_dc_pairs list
            c = list(x_with_coeffs.keys()) # could use list or set in the implementation ... it doesn't really matter ... but the object represented is a set
            c_dc_pairs.append((c, dx)) 
            print("grew c_dc_pairs")
            print("c_dc_pairs=",c_dc_pairs)

            # trim delta
            for pair,val in list(delta.items()):
                 if pair in c:
                     if val == dx:
                        del delta[pair]
                     elif val>dx:
                        delta[pair] = val-dx
                     else:
                        print("val=",val,"dx=",dx)
                        raise Exception("IMPLEMENTATION ERROR! Should not have val<dx.")

        # trim and update x_with_coeffs:

        del x_with_coeffs[e] # since this part should be gone.  Needed by next line!
        # Set up new keys:
        new_keys = list(x_with_coeffs.keys()) # Will not contain e.
        if e[1]>1:
            new_e = (z, e[1]-1)
            new_keys.append(new_e)

        # refresh x_with_coeffs:
        x_with_coeffs = { new_key:delta.get(new_key,0)  for new_key in new_keys } 
           

    # We are done:        
    return c_dc_pairs

def pr(r, big_n):
    return np.power(r, np.arange(1, big_n+1))

def map_Delta_k_to_the_n_to_c_l_dc_triples(n, k, delta):
    c_dc_pairs = map_Delta_k_to_the_n_to_c_dc_pairs(delta=delta)
    c_l_dc_triples = [ (c, ell(c,k), dc) for (c,dc) in c_dc_pairs ]
    big_n = n*k+1
    # Please someone re-implement this dot product without so many comprehensions ... or at any rate BETTER:
    # Want output here to be sum_i pr(r_i, big_n) x_i)
    # where, in effect, r_i and x_i would be defined by
    # [ blah for _, r_i, x_i in c_l_dc_triples ]
    # Help Jeremy!

    point_in_R_bigN = sum([d * pr(r, big_n) for _, r, d in c_l_dc_triples]) + pr(0, big_n) # Addition of zero term at end ensures that we still get a zero vec (not 0) in the event that c_l_dc_triples is empty!

    return c_l_dc_triples, point_in_R_bigN 

def vector_to_simplex_point(vec):
    k = len(vec)
    vec = np.array(vec)
    return 1.0/(k*(1.0+np.power(2.0,vec))) # This somewhat crude parametrisation does not use the WHOLE of the simplex -- so it's a bit wasteful. It also has terrible dynamic range problems and even unit issues. Might want to address all of these points with a better mapping.

def vectors_to_delta(vecs):
    n=len(vecs)
    delta = {}
    if not vecs:
        return delta
    # vecs is not empty
    k = len(vecs[0])
    for j in range(n):
        vec = vecs[j]
        simplex_point = vector_to_simplex_point(vec)
        k_this = len(vec)
        if k!=k_this:
            raise Exception("Vectos supplied to vectors_to_delta are not all the same dimension!")
        for i in range(k):
            delta[(j+1,i+1)]=simplex_point[i]
    return delta


if __name__ == "__main__":

    unit_test_tuple_rank()

    short = map_Delta_k_to_the_n_to_c_l_dc_triples

    ans1 = short(n=3, k=3, 
                 delta = {  (1,2) : 0.5, (2,3) : 0.25 }, )

    # Next three all similar to each other.
    ans2a = short(n=3, k=3, 
                  delta = {  (1,3) : 0.5, (2,3) : 0.25, (3,3):0.1 }, )
    ans2b = short(n=3, k=3, 
                  delta = {  (1,3) : 0.5, (2,3) : 0.25, (3,3):0.1,  (2,2):0.0001}, )
    ans2c = short(n=3, k=3, 
                  delta = {  (1,3) : 0.5, (2,3) : 0.25, (3,3):0.1001,  }, )

    # Perm invariance
    ans3c1 = short(n=3, k=3, 
                   delta = {  (1,3) : 0.5, (2,1):0.001, (2,3) : 0.25, (3,3):0.1001,  }, )
    ans3c2 = short(n=3, k=3, 
                   delta = {  (2,3) : 0.5, (1,1):0.001, (1,3) : 0.25, (3,3):0.1001,  }, )

    # Trick case:
    ans4 = short(n=3, k=3, 
             delta = {
             (1,1) : 0.5, (1,2) : 0.2, (1,3) : 0.1,    #a point in the 1st simplex
             (2,3) : 0.25,                             #a point in the 2nd simplex 
             (3,1) : 0.1,                              #a point in the 3rd simplex
             })

    # Trick case:
    ans5 = short(n=7, k=3, 
             delta = {
             (1,1) : 0.5, (1,2) : 0.2, (1,3) : 0.1,    #a point in the 1st simplex
             (2,3) : 0.25,                             #a point in the 2nd simplex 
             (3,1) : 0.1,                              #a point in the 3rd simplex
             })

    # Zero cases:
    ans6a = short(n=7, k=3, 
                  delta = { (1,2) : 0.0, (2,3) : 0.0, })
    ans6b = short(n=7, k=3,
                  delta = dict()                       )
    ans6c = short(n=7, k=3,
                  delta = vectors_to_delta( [] )       )

    ans7 = short(n=3, k=2,
                  delta = vectors_to_delta( [
                     np.array([1,2]), # k-vector number 1 of n
                     np.array([1,0]), # k-vector number 2 of n
                     np.array([5,2]), # k-vector number 3 of n
                  ] )
                )

    print("Ans1 was ",ans1)
    print("Ans2a was ",ans2a)
    print("Ans2b was ",ans2b)
    print("Ans2c was ",ans2c)
    print("Ans3c1 was ",ans3c1)
    print("Ans3c2 was ",ans3c2)
    print("Ans5 was ",ans5)
    print("Ans6a was ",ans6a)
    print("Ans6b was ",ans6b)
    print("Ans6c was ",ans6c)
    print("Ans7 was ",ans7)

    print("Ans1 was ",ans1[1])
    print("Ans2a was ",ans2a[1])
    print("Ans2b was ",ans2b[1])
    print("Ans2c was ",ans2c[1])
    print("Ans3c1 was ",ans3c1[1])
    print("Ans3c2 was ",ans3c2[1])
    print("Ans5 was ",ans5[1])
    print("Ans6a was ",ans6a[1])
    print("Ans6b was ",ans6b[1])
    print("Ans6c was ",ans6c[1])
    print("Ans7 was ",ans7[1])
    
    

