# environment.py

import numpy as np
import pygame
from agent import Drone
from defense import DefenseSystem

random_seed = 0

class CombatEnvironment:
    def __init__(self, grid_size=(10, 10), num_drones=2, num_defenses=3, cell_size=60):
        """
        Initialize the CombatEnvironment class.

        Args:
        - grid_size (tuple): Size of the grid.
        - num_drones (int): Number of drones.
        - num_defenses (int): Number of defense systems.
        - cell_size (int): Size of each cell in pixels.
        """
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
        """
        Place drones and defense systems on the grid.
        """
        for entity in self.drones + self.defenses:
            self.grid[entity.position] = entity

    def step(self, actions):
        """
        Move drones based on the provided actions.

        Args:
        - actions (list): List of actions for each drone.
        """
        for action, drone in zip(actions, self.drones):
            if action == 'move_right' and drone.position[1] < self.grid_size[1] - 1:
                self.grid[drone.position] = None  # Clear current position
                drone.position = (drone.position[0], drone.position[1] + 1)
                self.grid[drone.position] = drone  # Move drone to new position

            if action == 'move_left' and drone.position[1] > 0:
                self.grid[drone.position] = None
                drone.position = (drone.position[0], drone.position[1] - 1)
                self.grid[drone.position] = drone

            if action == 'move_up' and drone.position[0] > 0:
                self.grid[drone.position] = None
                drone.position = (drone.position[0] - 1, drone.position[1])
                self.grid[drone.position] = drone

            if action == 'move_down' and drone.position[0] < self.grid_size[0] - 1:
                self.grid[drone.position] = None
                drone.position = (drone.position[0] + 1, drone.position[1])
                self.grid[drone.position] = drone

            if action == 'shoot':
                for defense in self.defenses:
                    if defense.position == drone.position:
                        defense.health -= 1
                        if defense.health == 0:
                            self.grid[defense.position] = None  # Remove defense system
                            self.defenses.remove(defense)

            

    def render(self):
        """
        Render the environment.
        """
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
        """
        Reset the environment.
        """
        self.grid = np.zeros(self.grid_size, dtype=object)
        self.place_entities()
