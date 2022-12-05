import abc

class CratesState:

    def __init__( self, ncols ):
        self._cols = tuple( [] for i in range( 0, ncols ) )

    def add( self, ncol, item ):
        self._cols[ncol].append( item )

    def moveOne( self, src, dst, group=1 ):
        self._cols[dst].append( self._cols[src].pop() )

    def moveMulti( self, count, src, dst ):
        src_cols = self._cols[src]
        self._cols[dst].extend( src_cols[-count:] )
        self._cols[src][:] = src_cols[:-count]

    def signature( self ):
        return ''.join( map( lambda x: x and x[-1] or '.', self._cols ) ) 

class Crane:

    def __init__( self, crates ):
        self._crates = crates

    @abc.abstractmethod
    def move( self, *, count, src, dst ): ... 

    def applyMoves( self, moves ):
        for m in moves:
            self.move( **m )

class Crane9000( Crane ):

    def move( self, *, count, src, dst ):
        for i in range( 0, count ):
            self._crates.moveOne( src, dst )

class Crane9001( Crane ):

    def move( self, *, count, src, dst ):
       self._crates.moveMulti( count, src, dst )

def _cut( line ):
    return tuple( line[i:i+4].strip() for i in range( 0, len( line ), 4 ) )

def _readInitialPosition( file ):
    rows = []
    for line in map( str.rstrip, file ):
        if not( line ): 
            break
        rows.append( _cut( line ) )
    counts = rows.pop()
    state = CratesState( len( counts ) )
    for row in reversed( rows ):
        for n, item in enumerate( row ):
            if item:
                state.add( n, item[1:-1] )
    return state

def _readMoves( file ):
    for line in map( str.rstrip, file ):
        mv = line.split()
        yield dict( count=int(mv[1]), src=int(mv[3])-1, dst=int(mv[5])-1 )

def readCratesFile( fname ):
    with open( fname, 'r' ) as file:
        state = _readInitialPosition( file )
        moves = tuple( _readMoves( file ) )
        return ( state, moves )
