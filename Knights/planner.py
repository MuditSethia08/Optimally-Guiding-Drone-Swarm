import argparse
import copy
import numpy as np
import pulp

def get_policy_from_V(num_S, num_A, R, T, gamma, V):
    pi = np.zeros(num_S)
    for s in range(num_S):
        pi[s] = np.argmax([np.sum([T[s, a, s_]*(R[s, a, s_] + gamma*V[s_]) for s_ in range(num_S)]) for a in range(num_A)])
    return pi

def linear_programming(num_S, num_A, R, T, gamma):
    prob = pulp.LpProblem('solve_MDP', pulp.LpMinimize)
    V_pulp = np.array([pulp.LpVariable('V{s}'.format(s=s)) for s in range(num_S)])
    prob += pulp.lpSum(V_pulp), 'objective'
    for s in range(num_S):
        for a in range(num_A):
            prob += V_pulp[s] >= pulp.lpSum(np.multiply(T[s, a], R[s, a]) + np.multiply(T[s, a], gamma*V_pulp))
    solver = pulp.PULP_CBC_CMD(msg=False)
    status = prob.solve(solver=solver)
    V_optimal = np.array([V_pulp[s].varValue for s in range(num_S)])
    return V_optimal

def parse_mdp(file_path):
    with open(file_path, 'r') as file:
        num_S = 0
        num_A = 0
        end = []
        R = []
        T = []
        mdptype = None
        gamma = None
        for line in file:
            line = line.strip()
            parts = line.split(' ')
            parts = [item for item in parts if item != '']
            if parts[0] == 'numStates':
                num_S = int(parts[-1])
            elif parts[0] == 'numActions':
                num_A = int(parts[-1])
            elif parts[0] == 'end':
                for i in range(1,len(parts)):
                    end.append(int(parts[i]))
                R = np.zeros((num_S, num_A, num_S))
                T = np.zeros((num_S, num_A, num_S))
                mdptype = None
                gamma = None
            elif parts[0] == 'transition':
                R[int(parts[1]), int(parts[2]), int(parts[3])] = float(parts[4])
                T[int(parts[1]), int(parts[2]), int(parts[3])] = float(parts[5])
            elif parts[0] == 'mdptype':
                mdptype = parts[-1]
            elif parts[0] == 'discount':
                gamma = float(parts[-1])
    return num_S, num_A, R, T, end, mdptype, gamma

def parse_policy(file_path):
    with open(file_path, 'r') as file:
        pi = []
        for line in file:
            line = line.strip()
            pi.append(int(line))
    return pi

def pretty_print(V, pi):
    for i in range(len(V)):
        print('%.6f' % V[i], int(pi[i]))

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mdp', required=True)
    parser.add_argument('--algorithm')
    parser.add_argument('--policy')
    args = parser.parse_args()

    num_S, num_A, r, t, end, mdptype, gamma = parse_mdp(args.mdp)

    # Using lp as my default program as it is the fastest for episodic
    V = linear_programming(num_S, num_A, r, t, gamma)
    pi = get_policy_from_V(num_S, num_A, r, t, gamma, V)
    pretty_print(V, pi)
    exit(0)