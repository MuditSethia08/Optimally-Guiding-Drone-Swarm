# environment.py
import numpy as np
import pygame
from agent import Drone
from defense import DefenseSystem

class CombatEnvironment:
    def __init__(self, grid_size=(10, 10), num_drones=2, num_defenses=3, cell_size=60):
        self.grid_size = grid_size
        self.cell_size = cell_size  # Size of each cell in pixels
        self.screen_size = (grid_size[0] * cell_size, grid_size[1] * cell_size)
        self.grid = np.zeros(grid_size, dtype=object)  # Empty grid
        self.drones = [Drone((i, 0)) for i in range(num_drones)]
        self.defenses = [DefenseSystem((np.random.randint(0, grid_size[0]), np.random.randint(0, grid_size[1]))) for _ in range(num_defenses)]
        self.place_entities()
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Drone Swarm Optimization Simulation')

    def place_entities(self):
        for entity in self.drones + self.defenses:
            self.grid[entity.position] = entity

    def step(self, actions):
        for action, drone in zip(actions, self.drones):
            if action == 'move_right' and drone.position[1] < self.grid_size[1] - 1:
                self.grid[drone.position] = None  # Clear current position
                drone.position = (drone.position[0], drone.position[1] + 1)
                self.grid[drone.position] = drone  # Move drone to new position

    def render(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)  # Draw grid lines
                if isinstance(self.grid[i, j], Drone):
                    pygame.draw.circle(self.screen, (0, 255, 0), rect.center, self.cell_size // 4)  # Draw drones
                elif isinstance(self.grid[i, j], DefenseSystem):
                    pygame.draw.rect(self.screen, (255, 0, 0), rect.inflate(-20, -20))  # Draw defenses
        pygame.display.flip()  # Update the display

    def reset(self):
        self.grid = np.zeros(self.grid_size, dtype=object)
        self.place_entities()
