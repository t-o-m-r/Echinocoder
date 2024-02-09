#!/usr/bin/env python3

# some random data that is a length-n list of lenth-m lists:
def random_real_2D_data(mn=(1,1) ):
    import random
    m,n = mn
    return ([    list(           ( random.randrange(-10,10) for j in range(m))             )            for i in range(n)])
    #return ([                    ( random.randrange(-10,10) for j in range(m))                          for i in range(n)])

# some random data that is a length-n list of reals
def random_real_1D_data(n=1):
    import random
    return ( random.randrange(-10,10) for i in range(n) )

# some random data that is a length-n list of complex numbers
def random_complex_1D_data(n=1):
    import random
    return ( complex(random.randrange(-10,10), random.randrange(-10,10)) for i in range(n) )




