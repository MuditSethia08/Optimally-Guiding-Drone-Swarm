import argparse
import numpy as np
import matplotlib.pyplot as plt

def get_state_code(drone_pos, aa1_status, aa2_status):
    # Winning
    if aa1_status == 0 and aa2_status == 0:
        return 0
    return 1000*drone_pos[0] + 100*drone_pos[1] + 10*aa1_status + aa2_status

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', required=True)
    args = parser.parse_args()

    strategy = []
    with open(args.file_path) as file:
        for line in file.readlines():
            split = line.strip().split(' ')
            value = float(split[0])
            action = int(split[1])
            strategy.append((action))

    strategy = strategy[2:50]
    aa2_up_strategy = [strategy[i] for i in range(len(strategy)) if i%3 == 0]
    aa1_up_strategy = [strategy[i] for i in range(len(strategy)) if i%3 == 1]
    both_up_strategy = [strategy[i] for i in range(len(strategy)) if i%3 == 2]

    print("Only aa1 is active")
    for i in range(4):
        row = []
        for j in range(4):
            index = 4*j + i
            row.append(aa1_up_strategy[index])
        print(row)

    print("Only aa2 is active")
    for i in range(4):
        row = []
        for j in range(4):
            index = 4*j + i
            row.append(aa2_up_strategy[index])
        print(row)

    print("Both aa1 and aa2 are active")
    for i in range(4):
        row = []
        for j in range(4):
            index = 4*j + i
            row.append(both_up_strategy[index])
        print(row)

