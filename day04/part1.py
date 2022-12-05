from assignments import *

def part1( fname ):
    count = 0
    for ( lhs, rhs ) in readAssignmentsFile( fname ):
        if lhs.isFullyOverlapping( rhs ):
            count += 1
    print( count )

if __name__ == "__main__":
    part1( 'input.txt' )
