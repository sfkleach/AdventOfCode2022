from jets import *

def part2( fname, count ):
    S = readSimulationFile( fname )
    loop = S.detectLoop()
    count_after_loop_start = count - loop['start']
    increase_due_to_looping = ( count_after_loop_start // loop['steps_delta'] ) * loop['height_delta'] 
    initial_height = loop['start_height']
    current_height = S.highestPoint()
    S.run( ( count - loop['start'] ) % loop['steps_delta'] )
    height_added_by_remainder = S.highestPoint() - current_height
    predicted = initial_height + increase_due_to_looping + height_added_by_remainder
    print( predicted )

if __name__ == "__main__":
    # part2( 'test.txt', 1000000000000 )   # 1514285714288
    part2( 'input.txt', 1000000000000 )  # 