from decider_function import generate_electrostatic, generate_sobol

def test_electrostatic():
    B1 = generate_electrostatic(M=6, k=2, iters=500, learning_rate=0.01, power=2.0)
    B2 = generate_electrostatic(M=50, k=2, iters = 500, learning_rate= 0.01, power= 2.0)
    B3 = generate_electrostatic(M=50, k=5, iters = 500, learning_rate= 0.01, power= 2.0)
    for combo in itertools.combinations(range(M), k):
            for B in [B1, B2, B3]:
                matrix = B[list(combo), :]   # shape (k, k)
                det = np.linalg.det(matrix)
                assert abs(det) < tol, "Bad bats not lin ind"
                
    
