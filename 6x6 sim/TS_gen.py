import argparse
import numpy as np

gridsize = 7
num_d = 5
num_aa = 5
import itertools

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
    num=0
    for i in len(a):
        num+=a[i]*4**(num_d-i)
    return num

def get_state_code(drone_pos, aa_status):
    # Winning
    if np.sum(aa_status)==0:
        return 0
    state_code = 0
    for i in range(num_aa):
        state_code += aa_status[i]*10**i
    for j in range(num_d):
        for k in range(0,2):
            state_code += drone_pos[j,k]*10**(i+j+k)
    return state_code #100000*drone_pos1[0] + 10000*drone_pos1[1]+1000*drone_pos2[0] + 100*drone_pos2[1] + 10*aa1_status + aa2_status

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
        (3,2),
        (2,1),
        (5,4),
        (4,5)
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
    num_A = 4**(num_d)
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

    drone_pos = np.zeros([num_d,2])
    aa_statuses = np.zeros(num_aa)
    transitions = []
    states = [-1, 0] #change
    def generate_tuples(n):
        if n == 1:
            return [(0,), (1,)]
        else:
            tuples = generate_tuples(n - 1)
            result = []
            for tup in tuples:
                result.append(tup + (0,))
                result.append(tup + (1,))
            return result

    def filter_non_zero_sum_tuples(tuples):
        return [tup for tup in tuples if sum(tup) != 0]

    def generate_tuples_with_non_zero_sum(n):
        tuples = generate_tuples(n)
        return filter_non_zero_sum_tuples(tuples)
    
    aa_statuses=generate_tuples_with_non_zero_sum(num_aa)

    def generate_particle_states(n, m):
        coordinates = list(itertools.product(range(m), repeat=2))
        return list(itertools.product(coordinates, repeat=n))

    # Example usage
    n = 2 # Number of particles
    m = 6  # Size of the grid (m x m)
    states = generate_particle_states(n, m)
    print(len(states))
    print(states[5])
    for i in range(num_d):
        for x_coord in range(gridsize):
            for y_coord in range(gridsize):
                drone_pos[i,]=(x_coord,y_coord)
                for aa in range(num_aa):
                    for aa_status in aa_statuses:
                        states.append(get_state_code(drone_pos ,aa_statuses))
    for i in range(num_d):
        for x_coord in range(gridsize):
            for y_coord in range(gridsize):
                drone_pos[i,]=(x_coord,y_coord)
                drone_pos1 = (x_coord1, y_coord1)
                drone_pos2 = (x_coord2, y_coord2)#change made                    
                ################
                ## move-move ###
                # d1 move d2 move
                next_pos=[]
                for aa_status in aa_statuses:
                    for i in range(num_d):
                        for move_action in range(0,4,1):
                            next_pos[i] = np.array(drone_pos[i]) + np.array(movement_delta[move_action])
                            # Negative reward for going out of bounds
                            if out_of_arena(next_pos):
                                for move_action2 in range(1,4,1):
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
