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

    def show( self, limit=-1 ):
        for n, r in enumerate( reversed( self._rocks ) ):
            if n == limit:
                break
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
        
    def profile( self ):
        return tuple( self._highest - n for n in self._highest_in_col )


class Simulation:

    def __init__( self, jets ):
        self._chamber = Chamber()
        self._jets = deque( jets )
        self._falling_rocks = deque( ( ROCK1, ROCK2, ROCK3, ROCK4, ROCK5 ) )
        self._njets = 0
        self._nfalls = 0
        print( '#jets', len( self._jets ) )
        print( '#rocks', len( self._falling_rocks ) )
        self._nsteps = 0

    def signature( self ):
        return ( self._njets, self._nfalls, self._chamber.profile() )

    def highestPoint( self ):
        return self._chamber.highestPoint()

    def nextRock( self ):
        self._nfalls = ( self._nfalls + 1 ) % len( self._falling_rocks ) 
        r = self._falling_rocks.popleft()
        self._falling_rocks.append( r )
        return r

    def nextJet( self ):
        self._njets = ( self._njets + 1 ) % len( self._jets ) 
        j = self._jets.popleft()
        self._jets.append( j )
        return j        

    def step( self ):
        self._nsteps += 1
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

    def cycle( self ):
        while True:
            before = self._njets
            self.step()
            if self._njets < before:
                break

    def detectLoop( self ):
        self._signatures = {}
        while True:
            self.cycle()
            sig = self.signature()
            if sig in self._signatures:
                ( old_nsteps, old_height ) = self._signatures[ sig ]
                new_height = self._chamber.highestPoint()
                return dict( steps_delta=self._nsteps - old_nsteps, signature=sig, start=old_nsteps, start_height=old_height, height_delta=new_height - old_height )
            else:
                self._signatures[ sig ] = ( self._nsteps, self._chamber.highestPoint() )
        
    def show( self ):
        self._chamber.show()

    def run( self, count ):
        for n in range( 0, count ):
            if n % 1000 == 0:
                print( 'progress', n )
            self.step()
            

def readSimulationFile( fname ):
    with open( fname, 'r' ) as file:
        return Simulation( file.read().strip() )
