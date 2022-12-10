from machine import *

def part2( fname ):
    m = Machine( readSignalProgram( fname ) )
    for row in range( 0, 6 ):
        for col in range( 0, 40 ):
            print( m.vram( col ), end='' )
            m.tick()
        print()

if __name__ == "__main__":
    # part2( 'test2.txt' )
    part2( 'input.txt' )
