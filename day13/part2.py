from packets import *
from functools import cmp_to_key

def cmp( left, right ):
    r = compare( left, right )
    return -1 if r is True else 1 if r is False else 0

def part2( fname ):
    pairs = readPacketsFile( fname )
    packets = [ i for p in pairs for i in p ]
    packets.append( [[2]] )
    packets.append( [[6]] )
    packets.sort( key=cmp_to_key( cmp ) )
    a = packets.index( [[2]] )
    b = packets.index( [[6]] )
    print( (a+1)*(b+1) )

if __name__ == "__main__":
    part2( 'input.txt' )
