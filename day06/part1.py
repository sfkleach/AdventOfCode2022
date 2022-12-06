from signal import *

def part1( fname ):
    print( findStartOfPacketMarker( readSignalFile( fname ) ) )

if __name__ == "__main__":
    part1('input.txt')
