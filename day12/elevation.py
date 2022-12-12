
class Elevation:

    def __init__( self, heights_strings ):
        self._rows = []
        self._start = None
        self._end = None
        for heights in heights_strings:
            self._addLine( heights )

    def _addLine( self, heights ):
        row = []
        nrow = len( self._rows )
        for ncol, ch in enumerate( heights ):
            if ch == "S":
                row.append( 0 )                 # 0 is accessible from anywhere.
                self._start = ( nrow, ncol )
            elif ch == "E":
                row.append( 0 )                 # As above.
                self._end = ( nrow, ncol )
            else:
                row.append( ord( ch ) - ord( 'a' ) )
        self._rows.append( row )

    def at( self, rowcol ):
        ( row, col ) = rowcol
        try:
            return self._rows[ row ][ col ]
        except IndexError:
            return None

    @staticmethod
    def neighbours( rowcol ):
        ( row, col ) = rowcol
        yield ( row+1, col )
        yield ( row-1, col )
        yield ( row, col+1 )
        yield ( row, col-1 )

    def canReach( self, rowcol ):
        ( row, col ) = rowcol
        h = self.at( rowcol )
        for rc in self.neighbours( rowcol ):
            h1 = self.at( rc )
            if h1 and h1 <= h + 1:
                yield rc

    def shortestPath( self ):
        found = { self._start: None }
        sofar = [ self._start ]
        while sofar and self._end not in found:
            rowcol = sofar.pop()
            for rc in self.canReach( rowcol ):
                if rc not in found:
                    found[ rc ] = rc
                    sofar.append( rc )
        if self._end in found:
            route = []
            rc = self._end
            while rc:
                route.append( rc )
                rc = found[ rc ]
        return route



def readElevationFile( fname ):
    with open( fname, 'r' ) as file:
        return Elevation( file )