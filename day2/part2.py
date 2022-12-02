from rock_paper_scissors import *

def part2():
    data = parseRockPaperScissorsFile( 'input.txt' )
    print( sum( map( eval_outcome, data ) ) )

if __name__ == "__main__":
    part2()