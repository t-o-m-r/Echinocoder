# Encode list of real  numbers treated as multiset.
# E.g. this method can encode things like:
#
#        [3,4,-2,]
#
# representing the multiset
#
#        {{ 3,4,-2, }}
#
# into
#
#        [-2, 3, 4].

name="C0_sorting_encoder_for_lists_of_reals_as_multiset"

def encode(data):
    return sorted(data)
