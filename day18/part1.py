from droplet import *

def part1( fname ):
    D = readDropletFile( fname )
    print( D.surfaceArea() )

if __name__ == "__main__":
    # part1( 'test.txt' )     # 64
    part1( 'input.txt' )    # 
    