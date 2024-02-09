#!/usr/bin/env python3

import encoder_for_list_of_reals as encoder

# some random data that is a length-n list of lenth-m lists:
def some_random_real_2D_data(mn=(1,1) ):
    import random
    m,n = mn
    return ([    list(           ( random.randrange(-10,10) for j in range(m))             )            for i in range(n)])
    #return ([                    ( random.randrange(-10,10) for j in range(m))                          for i in range(n)])

# some random data that is a length-n list of reals
def some_random_real_1D_data(n=1):
    import random
    return ( random.randrange(-10,10) for i in range(n) )

# some random data that is a length-n list of complex numbers
def some_random_complex_1D_data(n=1):
    import random
    return ( complex(random.randrange(-10,10), random.randrange(-10,10)) for i in range(n) )


for i in range(10):
    data = list(some_random_real_1D_data(n=3))
    print("DATA is ",data)
    encoding = list(encoder.encode(data))
    print("ENCH is ",encoding)
    print()

    data = list(some_random_complex_1D_data(n=3))
    print("DATA is ",data)
    encoding = list(encoder.encode(data))
    print("ENCH is ",encoding)
    print()


