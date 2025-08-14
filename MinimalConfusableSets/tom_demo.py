import sympy as sp
from functools import partial
from vertex_matches import generate_viable_vertex_match_matrices

def demo():
    print("== Test of Matrix Generation =========")

    def max_row_requirement(mat, max_rows):
        return sp.shape(mat)[0] <= max_rows

    def f(mat: sp.Matrix):
        return sp.shape(mat)[0] <= 5 # True if mat has 4 or fewer rows.

    def some_row_causes_collapse(mat: sp.Matrix, k: int):
            """
            Return True if there exists a row in M that has:
            - at least one non-zero entry, and
            - fewer than k+1 non-zero entries.
            """
            k_plus_1 = k+1
            rows, cols = mat.shape
            for r in range(rows):
                nonzero_count = 0
                for c in range(cols):
                    if mat[r, c] != 0:
                        nonzero_count += 1
                        if nonzero_count == k_plus_1:
                            # This row is a good row as it has >= k+1 non-zero entries.
                            break # i.e. stop scanning the columns of this row!
                # We reached the end of the row, so assess what to do:
                if 1 <= nonzero_count < k_plus_1:
                    return True #  This is a bad row! It has a number of non-zero entreis in {1, 2, ... , k}
                assert nonzero_count==0 or nonzero_count==k_plus_1
                # This row was good, so try the next row.
            # We finished trying rows, so if we got here all rows are good!
            return False

    def matrix_is_not_definitely_bad(mat: sp.Matrix, k:int):
        rre, _ = mat.rref()
        #print("inside mat", mat)
        #print("inside rre", rre)
        if some_row_causes_collapse(rre, k):
            #print("Some row causes collapse!")
            return False # Matrix is bad!!

        return True # Can't say that matrix is bad, yet!

    M=5
    k=4
    mat_gen = generate_viable_vertex_match_matrices(
        M=M,
        k=k,
        # All of the next three lines have the same effect, but different pros/cons.
        # Try changing which one(s) is(are) commented out.
        #yield_matrix = partial(max_row_requirement, max_rows=4),
        #go_deeper = partial(max_row_requirement, max_rows=3), # fastest option, where possible
        yield_matrix = partial(matrix_is_not_definitely_bad, k=k),
        ) 

    for i, mat in enumerate(mat_gen):
        print("outside", i, mat.rref())

if __name__ == "__main__":
    demo()
