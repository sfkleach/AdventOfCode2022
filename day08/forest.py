from operator import mul
from functools import reduce

def directions():
    yield ( 1, 0 )
    yield ( 0, 1 )
    yield ( -1, 0 )
    yield ( 0, -1 )

def product( iterable ):
    return reduce( mul, iterable, 1 )    

class Tree:

    def __init__( self, height ):
        self._height = height
        self._forest = None
        self._location = None
        self._can_see = {}
        self._max = {}

    def height( self ):
        return self._height

    def youAreHere( self, forest, row, col ):
        self._forest = forest
        self._rowcol = ( row, col )

    def step( self, inc_row, inc_col ):
        ( row, col ) = self._rowcol
        return self._forest.get( row + inc_row, col + inc_col )

    def travel( self, delta_row, delta_col ):
        e = self
        while True:
            e = e.step( delta_row, delta_col )
            if e:
                yield e   
            else:
                return

    def viewDistDirn( self, delta_rowcol ):
        """Viewing distance in a given direction"""
        d = 0
        for t in self.travel( *delta_rowcol ):
            d += 1
            if t.height() >= self.height():
                break
        return d

    def scenicScore( self ):
        return product( self.viewDistDirn(d) for d in directions() )

    def maxDirn( self, delta_rowcol ):
        if delta_rowcol not in self._max:
            neighbour = self.step( *delta_rowcol )
            if neighbour:
                # print( self.height(), 'vs', neighbour.height() )
                self._max[ delta_rowcol ] = max( neighbour.height(), neighbour.maxDirn( delta_rowcol ) )
            else:
                # print( 'no neighbour' )
                self._max[ delta_rowcol ] = -1
        return self._max[ delta_rowcol ]

    def canSeeDirn( self, delta_rowcol ):
        return self.height() > self.maxDirn( delta_rowcol )

    def isVisible( self ):
        return any( self.canSeeDirn( d ) for d in directions() )

class Forest:

    def __init__( self ):
        self._rows = []

    def add( self, trees ):
        for ( ncol, t ) in enumerate( trees ):
            t.youAreHere( self, len( self._rows ), ncol )
        self._rows.append( trees )

    def get( self, row, col ):
        # print( 'get', row, col )
        if row < 0 or col < 0:
            return None
        try:
            return self._rows[ row ][ col ]
        except IndexError:
            return None

    def trees( self ):
        for row in self._rows:
            yield from row 

def readForestFile( fname ):
    forest = Forest()
    with open( fname, 'r' ) as file:
        for line in file:
            forest.add( tuple( Tree( height ) for height in map( int, line.strip() ) ) )
    return forest
                