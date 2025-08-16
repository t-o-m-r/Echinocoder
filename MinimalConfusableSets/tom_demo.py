import sympy as sp
from functools import partial
from vertex_matches import generate_viable_vertex_match_matrices
from sympy_tools import strip_zero_rows, some_row_causes_collapse

def demo():

    def max_row_requirement(mat, max_rows):
        return sp.shape(mat)[0] <= max_rows

    def f(mat: sp.Matrix):
        return sp.shape(mat)[0] <= 5 # True if mat has 4 or fewer rows.

    #def matrix_is_not_definitely_bad(mat: sp.Matrix, k:int):
    #    rre, _ = mat.rref()
    #    if some_row_causes_collapse(rre, k):
    #        #print("Some row causes collapse!")
    #        return False # Matrix is bad!!

    #    # Let's now strip the zero rows and make the R-rre hashable
    #    rre = sp.ImmutableMatrix(strip_zero_rows(rre))

    #    return True # Can't say that matrix is bad, yet!

    for M,k in (
            #(5,4),
            (7,4),
            #(7,3),
            #(7,2),
            #(9,4),
            #(11,4),
            #(13,4),
            #(15,4),
        ):
        print( "====================================================================")
        print(f"For M={M} and k={k} the not obviously bad vertex match matrices are:")
        print( "--------------------------------------------------------------------")

        mat_gen = generate_viable_vertex_match_matrices(
            M=M,
            k=k,
            return_mat = True,
            return_hashable_rre = True,
            # yield_matrix = partial(max_row_requirement, max_rows=4),
            # go_deeper = partial(max_row_requirement, max_rows=3), # fastest option, where possible
            # yield_matrix = partial(matrix_is_not_definitely_bad, k=k),
            )
        
        from collections import defaultdict 
        mat_lists = defaultdict(list)
        for i, (mat,rre) in enumerate(mat_gen):
            print(f"    {i} raw={mat}, rre={rre}")
            mat_lists[rre].append(mat)
        
        number_enumerated = i+1
        print(f"There were {len(mat_lists)} distinct rre's from {number_enumerated} enumerated.")

        print(f"Those {number_enumerated-len(mat_lists)} which were repeated were:")
        for rre,mat_list in ((r,m) for r,m in mat_lists.items() if len(m)>1):
            print(f"{rre}:",)
            for mat in mat_list:
                print("   L--    ", repr(mat))
               
        

        print("====================================================================")
        print()
        print()

if __name__ == "__main__":
    demo()
