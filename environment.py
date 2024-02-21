# environment.py

import numpy as np
from agent import Drone
from defense import DefenseSystem
from utils import initialize_defenses, initialize_drones

class CombatEnvironment:
    def __init__(self, grid_size=(10, 10), num_drones=5, num_defenses=10):
        self.grid_size = grid_size
        self.grid = np.zeros(grid_size, dtype=object)
        self.drones = initialize_drones(num_drones, self.grid_size)
        self.defenses = initialize_defenses(num_defenses, self.grid_size)
        self.place_entities()

    def place_entities(self):
        for drone in self.drones:
            self.grid[drone.position] = drone
        for defense in self.defenses:
            self.grid[defense.position] = defense

    def render(self):
        # Optional: Implement a method to visually render the grid and the entities on it
        pass

    def reset(self):
        # Reset the environment to its initial state
        self.grid = np.zeros(self.grid_size, dtype=object)
        self.drones = initialize_drones(len(self.drones), self.grid_size)
        self.defenses = initialize_defenses(len(self.defenses), self.grid_size)
        self.place_entities()

    def step(self, drone_actions):
        total_reward = 0
        for drone, action in zip(self.drones, drone_actions):
            initial_reward = total_reward

            # Assuming action is a tuple like ('move', 'up') or ('attack', (x, y))
            if action[0] == 'move':
                drone.move(action[1], self.grid_size)
            elif action[0] == 'attack':
                success = drone.attack(action[1], self)
                if success:
                    total_reward += 10  # Reward for successful attack

            # Check if the drone was attacked this turn
            if drone.health < 100:  # Assuming drones start with 100 health
                total_reward -= 5  # Penalty for being hit

        # Reward for surviving drones
        total_reward += len([d for d in self.drones if d.health > 0]) * 1

        # Check if all defenses are destroyed
        if not any(isinstance(self.grid[position], DefenseSystem) for position in np.ndindex(self.grid.shape)):
            total_reward += 100  # Bonus for completing the objective

        return total_reward
