from assignments import *

def part2( fname ):
    count = 0
    for ( lhs, rhs ) in readAssignmentsFile( fname ):
        if lhs.isPartlyOverlapping( rhs ):
            count += 1
    print( count )

if __name__ == "__main__":
    part2( 'input.txt' )
