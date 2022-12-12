from elevation import *

def solutionsFromZeroElevations( e ):
    """
    Does a lot of duplicated work. Maybe Warshall's algorithm was a better bet.
    But it completes in a few seconds, so good enough for the puzzle.
    """
    for rc in e.findZeroElevations():
        n = e.shortestPathFrom( rc )    # Duplication of work.
        if n is not None:
            yield n

def part2( fname ):
    e = readElevationFile( fname )
    print( min( solutionsFromZeroElevations( e ) ) )

if __name__ == "__main__":
    part2( 'input.txt' )
