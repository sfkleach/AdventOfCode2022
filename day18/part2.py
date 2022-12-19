from droplet import *

def part2( fname ):
    D = readDropletFile( fname )
    print( D.exterior() )

if __name__ == "__main__":
    # part2( 'test.txt' )     # 58
    part2( 'input.txt' )    # 
    