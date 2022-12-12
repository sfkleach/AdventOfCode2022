from collections import deque

class Routes:
    """
    This class encapsulates the chain of steps in the format:
        Map< Location, ( previous_location: Location?, distance_travelled: int ) >
    For simplicity I set the previous location to the start to be None. Since
    we do not actually report on the path, I could simply have used a 
        Map< Location, distance_travelled: int >
    """

    def __init__( self, start, end ):
        self._found = { start: ( None, 0 ) }
        self._end = end

    def shouldContinue( self ):
        return self._end not in self._found

    def tryAdd( self, src_rc, dst_rc ):
        """
        src_rc = source row&col
        dst_rc = destination row&col
        Returns True iff the dst_rc was not previously visited.
        """
        ( _, dist ) = self._found[ src_rc ]
        dist1 = dist + 1
        rcd = ( src_rc, dist1 )
        try:
            ( _, prev_dist ) = self._found[ dst_rc ]
            if prev_dist > dist1:
                self._found[ dst_rc ] = rcd
        except KeyError:
            self._found[ dst_rc ] = rcd
            return True
        return None

    def length( self ):
        return self._found[ self._end ][1]  # [1] selects the distance.



class Elevation:

    def __init__( self, heights_strings ):
        self._rows = []
        self._start = None
        self._end = None
        for heights in heights_strings:
            self._addLine( heights.strip() )

    def _addLine( self, heights ):
        row = []
        nrow = len( self._rows )
        for ncol, ch in enumerate( heights ):
            if ch == "S":
                row.append( 0 )                 # 0 is accessible from anywhere.
                self._start = ( nrow, ncol )
            elif ch == "E":
                row.append( ord( 'z' ) - ord( 'a' ) )                 # As above.
                self._end = ( nrow, ncol )
            else:
                row.append( ord( ch ) - ord( 'a' ) )
        self._rows.append( row )

    def at( self, rowcol ):
        """
        Returns the elevation at a row&col pair. The location must be within
        bounds.
        """
        ( row, col ) = rowcol
        return self._rows[ row ][ col ]

    def neighbours( self, rowcol ):
        """Generates the possible neighbours of a row&col pair."""
        ( row, col ) = rowcol
        if row + 1 < len( self._rows ):
            yield ( row+1, col )
        if row > 0:
            yield ( row-1, col )
        if col + 1 < len( self._rows[row] ):
            yield ( row, col+1 )
        if col > 0:
            yield ( row, col-1 )

    def canReach( self, rowcol ):
        """Generates the reachable neighbours of a row&col pair."""
        ( row, col ) = rowcol
        h = self.at( rowcol )
        for rc in self.neighbours( rowcol ):
            h1 = self.at( rc )
            if h1 is not None and h1 <= h + 1:
                yield rc

    def shortestPath( self ):
        return self.shortestPathFrom( self._start )

    def shortestPathFrom( self, start ):
        """
        Effectively this is Dijkstra's algorithm, although I just use a straight
        breath-first search rather than a priority queue (all weights are 1).
        """
        routes = Routes( start, self._end )
        sofar = deque( [ start ] )                # Use a deque for breaths-first search - pop from front but add to back.
        while sofar and routes.shouldContinue():
            rowcol = sofar.popleft()
            for rc in self.canReach( rowcol ):
                if routes.tryAdd( rowcol, rc ):
                    sofar.append( rc )
        if sofar:
            return routes.length()

    def findZeroElevations( self ):
        """Generates the locations with a zero elevation."""
        for nrow in range( 0, len( self._rows ) ):
            for ncol in range( 0, len( self._rows[nrow] ) ):
                rc = ( nrow, ncol )
                if self.at( rc ) == 0:
                    yield rc


def readElevationFile( fname ):
    with open( fname, 'r' ) as file:
        return Elevation( file )
