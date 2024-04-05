# main.py
import pygame
from environment import CombatEnvironment
from nextState import nextState

def main():
    env = CombatEnvironment()
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        env.render()
        # Extract current positions
        current_positions = ','.join([f'{drone.position[0]},{drone.position[1]}' for drone in env.drones] + 
                                     [f'{defense.position[0]},{defense.position[1]}' for defense in env.defenses])
        # Get the next positions from nextState.py
        position = nextState(current_positions)
        if position == "exit":
            break
        env.step(position, 2, 2)
        clock.tick(2)  # Control simulation speed, 2 steps per second

        # Add additional game logic (e.g., user input) as needed

    pygame.quit()

if __name__ == "__main__":
    main()
