import re
from collections import deque

class Blueprint:

    def __init__( self, number, bluedata ):
        self._number = number
        self._bluedata = bluedata

    def best( self ):
        S = Simulation( Factory( bluedata=self._bluedata ) )
        return S.run()

    def quality( self ):
        return self._number * self.best()

class Factory:

    def __init__( self, *, factory=None, bluedata=None ):
        self._time = factory and factory._time or 0
        self._robots = factory and factory._robots.copy() or [1, 0, 0, 0]
        self._stocks = factory and factory._stocks.copy() or [0, 0, 0, 0]
        self._plan = factory and factory._plan
        self._bluedata = factory and factory._bluedata or bluedata
        self._limits = factory and factory._limits or tuple( max( robreq[n] for robreq in self._bluedata ) for n in range( 0, 4 ) )

    def copy( self ):
        return Factory( factory=self )
    
    def round( self ):
        self._time += 1
        # Build a robot if possible.
        requirements = self._bluedata[ self._plan ]
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
            for i in range( 0, 4 ):
                requirements = self._bluedata[ i ]
                feasible = all( req == 0 or rob > 0 for ( req, rob ) in zip( requirements, self._robots ) )
                # print( f'feasible to build {i}', [ req == 0 or rob > 0 for ( req, rob ) in zip( requirements, self._robots ) ], feasible )
                if feasible:
                    desirable = i == 3 or ( self._robots[ i ] < self._limits[ i ] )
                    # print( f'desireable to build {i}', i == 3, self._robots[ i ] < self._limits[ i ], desirable )
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
            # self.show()
        self._Q.extend( f.oneStep() )
        # self.show()

    def show( self ):
        print( 'Best:', self._best )
        for n, f in enumerate( self._Q ):
            print( f'{n})', f._time, f._plan, f._robots, f._stocks )

    def run( self ):
        while self._Q:
            self.tick()
        return self._best

def readBlueprints( file ):
    for line in file:
        # print( line )
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
        number = int( re.match( r'[^0-9]*([0-9]+)', bp_words[0] )[1] )
        yield Blueprint( number, tuple( bp ) )

def readBlueprintsFile( fname ):
    with open( fname, 'r' ) as file:
        return tuple( readBlueprints( file ) )


                