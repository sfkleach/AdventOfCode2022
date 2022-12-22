from mix import *

def part1( fname ):
    mix = readMixFile( fname )
    # print( mix.__dict__ )
    mix.mix()
    a = mix.lookup( 1000 )
    b = mix.lookup( 2000 )
    c = mix.lookup( 3000 )
    # print( sorted( list( mix._original_order ) ) == sorted( mix._items ) )
    print( a + b + c, a, b, c )

if __name__ == "__main__":
    # part1( 'test.txt' )
    part1( 'input.txt' )
