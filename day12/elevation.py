from collections import deque

class Routes:

    def __init__( self, start, end ):
        self._found = { start: ( None, 0 ) }
        self._end = end

    def shouldContinue( self ):
        return self._end not in self._found

    def tryAdd( self, src_rc, dst_rc ):
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
        return self._found[ self._end ][1]



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
        ( row, col ) = rowcol
        try:
            if row >= 0 and col >= 0:
                return self._rows[ row ][ col ]
            else:
                return None
        except IndexError:
            return None

    @staticmethod
    def neighbours( rowcol ):
        ( row, col ) = rowcol
        yield ( row+1, col )
        if row > 0:
            yield ( row-1, col )
        yield ( row, col+1 )
        if col > 0:
            yield ( row, col-1 )

    def canReach( self, rowcol ):
        ( row, col ) = rowcol
        h = self.at( rowcol )
        for rc in self.neighbours( rowcol ):
            h1 = self.at( rc )
            if h1 is not None and h1 <= h + 1:
                yield rc

    def shortestPath( self ):
        routes = Routes( self._start, self._end )
        sofar = deque( [ self._start ] )
        while sofar and routes.shouldContinue():
            rowcol = sofar.popleft()
            for rc in self.canReach( rowcol ):
                if routes.tryAdd( rowcol, rc ):
                    sofar.append( rc )
        return routes.length()

    def show( self ):
        for row in self._rows:
            print( ''.join( chr( i + ord( 'a' ) ) for i in row ) )


def readElevationFile( fname ):
    with open( fname, 'r' ) as file:
        return Elevation( file )
