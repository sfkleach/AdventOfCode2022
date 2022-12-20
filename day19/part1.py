from factory import *

def part1( fname ):
    total = 0
    for bp in readBlueprintsFile( fname ):
        best = bp.best()
        print( 'BEST', bp._number, best )
        total += bp._number * best
    print( 'TOTAL', total )


if __name__ == "__main__":
    # part1( 'test.txt' )     # 33
    # part1( 'bug.txt' )
    part1( 'input.txt' )
