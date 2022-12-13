from itertools import islice
import re

def compare( left, right ):
    if isinstance( left, int ):
        if isinstance( right, int ):
            if left < right:
                return True
            elif left > right:
                return False
            else:
                return None
        else:
            return compare( [left], right )
    elif isinstance( right, int ):
        return compare( left, [right] )
    else:
        for (lhs, rhs) in zip( left, right ):
            cmp = compare( lhs, rhs )
            if cmp is not None:
                return cmp
        return compare( len( left ), len( right ) )            

def _eval( line ):
    if re.match( r'[0-9,\[\]\s\n]', line ):
        return eval( line )
    else:
        raise Exception( f'BAD LINE: {line}' )

def readPackets( lines ):
    while True:
        L = tuple( islice( lines, 3 ) )
        if not L:
            break
        yield ( _eval( L[0] ), _eval( L[1] ) )

def readPacketsFile( fname ):
    with open( fname, 'r' ) as file:
        return list( readPackets( iter( file ) ) )