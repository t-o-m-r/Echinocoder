class Equivalent_Places:
    """
        When generating matches, some match places maye be equivalent in the present context,
        while others may not be.
        E.g. if no symmetry among three places has yet been broken (like in the word "aaa") 
        then it may be sufficient to consider just the matches:
            (+1, +1, -1)
            (-1,  0,  0)
        however if only the first two places are equivalent (like in the word "ooh") 
        then these matches are all different:
            (+1, +1, -1)
            ( 0, -1,  0)
            (-1,  0,  0).
        If all places are distinct (like in the word "cow") then you would need:
            (+1, +1, -1)
            (+1, -1, +1)
            (-1, +1, +1)
            ( 0,  0, -1)
            ( 0, -1,  0)
            (-1,  0,  0).
        The argument "equivalent_places" (when not None) should be something which specifies which places
        are equivalent and which are not. 

        We would do this two ways:

        ======================================================
        Way 1: The SIMPLE_TO_GENERATE but MESSY way:
        ======================================================

        In this case equivalent_places could be an iterable over the
        collections of equivalent places.
        E.g. if the equivalence was as in the word "Cabbage" then a suitable value for
        equivalent_places could be constructed like this:
        d = {
         "a" : (1,4,),
         "b" : (2,3,),
         "C" : (0,),
         "g" : (5,),
         "e" : (6,)
        } # Dictionary for "Cabbage"
        equivalent_places = d.values() = [ (1,4,), (2,4,), (0,), (5,), (6,) ] # (or similar)

        There are two "special cases" for which the user may benefit from some shortcuts, namely:

        NONE: equivalent_places = tuple( (i,) for i in range(len(data)) ) # No places are equivalent (i.e all are different).
        ALL:  equivalent_places = ( tuple(range(len(data))), )            # All places are equivalent (i.e. none are different).

        While easy to make, this is annoying because most of the code will likely live in a region where many points are inequivalent, at which point the representation is a LONG tupe of tuples MOST OF WHICH have only one element in them. (And since (6,) is not the same as (6) errors could arise easily.) Furthermore, in recurisve methods these long structurs may have to be copied and modified repeadedly with depth while always getting longer the deeper in the stack. Not good.

        ======================================================
        Way 2: The HARDER_TO_GENERATE but MORE ELEGANT WAY
        ======================================================

        Like Way 1, except that:

            (a) tuples containing only a single object can (or should?) be omitted from the list, and
            (b) None and All can both be represented in universe now. 

        E.g. "Cabbage" could be represented by:

        d = {
         "a" : (1,4,),
         "b" : (2,3,),
        } # Dictionary for "Cabbage" only looking at repeats!
        equivalent_places = d.values() = [ (1,4,), (2,4,), ] # (or similar)

        while the special case values would become:

        NONE: equivalent_places = tuple()                      # No places are equivalent (i.e All are different).
        ALL:  equivalent_places = ( tuple(range(len(data))), ) # All places are equivalent (i.e. none are different).

        In the limit of complex code with many places inequivalent, this may possibly be the faster more economical, since the deeper in the stack one gets (increasingly inequivalent places) the shorter will the representation become. However, that's guess work.

        ====

        We select Way 2 for the internal representation.

        """

    def  __init__(self, size=None, all_equivalent=False, none_equivalent=False, equivalents_with_singletons=None, equivalents_without_singletons=None):
        """ Initialise in ONE of the following ways.  Any other initialisation is an error.

           (1) specify size (non-negative int) and all_equivalent=True
           (2) specify size (non-negative int) and none_equivalent=True
           (3) specify equivalents_with_singletons like this (Way 1 above) for "Cabbage": # TODO: Remove this option in the long term
                 d = {
                  "a" : (1,4,),
                  "b" : (2,3,),
                  "C" : (0,),
                  "g" : (5,),
                  "e" : (6,)
                 } # Dictionary for "Cabbage"
                 equivalents_with_singletons = d.values() = [ (1,4,), (2,4,), (0,), (5,), (6,) ] # (or similar).
                 Note that size can (and will) be deduced from this input. You can optionally specifiy size to allow an inconsistency check.
           (4) specify size and equivalents_without_singletons like this (Way 2 above) for "Cabbage":
                 d = {
                  "a" : (1,4,),
                  "b" : (2,3,),
                 } # Dictionary for "Cabbage"
                 equivalents_with_singletons = d.values() = [ (1,4,), (2,4,), (0,), (5,), (6,) ] # (or similar).
        """
        if size is not None and none_equivalent==True:
            self._equivalent_places_with_singletons = tuple( (i,) for i in range(size) ) # No places are equivalent (i.e all are different). # Way 1 # TODO: remove in long term
            self._equivalent_places_without_singletons = tuple() # No places are equivalent (i.e All are different). # Way 2
            self.size = size
            return

        if size is not None and all_equivalent==True:
            self._equivalent_places_with_singletons = ( tuple(range(size)), ) # All places are equivalent (i.e. none are different). # Way 1 # TODO: remove in long term
            self._equivalent_places_without_singletons = ( tuple(range(size)), ) # All places are equivalent (i.e. none are different). # Way 2
            self.size = size
            return
    
        # TODO: Remove construction method in long term
        if equivalents_with_singletons is not None:
            self._equivalent_places_with_singletons = tuple( i for i in equivalents_with_singletons ) # TODO: remove in long term
            self._equivalent_places_without_singletons = tuple( i for i in self._equivalent_places_with_singletons if len(i)>1 )
            self.size = max((max(i)+1 for i in self._equivalent_places_with_singletons), default=0) # Don't need to protect inner max as all should be at least singleton size.
            assert (size is None or self.size == size)
            return

        if equivalents_without_singletons is not None and size is not None:
            self._equivalent_places_without_singletons = tuple( i for i in equivalents_without_singletons )
            seen = tuple(i for tup in self._equivalent_places_without_singletons for i in tup)
            self._equivalent_places_with_singletons = self._equivalent_places_without_singletons + tuple((i,) for i in range(size) if i not in seen) # TODO: remove in long term
            self.size = size
            return

        raise ValueError()

    def __repr__(self):
        return f"EQUIVALENT_PLACES(size={self.size},\nwithout_singletons={self._equivalent_places_without_singletons},\nwith_singletons={self._equivalent_places_with_singletons}\n)"

def demo():

    all_3  = Equivalent_Places(size=3, all_equivalent=True)
    none_4 = Equivalent_Places(size=4, none_equivalent=True)
    mid_5a = Equivalent_Places(        equivalents_with_singletons    = ( (1,2), (3,0), (4,),       ))
    mid_5b = Equivalent_Places(size=5, equivalents_without_singletons = ( (1,2), (3,0),             ))

    mid_6a = Equivalent_Places(        equivalents_with_singletons    = ( (1,2), (5,0), (4,), (3,), ))
    mid_6b = Equivalent_Places(size=6, equivalents_without_singletons = ( (1,2), (5,0),             ))
    print("All 3",all_3)
    print("None 4", none_4)
    print("Mid_5a",mid_5a)
    print("Mid 5b", mid_5b)
    print("Mid_6a",mid_6a)
    print("Mid 6b", mid_6b)
    
if __name__ == "__main__":
    demo()

    
