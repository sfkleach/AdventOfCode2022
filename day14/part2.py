from rocks import *

def part2( fname ):
    r = readRocksFile( fname, floor=True )
    print( r.pourInSand() )

if __name__ == "__main__":
    part2( 'input.txt' )
    