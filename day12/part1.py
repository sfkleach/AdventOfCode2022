from elevation import *

def part1( fname ):
    e = readElevationFile( fname )
    print( e.shortestPath() )

if __name__ == "__main__":
    part1( 'input.txt' )
