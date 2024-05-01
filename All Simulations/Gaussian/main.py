# main.py
import pygame
import math
from environment import CombatEnvironment

def parse_strat(file_path,index):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        line = lines[index]
        columns = line.split()
        print(columns[1])
    return [math.floor(int(columns[1])/6), int(columns[1])%6]

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
        action = parse_strat('strategy_G.txt',current_state)
        print(action)

        input("Press Any Key For Next State")

        env.step(action, 2, 2)
        clock.tick(1)  # Control simulation speed, 2 steps per second

        # Add additional game logic (e.g., user input) as needed

    pygame.quit()

if __name__ == "__main__":
    main()