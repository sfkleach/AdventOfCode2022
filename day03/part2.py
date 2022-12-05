from rucksack import *

def part2():
    print( sum( map( tripletPriority, tripletsRucksackFile( 'input.txt' ) ) ) )

if __name__ == "__main__":
    part2()