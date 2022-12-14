
class Rocks:

    def __init__( self, coords, floor:bool ):
        self._coords = set( coords )
        self._floor = floor
        self._floor_level = max( map( lambda x: x[1], self._coords ) ) + 2
        self._sand_added = 0

    def isRockAt( self, x, y ):
        return ( x, y ) in self._coords or self._floor and y >= self._floor_level

    def tryAddSand( self ):
        sandx = 500
        sandy = 0
        if self.isRockAt( sandx, sandy ):
            # Source is blocked
            return False
        while True:
            if not self.isRockAt( sandx, sandy + 1 ):
                # Keep falling
                sandy += 1
            elif not self.isRockAt( sandx - 1, sandy + 1 ):
                # Down & left
                sandx -= 1
                sandy += 1
            elif not self.isRockAt( sandx + 1, sandy + 1 ):
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
            if sandy > self._floor_level:
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

def readRocksFile( fname, floor=False ):
    with open( fname, 'r' ) as file:
        return Rocks( readRocks( file ), floor )
