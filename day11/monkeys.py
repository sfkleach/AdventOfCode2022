import re
from pushable import Pushable
from collections import deque
from product import product

class Item:

    def __init__( self, worry ):
        self.worry = worry

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

    def monkeyNumber( self ):
        return self._monkey_number

    def popItem( self ):
        try:
            return self._items.popleft()
        except IndexError:
            return None

    def pushItem( self, item ):
        self._items.append( item )

    def inspectAndBeBoredWith( self, item, relief ):
        self._inspection_count += 1
        item.worry = relief( self._operation( item.worry ) )

    def throwDecision( self, item ):
        if item.worry % self._divisor == 0:
            return self._if_true
        else:
            return self._if_false

    def status( self ):
        s = ', '.join( str(x.worry) for x in self._items )
        print( f'Monkey {self._monkey_number}: {s}' )
        print( f'Monkey {self._monkey_number} inspected items {self._inspection_count} times.' )

    def inspectionCount( self ):
        return self._inspection_count

    def divisor( self ):
        return self._divisor


class MonkeyGame:

    def __init__( self, monkeys, relief_factor=1 ):
        self._monkeys = monkeys
        self._relief_factor = relief_factor
        self._relief_base = product( m.divisor() for m in monkeys )

    def turn( self, monkey ):
        relief = lambda w: (w // self._relief_factor) % self._relief_base
        while item := monkey.popItem():
            monkey.inspectAndBeBoredWith( item, relief )
            dst = monkey.throwDecision( item )
            self._monkeys[ dst ].pushItem( item )

    def round( self ):
        for m in self._monkeys:
            self.turn( m )

    def status( self ):
        for m in self._monkeys:
            m.status()

    def monkeyBusinessLevel( self ):
        ( *_, a, b ) = sorted( [ m.inspectionCount() for m in self._monkeys ] ) 
        return a * b

### readMonkeyFile #############################################################

def _readMonkeyNumber( lines ):
    line = next( lines )
    m = re.match( 'Monkey ([0-9]+):', line )
    # print( 'line', line, m is None, 'end' )
    assert m is not None, f'Unexpected line: {line}'
    return int( m[1] )

def _readStartingItems( lines ):
    line = next( lines )
    words = line.split()
    assert words[0] == "Starting"
    for w in words:
        try:
            yield int( w.replace( ',', '' ) )
        except:
            pass

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

def _readOperation( lines ):
    line = next( lines )
    m = re.match( r'[\s\t]+Operation: new = old (.*)', line )
    assert m is not None, f'Unexpected line: {line}'
    words = m[1].split()
    assert len( words ) == 2
    return _makeOperation( *words )
  
def _readTest( lines ):
    line = next( lines )
    m = re.match( r'[\s\t]+Test: divisible by (.+)', line )    
    assert m is not None, f'Unexpected line: {line}'
    words = m[1].split()
    assert len(words) == 1, f'Unexpected line: {line}'
    divisor = int( words[0] )
    line = next( lines )
    assert re.match( r'[\s\t]+If true:', line )
    if_true = int( line.split()[-1] )
    line = next( lines )
    assert re.match( r'[\s\t]+If false:', line )
    if_false = int( line.split()[-1] )
    return ( divisor, if_true, if_false )

def _tryReadMonkey( lines ):
    # Skip blank lines
    while lines and lines.peek() == '\n':
        next(lines)
    # Return None if there are no more Monkeys in the file.
    if lines:
        mn = _readMonkeyNumber( lines )
        items = tuple( _readStartingItems( lines ) )
        operation = _readOperation( lines )
        test = _readTest( lines )
        return Monkey( num=mn, items=items, operation=operation, test=test )

def _readAllMonkeys( lines ):
    while monkey := _tryReadMonkey( lines ):
        yield monkey

def readMonkeyFile( fname ):
    """Returns a list of freshly initialised monkeys in order"""
    monkeys = {}
    with open( fname, 'r' ) as file:
        lines = Pushable( iter( file ) )
        for m in _readAllMonkeys( lines ):
            monkeys[ m.monkeyNumber() ] = m
    return tuple( monkeys[n] for n in range( 0, len( monkeys ) ) )
