# main.py
import pygame
from environment import CombatEnvironment

def main():
    env = CombatEnvironment()
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        env.render()
        position = input("Enter new positions: ")
        env.step(position, 2, 2)
        clock.tick(2)  # Control simulation speed, 2 steps per second

        # Add additional game logic (e.g., user input) as needed

    pygame.quit()

if __name__ == "__main__":
    main()
