from factory import *

def part2( fname ):
    total = 1
    for bp in readBlueprintsFile( fname ):
        best = bp.calculateBest( 32 )
        total *= best.score()
        print( 'BEST', bp._number, best.score(), best.altScore() )
    print( 'TOTAL', total )


if __name__ == "__main__":
    # part2( 'test.txt' )     # 33
    part2( 'short_input.txt' )     # 33
    # part1( 'ex2.txt' )
    # part1( 'input.txt' )
