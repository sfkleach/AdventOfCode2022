from operator import mul
from functools import reduce

def directions():
    """Directions are represented by a pair of (row, column) increments"""
    return ( ( 1, 0 ), ( 0, 1 ), ( -1, 0 ), ( 0, -1 ) )

def product( iterable ):
    """Finds the multiplicative product of a sequence of numbers"""
    return reduce( mul, iterable, 1 )    

class Tree:

    def __init__( self, forest, rowcol, height ):
        self._height = height
        self._forest = forest
        self._rowcol = rowcol
        self._max_cache = {}

    def height( self ):
        return self._height

    def neighbour( self, inc_row, inc_col ):
        """Finds the neighbouring tree in a given direction"""
        ( row, col ) = self._rowcol
        return self._forest.get( row + inc_row, col + inc_col )

    def travel( self, delta_row, delta_col ):
        """Iterates across the neighbours in a given direction"""
        e = self
        while True:
            e = e.neighbour( delta_row, delta_col )
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

    # It's fairly obvious that this calculation benefits from caching, as long
    # as it is rewritten to exploit the cache. In practice, for the relatively
    # small input grid, caching is not essential. But I include both versions
    # out of interest.
    def maxInDirection( self, delta_rowcol ):
        """Max tree height, excluding self, in a given direction. -1 if no trees."""
        return max( ( t.height() for t in self.travel( *delta_rowcol ) ), default=-1 )

    # Same as maxInDirection but rewritten to exploit caching.
    def maxInDirectionCached( self, delta_rowcol ):
        """Max tree height, excluding self, in a given direction. -1 if no trees."""
        if delta_rowcol not in self._max_cache:
            neighbour = self.neighbour( *delta_rowcol )
            if neighbour:
                d = max( neighbour.height(), neighbour.maxInDirectionCached( delta_rowcol ) )
                self._max_cache[ delta_rowcol ] = d
            else:
                self._max_cache[ delta_rowcol ] = -1
        return self._max_cache[ delta_rowcol ]

    def canSeeInDirection( self, delta_rowcol ):
        """True if you can see to the edge of the forest in a given direction"""
        return self.height() > self.maxInDirectionCached( delta_rowcol )

    def isVisible( self ):
        """True if you can see to the edge of the forest in any direction"""
        return any( self.canSeeInDirection( d ) for d in directions() )

class Forest:
    """A rectangular array of trees"""

    def __init__( self ):
        self._rows = []         # Each row is a list of trees.

    def add( self, heights ):
        """Adds a row of trees of given heights"""
        trees = []
        row = len( self._rows ) # Before we add the new row of trees.
        self._rows.append( trees )
        for col, h in enumerate( heights ):
            trees.append( Tree( self, ( row, col ), h ))

    def get( self, row, col ):
        """Gets the tree at a given location"""
        if row < 0 or col < 0:
            return None
        try:
            return self._rows[ row ][ col ]
        except IndexError:
            return None

    def trees( self ):
        """Iterates across all the trees in the forest"""
        for row in self._rows:
            yield from row 

def readForestFile( fname ):
    forest = Forest()
    with open( fname, 'r' ) as file:
        for line in file:
            forest.add( tuple( height for height in map( int, line.strip() ) ) )
    return forest
                