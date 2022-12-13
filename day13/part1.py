from packets import *

def part1( fname ):
    packets = readPacketsFile( fname )
    print( sum( n+1 for n, p in enumerate( packets ) if compare( *p ) ) )

if __name__ == "__main__":
    part1( 'input.txt' )
