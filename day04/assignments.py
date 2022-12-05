
class SectionRange:

    def __init__( self, lo, hi ):
        self._lo = lo
        self._hi = hi

    def toTuple( self ):
        return ( self._lo, self._hi )

    def isWithin( self, other ):
        return ( other._lo <= self._lo ) and ( self._hi <= other._hi )
    
    def isFullyOverlapping( self, other ):
        return self.isWithin( other ) or other.isWithin( self )

    def isPartlyOverlapping( self, other ):
        return not( self._hi < other._lo or other._hi < self._lo )


def readAssignmentsFile( fname ):
    with open( fname, 'r' ) as file:
        for line in file:
            ( lhs, rhs ) = ( SectionRange( *( int( j ) for j in i.split( '-' ) ) ) for i in line.strip().split( ',' ) )
            yield ( lhs, rhs )

