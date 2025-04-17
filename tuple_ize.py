from numpy import array

def tuple_ize(a):
    """
    to_tuple turns numpy arrays (of any dimension or shape) into tuple arrays to make them hashable.

    Some examples of what should convert to what are given in to_tuple
    """

    if a.shape == ():
        return a.item()
    else:
        return tuple(map(tuple_ize, a))


tuple_ize.unit_test_input_output_pairs = [
     (   array([1,2,5]),    (1,2,5)   ),
     (   array([[1,2],[5,6]]),    ((1,2),(5,6))   ),
     (   array([[[1],[2]],[[5],[6]]]),    (((1,),(2,)),((5,),(6,)))   ),
     (   array([]),    tuple()   ),
     (   array([[],[]]),    ((),(),)   ),
     (   array([[[],],[[],]]),    (((),),((),))   ),
   ]
