from elephants import *

def part1( fname ):
    S = readElephantFile( fname ).newSearch( 'AA', 30 )
    while S.canContinue():
        S.check()
    print( S.highScore() )

if __name__ == "__main__":
    # part1( 'test.txt' )     # 1651
    part1( 'input.txt' )
