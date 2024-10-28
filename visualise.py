from cProfile import label

import numpy as np
from bokeh.io import curdoc
from iwpc.scalars.scalar import Scalar
from iwpc.scalars.scalar_function import ScalarFunction
from iwpc.visualise.bokeh_function_visualiser_2D import BokehFunctionVisualiser2D

from C0_good1_numpy_simplicialComplex_encoder_for_array_of_reals_as_multiset import encode
#from C0_bug2_numpy_simplicialComplex_encoder_for_array_of_reals_as_multiset import encode


def make_input_scalars(n, m):
    scalars = []
    for i in range(n):
        for j in range(m):
            scalars.append(Scalar(f"Vector {i} feature {j}", bins=np.linspace(-10, 10, 100)))
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


def evaluate_encoding(x, n, m):
    outs = []
    for sample in x:
        sample = sample.reshape(n, m)
        outs.append(encode(sample))
    return np.asarray(outs)


n = 3
m = 2

bokeh_vis = BokehFunctionVisualiser2D(
    lambda x: evaluate_encoding(x, n, m),
    make_input_scalars(n, m),
    make_output_scalars(2*n*m + 1),
    center_point=20 * (np.random.random(size=n * m) - 0.5),
    panel_1d_kwargs={'use_points': True},
    use_points_for_xsecs=True,
)
curdoc().add_root(bokeh_vis.root)
