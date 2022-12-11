from monkeys import *
from operator import mul

def part1( fname ):
    m = readMonkeyFile( fname )
    g = MonkeyGame( m, relief_factor=3 )
    for i in range( 0, 20 ):
        g.round()
    print( g.monkeyBusinessLevel() )

if __name__ == "__main__":
    part1( 'input.txt' )
