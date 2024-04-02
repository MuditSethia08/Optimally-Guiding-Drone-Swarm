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

def value_iteration(num_S, num_A, R, T, gamma):
    V = np.random.normal(size=num_S)
    while(True):
        V_prev = np.array(V)
        for s in range(num_S):
            V[s] = np.max([np.sum(np.multiply(T[s, a], R[s, a]) + np.multiply(T[s, a], gamma*V_prev)) for a in range(num_A)])
        if np.max(np.absolute(V - V_prev)) < 1e-8:
            return V

def evaluate_policy(num_S, num_A, R, T, gamma, pi):
    V = np.random.normal(size=num_S)
    while(True):
        V_prev = np.array(V)
        for s in range(num_S):
            V[s] = np.sum(np.multiply(T[s, pi[s]], R[s, pi[s]]) + np.multiply(T[s, pi[s]], gamma*V_prev))
        if np.max(np.absolute(V - V_prev)) < 1e-8:
            return V

def howard_policy_iteration(num_S, num_A, R, T, gamma):
    pi = np.random.randint(0,num_A,size=num_S)
    while(True):
        V = evaluate_policy(num_S, num_A, R, T, gamma, pi)
        Q = np.zeros((num_S, num_A))
        for s in range(num_S):
            for a in range(num_A):
                Q[s, a] = np.sum(np.multiply(T[s, a], R[s, a]) + np.multiply(T[s, a], gamma*V))
        optimal_policy_found = True
        for s in range(num_S):
            best_action = np.argmax(Q[s])
            if pi[s] != best_action:
                optimal_policy_found = False
                p = np.random.rand()
                if p > 0.1:
                    pi[s] = best_action
        if optimal_policy_found:
            break
    return V, pi

def parse_mdp(file_path):
    with open(file_path, 'r') as file:
        num_S = None
        num_A = None
        end = []
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

    num_S, num_A, R, T, end, mdptype, gamma = parse_mdp(args.mdp)

    if args.policy is not None:
        pi = parse_policy(args.policy)
        V = evaluate_policy(num_S, num_A, R, T, gamma, pi)
        pretty_print(V, pi)
        exit(0)

    # Using lp as my default program as it is the fastest for episodic
    if args.algorithm is None:
        V = linear_programming(num_S, num_A, R, T, gamma)
        pi = get_policy_from_V(num_S, num_A, R, T, gamma, V)
        pretty_print(V, pi)
        exit(0)

    if args.algorithm == 'vi':
        V = value_iteration(num_S, num_A, R, T, gamma)
        pi = get_policy_from_V(num_S, num_A, R, T, gamma, V)
        pretty_print(V, pi)
        exit(0)
    elif args.algorithm == 'hpi':
        V, pi = howard_policy_iteration(num_S, num_A, R, T, gamma)
        pretty_print(V, pi)
        exit(0)
    elif args.algorithm == 'lp':
        V = linear_programming(num_S, num_A, R, T, gamma)
        pi = get_policy_from_V(num_S, num_A, R, T, gamma, V)
        pretty_print(V, pi)
        exit(0)
