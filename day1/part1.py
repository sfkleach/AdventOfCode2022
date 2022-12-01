from calories import parseCaloriesFile

def findMax( data ):
    return max( map( sum, data ) )

def part1( *, srcfile ):
    data = parseCaloriesFile( srcfile )
    mx = findMax( data )
    print( mx )

if __name__ == "__main__":
    part1( srcfile='input.txt' )