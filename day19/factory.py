import re
from collections import deque

class Factory:

    def __init__( self ):
        self._time = 0
        self._robots = [1, 0, 0, 0]
        self._stocks = [0, 0, 0, 0]
        self._plan = None
        self._blueprint = (
            ( 4, 0, 0, 0 ),
            ( 2, 0, 0, 0 ),
            ( 3, 14, 0, 0 ),
            ( 2, 0, 7, 0 )
        )
        self._limits = tuple( max( robreq[n] for robreq in self._blueprint ) for n in range( 0, 4 ) )

    def copy( self ):
        c = Factory()
        c._time = self._time
        c._robots = list( self._robots )
        c._stocks = list( self._stocks )
        c._plan = self._plan
        c._blueprint = self._blueprint
        c._limits = self._limits
        return c
    
    def round( self ):
        self._time += 1
        # Build a robot if possible.
        requirements = self._blueprint[ self._plan ]
        build = all( req <= got for ( req, got ) in zip( requirements, self._stocks ) )
        if build:
            for ( n, level ) in enumerate( self._stocks ):
                self._stocks[ n ] -= requirements[ n ]
        # Add to stocks.
        for ( n, k ) in enumerate( self._robots ):
            self._stocks[ n ] += k
        # Add the robot to the collection.
        if build:
            self._robots[ self._plan ] += 1
            self._plan = None

    def oneStep( self ):
        if self._plan is not None:
            self.round()
            if self._time <= 24:
                yield self
        else:
            for i in reversed( range( 0, 4 ) ):
                requirements = self._blueprint[ i ]
                feasible = all( req == 0 or rob > 0 for ( req, rob ) in zip( requirements, self._robots ) )
                # print( f'feasible to build {i}', [ req == 0 or rob > 0 for ( req, rob ) in zip( requirements, self._robots ) ], feasible )
                if feasible:
                    desirable = i == 3 or ( self._robots[ i ] < self._limits[ i ] )
                    if desirable:
                        c = self.copy()
                        c._plan = i
                        c.round()
                        if c._time <= 24:
                            yield c

class Simulation:

    def __init__( self, factory ):
        self._Q = deque( [ factory.copy() ] )
        self._best = 0

    def tick( self ):
        f = self._Q.pop()
        geodes = f._stocks[3]
        if geodes > self._best:
            self._best = geodes
            self.show()
        self._Q.extend( f.oneStep() )
        # self.show()

    def show( self ):
        print( 'Best:', self._best )
        for n, f in enumerate( self._Q ):
            print( f'{n})', f._time, f._plan, f._robots, f._stocks )

    def run( self ):
        while self._Q:
            self.tick()

def readBlueprintsFile( fname ):
    with open( fname, 'r' ) as file:
        for line in file:
            print( line )
            bp_words = line.split( 'Each' )
            bp = []
            for w in bp_words[1:]:
                robreq = []
                m = re.match( r'[^0-9]+costs ([^.]*)', w )
                assert bool( m )
                for item in m[1].split( ' and '):
                    ( n, mats ) = ( pair := item.split() )
                    # print( 'Pair', pair )
                    robreq.append( pair )
                reqs = 4 * [ 0 ]
                for ( i, mat) in enumerate( [ 'ore', 'clay', 'obsidian' ] ):
                    req = 0
                    for item in robreq:
                        if item[1] == mat:
                            reqs[ i ] = int( item[0] )
                bp.append( tuple( reqs ) )
            yield tuple( bp )


                