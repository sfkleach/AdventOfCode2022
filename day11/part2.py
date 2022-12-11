from monkeys import *
from operator import mul

def part2( fname ):
    m = readMonkeyFile( fname )
    g = MonkeyGame( m, relief_factor=1 )
    for n in range( 0, 10000 ):
        g.round()
    # g.status()
    print( g.monkeyBusinessLevel() )

if __name__ == "__main__":
    part2( 'input.txt' )
