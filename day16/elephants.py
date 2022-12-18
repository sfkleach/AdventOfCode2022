import re
from collections import deque

class Valve:

    def __init__( self, name, rate, neighbours ):
        self.name = name                    # public
        self.rate = rate                    # public
        self.neighbours = neighbours        # public

    def __repr__( self ):
        return f'<{self.name} rate={self.rate}>'


class Cave:

    def __init__( self, valve_map ):
        self._valves = valve_map
        self._route_cache = {}

    def valve( self, name ):
        return self._valves[ name ]

    def newSearch( self, start_names, countdown ):
        return Search( start_names=start_names, valves=self._valves, countdown=countdown, cave=self )

    def findShortestRoute( self, src_name, dst_name ):
        # print( 'find', src_name, dst_name )
        start_route = (src_name, None)
        if src_name == dst_name:
            raise Exception( 'Already there' )
        try:
            if next_name := self._route_cache[ (src_name, dst_name) ]:
                return next_name
        except KeyError:
            pass
        Q = deque( [ start_route ] )
        while Q:
            ( here, rest ) = ( route := Q.popleft() )
            for v in self._valves[ here ].neighbours:
                there = v.name                  
                new_route = ( there, route )
                if there == dst_name:
                    # print( route )
                    r = self._findStep( new_route )
                    self._route_cache[ (src_name, dst_name) ] = r
                    return r
                Q.append( new_route )
        raise Exception( 'No route' )
    
    @staticmethod
    def _findStep( route ):
        # print( 'start', route )
        while route[1][1] is not None:
            route = route[1]
            # print( 'next', route )
        return route[0]


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



class Agent:

    def __init__( self, current_valve: str, goal_valve=True ):
        self.current_valve_name = current_valve
        self.goal_valve_name = goal_valve           # Usually a string.

    def hasReachedGoal( self ):
        return self.current_valve_name == self.goal_valve_name

    def hasQuit( self ):
        return self.goal_valve_name is None

    def isClueless( self ):
        return self.goal_valve_name is True

    def __repr__( self ):
        return f'{self.current_valve_name}.{self.goal_valve_name}'


class SearchStatus:

    def __init__( self, agents, unopened_valves, countdown, score, cave: Cave ):
        self._countdown = countdown
        self._agents = agents
        self._unopened = unopened_valves
        self._score = score
        self._best_possible = None
        self._cave = cave

    def isSolution( self ):
        return self._countdown <= 0

    def score( self ):
        return self._score

    def bestPossible( self ):
        if self._best_possible is None:
            timeslots_available = self._countdown - 1
            total = 0
            Q = deque( self._unopened.values() )
            while Q and timeslots_available > 0:
                for i in range( 0, len( self._agents ) ):
                    if Q:
                        total += Q.popleft().rate * timeslots_available
                timeslots_available -= 2
            self._best_possible = self._score + total
        return self._best_possible

    def worthOpening( self ):
        for ( goal_name, goal_valve ) in self._unopened.items():
            if goal_valve.rate > 0:
                yield goal_name

    def getClue( self, agent_number ):
        agent = self._agents[ agent_number ]
        currentName = agent.current_valve_name
        count = 0
        for goal_name in self.worthOpening():
            skip = False
            for g in self._agents:
                if g.goal_valve_name == goal_name:
                    skip = True
                    break
            if not skip:
                count += 1
                new_agents = self._agents.copy()
                new_agents[ agent_number ] = Agent( currentName, goal_name )
                yield SearchStatus( new_agents, self._unopened, self._countdown, self._score, self._cave )        
        if count == 0:
            new_agents = self._agents.copy()
            new_agents[ agent_number ] = Agent( currentName, None )
            yield SearchStatus( new_agents, self._unopened, self._countdown, self._score, self._cave )             

    def baseOptions( self, agent_number: int ):
        agent = self._agents[ agent_number ]
        currentName = agent.current_valve_name
        currentValve = self._cave.valve( currentName )
        if agent.hasQuit():
            yield SearchStatus( self._agents, self._unopened, self._countdown, self._score, self._cave )
        elif agent.hasReachedGoal():
            # When the agent reaches the goal node it will open a valve and become clueless.
            if currentName not in self._unopened or currentValve.rate <= 0:
                # This plan is a bad one - abort.
                return
            # Open this valve and become clueless.
            new_unopened = self._unopened.copy()
            del new_unopened[ currentName ]
            new_score = self._score + currentValve.rate * max( 0, self._countdown - 1 )
            new_agents = self._agents.copy()
            new_agents[ agent_number ] = Agent( currentName )
            yield SearchStatus( new_agents, new_unopened, self._countdown, new_score, self._cave )
        else:
            # Move the agent towards the goal, assuming it is still open.
            if agent.goal_valve_name in self._unopened:
                next = self._cave.findShortestRoute( currentName, agent.goal_valve_name )
                new_agents = self._agents.copy()
                new_agents[ agent_number ] = Agent( next, agent.goal_valve_name )            
                yield SearchStatus( new_agents, self._unopened, self._countdown, self._score, self._cave )

    def tick( self ):
        self._countdown -= 1
        return self

    def options( self ):
        if self._countdown <= 0:
            return
        if not self._unopened:
            return
        if len( self._agents ) == 1:
            if self._agents[0].isClueless():
                yield from self.getClue( 0 )
            else:
                yield from ( s.tick() for s in self.baseOptions( 0 ) )
        elif len( self._agents ) == 2:
            if self._agents[0].isClueless():
                yield from self.getClue( 0 )
            elif self._agents[1].isClueless():
                yield from self.getClue( 1 )
            else:
                for s in self.baseOptions( 0 ):
                    yield from ( t.tick() for t in s.baseOptions( 1 ) )

    def merit( self ):
        return self._score

    def __repr__( self ):
        names = ':'.join( map( str, self._agents ) )
        return f'<at={names} merit={self.merit()} t={self._countdown}>'


class Search:

    def __init__( self, *, valves, start_names, countdown, cave ):
        self._Q = []
        agents = [ Agent( current_name ) for current_name in start_names ]
        s = SearchStatus( agents, valves, countdown, 0, cave )
        self._Q.append( s )
        self._high_score = 0
        self._best = None

    def canContinue( self ):
        return bool( self._Q )

    def check( self ):
        s = self._Q.pop()
        if s.score() > self._high_score:
            self._high_score = s.score()
            self._best = s
            # print( 'SOLUTION', s, s._countdown, [ v for ( n, v ) in s._unopened.items() if v.rate > 0 ] )
        if s.bestPossible() > self._high_score:
            n = len( self._Q )
            for t in s.options():
                if t.bestPossible() > self._high_score:
                    self._Q.append( t )
            if len( self._Q ) > n:
                self._Q.sort( key=lambda s: s.score() )

    def highScore( self ):
        return self._high_score
