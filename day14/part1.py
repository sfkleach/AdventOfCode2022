from rocks import *

def part1( fname ):
    r = readRocksFile( fname )
    print( r.pourInSand() )

if __name__ == "__main__":
    part1( 'input.txt' )
    