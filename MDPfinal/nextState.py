# nextState.py

def nextState(current_positions):
    # Split the current positions string into a list of integers
    positions_list = [int(pos) for pos in current_positions.split(',')]

    # Increment the x-coordinate of drone1 (first drone) for rightward movement
    positions_list[0] += 1

    # Convert the updated positions list back to the required string format
    next_positions = ','.join(map(str, positions_list))

    return next_positions
