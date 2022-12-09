from rope import *

def part1( fname ):
    c = readRopeCommandFile( fname )
    positions = set( LongRope().tailTrace( c ) )
    print( len( positions ) )

if __name__ == "__main__":
    part1( 'input.txt' )
