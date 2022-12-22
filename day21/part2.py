from monkeys import *

def part2( fname ):
    M = readMonkeysFile( fname, 'humn' )
    M['root']._op = "=="
    R = M['root'].simplify()
    R.solve( None )

if __name__ == "__main__":
    # part2( 'test.txt' )
    part2( 'input.txt' )