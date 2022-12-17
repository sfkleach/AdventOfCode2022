import re
from collections import deque
from queue import PriorityQueue
import heapq

class Valve:

    def __init__( self, name, rate, neighbours ):
        self.name = name                    # public
        self.rate = rate                    # public
        self.neighbours = neighbours        # public

    def __repr__( self ):
        return f'<{self.name} rate={self.rate}>'

class SearchStatus:

    def __init__( self, valve, unopened_valves, countdown, score ):
        self._countdown = countdown
        self._at = valve
        self._unopened = unopened_valves
        self._score = score
        self._best_possible = None

    def _getCountdown( self ):
        n = self._countdown - 1
        while n > 0:
            yield n
            n -= 2

    def bestPossible( self ):
        if self._best_possible is None:
            self._best_possible = self._score + sum( m * v.rate for ( m, v ) in zip( self._getCountdown(), self._unopened.values() ) )
        return self._best_possible

    def isSolution( self ):
        return self._countdown <= 0

    def score( self ):
        return self._score

    def __repr__( self ):
        return f'<{self._at.name} score={self._score} count={self._countdown} visited={self.visited()}>'

    def _genVisited( self ):
        linked_list = self._visited
        while linked_list:
            ( t, rest ) = linked_list
            linked_list = rest
            yield t

    def options( self ):
        if self._countdown <= 0:
            return
        new_countdown = self._countdown - 1
        if self._at.name in self._unopened and self._at.rate > 0:
            # Open valve.
            new_unopened = self._unopened.copy()
            del new_unopened[ self._at.name ]
            new_score = self._score + self._at.rate * max( 0, self._countdown - 1 )
            # print( 'score', new_score )
            new_at = self._at
            yield SearchStatus( new_at, new_unopened, new_countdown, new_score )
        if self._unopened:
            for n in self._at.neighbours:
                # Move to a neighbour.
                new_unopened = self._unopened
                new_score = self._score
                new_at = n
                yield SearchStatus( new_at, new_unopened, new_countdown, new_score )
        else:
            yield SearchStatus( self._at, self._unopened, 0, self._score )

class Search:

    def __init__( self, *, valves, start_name, countdown ):
        self._Q = [ SearchStatus( valves[ start_name ], valves, countdown, 0 ) ]
        self._high_score = 0
        self._best = None

    def canContinue( self ):
        return bool( self._Q )

    def check( self ):
        s = self._Q.pop()
        if s.isSolution():
            if s.score() > self._high_score:
                self._high_score = s.score()
                self._best = s
                # print( 'SOLUTION', s )
        else:
            if s.bestPossible() > self._high_score:
                n = len( self._Q )
                for t in s.options():
                    if t.bestPossible() > self._high_score:
                        self._Q.append( t )
                if len( self._Q ) > n:
                    self._Q.sort( key=lambda s: s.score() )

    def highScore( self ):
        return self._high_score


class Cave:

    def __init__( self, valve_map ):
        self._valves = valve_map

    def newSearch( self, start, countdown ):
        return Search( start_name=start, valves=self._valves, countdown=countdown )

def newCave( valve_tuples ):
    valves = tuple( valve_tuples )
    valve_map = {}
    for ( name, rate, neighbours ) in sorted( valves, key=lambda x: int(x[1]), reverse=True ):
        # print( 'add', name, rate )
        valve_map[ name ] = Valve( name, int( rate ), [] )
    for ( name, rate, neighbours ) in valves:
        valve_map[ name ].neighbours = sorted( tuple( valve_map[ n ] for n in neighbours ), key=lambda v: v.rate ) 
    return Cave( valve_map )

def readValves( file ):
    for line in file:
        if m := re.match( r'Valve ([A-Z]+) has flow rate=([0-9]+); tunnel[s]? lead[s]? to valve[s]? (.*)$', line ):
            yield ( m[1], int(m[2]), m[3].replace( ',', ' ' ).split() )
        else:
            raise Exception( 'BAD INPUT ' + line )

def readElephantFile( fname ):
    with open( fname, 'r' ) as file:
        return newCave( readValves( file ) )

