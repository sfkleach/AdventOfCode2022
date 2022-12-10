from machine import *

def signalStrengthsAt( m, observation_points ):
    for i in observation_points:
        m.runTo( i )
        yield m.signalStrength()

def part1( fname ):
    m = Machine( readSignalProgram( fname ) )
    print( sum( signalStrengthsAt( m, range( 20, 221, 40 ) ) ) )

if __name__ == "__main__":
    # part1( 'test2.txt' )
    part1( 'input.txt' )