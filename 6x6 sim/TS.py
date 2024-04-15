import argparse
import numpy as np

gridsize = 6


def aa_hit_prob(drone_pos1,drone_pos2, aa):
    d1 = np.linalg.norm(np.array(drone_pos1) - np.array(aa))
    d2 = np.linalg.norm(np.array(drone_pos2) - np.array(aa))
    if(d1<d2):
        return [1*np.e**(-d1),0]
    elif(d1>d2):
        return [0,1*np.e**(-d2)]
    else:
        return [0.5*np.e**(-d1),0.5*np.e**(-d2)]

def drone_hit_prob(drone_pos, aa):
    return 1*np.e**-(np.linalg.norm(np.array(drone_pos) - np.array(aa)))

def out_of_arena(drone_pos1,drone_pos2):
    if drone_pos1[0] < 0 or drone_pos1[0] > gridsize-1 or drone_pos2[0] < 0 or drone_pos2[0] > gridsize-1:
        return True
    if drone_pos1[1] < 0 or drone_pos1[1] > gridsize-1 or drone_pos2[1] < 0 or drone_pos2[1] > gridsize-1:
        return True
    return False

def spit_action(a):
    return 4*a[0]+a[1]

def get_state_code(drone_pos1,drone_pos2, aa1_status, aa2_status):
    # Winning
    if aa1_status == 0 and aa2_status == 0:
        return 0
    return 100000*drone_pos1[0] + 10000*drone_pos1[1]+1000*drone_pos2[0] + 100*drone_pos2[1] + 10*aa1_status + aa2_status

def print_as_mdp(num_S, num_A, transitions):
    print("numStates", num_S)
    print("numActions", num_A)
    print("end 0 1")
    for t in transitions:
        print("transition", t[0], t[1], t[2], t[3], t[4])
    print("mdptype episodic")
    print("discount 1.0")

if __name__=="__main__":
    aa_positions = [
        (2,0),
        (3,2)
    ]
    # abcd
    # a-drone x
    # b-drone y
    # c-aa1 alive
    # d-aa2 alive
    # 16 for each drone
    # 3 for statuses of both the anti-airs
    # 3 end states:
    # -1 -> any drone dies
    # 0 -> both anti-airs dead

    num_S = 2 + gridsize*gridsize*gridsize*gridsize*3  #change made
    num_A = 16
    drone_death_reward = -2
    aa_kill_reward = 5
    actions = {
        #0: "shoot first aa",
        #1: "shoot second aa",
        0: "move up",
        1: "move left",
        2: "move down",
        3: "move right"
    }
    movement_delta = {
        0: (0,-1),
        1: (-1,0),
        2: (0,1),
        3: (1,0)
    }

    transitions = []
    states = [-1, 0] #change
    for x_coord1 in range(gridsize):
        for y_coord1 in range(gridsize):
            for x_coord2 in range(gridsize):
                for y_coord2 in range(gridsize):
                    states.append(get_state_code((x_coord1, y_coord1),(x_coord2, y_coord2), 0, 1))
                    states.append(get_state_code((x_coord1, y_coord1),(x_coord2, y_coord2), 1, 0))
                    states.append(get_state_code((x_coord1, y_coord1),(x_coord2, y_coord2), 1, 1))
    
    for x_coord1 in range(gridsize):
        for y_coord1 in range(gridsize):
            for x_coord2 in range(gridsize):
                for y_coord2 in range(gridsize):
                    drone_pos1 = (x_coord1, y_coord1)
                    drone_pos2 = (x_coord2, y_coord2)#change made
                    
                    ################
                    ## move-move ###
                    # d1 move d2 move
                    for aa_statuses in [(0,1), (1,0), (1,1)]:
                        for move_action1 in range(0,4,1):
                            next_pos1 = np.array(drone_pos1) + np.array(movement_delta[move_action1])
                                # Negative reward for going out of bounds
                            if out_of_arena(next_pos1,drone_pos2):
                                for move_action2 in range(1,4,1):
                                    transitions.append((
                                        states.index(get_state_code(drone_pos1, drone_pos2, aa_statuses[0], aa_statuses[1])),
                                        spit_action([move_action1,move_action2]), states.index(-1), drone_death_reward, 1
                                    ))
                                continue
                            for move_action2 in range(0,4,1):
                                next_pos2 = np.array(drone_pos2) + np.array(movement_delta[move_action2])
                                # Negative reward for going out of bounds
                                if out_of_arena(next_pos1,next_pos2):
                                    transitions.append((
                                        states.index(get_state_code(drone_pos1, drone_pos2, aa_statuses[0], aa_statuses[1])),
                                        spit_action([move_action1,move_action2]), states.index(-1), drone_death_reward, 1
                                    ))
                                    continue
                                # Remaining cases
                                a1 = [0,0]#aa_hit_prob(drone_pos1,drone_pos2,aa_positions[0])
                                a2 = [0,0]#aa_hit_prob(drone_pos1,drone_pos2,aa_positions[1])
                                aa1_d1 = a1[0]
                                aa1_d2 = a1[1]
                                aa2_d1 = a2[0]
                                aa2_d2 = a2[1]
                                prob_drone_not_hit1 =1#(1-aa_statuses[0]*aa1_d1)*(1-aa_statuses[1]*aa2_d1)
                                prob_drone_not_hit2 =1#(1-aa_statuses[0]*aa1_d2)*(1-aa_statuses[1]*aa2_d2)

                                if np.linalg.norm(np.array(next_pos1) - np.array(aa_positions[0])) == 0:
                                    d1_aa1 = 1*aa_statuses[0]
                                else:
                                    d1_aa1 = 0
                                if np.linalg.norm(np.array(next_pos1) - np.array(aa_positions[1])) == 0:
                                    d1_aa2 = 1*aa_statuses[1]
                                else:
                                    d1_aa2 = 0
                                if np.linalg.norm(np.array(next_pos2) - np.array(aa_positions[0])) == 0:
                                    d2_aa1 = 1*aa_statuses[0]
                                else:
                                    d2_aa1 = 0
                                if np.linalg.norm(np.array(next_pos2) - np.array(aa_positions[1])) == 0:
                                    d2_aa2 = 1*aa_statuses[1]
                                else:
                                    d2_aa2 = 0
                                
                                aa1_not_killed_prob = (1-d1_aa1)*(1-d2_aa1)
                                aa2_not_killed_prob = (1-d1_aa2)*(1-d2_aa2)

                                transitions.append(( #all miss
                                    states.index(get_state_code(drone_pos1, drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action([move_action1,move_action2]),
                                    states.index(get_state_code(next_pos1, next_pos2, aa_statuses[0], aa_statuses[1])), -0.5, prob_drone_not_hit1*prob_drone_not_hit2*aa1_not_killed_prob*aa2_not_killed_prob
                                ))
                                # transitions.append(( #any drone dies    
                                #     states.index(get_state_code(drone_pos1,drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action([move_action1,move_action2]),
                                #     states.index(-1), drone_death_reward, (1-prob_drone_not_hit1*prob_drone_not_hit2)
                                # ))
                                transitions.append(( #a1 dies
                                    states.index(get_state_code(drone_pos1,drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action([move_action1,move_action2]),
                                    states.index(get_state_code(next_pos1, next_pos2, 0, aa_statuses[1])), aa_kill_reward, prob_drone_not_hit1*prob_drone_not_hit2*(1-aa1_not_killed_prob)*aa2_not_killed_prob
                                ))
                                transitions.append(( #a2 dies
                                    states.index(get_state_code(drone_pos1,drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action([move_action1,move_action2]),
                                    states.index(get_state_code(next_pos1, next_pos2, aa_statuses[0], 0)), aa_kill_reward, prob_drone_not_hit1*prob_drone_not_hit2*aa1_not_killed_prob*(1-aa2_not_killed_prob)
                                ))
                                transitions.append(( #both a1,a2 die
                                    states.index(get_state_code(drone_pos1,drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action([move_action1,move_action2]),
                                    states.index(get_state_code(next_pos1, next_pos2, 0, 0)), 2*aa_kill_reward, prob_drone_not_hit1*prob_drone_not_hit2*(1-aa1_not_killed_prob)*(1-aa2_not_killed_prob)
                                ))      

    transitions = [item for item in transitions if item[4] != 0]
    print_as_mdp(num_S, num_A, transitions)
