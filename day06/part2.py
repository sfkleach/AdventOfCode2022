from signal import *

def part2( fname ):
    print( findStartOfMessageMarker( readSignalFile( fname ) ) )

if __name__ == "__main__":
    part2('input.txt')
