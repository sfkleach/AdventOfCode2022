from jets import *

def part1( fname, count ):
    S = readSimulationFile( fname )
    S.run( count )
    print( S.highestPoint() )

if __name__ == "__main__":
    part1( 'test.txt', 2022 )   # 3068
    # part1( 'input.txt', 2022 )  # 3173
