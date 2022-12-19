from collections import deque

class Rock:

    def __init__( self, ascii_art ):
        self._data = tuple( reversed( ascii_art.split() ) )

    def height( self ):
        return len( self._data )

    def width( self ):
        return len( self._data[0] )

    def points( self ):
        for ( j, row ) in enumerate( self._data ):
            for ( i, ch ) in enumerate( row ):
                if ch == '#':
                    yield i, j

ROCK1 = Rock(
"""
####
""" )

ROCK2 = Rock(
"""
.#.
###
.#.
""" )

ROCK3 = Rock(
"""
..#
..#
###
""" )

ROCK4 = Rock(
"""
#
#
#
#
""" )

ROCK5 = Rock(
"""
##
##
""" )


class Chamber:

    def __init__( self, width=7 ):
        self._width = width
        self._rocks = []
        self._highest_in_col = width * [ -1 ]
        self._highest = -1
        self._lo = 0
        self._hi = 0

    def highestPoint( self ):
        return self._highest + 1

    def show( self ):
        for r in reversed( self._rocks ):
            print( f'|{"".join(r)}|' )
        print( f'+{self._width*"-"}+' )
    
    def set( self, x, y, ch ):
        for i in range( len( self._rocks ), y + 1 ):
            self._rocks.append( list( self._width * '.' ) )
        self._rocks[ y ][ x ] = ch

    def insert( self, rock ):
        h = self.highestPoint() + 3
        hi = 0
        lo = h
        for ( i, j ) in rock.points():
            # print( i, j )
            new_j = h + j
            self.set( i + 2, new_j, '@' )
            hi = max( hi, new_j )
            lo = min( lo, new_j )
        self._lo = lo
        self._hi = hi + 1

    def canNudge( self, dx, dy ):
        erase = set()
        add = set()
        for j in range( self._lo, self._hi ):
            for i in range( 0, self._width ):
                if self._rocks[ j ][ i ] == '@':
                    try:
                        x1 = i + dx
                        y1 = j + dy
                        if x1 < 0 or y1 < 0:
                            return False
                        ch = self._rocks[ j + dy ][ i + dx ]
                        if ch != '.' and ch != '@':
                            return False
                        erase.add( ( i, j ) )
                        add.add( ( x1, y1 ) )
                    except IndexError:
                        return False
        return ( erase - add, add - erase )

    def tryNudge( self, dx, dy ):
        if m := self.canNudge( dx, dy ):
            ( erase, add ) = m
            for ( x, y ) in erase:
                self.set( x, y, '.' )
            for ( x, y ) in add:
                self.set( x, y, '@' )
            if dy < 0:
                # Falling
                self._lo -= 1
                self._hi -= 1
        return m

    def petrify( self ):
        for j in range( self._lo, self._hi ):
            for i in range( 0, self._width ):
                if self._rocks[ j ][ i ] == '@':
                    self._rocks[ j ][ i ] = '#'
                    if j > self._highest_in_col[ i ]:
                        self._highest_in_col[ i ] = j
                    if j > self._highest:
                        self._highest = j


class Simulation:

    def __init__( self, jets ):
        self._chamber = Chamber()
        self._jets = deque( jets )
        self._falling_rocks = deque( ( ROCK1, ROCK2, ROCK3, ROCK4, ROCK5 ) )
        print( '#jets', len( self._jets ) )
        print( '#rocks', len( self._falling_rocks ) )

    def highestPoint( self ):
        return self._chamber.highestPoint()

    def nextRock( self ):
        r = self._falling_rocks.popleft()
        self._falling_rocks.append( r )
        return r

    def nextJet( self ):
        j = self._jets.popleft()
        self._jets.append( j )
        return j        

    def step( self ):
        rock = self.nextRock()
        self._chamber.insert( rock )
        while True:
            # self._chamber.show()
            j = self.nextJet()
            if j == "<":
                # print( 'left' )
                self._chamber.tryNudge( -1, 0 )
            elif j == ">":
                # print( 'right' )
                self._chamber.tryNudge( 1, 0 )
            else:
                raise Exception( 'BAD INPUT' )
            if not self._chamber.tryNudge( 0, -1 ):
                # print( 'petrify' )
                self._chamber.petrify()
                break
        
    def show( self ):
        self._chamber.show()

    def run( self, count ):
        for n in range( 0, count ):
            if n % 100 == 0:
                print( 'progress', n )
            self.step()
            

def readSimulationFile( fname ):
    with open( fname, 'r' ) as file:
        return Simulation( file.read().strip() )
