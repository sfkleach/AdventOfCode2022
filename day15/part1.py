from sensors import *

def part1( fname, line ):
    A = readSensorArrayFile( fname )
    x_covered = set( A.intersect( line ) )
    x_beacons = set( A.beacons( line ) )
    print( len( x_covered - x_beacons ) )


if __name__ == "__main__":
    part1( 'test.txt', 10 )        # 26
    # part1( 'input.txt', 2000000 )   # ???
