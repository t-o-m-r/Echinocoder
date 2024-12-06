#!/usr/bin/env python3

import  Cinf_python_polynomial_encoder_for_list_of_reals_as_multiset as encoder_Cinf_py_li
import  Cinf_numpy_polynomial_encoder_for_array_of_reals_as_multiset as Cinf_np_ar
encoder_Cinf_np_ar = Cinf_np_ar.Encoder()
import      Cinf_sympy_bursar_encoder_for_array_of_reals_as_multiset as encoder_Cinf_sp_bur_ar
import  Cinf_sympy_evenBursar_encoder_for_array_of_reals_as_multiset as encoder_Cinf_sp_evenBur_ar
import   Cinf_numpy_polynomial_encoder_for_list_of_reals_as_multiset as encoder_Cinf_np_li
import              C0_sorting_encoder_for_list_of_reals_as_multiset as encoder_C0_li
import Historical.C0_simplicialComplex_encoder_1_for_array_of_reals_as_multiset as C0_np_simplex_good1
encoder_C0_np_simplex_good1 = C0_np_simplex_good1.Encoder()

import data_sources
import numpy as np
import unittest
from tools import __line__

fail_count = 0

def self_test_realprojectivespace_encoder(encoder):
    for inp, out in encoder.unit_test_input_output_pairs:
       test_realprojectivespace_encoder(inp, encoder=encoder, expected_encoding=out)

def test_realprojectivespace_encoder(data, encoder=None, encoders=None, expected_encoding=None):
    global fail_count
    print("ORIGINAL DATA is",data)
    data_copy = data.copy()
    if encoders is None:
        encoders = [ encoder ]
    for sign in [+1,-1]:
        data_copy *= sign
        for encoder in encoders:
            encoding = encoder.encode(data_copy)
            encoding_fails = expected_encoding is not None and not np.array_equal(np.asarray(encoding),np.asarray(expected_encoding))
            if encoding_fails:
                fail_count += 1
                print("FAIL! Expected "+str(expected_encoding)+" ... ", end='')
            print("ENCH",encoder.__name__,"generates",encoding,"of length",len(encoding),"when encoding",data_copy,"having n=",len(data_copy),". Expectation was "+str(expected_encoding))
    print()

def make_randoms_reproducable():
    import random
    random.seed(1)
    np.random.seed(1)

def test_tools():


    global fail_count
    import tools


    data = np.asarray([3+4j, 4+2j])
    out_expected = [3, 4, 4, 2]
    out_real = tools.expand_complex_to_real_pairs(data)
    print("tools.expand_complex_to_real_pairs")
    print("data in ",data)
    print("out_expected ",out_expected)
    print("out_real     ",out_real)
    if not np.array_equal(out_expected,out_real):
        fail_count += 1
        print("FAIL in expand_complex_to_real_pairs")
    print()

    for data, expected in ( ([1,2,3,4,5,], [1+2j, 3+4j, 5,]),  ([1,2,3,4,], [1+2j, 3+4j, ]),  ):
       data = np.asarray(data)
       expected = np.asarray(expected)
       out = tools.real_pairs_to_complex_zip(data)
       print("tools.real_pairs_to_complex_zip")
       print("data in ",data)
       print("out_expected ",expected)
       print("out_real     ",out)
       if not np.array_equal(expected,out):
           fail_count += 1
           print("FAIL in real_pairs_to_complex_zip")
       print()

    perm = [3,0,1,2]
    inverse_perm_calculated = tools.invert_perm(perm)
    inverse_perm_expected = [1,2,3,0]

    if not np.array_equal(inverse_perm_calculated, inverse_perm_expected):
        fail_count += 1
        print("FAIL in tools.invert_perm")
        
    perm = [3,5,0,4,1,2]
    inverse_perm_calculated = tools.invert_perm(perm)
    inverse_perm_expected = [2, 4, 5, 0, 3, 1]

    if not np.array_equal(inverse_perm_calculated, inverse_perm_expected):
        fail_count += 1
        print("FAIL in tools.invert_perm")

    inp = np.array([[1, 0, 2],
                    [0, 5, 2],
                    [3, 0, 8]])

    expected = np.array([[0, 1, 2],
                         [0, 2, 5],
                         [0, 3, 8]])
    got = tools.sort_each_np_array_row(inp)

    assert (got == expected).all()

        

class Test_Encoders(unittest.TestCase):
    def tost_multiset_encoder(self, data, encoder=None, encoders=None, number_of_shuffled_copies=3, expected_encoding=None, relative_tolerance=0, absolute_tolerance=0):
        global fail_count
        exact = relative_tolerance == 0 and absolute_tolerance == 0
        print("ORIGINAL DATA is",data)
        shuffled_data = data.copy()
        if encoders is None:
            encoders = [ encoder ]
        first_encoding = dict()
        for i in range(number_of_shuffled_copies):
            for encoder in encoders:
                encoding = encoder.encode(shuffled_data)
                #encoding_fails = expected_encoding is not None and not np.array_equal(np.asarray(encoding),np.asarray(expected_encoding))
                # Check subsequent encodings are same as first encoding. I.e. check for permutation invariance.
                if i==0:
                    first_encoding[encoder]=encoding
                else:
                    #print("MOOOCOWFIRST",encoder, first_encoding[encoder])
                    #print("MOOOCOW__NOW",encoder, encoding)
                    if exact:
                        np.testing.assert_equal(encoding, first_encoding[encoder], strict=True)
                    else:
                        np.testing.assert_allclose(np.array(encoding, dtype=float), np.array(first_encoding[encoder], dtype=float), atol=absolute_tolerance, rtol=relative_tolerance, strict=True, equal_nan=False)

                # Also checks encoding against expected, if given
                if expected_encoding is not None:
                    #print("MOOO1",encoding)
                    #print("MOOO2",expected_encoding)
                    if exact:
                        np.testing.assert_equal(encoding, expected_encoding, strict=True)
                    else:
                        np.testing.assert_allclose(np.array(encoding, dtype=float), np.array(expected_encoding, dtype=float), atol=absolute_tolerance, rtol=relative_tolerance, strict=True, equal_nan=False)

            np.random.shuffle(shuffled_data) 
        print()

    def test_various_encoders(self):

        #with lists as inputs:
        #self.assertEqual(ell( [(1,5),(2,42),(3,100)], 101),
        #                 ell( [(7,5),(1,42),(3,100)], 101))  # ( (172) maps 1->7 and 2->1 in S(8) )


        make_randoms_reproducable()
    
        print(__file__, __line__)
        self.tost_multiset_encoder(
           data=np.asarray([9,-4,21,-8,5]),
           encoder=encoder_C0_li,
           expected_encoding = [-8,-4,5,9,21],
        )
    
        print(__file__, __line__)
        self.tost_multiset_encoder(
           data=data_sources.random_real_linear_data(n=4),
           encoder=encoder_C0_li,
        )
    
        print(__file__, __line__)
        self.tost_multiset_encoder(
           data=data_sources.random_complex_linear_data(n=4),
           encoders=[ encoder_Cinf_np_li, encoder_Cinf_py_li, ],
        )
    
        print(__file__, __line__)
        self.tost_multiset_encoder(
           data=data_sources.random_real_linear_data(n=4),
           encoders=[ encoder_Cinf_np_li, encoder_Cinf_py_li, ],
        )
    
        print(__file__, __line__)
        self.tost_multiset_encoder(
           data=data_sources.random_real_array_data(mn=(1,4)),
           encoders=[ encoder_Cinf_np_ar, ],
        )
    
        print(__file__, __line__)
        self.tost_multiset_encoder(
           data=data_sources.random_real_array_data(mn=(2,3)),
           encoders=[ encoder_Cinf_np_ar, ],
        )
    
        print(__file__, __line__)
        self.tost_multiset_encoder(
           data=data_sources.random_real_array_data(mn=(3,3)),
           encoders=[ encoder_Cinf_np_ar, ],
        )
    
        print(__file__, __line__)
        self.tost_multiset_encoder(
           data=data_sources.random_real_array_data(mn=(4,3)),
           encoders=[ encoder_Cinf_np_ar, encoder_Cinf_sp_bur_ar, ],
        )
    
        print(__file__, __line__)
        self.tost_multiset_encoder(
           data=np.array(((-7,-8,-1,-9),(9,-7,-6,5),(-9,4,9,-7))),
           encoders=[ encoder_Cinf_sp_bur_ar, ],
           expected_encoding = [-11, 2, -11, -7, -17, 62, 55, -202, 110, 120, -81, 315, -748, 58, 1289, -1497, 457, 1139, -1460, -45, 567],
        )
    
        print(__file__, __line__)
        self.tost_multiset_encoder(
           data=np.array(((8,-1,-4,3),(-8,-5,9,7),(8,2,7,-7))),
           encoders=[ encoder_Cinf_np_ar, ],
           expected_encoding = [   8.0,   -4,  -57,  -80, -488, -394,    8,   12,  -63,  144, -952,  636, 8,    3,  -15,  112, -456,  851,   -4,   12,   -6,  -21,    5,  309, -4,    3,   42,   40, -186,   68,   12,    3,   48,   34, -406,  392], 
        )
   
        print(__file__, __line__)
        self.tost_multiset_encoder(
           data=np.array(((3,1,4),(2,2,5))),
           encoders=[ encoder_Cinf_sp_bur_ar, ],
           expected_encoding =  [9, 3, 5, 20, 13, 25, 8, 6],
        )
    
        print(__file__, __line__)
        self.tost_multiset_encoder(
           data=np.array(((3,1,4),(2,2,5))),
           encoders=[ encoder_Cinf_sp_evenBur_ar, ],
           number_of_shuffled_copies=10,
           expected_encoding = [9, 20, 3, 13, 2, 5, 23, 8, 6],
        )
    
        print(__file__, __line__)
        import Cinf_numpy_regular_encoder_for_list_of_realsOrComplex_as_realOrComplexprojectivespace
        self_test_realprojectivespace_encoder(Cinf_numpy_regular_encoder_for_list_of_realsOrComplex_as_realOrComplexprojectivespace)

        print(__file__, __line__)
        import Cinf_numpy_complexPacked_encoder_for_list_of_reals_as_realprojectivespace
        self_test_realprojectivespace_encoder(Cinf_numpy_complexPacked_encoder_for_list_of_reals_as_realprojectivespace)
    
        print(__file__, __line__)
        self.tost_multiset_encoder(
           data=np.array(((1,2),(1,0),(5,2))),
           encoders=[ 
             encoder_C0_np_simplex_good1,
           ],
           number_of_shuffled_copies=100,
           expected_encoding = [ 0.41666667, -0.28108724,  0.26858269, -0.34436233,  0.16483989, -0.15923648,
                                 0.21872145, -0.05275334,  0.10091283, -0.17636017,  0.04387883, -0.13616001,
                                 0.19830351, -0.11750502,  0.04748888, -0.16028752,  0.22837654, -0.1166443,
                                 0.19825184, -0.2125061 ,  0.07986435, -0.16658635,  0.17372507, -0.07108562,
                                 0.20191163, ],
           relative_tolerance=1e-7,
           absolute_tolerance=1e-7,
        )

def test_everything():
    test_tools()
    print(str(fail_count)+" failures")
    import tuple_rank
    tuple_rank.unit_test_tuple_rank()

print(__file__, __line__)
test_everything()
unittest.main(exit=False)

