# main.py
import pygame
import math
from environment import CombatEnvironment
import numpy as np
from pygame_screen_record import ScreenRecorder

def parse_strat(file_path,index):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        line = lines[index]
        columns = line.split()
        A = int(columns[1])
        a = np.zeros((2,1))
        for i in range(2):
            a[i] = math.floor(int(A%6))
            A = math.floor(int(A/6))
    return a

def main():
    env = CombatEnvironment()
    running = True
    clock = pygame.time.Clock()
    recorder = ScreenRecorder(60).start_rec()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_state = env.render()
        if(current_state == 1):
            print('Game Over')
            break
        action = parse_strat('strategy.txt',current_state)
        # print(current_state,action)

        # input("Press Any Key For Next State")

        env.step(action,2,2)
        clock.tick(1)  # Control simulation speed, 2 steps per second

        # Add additional game logic (e.g., user input) as needed
    clock.tick(1)

    recorder.stop_rec().get_single_recording().save(('r2','mp4'))
    clock.tick(1)
    pygame.quit()

if __name__ == "__main__":
    main()