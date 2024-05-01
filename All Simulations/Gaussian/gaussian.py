import argparse
import numpy as np

gridsize = 4

def aa_hit_prob(drone_pos1,drone_pos2, aa):
    d1 = np.linalg.norm(np.array(drone_pos1) - np.array(aa))
    d2 = np.linalg.norm(np.array(drone_pos2) - np.array(aa))
    p1 = 0.7*np.e**(-(3**2)*(d1-2)**2)
    p2 = 0.7*np.e**(-(3**2)*(d2-2)**2)
    if(p1>p2):
        return [p1,0]
    elif(p1<p2):
        return [0,p2]
    elif(p1==p2):
        return [p1/2,p2/2]

def drone_hit_prob(drone_pos, aa):
    d = np.linalg.norm(np.array(drone_pos) - np.array(aa))
    return np.e**(-0.75*d)

def out_of_arena(drone_pos1,drone_pos2):
    if drone_pos1[0] < 0 or drone_pos1[0] >= gridsize or drone_pos2[0] < 0 or drone_pos2[0] >= gridsize:
        return True
    if drone_pos1[1] < 0 or drone_pos1[1] >= gridsize or drone_pos2[1] < 0 or drone_pos2[1] >= gridsize:
        return True
    return False

def spit_action(a):
    return 6*a[0]+a[1]

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
        (3,0),
        (0,3)
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

    num_S = 2 + 3*(gridsize**4)  #change made
    num_A = 36
    drone_death_reward = -2
    aa_kill_reward = 5
    actions = {
        0: "shoot first aa",
        1: "shoot second aa",
        2: "move up",
        3: "move left",
        4: "move down",
        5: "move right"
    }
    movement_delta = {
        2: (0,-1),
        3: (-1,0),
        4: (0,1),
        5: (1,0)
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
    #states=[-1,0,next 16 numbers have state val when aa2 is alive,next 16 when aa1 is alive, next 16 when both alive]
    #-1 and 0 are default states
    for x_coord1 in range(gridsize):
        for y_coord1 in range(gridsize):
            for x_coord2 in range(gridsize):
                for y_coord2 in range(gridsize):
                    drone_pos1 = (x_coord1, y_coord1)
                    drone_pos2 = (x_coord2, y_coord2)#change made
                    
                    ##################
                    ### attack-attack ###
                    for aa_statuses in [(0,1), (1,0), (1,1)]:
                        for action in [(0,0),(0,1),(1,0),(1,1)]:
                            a1 = aa_hit_prob(drone_pos1,drone_pos2,aa_positions[0])
                            a2 = aa_hit_prob(drone_pos1,drone_pos2,aa_positions[1])
                            aa1_d1 = a1[0]
                            aa2_d1 = a1[1]
                            aa1_d2 = a2[0]
                            aa2_d2 = a2[1]
                            prob_drone_not_hit1 =(1-aa_statuses[0]*aa1_d1)*(1-aa_statuses[1]*aa2_d1)
                            prob_drone_not_hit2 =(1-aa_statuses[0]*aa1_d2)*(1-aa_statuses[1]*aa2_d2)

                            d1_aa1 = drone_hit_prob(drone_pos2,aa_positions[0])*aa_statuses[0]*(1-action[0])
                            d1_aa2 = drone_hit_prob(drone_pos2,aa_positions[1])*aa_statuses[1]*(action[0])
                            d2_aa1 = drone_hit_prob(drone_pos2,aa_positions[0])*aa_statuses[0]*(1-action[1])
                            d2_aa2 = drone_hit_prob(drone_pos2,aa_positions[1])*aa_statuses[1]*(action[1])
                            aa1_not_killed_prob = (1-d1_aa1)*(1-d2_aa1)
                            aa2_not_killed_prob = (1-d1_aa2)*(1-d2_aa2)

                            transitions.append(( #all miss
                                states.index(get_state_code(drone_pos1, drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action(action),
                                states.index(get_state_code(drone_pos1, drone_pos2, aa_statuses[0], aa_statuses[1])), 0, prob_drone_not_hit1*prob_drone_not_hit2*aa1_not_killed_prob*aa2_not_killed_prob
                            ))
                            transitions.append(( #any drone dies    
                                states.index(get_state_code(drone_pos1,drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action(action),
                                states.index(-1), drone_death_reward, (1-prob_drone_not_hit1*prob_drone_not_hit2)
                            ))
                            transitions.append(( #a1 dies
                                states.index(get_state_code(drone_pos1,drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action(action),
                                states.index(get_state_code(drone_pos1,drone_pos2, 0, aa_statuses[1])), aa_kill_reward, prob_drone_not_hit1*prob_drone_not_hit2*(1-aa1_not_killed_prob)*aa2_not_killed_prob
                            ))
                            transitions.append(( #a2 dies
                                states.index(get_state_code(drone_pos1,drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action(action),
                                states.index(get_state_code(drone_pos1,drone_pos2, aa_statuses[0], 0)), aa_kill_reward, prob_drone_not_hit1*prob_drone_not_hit2*aa1_not_killed_prob*(1-aa2_not_killed_prob)
                            ))
                            transitions.append(( #both a1,a2 die
                                states.index(get_state_code(drone_pos1,drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action(action),
                                states.index(get_state_code(drone_pos1,drone_pos2, 0, 0)), 2*aa_kill_reward, prob_drone_not_hit1*prob_drone_not_hit2*(1-aa1_not_killed_prob)*(1-aa2_not_killed_prob)
                            ))
                    
                    ################
                    ## move-attack ###
                    # d1 moves d2 attack
                    for aa_statuses in [(0,1), (1,0), (1,1)]:
                        for action in [0,1]:
                            for move_action in range(2,6,1):
                                next_pos = np.array(drone_pos1) + np.array(movement_delta[move_action])
                                # Negative reward for going out of bounds
                                if out_of_arena(next_pos,drone_pos2):
                                    transitions.append((
                                        states.index(get_state_code(drone_pos1, drone_pos2, aa_statuses[0], aa_statuses[1])),
                                        spit_action([move_action,action]), states.index(-1), drone_death_reward, 1
                                    ))
                                    continue
                                # Remaining cases
                                a1 = aa_hit_prob(drone_pos1,drone_pos2,aa_positions[0])
                                a2 = aa_hit_prob(drone_pos1,drone_pos2,aa_positions[1])
                                aa1_d1 = a1[0]
                                aa2_d1 = a1[1]
                                aa1_d2 = a2[0]
                                aa2_d2 = a2[1]
                                prob_drone_not_hit1 =(1-aa_statuses[0]*aa1_d1)*(1-aa_statuses[1]*aa2_d1)
                                prob_drone_not_hit2 =(1-aa_statuses[0]*aa1_d2)*(1-aa_statuses[1]*aa2_d2)

                                if np.linalg.norm(np.array(next_pos) - np.array(aa_positions[0])) == 0:
                                    d1_aa1 = 1*aa_statuses[0]
                                else:
                                    d1_aa1 = 0
                                if np.linalg.norm(np.array(next_pos) - np.array(aa_positions[1])) == 0:
                                    d1_aa2 = 1*aa_statuses[1]
                                else:
                                    d1_aa2 = 0

                                d2_aa1 = drone_hit_prob(drone_pos2,aa_positions[0])*aa_statuses[0]*(1-action)
                                d2_aa2 = drone_hit_prob(drone_pos2,aa_positions[1])*aa_statuses[1]*(action)
                                aa1_not_killed_prob = (1-d1_aa1)*(1-d2_aa1)
                                aa2_not_killed_prob = (1-d1_aa2)*(1-d2_aa2)

                                transitions.append(( #all miss
                                states.index(get_state_code(drone_pos1, drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action([move_action,action]),
                                states.index(get_state_code(next_pos, drone_pos2, aa_statuses[0], aa_statuses[1])), 0, prob_drone_not_hit1*prob_drone_not_hit2*aa1_not_killed_prob*aa2_not_killed_prob
                                ))
                                transitions.append(( #any drone dies    
                                    states.index(get_state_code(drone_pos1,drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action([move_action,action]),
                                    states.index(-1), drone_death_reward, (1-prob_drone_not_hit1*prob_drone_not_hit2)
                                ))
                                transitions.append(( #a1 dies
                                    states.index(get_state_code(drone_pos1,drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action([move_action,action]),
                                    states.index(get_state_code(next_pos,drone_pos2, 0, aa_statuses[1])), aa_kill_reward, prob_drone_not_hit1*prob_drone_not_hit2*(1-aa1_not_killed_prob)*aa2_not_killed_prob
                                ))
                                transitions.append(( #a2 dies
                                    states.index(get_state_code(drone_pos1,drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action([move_action,action]),
                                    states.index(get_state_code(next_pos,drone_pos2, aa_statuses[0], 0)), aa_kill_reward, prob_drone_not_hit1*prob_drone_not_hit2*aa1_not_killed_prob*(1-aa2_not_killed_prob)
                                ))
                                transitions.append(( #both a1,a2 die
                                    states.index(get_state_code(drone_pos1,drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action([move_action,action]),
                                    states.index(get_state_code(next_pos,drone_pos2, 0, 0)), 2*aa_kill_reward, prob_drone_not_hit1*prob_drone_not_hit2*(1-aa1_not_killed_prob)*(1-aa2_not_killed_prob)
                                ))
                    
                    ################
                    ## attack-move ###
                    # d1 attack d2 move
                    for aa_statuses in [(0,1), (1,0), (1,1)]:
                        for action in [0,1]:
                            for move_action in range(2,6,1):
                                next_pos = np.array(drone_pos2) + np.array(movement_delta[move_action])
                                # Negative reward for going out of bounds
                                if out_of_arena(drone_pos1,next_pos):
                                    transitions.append((
                                        states.index(get_state_code(drone_pos1, drone_pos2, aa_statuses[0], aa_statuses[1])),
                                        spit_action([move_action,action]), states.index(-1), drone_death_reward, 1
                                    ))
                                    continue
                                # Remaining cases
                                a1 = aa_hit_prob(drone_pos1,drone_pos2,aa_positions[0])
                                a2 = aa_hit_prob(drone_pos1,drone_pos2,aa_positions[1])
                                aa1_d1 = a1[0]
                                aa2_d1 = a1[1]
                                aa1_d2 = a2[0]
                                aa2_d2 = a2[1]
                                prob_drone_not_hit1 =(1-aa_statuses[0]*aa1_d1)*(1-aa_statuses[1]*aa2_d1)
                                prob_drone_not_hit2 =(1-aa_statuses[0]*aa1_d2)*(1-aa_statuses[1]*aa2_d2)

                                if np.linalg.norm(np.array(next_pos) - np.array(aa_positions[0])) == 0:
                                    d2_aa1 = 1*aa_statuses[0]
                                else:
                                    d2_aa1 = 0
                                if np.linalg.norm(np.array(next_pos) - np.array(aa_positions[1])) == 0:
                                    d2_aa2 = 1*aa_statuses[1]
                                else:
                                    d2_aa2 = 0

                                d1_aa1 = drone_hit_prob(drone_pos2,aa_positions[0])*aa_statuses[0]*(1-action)
                                d1_aa2 = drone_hit_prob(drone_pos2,aa_positions[1])*aa_statuses[1]*(action)
                                aa1_not_killed_prob = (1-d1_aa1)*(1-d2_aa1)
                                aa2_not_killed_prob = (1-d1_aa2)*(1-d2_aa2)

                                transitions.append(( #all miss
                                    states.index(get_state_code(drone_pos1, drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action([move_action,action]),
                                    states.index(get_state_code(drone_pos1, next_pos, aa_statuses[0], aa_statuses[1])), 0, prob_drone_not_hit1*prob_drone_not_hit2*aa1_not_killed_prob*aa2_not_killed_prob
                                ))
                                transitions.append(( #any drone dies    
                                    states.index(get_state_code(drone_pos1,drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action([move_action,action]),
                                    states.index(-1), drone_death_reward, (1-prob_drone_not_hit1*prob_drone_not_hit2)
                                ))
                                transitions.append(( #a1 dies
                                    states.index(get_state_code(drone_pos1,drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action([move_action,action]),
                                    states.index(get_state_code(drone_pos1,next_pos, 0, aa_statuses[1])), aa_kill_reward, prob_drone_not_hit1*prob_drone_not_hit2*(1-aa1_not_killed_prob)*aa2_not_killed_prob
                                ))
                                transitions.append(( #a2 dies
                                    states.index(get_state_code(drone_pos1,drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action([move_action,action]),
                                    states.index(get_state_code(drone_pos1,next_pos, aa_statuses[0], 0)), aa_kill_reward, prob_drone_not_hit1*prob_drone_not_hit2*aa1_not_killed_prob*(1-aa2_not_killed_prob)
                                ))
                                transitions.append(( #both a1,a2 die
                                    states.index(get_state_code(drone_pos1,drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action([move_action,action]),
                                    states.index(get_state_code(drone_pos1,next_pos, 0, 0)), 2*aa_kill_reward, prob_drone_not_hit1*prob_drone_not_hit2*(1-aa1_not_killed_prob)*(1-aa2_not_killed_prob)
                                ))
                    
                    ################
                    ## move-move ###
                    # d1 move d2 move
                    for aa_statuses in [(0,1), (1,0), (1,1)]:
                        for move_action1 in range(2,6,1):
                            next_pos1 = np.array(drone_pos1) + np.array(movement_delta[move_action])
                                # Negative reward for going out of bounds
                            if out_of_arena(next_pos1,drone_pos2):
                                for move_action2 in range(2,6,1):
                                    transitions.append((
                                        states.index(get_state_code(drone_pos1, drone_pos2, aa_statuses[0], aa_statuses[1])),
                                        spit_action([move_action1,move_action2]), states.index(-1), drone_death_reward, 1
                                    ))
                                continue
                            for move_action2 in range(2,6,1):
                                next_pos2 = np.array(drone_pos2) + np.array(movement_delta[move_action])
                                # Negative reward for going out of bounds
                                if out_of_arena(next_pos1,next_pos2):
                                    transitions.append((
                                        states.index(get_state_code(drone_pos1, drone_pos2, aa_statuses[0], aa_statuses[1])),
                                        spit_action([move_action1,move_action2]), states.index(-1), drone_death_reward, 1
                                    ))
                                    continue
                                # Remaining cases
                                a1 = aa_hit_prob(drone_pos1,drone_pos2,aa_positions[0])
                                a2 = aa_hit_prob(drone_pos1,drone_pos2,aa_positions[1])
                                aa1_d1 = a1[0]
                                aa2_d1 = a1[1]
                                aa1_d2 = a2[0]
                                aa2_d2 = a2[1]
                                prob_drone_not_hit1 =(1-aa_statuses[0]*aa1_d1)*(1-aa_statuses[1]*aa2_d1)
                                prob_drone_not_hit2 =(1-aa_statuses[0]*aa1_d2)*(1-aa_statuses[1]*aa2_d2)

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
                                transitions.append(( #any drone dies    
                                    states.index(get_state_code(drone_pos1,drone_pos2, aa_statuses[0], aa_statuses[1])), spit_action([move_action1,move_action2]),
                                    states.index(-1), drone_death_reward, (1-prob_drone_not_hit1*prob_drone_not_hit2)
                                ))
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
