from forest import *

def part2( fname ):
    f = readForestFile( fname )
    print( max( map( lambda x: x.scenicScore(), f.trees() ) ) )

if __name__ == "__main__":
    part2( 'input.txt' )
