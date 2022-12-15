class Vector:
    """Immutable pair of ints that can be treated as 2D coords or vectors"""

    def __init__( self, x, y ):
        self._x = x
        self._y = y

    # Define both __eq__ and __hash__ so we can make sets of these.
    def __eq__( self, other ):
        return self._x == other._x and self._y == other._y

    def __hash__( self ):
        return self._x.__hash__() ^ self._y.__hash__()

    def x( self ):
        return self._x

    def y( self ):
        return self._y

    def __repr__( self ):
        return f"<{self._x}, {self._y}>"

    def __add__( self, other ):
        return Vector( self._x + other._x, self._y + other._y )

    def __neg__( self ):
        return Vector( -self._x, -self._y )

    def __sub__( self, other ):
        return -other + self

    @staticmethod
    def sign( x ):
        return 1 if x > 0 else -1 if x < 0 else 0

    def normalise( self ):
        """It is purely coincidental that the limit function is effectively the same as sign"""
        return Vector( Vector.sign( self._x ), Vector.sign( self._y ) )

    def mag2( self ):
        """The magnitude of the vector (or equally the distance from the origin)"""
        return self._x ** 2 + self._y ** 2

    def manhattan( self ):
        """The Manhattan distance from the origin"""
        return abs( self._x ) + abs( self._y )
