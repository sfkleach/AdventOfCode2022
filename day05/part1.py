from crates import *

def part1( fname ):
    ( crates, moves ) = readCratesFile( fname )
    Crane9000( crates ).applyMoves( moves )
    print( crates.signature() )

if __name__ == "__main__":
    part1( 'input.txt' )
