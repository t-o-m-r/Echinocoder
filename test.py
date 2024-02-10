#!/usr/bin/env python3

import Cinf_py_polynomial_encoder_for_list_of_real_or_complex_numbers as encoder_Cinf_py
import Cinf_np_polynomial_encoder_for_list_of_real_or_complex_numbers as encoder_Cinf_np
import C0_sorting_encoder_for_list_of_real_numbers as encoder_C0
import data_sources

def test_encoder(data, encoder=None, encoders=None, number_of_shuffled_copies=3):
    import numpy
    print("ORIGINAL DATA is",data)
    shuffled_data = data.copy()
    if encoders is None:
        encoders = [ encoder ]
    for i in range(number_of_shuffled_copies):
        for encoder in encoders:
            encoding = encoder.encode(shuffled_data)
            print("ENCH",encoder.name,"generates",encoding,"from",shuffled_data)
            numpy.random.shuffle(shuffled_data) 
    print()

def test_various_encoders():

    test_encoder(
       data=data_sources.random_real_linear_data(n=4),
       encoders=[ encoder_Cinf_np, encoder_Cinf_py, ],
    )

    test_encoder(
       data=data_sources.random_complex_linear_data(n=4),
       encoders=[ encoder_Cinf_np, encoder_Cinf_py, ],
    )

    test_encoder(
       data=data_sources.random_real_linear_data(n=4),
       encoder=encoder_C0,
    )

test_various_encoders()
