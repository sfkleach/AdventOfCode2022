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


DIRECTIONS = {
    "R": Vector(1, 0),
    "L": Vector(-1, 0),
    "U": Vector(0, 1),
    "D": Vector(0, -1)
}


class LongRope:

    def __init__( self, nknots=2 ):
        assert( nknots >= 2 )
        self._head = Vector(0,0)
        self._knots = []
        for _ in range( 0, nknots-1 ):
            self._knots.append( Vector(0,0) )

    def head( self ):
        return self._head
    
    def tail( self ):
        return self._knots[-1]

    @staticmethod
    def isStretched( vector ):
        """This is just a hackish way of checking that neither x nor y >= 2"""
        return vector.mag2() > 2

    def goSelf( self, dirn ):
        """Updates in-place"""
        dv = DIRECTIONS[ dirn ]
        self._head = self._head + dv
        prev_knot = self._head
        for n, knot in enumerate( self._knots ):
            delta = prev_knot - knot
            if not LongRope.isStretched( delta ):
                # If it isn't stretched we don't need to bother with the remainder of the 'worm'.
                break
            prev_knot = knot + delta.normalise()
            self._knots[ n ] = prev_knot
        return self
    
    def tailTrace( self, commands ):
        rope = self
        yield rope.tail()
        for c in commands:
            for _ in range( 0, c[1] ):
                rope = rope.goSelf( c[0] )
                yield rope.tail()


def readRopeCommandFile( fname ):
    with open( fname, 'r' ) as file:
        for line in file:
            ( d, n ) = line.strip().split()            
            yield d, int( n )

