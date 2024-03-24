import argparse
import numpy as np

def aa_hit_prob(drone_pos, aa):
    return 0.5*np.e**-(np.linalg.norm(
        np.array(drone_pos) - np.array(aa)
    ))

def drone_hit_prob(drone_pos, aa):
    return 2*np.e**-(np.linalg.norm(
        np.array(drone_pos) - np.array(aa)
    ))

def out_of_arena(drone_pos):
    if drone_pos[0] < 0 or drone_pos[0] > 3:
        return True
    if drone_pos[1] < 0 or drone_pos[1] > 3:
        return True
    return False

def get_state_code(drone_pos, aa1_status, aa2_status):
    # Winning
    if aa1_status == 0 and aa2_status == 0:
        return 0
    return 1000*drone_pos[0] + 100*drone_pos[1] + 10*aa1_status + aa2_status

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
    # 2 end states:
    # -1 -> drone dead
    # 0 -> both anti-airs dead
    num_S = 2 + 16*3
    num_A = 7
    drone_death_reward = -2
    aa_kill_reward = 5
    actions = {
        0: "do nothing",
        1: "shoot first aa",
        2: "shoot second aa",
        3: "move up",
        4: "move left",
        5: "move down",
        6: "move right"
    }
    movement_delta = {
        3: (0,-1),
        4: (-1,0),
        5: (0,1),
        6: (1,0)
    }

    transitions = []
    states = [-1, 0]
    for x_coord in range(4):
        for y_coord in range(4):
            states.append(get_state_code((x_coord, y_coord), 0, 1))
            states.append(get_state_code((x_coord, y_coord), 1, 0))
            states.append(get_state_code((x_coord, y_coord), 1, 1))
    #states=[-1,0,next 16 numbers have state val when aa2 is alive,next 16 when aa1 is alive, next 16 when both alive]
    #-1 and 0 are default states
    for x_coord in range(4):
        for y_coord in range(4):
            drone_pos = (x_coord, y_coord)

            # Do nothing transitions
            for aa_statuses in [(0,1), (1,0), (1,1)]:
                #change little calc error
                prob_drone_gets_hit = aa_statuses[0]*aa_hit_prob(drone_pos, aa_positions[0])+aa_statuses[1]*aa_hit_prob(drone_pos, aa_positions[1])-aa_statuses[0]*aa_hit_prob(drone_pos, aa_positions[0])*aa_statuses[1]*aa_hit_prob(drone_pos, aa_positions[1])
                transitions.append((
                    states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), 0,
                    states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), 0, 1-prob_drone_gets_hit
                ))
                transitions.append((
                    states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), 0,
                    states.index(-1), drone_death_reward, prob_drone_gets_hit
                ))

            # Attack transitions
            for aa_statuses in [(0,1), (1,0), (1,1)]:
                prob_drone_gets_hit = aa_statuses[0]*aa_hit_prob(drone_pos, aa_positions[0])+aa_statuses[1]*aa_hit_prob(drone_pos, aa_positions[1])-aa_statuses[0]*aa_hit_prob(drone_pos, aa_positions[0])*aa_statuses[1]*aa_hit_prob(drone_pos, aa_positions[1])
                aa1_killed_prob = drone_hit_prob(drone_pos, aa_positions[0])*aa_statuses[0]
                aa2_killed_prob = drone_hit_prob(drone_pos, aa_positions[1])*aa_statuses[1]
                # No reward if everyone misses their shots
                transitions.append((
                    states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), 1,
                    states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), 0, (1-prob_drone_gets_hit)*(1-aa1_killed_prob)
                ))
                transitions.append((
                    states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), 2,
                    states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), 0, (1-prob_drone_gets_hit)*(1-aa2_killed_prob)
                ))
                # Reward if the drone kills the aa without dying
                transitions.append((
                    states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), 1,
                    states.index(get_state_code(drone_pos, 0, aa_statuses[1])), aa_kill_reward, (1-prob_drone_gets_hit)*(aa1_killed_prob)
                ))
                transitions.append((
                    states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), 2,
                    states.index(get_state_code(drone_pos, aa_statuses[0], 0)), aa_kill_reward, (1-prob_drone_gets_hit)*(aa2_killed_prob)
                ))
                # Negative reward if the drone gets hit without hitting the aa
                transitions.append((
                    states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), 1,
                    states.index(-1), drone_death_reward, prob_drone_gets_hit*(1-aa1_killed_prob)
                ))
                transitions.append((
                    states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), 2,
                    states.index(-1), drone_death_reward, prob_drone_gets_hit*(1-aa2_killed_prob)
                ))
                # Reward for killing the aa and negative reward for dying
                transitions.append((
                    states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), 1,
                    states.index(-1), aa_kill_reward + drone_death_reward, prob_drone_gets_hit*aa1_killed_prob
                ))
                transitions.append((
                    states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), 2,
                    states.index(-1), aa_kill_reward + drone_death_reward, prob_drone_gets_hit*aa2_killed_prob
                ))

            # Movement transitions
            for move_action in range(3,7,1):
                next_pos = np.array(drone_pos) + \
                    np.array(movement_delta[move_action])
                # Negative reward for going out of bounds
                if out_of_arena(next_pos):
                    transitions.append((
                        states.index(get_state_code(drone_pos, 1, 1)),
                        move_action, states.index(-1), drone_death_reward, 1
                    ))
                    transitions.append((
                        states.index(get_state_code(drone_pos, 0, 1)),
                        move_action, states.index(-1), drone_death_reward, 1
                    ))
                    transitions.append((
                        states.index(get_state_code(drone_pos, 1, 0)),
                        move_action, states.index(-1), drone_death_reward, 1
                    ))
                    continue
                # Moving with a probability of getting shot down by an aa
                for aa_statuses in [(0,1), (1,0), (1,1)]:
                    #change movement suicide rewards
                    prob_drone_gets_hit = aa_statuses[0]*aa_hit_prob(drone_pos, aa_positions[0])+aa_statuses[1]*aa_hit_prob(drone_pos, aa_positions[1])-aa_statuses[0]*aa_hit_prob(drone_pos, aa_positions[0])*aa_statuses[1]*aa_hit_prob(drone_pos, aa_positions[1])
                    # Invading airspace of aa1
                    if np.linalg.norm(np.array(next_pos) - np.array(aa_positions[0])) == 0:
                        # Reward for killing the aa
                        transitions.append((
                            states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), move_action,
                            states.index(get_state_code(next_pos, aa_statuses[0], aa_statuses[1])), 0, 1-prob_drone_gets_hit
                        ))
                        # Reward for killing the aa and negative reward for dying
                        transitions.append((
                            states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), move_action,
                            states.index(-1), aa_kill_reward + drone_death_reward, prob_drone_gets_hit
                        ))
                    # Invading airspace of aa2
                    elif np.linalg.norm(np.array(next_pos) - np.array(aa_positions[1])) == 0:
                        # Reward for killing the aa
                        transitions.append((
                            states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), move_action,
                            states.index(get_state_code(next_pos, aa_statuses[0], aa_statuses[1])), 0, 1-prob_drone_gets_hit
                        ))
                        # Reward for killing the aa and negative reward for dying
                        transitions.append((
                            states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), move_action,
                            states.index(-1), aa_kill_reward + drone_death_reward, prob_drone_gets_hit
                        ))
                    # No reward for moving freely
                    # change -0.5 reward for wasting everyones time
                    else:
                        transitions.append((
                            states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), move_action,
                            states.index(get_state_code(next_pos, aa_statuses[0], aa_statuses[1])), -0.5, 1-prob_drone_gets_hit
                        ))
                        transitions.append((
                            states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), move_action,
                            states.index(get_state_code(drone_pos, aa_statuses[0], aa_statuses[1])), drone_death_reward, prob_drone_gets_hit
                        ))

    transitions = [item for item in transitions if item[4] != 0]
    print_as_mdp(num_S, num_A, transitions)


