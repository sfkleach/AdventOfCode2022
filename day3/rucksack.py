# a-z followed by A-Z
AZ = (
    ''.join( chr( ord( 'a' ) + i ) for i in range( 0, 26 ) ) + 
    ''.join( chr( ord( 'A' ) + i ) for i in range( 0, 26 ) )
)    

# Lowercase item types a through z have priorities 1 through 26.
# Uppercase item types A through Z have priorities 27 through 52.

# Turn a list into a dictionary
PRIORITY = dict( zip( AZ, range( 0, len( AZ ) ) ) )

def letterPriority( letter ):
    return PRIORITY[ letter ] + 1

def priority( arg, *args ):
    sofar = set( arg )
    for arg in args:
        sofar = sofar.intersection( set( arg ) )
    return letterPriority( sofar.pop() )

def linePriority( line ):
    n = len( line ) // 2
    lhs = set( line[:n] )
    rhs = set( line[n:] )
    return priority( lhs, rhs )

def tripletPriority( triplet ):
    return priority( *triplet )

def linesRucksackFile( fname ):
    with open( fname, 'r' ) as file:
        for line in file:
            yield line.strip()

def tripletsRucksackFile( fname ):
    with open( fname, 'r' ) as file:
        while True:        
            try:
                yield tuple( next( file ).strip() for i in range( 0, 3 ) )
            except:
                return

