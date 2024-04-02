import random,argparse,sys,subprocess,os
from matplotlib import pyplot as plt

def run(opponent, p, q):
    cmd_encoder = "python3","encoder.py","--opponent", opponent, "--p", str(p), "--q", str(q)
    print("\n","Generating the MDP encoding using encoder.py")
    f = open('verify_attt_mdp','w')
    subprocess.call(cmd_encoder,stdout=f)
    f.close()

    cmd_planner = "python3","planner.py","--mdp","verify_attt_mdp"
    print("\n","Generating the value policy file using planner.py using default algorithm")
    f = open('verify_attt_planner','w')
    subprocess.call(cmd_planner,stdout=f)
    f.close()

    cmd_decoder = "python3","decoder.py","--value-policy","verify_attt_planner","--opponent", opponent 
    print("\n","Generating the decoded policy file using decoder.py")
    cmd_output = subprocess.check_output(cmd_decoder,universal_newlines=True)

    os.remove('verify_attt_mdp')
    os.remove('verify_attt_planner')
    return cmd_output

opponent_policy_file = 'data/football/test-1.txt'

## Graph_1
rewards = []
p_arr = [0,0.1,0.2,0.3,0.4,0.5]
for p in p_arr:
    output = run(opponent_policy_file, p, 0.7)
    output = output.split('\n')
    output.remove('')
    rewards.append(float(output[2318].split()[2]))
plt.plot(p_arr, rewards)
plt.xlabel("Varying p with fixing q as 0.7")
plt.ylabel("Corresponding rewards")
plt.savefig("graph1.png")
plt.close()

## Graph_2
rewards = []
q_arr = [0.6, 0.7, 0.8, 0.9, 1]
for q in q_arr:
    output = run(opponent_policy_file, 0.3, q)
    output = output.split('\n')
    output.remove('')
    rewards.append(float(output[2318].split()[2]))
plt.plot(q_arr, rewards)
plt.xlabel("Varying q with fixing p as 0.3")
plt.ylabel("Corresponding rewards")
plt.savefig("graph2.png")
plt.close()