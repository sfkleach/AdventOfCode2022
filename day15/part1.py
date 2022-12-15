from sensors import *

def part1( fname, line ):
    A = readSensorArrayFile( fname )
    x_covered = A.intersect( line )
    x_beacons = A.beacons( line )
    d = x_covered - x_beacons
    g = P.iterate( d, step=1 )
    # for x in g:
    #     print( x )
    n = sum( 1 for i in g )
    print( n )


if __name__ == "__main__":
    # part1( 'test.txt', 10 )         # 26
    part1( 'input.txt', 2000000 )   # 4861076
