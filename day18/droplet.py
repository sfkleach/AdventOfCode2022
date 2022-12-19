
class Droplet:

    def __init__( self, cubes ):
        self._cubes = set( cubes )

    def surfaceArea( self ):
        total = 0
        for (a, b, c) in self._cubes:
            total += sum((
                ( a+1, b, c ) not in self._cubes,
                ( a-1, b, c ) not in self._cubes,
                ( a, b+1, c ) not in self._cubes,
                ( a, b-1, c ) not in self._cubes,
                ( a, b, c+1 ) not in self._cubes,
                ( a, b, c-1 ) not in self._cubes
            ))
        return total

    def bounds( self ):
        return(
            ( min( a for (a, b, c) in self._cubes ) - 1, max( a for (a, b, c) in self._cubes ) + 1 ),
            ( min( b for (a, b, c) in self._cubes ) - 1, max( b for (a, b, c) in self._cubes ) + 1 ),
            ( min( c for (a, b, c) in self._cubes ) - 1, max( c for (a, b, c) in self._cubes ) + 1 )
        )

    @staticmethod
    def inBounds( cube, bounds ):
        ( (alo, ahi), (blo, bhi), (clo, chi) ) = bounds
        ( a, b, c ) = cube
        return (
            alo <= a <= ahi and
            blo <= b <= bhi and
            clo <= c <= chi
        )

    def outside( self, cube, enclosure ):
        if cube in enclosure:
            return enclosure[ cube ] == 1
        else:
            return False

    def exterior( self ):
        ( alim, blim, clim ) = ( bounds := self.bounds() )
        enclosure = {}
        for cube in self._cubes:
            enclosure[ cube ] = 0
        flood = [ ( alim[0], blim[0], clim[0] ) ]
        while flood:
            cube = flood.pop()
            if cube not in enclosure and self.inBounds( cube, bounds ):
                enclosure[ cube ] = 1
                ( a, b, c ) = cube
                flood.extend((
                    ( a+1, b, c ),
                    ( a-1, b, c ), 
                    ( a, b+1, c ), 
                    ( a, b-1, c ), 
                    ( a, b, c+1 ), 
                    ( a, b, c-1 ) 
                ))
        total = 0
        for (a, b, c) in self._cubes:
            total += sum((
                self.outside( ( a+1, b, c ), enclosure ),
                self.outside( ( a-1, b, c ), enclosure ),
                self.outside( ( a, b+1, c ), enclosure ),
                self.outside( ( a, b-1, c ), enclosure ),
                self.outside( ( a, b, c+1 ), enclosure ),
                self.outside( ( a, b, c-1 ), enclosure )
            ))
        return total           

def readDroplet( file ):
    for line in file:
        yield tuple( int(d) for d in line.strip().split(',') )

def readDropletFile( fname ):
    with open( fname, 'r' ) as file:
        return Droplet( readDroplet( file ) )
