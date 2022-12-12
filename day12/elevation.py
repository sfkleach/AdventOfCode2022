
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
        # print( 'at', rowcol )
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
            # print( 'check', rc, h, h1 )
            if h1 is not None and h1 <= h + 1:
                yield rc

    def shortestPath( self ):
        found = { self._start: ( None, 0 ) }
        sofar = [ ( self._start, 0 ) ]
        while sofar and self._end not in found:
            ( rowcol, dist ) = sofar.pop()
            # print( 'consider', rowcol )
            for rc in self.canReach( rowcol ):
                # print( 'neighbour', rc )
                dist1 = dist + 1
                if rc not in found:
                    # print('new', f'{rowcol} -> {rc}' )
                    found[ rc ] = ( rowcol, dist1 )
                    sofar.append( ( rc, dist + 1 ) )
                elif found[ rc ][1] > dist1:
                    # print('old', f'{rowcol} -> {rc}', rc, found[rc], dist1 )
                    found[ rc ] = ( rowcol, dist1 )
        return found[ self._end ][1]
        # if self._end in found:
        #     route = []
        #     rc = self._end
        #     while rc is not None:
        #         # print( 'route', rc )
        #         (rc, d) = found[ rc ]
        #         if rc is None:
        #             break
        #         route.append( (rc, d, chr( self.at( rc ) + ord('a') ) ) )
        #     return route

    def show( self ):
        for row in self._rows:
            print( ''.join( chr( i + ord( 'a' ) ) for i in row ) )



def readElevationFile( fname ):
    with open( fname, 'r' ) as file:
        return Elevation( file )