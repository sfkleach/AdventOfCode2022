from monkeys import *

def part1( fname ):
    M = readMonkeysFile( fname, None )
    print( M['root'].eval() )

if __name__ == "__main__":
    # part1( 'test.txt' )
    part1( 'input.txt' )