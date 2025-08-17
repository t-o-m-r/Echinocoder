import sympy as sp

def strip_zero_rows(M: sp.Matrix) -> sp.Matrix:
    """Return a copy of M with all-zero rows removed."""
    nonzero_rows = [i for i in range(M.rows) if any(M[i, j] != 0 for j in range(M.cols))]
    return M[nonzero_rows, :]

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
