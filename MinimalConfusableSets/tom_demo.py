import sympy as sp
from functools import partial
from vertex_matches import generate_viable_vertex_match_matrices
from sympy_tools import strip_zero_rows, some_row_causes_collapse
import decider_functions.decider_function as df








#########################################################

def demo():
    print("== Test of Matrix Generation =========")

    def max_row_requirement(mat, max_rows):
        return sp.shape(mat)[0] <= max_rows

    def f(mat):
        return sp.shape(mat)[0] <= 4 # True if mat has 4 or fewer rows.

    mat_gen = generate_viable_vertex_match_matrices(
        M=M,
        k=k,
        # All of the next three lines have the same effect, but different pros/cons.
        # Try changing which one(s) is(are) commented out.
        #yield_matrix = partial(max_row_requirement, max_rows=4),
        #go_deeper = partial(max_row_requirement, max_rows=3), # fastest option, where possible
        yield_matrix = f,
        )

    return(mat_gen)


class Decider:
    def __init__(self, M, k, method="electrostatic", iters = 500, learning_rate = 0.01, power = 2.0, sample = 'rr', spread = 'gauss'):
        self.M = M
        self.k = k

        # prepare bad bats once. Arguments explained in decider_function
        self.B = df.prepare_B(k=k, M=M, method=method, iters = iters, learning_rate = learning_rate, power = power, sample = sample, spread = spread)

    def matrix_does_not_collapse(self, L_matrix : sp.Matrix):
         # The decide_collapse function below returns False on Collapse, True otherwise.
         ans = df.decide_collapse(L_matrix, self.B, num_trials=1000, tol=1e-12)
         if ans:
            print("Allowing")
         else:
            print(f"VETO !!!!!!!!! {L_matrix}")
         return ans

    def function_factory(self):
        return lambda mat : self.matrix_does_not_collapse(mat)

#########################################################



def demo():

    def max_row_requirement(mat, max_rows):
        return sp.shape(mat)[0] <= max_rows

    def f(mat: sp.Matrix):
        return sp.shape(mat)[0] <= 5 # True if mat has 4 or fewer rows.

 

    for M,k in (
            #(5,4),
            (7,4),
            #(7,3),
            ##(7,2),
            #(9,4),
            #(11,4),
            #(13,4),
            #(15,4),
        ):
        print( "====================================================================")
        print(f"For M={M} and k={k} the not obviously bad vertex match matrices are:")
        print( "--------------------------------------------------------------------")

        collapse_checker = Decider(M=M, k=k)
        collapse_checking_function = collapse_checker.function_factory()

        mat_gen = generate_viable_vertex_match_matrices(
            M=M,
            k=k,
            return_mat = True,
            return_hashable_rre = True,
            remove_duplicates_via_hash = True,
            yield_matrix = collapse_checking_function,
            # yield_matrix = partial(max_row_requirement, max_rows=4),
            # go_deeper = partial(max_row_requirement, max_rows=3), # fastest option, where possible
            # yield_matrix = partial(matrix_is_not_definitely_bad, k=k),
            )
        
        for i, (mat,rre) in enumerate(mat_gen):
            print(f"    {i} raw={mat}, rre={rre}")
        
        number_enumerated = i+1
        print(f"There were {number_enumerated} found.")

        print("====================================================================")
        print()
        print()

if __name__ == "__main__":
    demo()
