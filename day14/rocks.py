
class Rocks:

    def __init__( self, coords ):
        self._coords = set( coords )
        self._abyss_level = max( map( lambda x: x[1], self._coords ) ) + 1
        self._sand_added = 0

    def tryAddSand( self ):
        sandx = 500
        sandy = 0
        while True:
            if ( sandx, sandy + 1 ) not in self._coords:
                # Keep falling
                sandy += 1
            elif ( sandx - 1, sandy + 1 ) not in self._coords:
                # Down & left
                sandx -= 1
                sandy += 1
            elif ( sandx + 1, sandy + 1 ) not in self._coords:
                # Down & right
                sandx += 1
                sandy += 1
            else:
                # Settle
                # print( sandx, sandy )
                self._coords.add( ( sandx, sandy ) )
                self._sand_added += 1
                return True
            # In the abyss?
            if sandy >= self._abyss_level:
                return False

    def pourInSand( self ):
        while self.tryAddSand():
            pass
        return self._sand_added



    


def coordinates( p1, p2 ):
    startx, starty = p1
    endx, endy = p2
    if startx == endx:
        for y in range( min( starty, endy ), max( starty, endy ) + 1 ):
            yield ( startx, y )
    elif starty == endy:
        for x in range( min( startx, endx ), max( startx, endx ) + 1 ):
            yield ( x, starty )
    else:
        raise Exception( 'BAD INPUT' )

def readRocks( file ):
    for line in file:
        str_coord_pairs = line.strip().split( ' -> ' )
        coord_pairs = [ tuple( map( int, p.split(',') ) ) for p in str_coord_pairs ]
        for p1, p2 in zip( coord_pairs, coord_pairs[1:] ):
            yield from coordinates( p1, p2 )

def readRocksFile( fname ):
    with open( fname, 'r' ) as file:
        return Rocks( readRocks( file ) )
