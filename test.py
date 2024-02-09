#!/usr/bin/env python3

import Cinf_polynomial_encoder_for_list_of_real_or_complex_numbers as encoder_Cinf
import C0_sorting_encoder_for_list_of_real_numbers as encoder_C0
import data_sources

def test_encoder(data, encoder, number_of_shuffled_copies=3):
    import random
    data=list(data)
    # shuffled_copies = [ random.shuffle(data.copy()) for i in range(number_of_shuffled_copies) ]
    shuffled_copies = [ random.sample(data, len(data)) for i in range(number_of_shuffled_copies) ]
    print("DATA is",data)
    for shuffled_data in shuffled_copies:
        #print("SHUFF DATA is",shuffled_data)
        encoding = list(encoder.encode(shuffled_data))
        print("ENCH",encoder.name,"is",encoding)
    print()

def test_various_encoders():

    test_encoder(
       data=data_sources.random_real_1D_data(n=3),
       encoder=encoder_Cinf,
    )

    test_encoder(
       data=data_sources.random_complex_1D_data(n=3),
       encoder=encoder_Cinf,
    )

    test_encoder(
       data=data_sources.random_real_1D_data(n=3),
       encoder=encoder_C0,
    )

test_various_encoders()
