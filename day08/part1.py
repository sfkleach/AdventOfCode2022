from forest import *

def part1( fname ):
    f = readForestFile( fname )
    print( sum(1 for _ in filter( lambda x: x.isVisible(), f.trees())) )

if __name__ == "__main__":
    part1( 'input.txt' )
