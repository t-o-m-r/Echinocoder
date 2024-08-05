#!/usr/bin/env python3

import Cinf_python_polynomial_encoder_for_list_of_reals as encoder_Cinf_py_li
import Cinf_numpy_polynomial_encoder_for_array_of_reals as encoder_Cinf_np_ar
import     Cinf_sympy_bursar_encoder_for_array_of_reals as encoder_Cinf_sp_bur_ar
import Cinf_sympy_evenBursar_encoder_for_array_of_reals as encoder_Cinf_sp_evenBur_ar
import  Cinf_numpy_polynomial_encoder_for_list_of_reals as encoder_Cinf_np_li
import             C0_sorting_encoder_for_list_of_reals as encoder_C0_li
import data_sources
import numpy as np

fail_count = 0

def test_multiset_encoder(data, encoder=None, encoders=None, number_of_shuffled_copies=3, expected_encoding=None):
    global fail_count
    print("ORIGINAL DATA is",data)
    shuffled_data = data.copy()
    if encoders is None:
        encoders = [ encoder ]
    for i in range(number_of_shuffled_copies):
        for encoder in encoders:
            encoding = encoder.encode(shuffled_data)
            encoding_fails = expected_encoding is not None and not np.array_equal(np.asarray(encoding),np.asarray(expected_encoding))
            if encoding_fails:
                fail_count += 1
                print("FAIL! Expected "+str(expected_encoding)+" ... ", end='')
            print("ENCH",encoder.name,"generates",encoding,"of length",len(encoding),"when encoding",shuffled_data,"with (m,n)=",shuffled_data.shape[::-1],".")
            
        np.random.shuffle(shuffled_data) 
    print()

def test_various_encoders():

    test_multiset_encoder(
       data=data_sources.random_real_linear_data(n=4),
       encoder=encoder_C0_li,
    )

    test_multiset_encoder(
       data=data_sources.random_complex_linear_data(n=4),
       encoders=[ encoder_Cinf_np_li, encoder_Cinf_py_li, ],
    )

    test_multiset_encoder(
       data=data_sources.random_real_linear_data(n=4),
       encoders=[ encoder_Cinf_np_li, encoder_Cinf_py_li, ],
    )

    test_multiset_encoder(
       data=data_sources.random_real_array_data(mn=(1,4)),
       encoders=[ encoder_Cinf_np_ar, ],
    )

    test_multiset_encoder(
       data=data_sources.random_real_array_data(mn=(2,3)),
       encoders=[ encoder_Cinf_np_ar, ],
    )

    test_multiset_encoder(
       data=data_sources.random_real_array_data(mn=(3,3)),
       encoders=[ encoder_Cinf_np_ar, ],
    )

    test_multiset_encoder(
       data=data_sources.random_real_array_data(mn=(4,3)),
       encoders=[ encoder_Cinf_np_ar, encoder_Cinf_sp_bur_ar, ],
    )

    test_multiset_encoder(
       data=np.array(((-7,-8,-1,-9),(9,-7,-6,5),(-9,4,9,-7))),
       encoders=[ encoder_Cinf_sp_bur_ar, ],
       expected_encoding = [-11, 2, -11, -7, -17, 62, 55, -202, 110, 120, -81, 315, -748, 58, 1289, -1497, 457, 1139, -1460, -45, 567],
    )

    test_multiset_encoder(
       data=np.array(((8,-1,-4,3),(-8,-5,9,7),(8,2,7,-7))),
       encoders=[ encoder_Cinf_np_ar, ],
       expected_encoding = [   8,   -4,  -57,  -80, -488, -394,    8,   12,  -63,  144, -952,  636, 8,    3,  -15,  112, -456,  851,   -4,   12,   -6,  -21,    5,  309, -4,    3,   42,   40, -186,   68,   12,    3,   48,   34, -406,  392], 
    )

    test_multiset_encoder(
       data=np.array(((3,1,4),(2,2,5))),
       encoders=[ encoder_Cinf_sp_bur_ar, ],
       expected_encoding =  [9, 3, 5, 20, 13, 25, 8, 6],
    )

    test_multiset_encoder(
       data=np.array(((3,1,4),(2,2,5))),
       encoders=[ encoder_Cinf_sp_evenBur_ar, ],
       number_of_shuffled_copies=10,
       expected_encoding = [9, 20, 3, 13, 2, 5, 23, 8, 6],
    )

    print(str(fail_count)+" failures")

test_various_encoders()
