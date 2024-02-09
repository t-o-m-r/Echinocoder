#!/usr/bin/env python3

import Cinf_polynomial_encoder_for_list_of_real_or_complex_numbers as encoder_Cinf
import C0_sorting_encoder_for_list_of_real_numbers as encoder_C0
import data_sources

def test_encoder(data, encoder, number_of_shuffled_copies=3):
    import numpy
    print("ORIGINAL DATA is",data)
    shuffled_data = data.copy()
    for i in range(number_of_shuffled_copies):
        encoding = encoder.encode(shuffled_data)
        print("ENCH",encoder.name,"generates",encoding,"from",shuffled_data)
        numpy.random.shuffle(shuffled_data) 
    print()

def test_various_encoders():

    test_encoder(
       data=data_sources.random_real_1D_data(n=4),
       encoder=encoder_Cinf,
    )

    test_encoder(
       data=data_sources.random_complex_1D_data(n=4),
       encoder=encoder_Cinf,
    )

    test_encoder(
       data=data_sources.random_real_1D_data(n=4),
       encoder=encoder_C0,
    )

test_various_encoders()
