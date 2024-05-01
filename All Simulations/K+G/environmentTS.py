# environment.py

import numpy as np
import pygame
import random
from agent import Drone
from defense import DefenseSystem
import itertools 

random_seed = 0
gridsize = 6
num_d = 1
aa_positions = [
        (2,0),
        (3,2),
        (2,1),
        (4,4),
        (4,5)
    ]
num_aa = len(aa_positions)

def get_state_code(drone_pos, aa_status):
    # Winning
    if np.sum(aa_status)==0:
        return 0
    state_code = 0
    for i in range(num_aa):
        state_code += aa_status[i]*10**i
    for j in range(num_d):
        for k in range(2):
            state_code = state_code + drone_pos[j,1-k]*(10**(num_aa+k+2*j))
    return state_code 

movement_delta = {
        0: (2,1),
        1: (2,-1),
        2: (-2,1),
        3: (-2,-1),
        4: (1,2),
        5: (-1,2),
        6: (1,-2),
        7: (-1,-2)
    }

def generate_particle_states(n, m):
    coordinates = list(itertools.product(range(m), repeat=2))
    return list(itertools.product(coordinates, repeat=n))
def generate_particle_combinations(n):
        values = [0, 1]
        combinations = list(itertools.product(values, repeat=n))
        # Filter out the combination where all particles have a value of 0
        combinations = [combo for combo in combinations if sum(combo) > 0]
        return combinations

    
aa_statuses=generate_particle_combinations(num_aa)
poses = generate_particle_states(num_d, gridsize)

states = [-1, 0] #change
for drone_pos in poses:
        for aa_status in aa_statuses:
            pos = np.array(drone_pos)
            states.append(get_state_code(pos ,aa_status))

class CombatEnvironment:
    def __init__(self, grid_size=(gridsize, gridsize), num_drones=num_d, num_defenses=num_aa, cell_size=60):
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
        self.drones = [Drone((np.random.randint(0,grid_size[0]), np.random.randint(0,grid_size[1])),1) for i in range(num_drones)]
        self.knight_image = pygame.image.load("knight.png")
        self.defenses = [DefenseSystem((aa_positions[i]),1) for i in range(num_defenses)]
        self.place_entities()
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Drone Swarm Optimization Simulation')

    def place_entities(self):
        """
        Place drones and defense systems on the grid.
        """
        for entity in self.drones + self.defenses:
            if(entity.status):
                self.grid[entity.position] = entity
            
                

    def step(self, action):
        """
        Set drones and defences according to the newly provided coordinates.
        """
        for i,a in enumerate(action):
            self.drones[i].prev_position = self.drones[i].position
            self.drones[i].position = tuple(t1 + t2 for t1, t2 in zip(self.drones[i].position, movement_delta[int(a)]))
            # b1 = (np.linalg.norm(np.array(self.drones[i].position) - np.array(aa_positions[0])))
            # b2 = (np.linalg.norm(np.array(self.drones[i].position) - np.array(aa_positions[1])))
            # print(b1,' b1', 'b2 ', b2)
            for j in range(num_aa):
                if(np.linalg.norm(np.array(self.drones[i].position) - np.array(self.defenses[j].position))<=0.1):
                    self.defenses[j].status=0

        # print(self.defenses[0].status,self.defenses[1].status)
        self.reset()

    def render(self):
        """
        Render the environment.
        """
        
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        for j in range(self.grid_size[0]):
            for i in range(self.grid_size[1]):
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)  # Draw grid lines
                if isinstance(self.grid[j, i], Drone):
                    # pygame.draw.circle(self.screen, (0, 255, 0), rect.center, self.cell_size // 4)  # Draw drones
                    scaled_knight_image = pygame.transform.scale(self.knight_image, (self.cell_size, self.cell_size))
                    self.screen.blit(scaled_knight_image,rect.topleft)
                elif isinstance(self.grid[j, i], DefenseSystem):
                    pygame.draw.rect(self.screen, (255, 0, 0), rect.inflate(-20, -20))  # Draw defenses
        for i in range(num_d):
            # print(self.drones[i].prev_position,self.drones[i].position)
            pygame.draw.line(self.screen,(255,255,0),np.multiply(self.drones[i].prev_position,60)+(30,30),np.multiply(self.drones[i].position,60)+(30,30),5)
        pygame.display.flip()  # Update the display
        
        d_p = np.zeros((num_d,2))
        for i in range(num_d):
            d_p[i,0] = self.drones[i].position[0]
            d_p[i,1] = self.drones[i].position[1]
        aa_s = np.zeros((num_aa,1))
        for i in range(num_aa):
            aa_s[i] = self.defenses[i].status
        state = states.index(get_state_code(d_p,aa_s))
        
        return state

    def reset(self):
        """
        Reset the environment.
        """
        self.grid = np.zeros(self.grid_size, dtype=object)
        self.place_entities()