import sympy as sp
from functools import partial
from vertex_matches import generate_viable_vertex_match_matrices

def demo():
    print("== Test of Matrix Generation =========")

    def max_row_requirement(mat, max_rows):
        return sp.shape(mat)[0] <= max_rows

    def f(mat):
        return sp.shape(mat)[0] <= 4 # True if mat has 4 or fewer rows.

    mat_gen = generate_viable_vertex_match_matrices(
        M=5,
        k=2,
        # All of the next three lines have the same effect, but different pros/cons.
        # Try changing which one(s) is(are) commented out.
        #yield_matrix = partial(max_row_requirement, max_rows=4),
        #go_deeper = partial(max_row_requirement, max_rows=3), # fastest option, where possible
        yield_matrix = f,
        ) 

    for i, mat in enumerate(mat_gen):
        print(i, mat)

if __name__ == "__main__":
    demo()
