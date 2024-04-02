import sys
import argparse
import math

parser = argparse.ArgumentParser()

# x coordinates goes from 0 to 3, from left to right
# y coordinate goes from 0 to 3, from top to bottom
# 0,1,2,3 is L,R,U,D for B1
# 4,5,6,7 is L,R,U,D for B2
# 8 is attempt to pass
# 9 is attempt a shot on goal

lines = []
mov_x = [-1,1,0,0] ## L,R,U,D
mov_y = [0,0,-1,1] ## L,R,U,D

def handle_movement_actions(player, arr_p_success, p_opp, r_x, r_y, b1_x, b1_y, b2_x, b2_y, s, a, possession, trap_state):
    # success_prob = 0
    p_success = arr_p_success[player - 1]
    for i in range(4): ## for L,R,U,D movement of opponent
        p_mov_opp = p_opp[i] ## prob of opponent of moving L,R,U,D
        r_x_new = r_x + mov_x[i]
        r_y_new = r_y + mov_y[i]
        b1_x_new = b1_x + (1 - int(a/4))*mov_x[a%4]
        b1_y_new = b1_y + (1 - int(a/4))*mov_y[a%4]
        b2_x_new = b2_x + int(a/4)*mov_x[a%4]
        b2_y_new = b2_y + int(a/4)*mov_y[a%4]
        arr_new_x = [b1_x_new, b2_x_new]
        arr_new_y = [b1_y_new, b2_y_new]
        arr_old_x = [b1_x, b2_x]
        arr_old_y = [b1_y, b2_y]
        if(p_mov_opp > 0): ## Opponent takes that step
            penalty_factor = 1
            if(possession == player and r_x_new == arr_new_x[player-1] and r_y_new == arr_new_y[player-1]): ## Tackling (A)
                penalty_factor = 0.5
            if(possession == player and r_x_new == arr_old_x[player-1] and r_y_new == arr_old_y[player-1] and arr_new_x[player-1] == r_x and arr_new_y[player-1] == r_y): ## Tackling (B)
                penalty_factor = 0.5
            print(f"transition {s} {a} {encode_state(possession, b1_x_new, b1_y_new, b2_x_new, b2_y_new, r_x_new, r_y_new)} {0} {p_mov_opp*penalty_factor*p_success}")
            # success_prob += p_mov_opp*penalty_factor*p_success
    ## Moving to trap state on failure
    # print(f"transition {s} {a} {trap_state} {0} {1 - success_prob}")

def encode_state(possession, b1_x, b1_y, b2_x, b2_y, r_x, r_y):
    position_b1 = b1_y*4 + b1_x + 1
    position_b2 = b2_y*4 + b2_x + 1
    position_r = r_y*4 + r_x + 1
    s_ = (possession - 1) + (position_r - 1)*2 + (position_b2 - 1)*32 + (position_b1 - 1)*512
    return s_

def handle_passing_actions(s,a,b1_x,b1_y,b2_x,b2_y,r_x,r_y,possession,trap_state,p_opp):
    p_success = q - 0.1*max(abs(b1_x - b2_x), abs(b1_y - b2_y))
    # success_prob = 0
    for i in range(4): ## for L,R,U,D movement of opponent
        p_mov_opp = p_opp[i] ## prob of opponent of moving L,R,U,D
        r_x_new = r_x + mov_x[i]
        r_y_new = r_y + mov_y[i]
        if(p_mov_opp > 0):
            penalty = 1
            if(in_between(b1_x, b1_y, b2_x, b2_y, r_x_new, r_y_new)):
                penalty = 0.5
            print(f"transition {s} {a} {encode_state(3-possession, b1_x, b1_y, b2_x, b2_y, r_x_new, r_y_new)} {0} {p_mov_opp*penalty*p_success}")
            # success_prob += p_mov_opp*penalty*p_success
    # print(f"transition {s} {a} {trap_state} {0} {1 - success_prob}")

def in_between(b1_x, b1_y, b2_x, b2_y, r_x, r_y): ## Returns true if R in between
    if(b1_x == b2_x): ## Vertical Line
        if(abs(r_y - b1_y) + abs(r_y - b2_y) == abs(b1_y - b2_y) and r_x == b1_x):
            return True
    elif(b1_y == b2_y): ## Horizontal Line
        if(abs(r_x - b1_x) + abs(r_x - b2_x) == abs(b1_x - b2_x) and r_y == b1_y):
            return True
    elif(abs(b1_x - b2_x) == abs(b1_y - b2_y)): ## Diagonal Line
        if((b1_x == r_x and b1_y == r_y) or (b2_x == r_x and b2_y == r_y)): 
            return True
        elif(abs((dist(r_x,r_y,b1_x,b1_y) + dist(r_x,r_y,b2_x,b2_y)) - dist(b1_x,b1_y,b2_x,b2_y)) < 1e-6):
            return True
    else:
        return False
    
def dist(x1,y1,x2,y2):
    return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))
    
def handle_shooting_actions(s, a, b1_x, b2_x, r_x, r_y, possession, trap_state, p_opp):
    if(possession == 1):
        p_success = q - 0.2*(3 - b1_x)
    else:
        p_success = q - 0.2*(3 - b2_x)
    success_prob = 0
    for i in range(4): ## for L,R,U,D movement of opponent
        p_mov_opp = p_opp[i] ## prob of opponent of moving L,R,U,D
        r_x_new = r_x + mov_x[i]
        r_y_new = r_y + mov_y[i]
        if(p_mov_opp > 0):
            penalty = 1
            if(r_x_new == 3 and (r_y_new == 1 or r_y_new == 2)):
                penalty = 0.5
            success_prob += p_mov_opp*penalty*p_success
    print(f"transition {s} {a} {trap_state} {1} {success_prob}")
    # print(f"transition {s} {a} {trap_state} {0} {1 - success_prob}")

def print_transitons(numStates, numActions, p, q):
    trap_state = numStates - 1
    for s in range(numStates-1):
        possession = s%2 + 1
        position_opponent = (s//2)%16 + 1
        position_b2 = (s//32)%16 + 1
        position_b1 = (s//512)%16 + 1
        r_x = int((position_opponent - 1)%4)
        r_y = int((position_opponent - 1)/4)
        b1_x = int((position_b1 - 1)%4)
        b1_y = int((position_b1 - 1)/4)
        b2_x = int((position_b2 - 1)%4)
        b2_y = int((position_b2 - 1)/4)
        words = lines[s+1].split()
        p_opp = [float(words[1]), float(words[2]), float(words[3]), float(words[4])] ## p_L, p_R, p_U, p_D
        if(possession == 1):
            p_success_b1 = 1 - 2*p
            p_success_b2 = 1 - p
        else:
            p_success_b1 = 1 - p
            p_success_b2 = 1 - 2*p
        arr_p_success = [p_success_b1, p_success_b2]
        out_board_arr_check = [b1_x, b1_x, b1_y, b1_y, b2_x, b2_x, b2_y, b2_y]

        ## Movement :
        for a in range(8):
            player = int(a/4) + 1
            if(out_board_arr_check[a] == 3*(a%2)): ## Going out of board
                continue
            handle_movement_actions(player=player, arr_p_success=arr_p_success, p_opp=p_opp, r_x=r_x, r_y=r_y, b1_x=b1_x, b1_y=b1_y, b2_x=b2_x, b2_y=b2_y, s=s, a=a, possession=possession, trap_state=trap_state)
            
        ## Passing :
        handle_passing_actions(s=s, a=8, b1_x=b1_x, b1_y=b1_y, b2_x=b2_x, b2_y=b2_y, r_x=r_x, r_y=r_y, possession=possession, trap_state=trap_state, p_opp=p_opp)
        
        ## Shooting :
        handle_shooting_actions(s=s, a=9, b1_x=b1_x, b2_x=b2_x, r_x=r_x, r_y=r_y, possession=possession, trap_state=trap_state, p_opp=p_opp)
        




if __name__ == "__main__":
    parser.add_argument("--opponent", type=str, default=None)
    parser.add_argument("--p", type=float, default=-1)
    parser.add_argument("--q", type=float, default=-1)

    args = parser.parse_args()

    opponent_file_loc = args.opponent
    p = args.p
    q = args.q

    with open(opponent_file_loc, 'r') as file:
        lines = file.readlines()

    if(opponent_file_loc == None or p == -1 or q == -1 ):
        print("Incorrect Arguments, Exiting")
        sys.exit()

    numStates = 8193
    numActions = 10

    print(f"numStates {numStates}")
    print(f"numActions {numActions}")
    print(f"end {numStates - 1}")
    print_transitons(numStates, numActions, p, q)
    print("mdptype episodic")
    print("discount 1.0")
