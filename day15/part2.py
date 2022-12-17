from sensors import *

def part2( fname, lo, hi ):
    A = readSensorArrayFile( fname )
    n = 0
    for y in reversed( range( lo, hi ) ): # heuristic - they will put the answer in the bottom half.
        n += 1
        if n % 100000 == 0:
            # Progress indicator.
            print( 'N', n )
        I = A.intersect( y )
        if not I.covers( range( lo, hi ) ):
            # We have the y-coordinate. Now to extract the x-coordinate. Assume unique answer.
            for x in range( lo, hi ):
                if x not in I:
                    print( x, y, x * 4000000 + y )
                    return

if __name__ == "__main__":
    # part2( 'test.txt', 0, 20 )          # 56000011
    part2( 'input.txt', 0, 4000000 )