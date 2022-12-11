import re
from collections import deque
from itertools import islice

from product import product


class Item:

    def __init__( self, worry ):
        self.worry = worry                  # PUBLIC

    def __repr__( self ):
        return f'<{self.worry}>'


class Monkey:

    def __init__( self, *, num, items, operation, test ):
        # Read-only fields
        self._monkey_number: int = num      # We do not really need this.
        self._operation = operation         # A lambda-function for adjusting worry.
        ( d, if_true, if_false ) = test
        self._divisor: int = d              # This field is visible as divisor (to preent the use of bignums)
        self._if_true: int= if_true
        self._if_false: int = if_false
        # Transactional fields
        self._items = deque( map( Item, items ) )
        self._inspection_count: int = 0

    def monkeyNumber( self ) -> int:
        return self._monkey_number

    def popItem( self ) -> Item:
        try:
            return self._items.popleft()
        except IndexError:
            return None

    def pushItem( self, item ):
        self._items.append( item )

    def inspectAndBeBoredWith( self, item, relief ):
        self._inspection_count += 1
        item.worry = relief( self._operation( item.worry ) )

    def throwDecision( self, item ) -> int:
        if item.worry % self._divisor == 0:
            return self._if_true
        else:
            return self._if_false

    def status( self ):
        s = ', '.join( str(x.worry) for x in self._items )
        print( f'Monkey {self._monkey_number}: {s}' )
        print( f'Monkey {self._monkey_number} inspected items {self._inspection_count} times.' )

    def inspectionCount( self ) -> int:
        return self._inspection_count

    def divisor( self ) -> int:
        return self._divisor


class MonkeyGame:

    def __init__( self, monkeys, relief_factor=1 ):
        self._monkeys = monkeys
        self._relief_factor = relief_factor
        self._relief_base = product( m.divisor() for m in monkeys.values() )

    def monkeys( self ):
        # Relies on the stable sort of Python's dictionaries.
        return self._monkeys.values()

    def turn( self, monkey ):
        relief = lambda w: (w // self._relief_factor) % self._relief_base
        while item := monkey.popItem():
            monkey.inspectAndBeBoredWith( item, relief )
            dst = monkey.throwDecision( item )
            self._monkeys[ dst ].pushItem( item )

    def round( self ):
        for m in self.monkeys():
            self.turn( m )

    def status( self ):
        for m in self.monkeys():
            m.status()

    def monkeyBusinessLevel( self ) -> int:
        ( *_, a, b ) = sorted( [ m.inspectionCount() for m in self.monkeys() ] ) 
        return a * b


### readMonkeyFile #############################################################

def _getIntsGenerator( line ):
    for w in re.sub( '[,:]', ' ', line ).split():
        try:
            yield int( w )
        except:
            pass

def _getIntTuple( line ):
    return tuple( _getIntsGenerator( line ) )

def _getInt( line ):
    return next( _getIntsGenerator( line ) )

def _readMonkeyNumber( line ):
    return _getInt( line )

def _readStartingItems( line ):
    return _getIntTuple( line )

def _makeOperation( op, src ):
    if src == "old":
        source = lambda old: old
    else:
        n = int( src )
        source = lambda old: n
    if op == "+":
        return lambda old: old + source( old )
    elif op == "*":
        return lambda old: old * source( old )

def _readOperation( line ):
    m = re.match( r'[\s\t]+Operation: new = old (.*)', line )
    assert m is not None, f'Unexpected line: {line}'
    ( op, src ) = m[1].split()
    return _makeOperation( op, src )
  
def _readTest( lines ):
    return tuple( _getInt( line ) for line in lines )

def _tryReadMonkey( lines ):
    L = tuple( islice( lines, 7 ) )
    if L:
        mn = _readMonkeyNumber( L[0] )
        items = _readStartingItems( L[1] )
        operation = _readOperation( L[2] )
        test = _readTest( L[3:6] )
        return Monkey( num=mn, items=items, operation=operation, test=test )

def _readAllMonkeys( lines ):
    while monkey := _tryReadMonkey( lines ):
        yield monkey

def readMonkeyFile( fname ):
    """Returns a suitably ordered dictionary of freshly initialised monkeys."""
    monkeys = {}
    with open( fname, 'r' ) as file:
        lines = iter( file )
        for m in _readAllMonkeys( lines ):
            monkeys[ m.monkeyNumber() ] = m
    # return tuple( monkeys[n] for n in range( 0, len( monkeys ) ) )
    return { k: monkeys[k] for k in sorted( monkeys.keys() ) }
