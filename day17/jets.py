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

    def highestPoint( self ):
        base = 0
        for ( j, r ) in enumerate( self._rocks ):
            for ch in r:
                if ch != '.':
                    base = j + 1
        return base

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
        for ( i, j ) in rock.points():
            # print( i, j )
            self.set( i + 2, h + j, '@' )

    def canNudge( self, dx, dy ):
        erase = set()
        add = set()
        for j in range( 0, len( self._rocks ) ):
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
        return m

    def petrify( self ):
        for j in range( 0, len( self._rocks ) ):
            for i in range( 0, self._width ):
                if self._rocks[ j ][ i ] == '@':
                    self._rocks[ j ][ i ] = '#'


class Simulation:

    def __init__( self, jets ):
        self._chamber = Chamber()
        self._jets = deque( jets )
        self._falling_rocks = deque( ( ROCK1, ROCK2, ROCK3, ROCK4, ROCK5 ) )

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
            j = self.nextJet()
            if j == "<":
                self._chamber.tryNudge( -1, 0 )
            elif j == ">":
                self._chamber.tryNudge( 1, 0 )
            else:
                raise Exception( 'BAD INPUT' )
            if not self._chamber.tryNudge( 0, -1 ):
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
