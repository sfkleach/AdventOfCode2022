from factory import *

def part1( fname ):
    total = 0
    for bp in readBlueprintsFile( fname ):
        best = bp.calculateBest( 24 )
        # print( 'BEST', bp._number, best.score(), best.altScore() )
        total += bp._number * best.score()
    print( 'TOTAL', total )


if __name__ == "__main__":
    part1( 'test.txt' )     # 33
    # part1( 'ex2.txt' )
    # part1( 'input.txt' )
