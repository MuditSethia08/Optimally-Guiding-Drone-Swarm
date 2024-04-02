import getopt, sys
import numpy as np
import sys
from pulp import *
from copy import deepcopy

def evaluate_policy(T,gamma,act,C):
    S = len(act)
    A = np.zeros((S,S))
    D = np.zeros(S)
    for i in range(S):
        D[i] = -C[i,act[i]]
        for j in range(S):
            A[i][j] = gamma*T[i][act[i]][j]
    A = A - np.identity(S)
    V_pi = np.linalg.solve(A,D)
    return V_pi

def compute_TV(tnz,V,S,A):
    Tv = np.zeros((S,A))
    for t in tnz:
        Tv[(t[0])[0],(t[0])[1]]+=t[1]*V[(t[0])[2]]
    return Tv

def value_iteration(S,A,tnz,mdptype,gamma,end,C):
    V1 = np.zeros(S)
    V2 = np.zeros(S)-1
    pi_star = np.zeros(S)
    while (abs(V2-V1)>=0.00000001).any():
        V1 = deepcopy(V2)
        #V2 = np.max( C + gamma*compute_TV(tnz,V1,S,A), 1)
        na = C + gamma*compute_TV(tnz,V1,S,A)
        for i in range(S):
            for j in range(A):
                if V2[i]<=na[i,j]:
                    V2[i]=na[i,j]
                    pi_star[i]=j
        #pi_star = np.argmax( C + gamma*compute_TV(tnz,V1,S,A), 1)
    for i in range(S):
        print('{:.6f}'.format(V2[i]),int(pi_star[i]))
    
def action_value(S,T,gamma,pol,C):
    Vf = evaluate_policy(T,gamma,pol,C)
    V_bar = np.reshape(Vf,(1,1,S))
    Q = C + np.sum(gamma*np.multiply(T,V_bar), 2)
    return Q

def howards(S,A,T,mdptype,gamma,end,C):
    pol1 = np.zeros(S,dtype=int)
    pol2 = np.zeros(S,dtype=int)
    Q=action_value(S,T,gamma,pol1,C)
    while(True):
        for i in range(S):
            pol2[i] = np.argmax(Q[i,:])
        if (pol1==pol2).all():
            break
        else:
            pol1 = deepcopy(pol2)
            Q=action_value(S,T,gamma,pol1,C)
    v_star = evaluate_policy(T,gamma,pol2,C)
    for k in range(S):
        print('{:.6f}'.format(v_star[k]),pol2[k])
    

def linear_program(S,A,T,mdptype,gamma,end, C):
    model = LpProblem("MDP_Planning", LpMaximize)
    Vi = [0]*S
    Vj = [0]*S
    for i in range(S):
        Vi[i]='V{ie}'.format(ie=i)
    for j in range(S):
        Vj[j]=LpVariable(Vi[j])
    model+= -lpSum(Vj[j] for j in range(S))
    Vk = np.reshape(Vj,(1,1,S))
    B = np.array(gamma*T*Vk)
    for k in range(S):
        for l in range(A):
            model+= lpSum(B[k,l]) <= -C[k][l] + Vj[k]
    model.solve(PULP_CBC_CMD(msg=0))
    opt_pol = np.zeros(S)
    final_value = np.zeros(S)
    for i in range(S):
        final_value[i] = Vj[i].varValue
    fv = np.reshape(final_value,(1,1,S))
    D = gamma*np.sum(T*fv, 2)
    opt_pol = np.argmax(C+D,1)
    for i in range(S):
        print('{:.6f}'.format(final_value[i]),opt_pol[i])

if __name__=='__main__':
    argument_list = sys.argv[1:]
    options = 'a:m:p:'
    long_options = ['algorithm=','mdp=','policy=']
    algo = 'None'
    policy = 0
    try:
        arguments, values = getopt.getopt(argument_list, options, long_options)
    
        for currentArgument, currentValue in arguments:
           
            if currentArgument in ('-m','--mdp'):
                path = currentValue
                fp = open(path,'r')
                line = fp.readline().strip()
                line = line.split(' ')
                S = int(line[1])
                line = fp.readline().strip()
                line = line.split(' ')
                A = int(line[1])
                line = fp.readline().strip()
                line = line.split(' ')
                end = []
                for i in line[1:]:
                    end.append(int(i))
                line = fp.readline().strip()
                transitions = np.zeros([S,A,S])
                C=np.zeros((S,A))
                tnz=[]
                while line!='':
                    line = line.split(' ')
                    if line[0]=='transition':
                        s1 = int(line[1])
                        a = int(line[2])
                        s2 = int(line[3])
                        transitions[s1][a][s2] = float(line[5])
                        t = float(line[5])
                        r = float(line[4])
                        if t!=0:
                            C[s1][a]+=t*r
                            tnz.append([[s1,a,s2],t])
                        line = fp.readline().strip()
                    elif line[0]=='mdptype':
                        mdptype = line[1]
                        line = fp.readline().strip()
                    elif line[0]=='discount':
                        gamma = float(line[1])
                        line = fp.readline().strip()
            elif currentArgument in ('p','--policy'):
                path = currentValue
                fp = open(path,'r')
                act = []
                line = fp.readline().strip()
                while line!='':
                    act.append(int(line))
                    line = fp.readline().strip()
                act = np.array(act)
                vf = evaluate_policy(transitions,gamma,act,C)
                for i in range(S):
                    print('{:.6f}'.format(vf[i]),'\t',act[i])
                sys.exit()
            elif currentArgument in ('a','--algorithm'):
                algo = currentValue
        if algo=='None':
            algo = 'vi'
        if algo=='vi':
            value_iteration(S,A,tnz,mdptype,gamma, end,C)
        elif algo=='hpi':
            howards(S,A,transitions,mdptype,gamma, end,C)
        elif algo=='lp':
            linear_program(S,A,transitions,mdptype,gamma, end, C)       
    except getopt.error as err:
        print (str(err))