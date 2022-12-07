from consoletrace import *

def part2( fname ):
    info = readConsoleTraceFile( fname )
    used = info.totalSize( () )
    capacity = 70000000
    free = capacity - used
    goal = 30000000
    must_delete = max( 0, goal - free )
    list = [ info.totalSize(p) for p in info.directories() ]
    list.sort()
    for n in list:
        if n >= must_delete:
            print( n )
            return

if __name__ == "__main__":
    part2( 'input.txt' )