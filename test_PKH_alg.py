#!/usr/bin/env python3

import unittest
from C0_good1_numpy_simplicialComplex_encoder_for_array_of_reals_as_multiset import *

class Test_Ell(unittest.TestCase):
    def test_sn_perm_collision(self):

        #with lists as inputs:
        self.assertEqual(ell( {(1,5),(2,4),(0,10)}, 11),
                         ell( {(2,4),(1,5),(0,10)}, 11))

    def test_set_function_collision(self):
        self.assertNotEqual(ell( {(1,5),(2,4),(0,10)}, 11), #     (start)
                            ell( {(2,5),(1,4),(0,10)}, 11)) #     (sets differ in content)

        self.assertNotEqual(ell( {(1,5),(2,4),(0,10)}, 11), #     (start)
                            ell( {(1,5),(2,7),(0,10)}, 11)) #     (4!=7)

        self.assertNotEqual(ell( {(1,5),(2,4),(0,10)}, 11), #     (start)
                            ell( {(1,5),      (0,10)}, 11)) #     (sets differ in length)

    def test_intention(self):
        k = 3

        self.assertEqual(ell(set(), k), 0)                   #   0

        self.assertEqual(ell({(0,0)}, k), 1)                 #   0 + 1
        self.assertEqual(ell({(0,1)}, k), 2)                 #   1 + 1
        self.assertEqual(ell({(0,2)}, k), 3)                 #   2 + 1

        self.assertEqual(ell({(0,0), (1,0)}, k), 4)          #   0 + k**0 + k**1
        self.assertEqual(ell({(0,0), (1,1)}, k), 5)          #   1 + k**0 + k**1
        self.assertEqual(ell({(0,0), (1,2)}, k), 6)          #   2 + k**0 + k**1
        self.assertEqual(ell({(0,1), (1,0)}, k), 7)          #  10 + k**0 + k**1
        self.assertEqual(ell({(0,1), (1,1)}, k), 8)          #  11 + k**0 + k**1
        self.assertEqual(ell({(0,1), (1,2)}, k), 9)          #  12 + k**0 + k**1
        self.assertEqual(ell({(0,2), (1,0)}, k), 10)         #  20 + k**0 + k**1
        self.assertEqual(ell({(0,2), (1,1)}, k), 11)         #  21 + k**0 + k**1
        self.assertEqual(ell({(0,2), (1,2)}, k), 12)         #  22  + k**0 + k**1

        self.assertEqual(ell({(0,0), (1,0), (2,0)}, k), 13)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,0), (1,0), (2,1)}, k), 14)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,0), (1,0), (2,2)}, k), 15)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,0), (1,1), (2,0)}, k), 16)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,0), (1,1), (2,1)}, k), 17)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,0), (1,1), (2,2)}, k), 18)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,0), (1,2), (2,0)}, k), 19)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,0), (1,2), (2,1)}, k), 20)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,0), (1,2), (2,2)}, k), 21)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,1), (1,0), (2,0)}, k), 22)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,1), (1,0), (2,1)}, k), 23)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,1), (1,0), (2,2)}, k), 24)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,1), (1,1), (2,0)}, k), 25)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,1), (1,1), (2,1)}, k), 26)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,1), (1,1), (2,2)}, k), 27)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,1), (1,2), (2,0)}, k), 28)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,1), (1,2), (2,1)}, k), 29)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,1), (1,2), (2,2)}, k), 30)  #   0  + k**0 + k**1 + k**2

class Test_flat_sums(unittest.TestCase):
    def test(self):

        delta = Position_within_Simplex_Product([
            [1, 4, 2],   # the first vector in the list
            [1, 54, 6],  # the second vector in the list
            [9, 10, 22], # the third vector in the list
            [-2, 3, 6],  # the fourth vector in the list
        ])

        flat_sums_expected = [
          (0, (0,1,2,), delta[0,0]+delta[0,1]+delta[0,2]),
          (0,   (1,2,),            delta[0,1]+delta[0,2]),
          (0,     (2,),                       delta[0,2]),
          (1, (0,1,2,), delta[1,0]+delta[1,1]+delta[1,2]),
          (1,   (1,2,),            delta[1,1]+delta[1,2]),
          (1,     (2,),                       delta[1,2]),
          (2, (0,1,2,), delta[2,0]+delta[2,1]+delta[2,2]),
          (2,   (1,2,),            delta[2,1]+delta[2,2]),
          (2,     (2,),                       delta[2,2]),
          (3, (0,1,2,), delta[3,0]+delta[3,1]+delta[3,2]),
          (3,   (1,2,),            delta[3,1]+delta[3,2]),
          (3,     (2,),                       delta[3,2]),
        ]
        flat_sums_calculated = make_flat_sums(delta)
        self.assertEqual(flat_sums_expected, flat_sums_calculated)

        flat_sums_expected = [ (None, tuple(), 0), ] + flat_sums_expected

        flat_sums_calculated = make_flat_sums(delta, prepend_zero = True)
        self.assertEqual(flat_sums_expected, flat_sums_calculated)

    def test_with_omitted_zeros(self):

        delta = Position_within_Simplex_Product([
            [1, 0, 2],   # the first vector in the list
            [1, 54, 6],  # the second vector in the list
            [9, 10, 22], # the third vector in the list
            [-2, 3, 0],  # the fourth vector in the list
        ])

        flat_sums_expected = [
          (0, (0,1,2,), delta[0,0]+           delta[0,2]),
          (0,   (1,2,),                       delta[0,2]),
          (0,     (2,),                       delta[0,2]),
          (1, (0,1,2,), delta[1,0]+delta[1,1]+delta[1,2]),
          (1,   (1,2,),            delta[1,1]+delta[1,2]),
          (1,     (2,),                       delta[1,2]),
          (2, (0,1,2,), delta[2,0]+delta[2,1]+delta[2,2]),
          (2,   (1,2,),            delta[2,1]+delta[2,2]),
          (2,     (2,),                       delta[2,2]),
          (3, (0,1,2,), delta[3,0]+delta[3,1]           ),
          (3,   (1,2,),            delta[3,1]           ),
          (3,     (2,),                                0),
        ]
        flat_sums_calculated = make_flat_sums(#n,k,
                                               delta)
        self.assertEqual(flat_sums_expected, flat_sums_calculated)

    def test_one_note_sorted_example(self):

        # am sneakily writing 0+ 0 for 0.00 to turn decimals into integers, just for testing. This is naughty as delta coords should be in [0,1] but it is OK for this test
        delta=Position_within_Simplex_Product([[0+ 0, 0+ 3, 0+22,],
                                               [0+00, 0+11, 0+10,],
                                               [0+10, 0+00, 0+50,],
                                               [0+ 1, 0+ 3, 0+20,]])

        flat_sums_expected = [
          (1,     (2,), 0+10), #                       delta[1,2]),
          (3,     (2,), 0+20), #                       delta[3,2]),
          (1,   (1,2,), 0+21), #            delta[1,1]+delta[1,2]),
          (1, (0,1,2,), 0+21), # delta[1,0]+delta[1,1]+delta[1,2]),
          (0,     (2,), 0+22), #                       delta[0,2]),
          (3,   (1,2,), 0+23), #            delta[3,1]+delta[3,2]),
          (3, (0,1,2,), 0+24), # delta[3,0]+delta[3,1]+delta[3,2]),
          (0,   (1,2,), 0+25), #            delta[0,1]+delta[0,2]),
          (0, (0,1,2,), 0+25), # delta[0,0]+delta[0,1]+delta[0,2]),
          (2,     (2,), 0+50), #                       delta[2,2]),
          (2,   (1,2,), 0+50), #            delta[2,1]+delta[2,2]),
          (2, (0,1,2,), 0+60), # delta[2,0]+delta[2,1]+delta[2,2]),
        ]
        flat_sums_calculated = make_flat_sums(delta, sort=True)
        self.assertEqual(flat_sums_expected, flat_sums_calculated)

class Test_c_dc_pair_generation(unittest.TestCase):
    def test(self):
        self.maxDiff=None

        delta=Position_within_Simplex_Product([
               [ 0, #0.00
                3, #0.03
               22,], #0.22
               [ 0, #0.00
               11, #0.11
               10,], #0.10
               [10, #0.10
                0, #0.00
               50,], #0.50
               [ 1, #0.01
                3, #0.03
               20,], #0.20
        ])

        c_dc_pairs_expected = [
                                 (Maximal_Simplex_Vertex({(0, 2), (1, 2), (2, 2), (3, 2)}), 10),
                                 (Maximal_Simplex_Vertex({(0, 2), (1, 1), (2, 2), (3, 2)}), 10),
                                 (Maximal_Simplex_Vertex({(0, 2), (1, 1), (2, 2), (3, 1)}), 1),
                                 (Maximal_Simplex_Vertex({(0, 2), (1, 0), (2, 2), (3, 1)}), 0),
                                 (Maximal_Simplex_Vertex({(0, 2), (2, 2), (3, 1)}), 1),
                                 (Maximal_Simplex_Vertex({(0, 1), (2, 2), (3, 1)}), 1),
                                 (Maximal_Simplex_Vertex({(0, 1), (2, 2), (3, 0)}), 1),
                                 (Maximal_Simplex_Vertex({(0, 1), (2, 2)}), 1),
                                 (Maximal_Simplex_Vertex({(0, 0), (2, 2)}), 0),
                                 (Maximal_Simplex_Vertex({(2, 2)}), 25),
                                 (Maximal_Simplex_Vertex({(2, 1)}), 0),
                                 (Maximal_Simplex_Vertex({(2, 0)}), 10),
                              ]

        c_dc_pairs_calculated = make_c_dc_pairs(delta)
        self.assertEqual(c_dc_pairs_expected, c_dc_pairs_calculated)

        for c, dc in c_dc_pairs_calculated:
            c.check_valid() # Will throw if bad!

class Test_simplex_eji_ordering_generation(unittest.TestCase):
    def test1(self):
        vertices = Maximal_Simplex_Vertices([
            Maximal_Simplex_Vertex({Eji(0, 2), Eji(1, 2), Eji(2, 2), Eji(3, 2)}),
            Maximal_Simplex_Vertex({Eji(0, 2), Eji(1, 1), Eji(2, 2), Eji(3, 2)}),
            Maximal_Simplex_Vertex({Eji(0, 2), Eji(1, 1), Eji(2, 2), Eji(3, 1)}),
            Maximal_Simplex_Vertex({Eji(0, 2), Eji(1, 0), Eji(2, 2), Eji(3, 1)}),
            Maximal_Simplex_Vertex({Eji(0, 2), Eji(2, 2), Eji(3, 1)}),
            Maximal_Simplex_Vertex({Eji(0, 1), Eji(2, 2), Eji(3, 1)}),
            Maximal_Simplex_Vertex({Eji(0, 1), Eji(2, 2), Eji(3, 0)}),
            Maximal_Simplex_Vertex({Eji(0, 1), Eji(2, 2)}),
            Maximal_Simplex_Vertex({Eji(0, 0), Eji(2, 2)}),
            Maximal_Simplex_Vertex({Eji(2, 2)}),
            Maximal_Simplex_Vertex({Eji(2, 1)}),
            Maximal_Simplex_Vertex({Eji(2, 0)}),
        ])
        vertices.check_valid()

        ordering_calculated = vertices.to_Eji_ordering()

        ordering_expected = Eji_Ordering([
            Eji(1, 2),
            Eji(3, 2),
            Eji(1, 1),
            Eji(1, 0),
            Eji(0, 2),
            Eji(3, 1),
            Eji(3, 0),
            Eji(0, 1),
            Eji(0, 0),
            Eji(2, 2),
            Eji(2, 1),
            Eji(2, 0),
        ])
        ordering_expected.check_valid()

        self.assertEqual(ordering_calculated, ordering_expected)

class TestSimplexPositions(unittest.TestCase):
        def test_pos_within_simplex(self):
            aBad = Position_within_Simplex([2, 2, 3])
            self.assertRaises(Exception, aBad.check_valid)

            a = Position_within_Simplex([0.1, 0.25, 0.15])
            a.check_valid()

            b = Position_within_Simplex(np.array([0.5, 0.25, 0.25]))
            b.check_valid()
            self.assertEqual(b, Position_within_Simplex([0.5, 0.25, 0.25])) # Not using np.array

            c = Position_within_Simplex([1.0/3.0, 1.0/3.0, 1.0/3.0])
            c.check_valid()

            dBad = Position_within_Simplex([0, -0.23, 0])
            self.assertRaises(Exception, dBad.check_valid)

            big_1 = Position_within_Simplex_Product([b, c, a, a, b])
            big_1.check_valid()

            self.assertEqual(big_1[0], b)
            self.assertEqual(big_1[1], c)
            self.assertEqual(big_1[2], a)
            self.assertEqual(big_1[3], a)
            self.assertEqual(big_1[4], b)

            big_2 = Position_within_Simplex_Product([[0.1, 0.2], [0.3, 0.11]])
            self.assertEqual(big_2[0], Position_within_Simplex([0.1, 0.2]))
            self.assertEqual(big_2[1], Position_within_Simplex([0.3, 0.11]))
            self.assertEqual(big_2[0, 0], 0.1)
            self.assertEqual(big_2[0, 1], 0.2)
            self.assertEqual(big_2[1, 0], 0.3)
            self.assertEqual(big_2[1, 1], 0.11)

            big_3 = Position_within_Simplex_Product([b, c, b, b, dBad])
            self.assertRaises(Exception, big_3.check_valid)

class Test_perm_detection(unittest.TestCase):
    def test(self):

        simplex_eji_ordering = Eji_Ordering(
            [(1, 2), (3, 2), (1, 1), (0, 2), (3, 1), (3, 0), (0, 1), (1, 0), (0, 0), (2, 2), (2, 1), (2, 0)])
        simplex_eji_canonical_ordering_expected = Eji_Ordering(
            [(0, 2), (1, 2), (0, 1), (2, 2), (1, 1), (1, 0), (2, 1), (0, 0), (2, 0), (3, 2), (3, 1), (3, 0)])

        simple_ordering_on_j_vals_from_left_expected = [ 1, 3, 0, 2 ] # j vals read from left, ignoring repeats
        simple_ordering_on_j_vals_from_right_expected = [ 2, 0, 1, 3 ] # j vals read from right, ignoring repeats

        ordering_from_left_calculated = simplex_eji_ordering.get_j_order()
        ordering_from_right_calculated = simplex_eji_ordering.get_j_order(from_right=True)

        self.assertEqual(simple_ordering_on_j_vals_from_left_expected, ordering_from_left_calculated)
        self.assertEqual(simple_ordering_on_j_vals_from_right_expected, ordering_from_right_calculated)

        simplex_eji_canonical_ordering_calculated = simplex_eji_ordering.get_canonical_form()
        self.assertEqual(simplex_eji_canonical_ordering_calculated,simplex_eji_canonical_ordering_expected)

class Test_canonicalisation_and_MSV(unittest.TestCase):
    def test(self):
        v = Maximal_Simplex_Vertex({Eji(2,3), Eji(1,5), Eji(4,2)})
        v_canonical_expected = Maximal_Simplex_Vertex({Eji(0,2), Eji(1,3), Eji(2,5)})
        v_canonical_calculated = v.get_canonical_form()
        self.assertEqual(v_canonical_expected, v_canonical_calculated)

        vBad = Maximal_Simplex_Vertex({Eji(2,3), Eji(2,5), Eji(4,2)}) # Bad since 2 repeats in the j
        self.assertRaises(Exception, vBad.check_valid)

def run_unit_tests():
    unittest.main(exit=False)

if __name__ == "__main__":
    run_unit_tests()
