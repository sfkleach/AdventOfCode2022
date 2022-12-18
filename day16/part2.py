from elephants import *

def part2( fname ):
    S = readElephantFile( fname ).newSearch( ['AA', 'AA'], 26 )
    while S.canContinue():
        S.check()
    print( S.highScore() )

if __name__ == "__main__":
    part2( 'test.txt' )     # 1707
    # part2( 'input.txt' )
