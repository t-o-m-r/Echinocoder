#!/usr/bin/env python3

import Cinf_encoder_for_list_of_real_or_complex_numbers as encoder_Cinf
import C0_encoder_for_list_of_real_numbers as encoder_C0
import data_sources



for i in range(10):
    data = list(data_sources.random_real_1D_data(n=3))
    print("DATA is ",data)
    encoding = list(encoder_Cinf.encode(data))
    print("Cinf ENCH is ",encoding)
    print()

    data = list(data_sources.random_complex_1D_data(n=3))
    print("DATA is ",data)
    encoding = list(encoder_Cinf.encode(data))
    print("Cinf ENCH is ",encoding)
    print()

    data = list(data_sources.random_real_1D_data(n=3))
    print("DATA is ",data)
    encoding = list(encoder_C0.encode(data))
    print("C0   ENCH is ",encoding)
    print()

