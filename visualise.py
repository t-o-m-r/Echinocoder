# Unomment one of the next few lines to select the encoder to use:

#from Cinf_numpy_polynomial_encoder_for_array_of_reals_as_multiset import Encoder
# from Cinf_sympy_bursar_encoder_for_array_of_reals_as_multiset import encode
from Historical.C0_simplicialComplex_encoder_1_for_array_of_reals_as_multiset import Encoder
# from C0HomDeg1_simplicialComplex_encoder_1_for_array_of_reals_as_multiset import Encoder





###############################################################################

from functools import lru_cache
from cProfile import label

import numpy as np
from bokeh.io import curdoc
from iwpc.scalars.scalar import Scalar
from iwpc.scalars.scalar_function import ScalarFunction
from iwpc.visualise.bokeh_function_visualiser_2D import BokehFunctionVisualiser2D


def make_input_scalars(n, k):
    scalars = []
    for i in range(n):
        for j in range(k):
            scalars.append(Scalar(f"Vector {i} feature {j}", bins=np.linspace(-5, 5, 100)))
    return scalars


def bla(x, i):
    # print(x)
    return x[:, i]


def make_output_scalars(R):
    return [
        ScalarFunction(
            lambda x, i=i: bla(x, i),
            label=f"Output {i}"
        ) for i in range(R)
    ]


n = 3
k = 2

encoder = Encoder()

big_n_for_encoding = encoder.size_from_n_k(n,k)

def evaluate_encoding(x, n, k):

    #print("Cache test")
    if evaluate_encoding.last_x is not None and len(x)==len(evaluate_encoding.last_x):
        if (x==evaluate_encoding.last_x).all() and (n==evaluate_encoding.last_n) and (k==evaluate_encoding.last_k):
            # We hit the cache!
            #print("Cache hit")
            return evaluate_encoding.last_ret
        else:
            #print("Cache fail")
            pass

    outs = []
    for sample in x:
        sample = sample.reshape(n, k)
        encoding = np.asarray(encoder.encode(sample), dtype=float)
        assert len(encoding) == big_n_for_encoding
        outs.append(encoding)

    evaluate_encoding.last_x = x.copy()
    evaluate_encoding.last_n = n
    evaluate_encoding.last_k = k
    evaluate_encoding.last_ret = np.asarray(outs)

    return evaluate_encoding.last_ret

evaluate_encoding.last_x=None
evaluate_encoding.last_n=None
evaluate_encoding.last_k=None
evaluate_encoding.last_outs=None

bokeh_vis = BokehFunctionVisualiser2D(
    lambda x: evaluate_encoding(x, n, k),
    make_input_scalars(n, k),
    make_output_scalars(big_n_for_encoding),
    center_point=10 * (np.random.random(size=n * k) - 0.5),
    panel_1d_kwargs={'use_points': True},
    use_points_for_xsecs=True,
)
curdoc().add_root(bokeh_vis.root)
