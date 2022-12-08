from consoletrace import *

def part1( fname ):
    info = readConsoleTraceFile( fname )
    total = sum( filter( lambda n: n <= 100000,  map( lambda d: d.totalSize(), info.scanDirs() ) ) )
    print( total )

if __name__ == "__main__":
    # Should be 1348005
    part1( 'input.txt' )
    