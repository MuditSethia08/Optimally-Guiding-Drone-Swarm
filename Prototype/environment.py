import numpy as np
import pygame
from agent import Drone, DQNAgent
from defense import DefenseSystem

class CombatEnvironment:
    def __init__(self, grid_size=(10, 10), num_drones=2, num_defenses=3, cell_size=60):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.screen_size = (grid_size[0] * cell_size, grid_size[1] * cell_size)
        self.grid = np.zeros(grid_size, dtype=object)
        self.drones = [Drone((i, 0)) for i in range(num_drones)]
        self.defenses = [DefenseSystem((np.random.randint(0, grid_size[0]), np.random.randint(0, grid_size[1])), "rocket", 100) for _ in range(num_defenses)]
        self.place_entities()
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Drone Swarm Optimization Simulation')
        self.action_space = ['move_right', 'move_left', 'move_up', 'move_down', 'shoot']
        self.agent = DQNAgent(state_size=4, action_size=len(self.action_space))

    def place_entities(self):
        for entity in self.drones + self.defenses:
            self.grid[entity.position] = entity

    def step(self, actions):
        rewards = []
        next_states = []
        done = False

        for action, drone in zip(actions, self.drones):
            reward = 0
            if action == 'move_right' and drone.position[1] < self.grid_size[1] - 1:
                self.grid[drone.position] = None
                drone.position = (drone.position[0], drone.position[1] + 1)
                self.grid[drone.position] = drone
            elif action == 'move_left' and drone.position[1] > 0:
                self.grid[drone.position] = None
                drone.position = (drone.position[0], drone.position[1] - 1)
                self.grid[drone.position] = drone
            elif action == 'move_up' and drone.position[0] > 0:
                self.grid[drone.position] = None
                drone.position = (drone.position[0] - 1, drone.position[1])
                self.grid[drone.position] = drone
            elif action == 'move_down' and drone.position[0] < self.grid_size[0] - 1:
                self.grid[drone.position] = None
                drone.position = (drone.position[0] + 1, drone.position[1])
                self.grid[drone.position] = drone
            elif action == 'shoot':
                for defense in self.defenses:
                    if defense.position == drone.position:
                        defense.health -= 10
                        reward += 10
                        if defense.health <= 0:
                            self.grid[defense.position] = None
                            self.defenses.remove(defense)
                            reward += 50

            rewards.append(reward)
            next_states.append([drone.position[0], drone.position[1], drone.health])
            if all(defense.health <= 0 for defense in self.defenses):
                done = True
                reward += 100

        return next_states, rewards, done

    def render(self):
        self.screen.fill((0, 0, 0))
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)
                if isinstance(self.grid[i, j], Drone):
                    pygame.draw.circle(self.screen, (0, 255, 0), rect.center, self.cell_size // 4)
                elif isinstance(self.grid[i, j], DefenseSystem):
                    pygame.draw.rect(self.screen, (255, 0, 0), rect.inflate(-20, -20))
        pygame.display.flip()

    def reset(self):
        self.grid = np.zeros(self.grid_size, dtype=object)
        self.place_entities()
        return [(drone.position[0], drone.position[1], drone.health) for drone in self.drones]

