#!/usr/bin/env python3

import analytic_encoder_for_list_of_real_or_complex_numbers as encoder
import data_sources



for i in range(10):
    data = list(data_sources.random_real_1D_data(n=3))
    print("DATA is ",data)
    encoding = list(encoder.encode(data))
    print("ENCH is ",encoding)
    print()

    data = list(data_sources.random_complex_1D_data(n=3))
    print("DATA is ",data)
    encoding = list(encoder.encode(data))
    print("ENCH is ",encoding)
    print()


