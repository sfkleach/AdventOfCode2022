from rucksack import *

def part1():
    print( sum( map( linePriority, linesRucksackFile( 'input.txt' ) ) ) )

if __name__ == "__main__":
    part1()