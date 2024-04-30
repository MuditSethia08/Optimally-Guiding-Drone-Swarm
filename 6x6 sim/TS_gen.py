import argparse
import numpy as np
import itertools

gridsize = 4
num_d = 2
aa_positions = [
        (2,0),
        (3,2)#,
        # (2,1),
        # (5,4),
        # (4,5)
    ]
num_aa = len(aa_positions)


def out_of_arena(drone_pos):
    a = np.any(drone_pos>=gridsize)
    b = np.any(drone_pos<0)
    return a or b

def split_action(a):
    num=0
    for i in range(len(a)):
        num = num + a[i]*(4**i)
    return int(num)

def get_state_code(drone_pos, aa_status):
    # Winning
    if np.sum(aa_status)==0:
        return 0
    state_code = 0
    for i in range(num_aa):
        state_code += aa_status[i]*10**i
    for j in range(num_d):
        for k in range(2):
            state_code = state_code + np.dot(drone_pos[j,k],(10**(num_aa-1+j+k)))
    return state_code 

def print_as_mdp(num_S, num_A, transitions):
    print("numStates", num_S)
    print("numActions", num_A)
    print("end 0 1")
    for t in transitions:
        print("transition", t[0], t[1], t[2], t[3], t[4])
    print("mdptype episodic")
    print("discount 1.0")

if __name__=="__main__":

    drone_death_reward = -2

    aa_kill_reward = 5

    movement_delta = {
        0: (0,-1),
        1: (-1,0),
        2: (0,1),
        3: (1,0)
    }

    drone_pos = np.zeros([num_d,2])
    aa_statuses = np.zeros(num_aa)
    transitions = []
    states = [-1,0] #change
    
    def generate_particle_combinations(n):
        values = [0, 1]
        combinations = list(itertools.product(values, repeat=n))
        # Filter out the combination where all particles have a value of 0
        combinations = [combo for combo in combinations if sum(combo) > 0]
        return combinations

    
    aa_statuses=generate_particle_combinations(num_aa)

    def generate_particle_states(n, m):
        coordinates = list(itertools.product(range(m), repeat=2))
        return list(itertools.product(coordinates, repeat=n))
    
    def generate_particle_actions(n, m):
        coordinates = list(itertools.product(range(m), repeat=1))
        return list(itertools.product(coordinates, repeat=n))

    poses = generate_particle_states(num_d, gridsize)
    actions = generate_particle_actions(num_d,4)
    for drone_pos in poses:
        for aa_status in aa_statuses:
            pos = np.array(drone_pos)
            states.append(get_state_code(pos ,aa_status))

    
    for drone_pos in poses:
                for aa_status in aa_statuses:
                    for action in actions:
                        next_pos = np.array(drone_pos)
                        for i in range(num_d):
                            next_pos[i] = np.array(next_pos[i]) + np.array(movement_delta[action[i][0]])
                        if out_of_arena(next_pos):
                            drone_pos = np.array(drone_pos)
                            action = np.array(action)
                            transitions.append((
                                states.index(get_state_code(drone_pos, aa_status)),
                                split_action(action), states.index(-1), drone_death_reward, 1
                             ))
                            continue
                        next_aa_status = np.array(aa_status)
                        for i in range(num_aa):
                            for j in range(num_d):
                                if(np.linalg.norm(np.array(next_pos[j]) - np.array(aa_positions[i]))==0):
                                    next_aa_status[i] = 0
                                    continue
                        reward = np.sum(np.array(aa_status) - next_aa_status)*5
                        if(reward==0):
                            reward = -5
                        drone_pos = np.array(drone_pos)
                        action = np.array(action)
                        transitions.append((
                                states.index(get_state_code(drone_pos, aa_status)),
                                split_action(action), states.index(get_state_code(next_pos, next_aa_status)), reward, 1
                             ))
                                
   
    num_S = len(states)
    num_A = len(actions)
    transitions = [item for item in transitions if item[4] != 0]
    print_as_mdp(num_S, num_A, transitions)
