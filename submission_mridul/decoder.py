import sys
import argparse

parser = argparse.ArgumentParser()

if __name__ == "__main__":
    parser.add_argument("--value-policy", type=str, default=None)
    parser.add_argument("--opponent", type=str, default=None)

    args = parser.parse_args()

    policy_file_loc = args.value_policy
    opponent_file_loc = args.opponent

    if(policy_file_loc==None or opponent_file_loc==None):
        print("Incorrect Arguments, Exiting")
        sys.exit()
    
    with open(policy_file_loc, 'r') as file:
        policy_file_lines = file.readlines()
    with open(opponent_file_loc, 'r') as file:
        opponent_file_lines = file.readlines()
    
    for i in range(len(policy_file_lines) - 1):
        state = opponent_file_lines[i+1].split()[0]
        val_actn = policy_file_lines[i].split()
        actn = int(val_actn[1])
        val = float(val_actn[0])
        print(f"{state} {actn} {val}")