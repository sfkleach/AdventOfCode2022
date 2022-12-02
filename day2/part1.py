from rock_paper_scissors import *

def part1():
    data = parseRockPaperScissorsFile( 'input.txt' )
    print( sum( map( eval_play, data ) ) )

if __name__ == "__main__":
    part1()
