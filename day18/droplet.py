
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

def readDroplet( file ):
    for line in file:
        yield tuple( int(d) for d in line.strip().split(',') )

def readDropletFile( fname ):
    with open( fname, 'r' ) as file:
        return Droplet( readDroplet( file ) )
