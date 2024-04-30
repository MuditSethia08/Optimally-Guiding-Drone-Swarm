import argparse
import numpy as np
import itertools

gridsize = 7
num_d = 5
num_aa = 5


def out_of_arena(drone_pos1,drone_pos2):
    if drone_pos1[0] < 0 or drone_pos1[0] > gridsize-1 or drone_pos2[0] < 0 or drone_pos2[0] > gridsize-1:
        return True
    if drone_pos1[1] < 0 or drone_pos1[1] > gridsize-1 or drone_pos2[1] < 0 or drone_pos2[1] > gridsize-1:
        return True
    return False

def split_action(a):
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
            state_code = state_code + np.dot(drone_pos[j*2+k],(10**(num_aa-1+j+k)))
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
    actions = generate_particle_states(n,4)

    for drone_pos in states:
        for aa_status in aa_statuses:
            states.append(get_state_code(drone_pos ,aa_statuses))
    for drone_pos in states:
                for aa_status in aa_statuses:
                    for action in actions:
                        next_pos = drone_pos
                        for i in range(n):
                            next_pos[i] = np.array(next_pos[i]) + np.array(movement_delta[action[i][0]])
                        if out_of_arena(next_pos):
                            transitions.append((
                                states.index(get_state_code(drone_pos, aa_statuses)),
                                split_action(action), states.index(-1), drone_death_reward, 1
                             ))
                        next_aa_status = aa_status
                        for i in range(len(aa_positions)):
                            for j in range(n):
                                if(np.linalg.norm(np.array(next_pos[j]) - np.array(aa_positions[i]))):
                                    next_aa_status[i] = 0
                                    continue
                        reward = np.sum(np.array(aa_status) - np.array(next_aa_status))*5
                        if(reward==0):
                            reward = -5
                        transitions.append((
                                states.index(get_state_code(drone_pos, aa_statuses)),
                                split_action(action), get_state_code(next_pos, next_aa_status), reward, 1
                             ))
                                

    transitions = [item for item in transitions if item[4] != 0]
    print_as_mdp(num_S, num_A, transitions)
