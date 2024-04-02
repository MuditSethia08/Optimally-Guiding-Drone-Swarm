import sys
import argparse
import numpy as np
import pulp


parser = argparse.ArgumentParser()
np.random.seed(42)

class MDP_Solver():
    def __init__(self, S, A, T, R, end, gamma, mdptype) -> None:
        self.S = S
        self.A = A
        self.T = T
        self.R = R
        self.end = end
        self.gamma = gamma
        self.mdptype = mdptype

    def solve_mdp(self, algo):
        if(algo=="vi"):
            return self.solve_vi()
        elif(algo=="hpi"):
            return self.solve_hpi()
        elif(algo=="lp"):
            return self.solve_lp()
        else:
            print("Wrong Algorithm, Terminating")
            sys.exit()

    def solve_vi(self):
        V_prev = np.zeros(self.S)
        V_curr = np.zeros(self.S)
        opt_policy = np.zeros(self.S)

        while(True):
            updates = np.zeros((self.S, self.A))
            for s in range(self.S):
                for a in range(self.A):
                    updates[s][a] = np.sum(self.T[s][a] * (self.R[s][a] + self.gamma * V_prev))
            opt_policy = np.argmax(updates, axis=1)
            V_curr = np.max(updates, axis=1)
            if(np.max(V_curr - V_prev) < 1e-8):
                break
            else:
                V_prev = V_curr.copy()

        return V_curr, opt_policy

    def solve_hpi(self):
        pi_old = np.zeros(self.S, dtype=int)

        improvable_states = self.find_improvable_states(pi_old)

        while(np.sum(improvable_states)>0):
            pi_new = pi_old.copy()
            for s in range(self.S):
                if(np.sum(improvable_states[s]) > 0):
                    pi_new[s] = np.where(improvable_states[s] == 1)[0][0]
            improvable_states = self.find_improvable_states(pi_new)
            pi_old = pi_new.copy()

        pi_opt = pi_old.copy()
        V_opt = self.evaluate_policy(pi_opt)
        return V_opt, pi_opt    

    def find_improvable_states(self, pi):
        improvable_states = np.zeros((self.S, self.A))
        V_pi = self.evaluate_policy(pi)
        for s in range(self.S):
            for a in range(self.A):
                if(a == pi[s]):
                    continue
                if(self.action_value(s, a, V_pi) > V_pi[s]):
                    improvable_states[s][a] = 1
        return improvable_states
    
    def action_value(self, s, a, V_pi):
        return np.sum(self.T[s][a] * (self.R[s][a] + self.gamma * V_pi))

    def evaluate_policy(self, pi):
        b = np.zeros(self.S)
        A = -np.eye(self.S)
        for s in range(self.S):
            actn = pi[s]
            b[s] = np.sum(np.array([self.T[s][actn][s_]*self.R[s][pi[s]][s_] for s_ in range(self.S)]))
            for s_ in range(self.S):
                A[s][s_] += self.gamma*self.T[s][pi[s]][s_]
        b = -b
        V = np.linalg.solve(A,b)
        # V[V<=0] = 0
        return V
    
    def find_policy_from_value_fn(self, V):
        pi = np.zeros(self.S, dtype = int)
        for s in range(self.S):
            updates = np.array([np.sum(np.array([(self.T[s][a][s_]*(self.R[s][a][s_] + self.gamma*V[s_])) for s_ in range(self.S)])) for a in range(self.A)])
            pi[s] = int(np.argmax(updates))
        return pi
    
    def solve_lp(self):
        lp_problem = pulp.LpProblem("MDP", pulp.LpMaximize)
        vars = [pulp.LpVariable(f'V{i}') for i in range(0, self.S)]
        lp_problem += pulp.lpSum([-vars[i] for i in range(0, self.S)]), "Objective"
        for s in range(self.S):
            for a in range(self.A):
                lp_problem += pulp.lpSum([vars[s_] * self.T[s][a][s_] * self.gamma for s_ in range(0, self.S)]) - vars[s] <= -np.sum(np.array([self.T[s][a][s_]*self.R[s][a][s_] for s_ in range(self.S)])), f"Constraint{s}_{a}."
        lp_problem.solve(pulp.PULP_CBC_CMD(msg=0))
        if lp_problem.status == pulp.LpStatusOptimal:
            V_opt = np.zeros(self.S)
            for s in range(self.S):
                V_opt[s] = vars[s].varValue
            # V_opt[V_opt <=0 ] = 0
        else:
            print("No Optimal Solution Found, Exiting")
            sys.exit()

        return V_opt, self.find_policy_from_value_fn(V_opt)



if __name__ == "__main__":
    parser.add_argument("--mdp", type=str)
    parser.add_argument("--algorithm", type=str, default="vi")
    parser.add_argument("--policy", type=str, default=None)

    args = parser.parse_args()

    mdp_file_loc = args.mdp
    algo = args.algorithm
    policy_file_loc = args.policy

    with open(mdp_file_loc, 'r') as file:
        for line in file:
            words = line.split()
            
            if(words[0]=="numStates"):
                numStates = int(words[1])
            elif(words[0]=="numActions"):
                numActions = int(words[1])
                T = np.zeros((numStates, numActions, numStates))
                R = np.zeros((numStates, numActions, numStates))
            elif(words[0]=="end"):
                endStates = [int(word) for word in words[1:]]
            elif(words[0]=="mdptype"):
                mdptype = words[1]
            elif(words[0]=="discount"):
                gamma = float(words[1])
            else:
                T[int(words[1])][int(words[2])][int(words[3])] += float(words[5])
                R[int(words[1])][int(words[2])][int(words[3])] += float(words[4])

    solver = MDP_Solver(numStates, numActions, T, R, endStates, gamma, mdptype)

    if(policy_file_loc):
        pi = []
        with open(policy_file_loc, 'r') as file:
            for line in file:
                words = line.split()
                pi.append(int(words[0]))
        pi = np.array(pi)
        V = solver.evaluate_policy(pi)
    else:
        V, pi = solver.solve_mdp(algo)

    for s in range(numStates):
        print(f"{V[s]:.6f} {int(pi[s])}")