#!/usr/bin/env python3

import Cinf_python_polynomial_encoder_for_list_of_reals as encoder_Cinf_py_li
import Cinf_numpy_polynomial_encoder_for_array_of_reals as encoder_Cinf_np_ar
import    Cinf_python_bursar_encoder_for_array_of_reals as encoder_Cinf_py_bur_ar
import  Cinf_numpy_polynomial_encoder_for_list_of_reals as encoder_Cinf_np_li
import             C0_sorting_encoder_for_list_of_reals as encoder_C0_li
import data_sources
import numpy as np

def test_encoder(data, encoder=None, encoders=None, number_of_shuffled_copies=3):
    print("ORIGINAL DATA is",data)
    shuffled_data = data.copy()
    if encoders is None:
        encoders = [ encoder ]
    for i in range(number_of_shuffled_copies):
        for encoder in encoders:
            encoding = encoder.encode(shuffled_data)
            print("ENCH",encoder.name,"generates",encoding,"of length",len(encoding),"when encoding",shuffled_data,"with (m,n)=",shuffled_data.shape[::-1],".")
        np.random.shuffle(shuffled_data) 
    print()

def test_various_encoders():

    test_encoder(
       data=data_sources.random_real_linear_data(n=4),
       encoder=encoder_C0_li,
    )

    test_encoder(
       data=data_sources.random_complex_linear_data(n=4),
       encoders=[ encoder_Cinf_np_li, encoder_Cinf_py_li, ],
    )

    test_encoder(
       data=data_sources.random_real_linear_data(n=4),
       encoders=[ encoder_Cinf_np_li, encoder_Cinf_py_li, ],
    )

    test_encoder(
       data=data_sources.random_real_array_data(mn=(1,4)),
       encoders=[ encoder_Cinf_np_ar, ],
    )

    test_encoder(
       data=data_sources.random_real_array_data(mn=(2,3)),
       encoders=[ encoder_Cinf_np_ar, ],
    )

    test_encoder(
       data=data_sources.random_real_array_data(mn=(3,3)),
       encoders=[ encoder_Cinf_np_ar, ],
    )

    test_encoder(
       data=data_sources.random_real_array_data(mn=(4,3)),
       encoders=[ encoder_Cinf_np_ar, encoder_Cinf_py_bur_ar, ],
    )

test_various_encoders()
