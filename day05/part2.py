from crates import *

def part2( fname ):
    ( crates, moves ) = readCratesFile( fname )
    Crane9001( crates ).applyMoves( moves )
    print( crates.signature() )

if __name__ == "__main__":
    part2( 'input.txt' )
