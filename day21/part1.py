from monkeys import *

def part1( fname ):
    M = readMonkeysFile( fname )
    print( M['root'].eval( M ) )

if __name__ == "__main__":
    # part1( 'test.txt' )
    part1( 'input.txt' )