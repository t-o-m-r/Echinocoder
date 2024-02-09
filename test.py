#!/usr/bin/env python3

import encoder_for_list_of_reals as encoder

# some random data
def some_random_data( mn=(1,1) ):
    import random
    m,n = mn
    return list([list(( random.randrange(10) for j in range(m))) for i in range(n)])


data = some_random_data(mn=(1,3))

print("DATA is ",data)
er = encoder.encode(data)
for i in er:
    print("ERN : ",list(i))




