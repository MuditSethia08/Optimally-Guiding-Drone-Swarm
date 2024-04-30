# main.py
import pygame
import math
from environmentTS import CombatEnvironment
move_actions=4
def parse_strat(file_path,index):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        line = lines[index]
        columns = line.split()
        print(columns[1])
    return [math.floor(int(columns[1])/move_actions), int(columns[1])%move_actions]

def main():
    env = CombatEnvironment()
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_state = env.render()
        if(current_state == -1):
            print('Game Over')
            break
        action = parse_strat('TS_s3.txt',current_state)
        print(action)

        input("Press Any Key For Next State")

        env.step(action)
        clock.tick(2)  # Control simulation speed, 2 steps per second

        # Add additional game logic (e.g., user input) as needed

    pygame.quit()

if __name__ == "__main__":
    main()