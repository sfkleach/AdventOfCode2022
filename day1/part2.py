from calories import parseCaloriesFile

def sumTop3( data ):
    sums = sorted( map( sum, data ), reverse=True )
    return sum( sums[0:3] )

def part2( *, srcfile ):
    data = parseCaloriesFile( srcfile )
    subtotal = sumTop3( data )
    print( subtotal )

if __name__ == "__main__":
    part2( srcfile='input.txt' )