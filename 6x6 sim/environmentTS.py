# environment.py

import numpy as np
import pygame
import random
from agent import Drone
from defense import DefenseSystem

random_seed = 0
gridsize=6
def get_state_code(drone_pos1,drone_pos2, aa1_status, aa2_status):
    # Winning
    if aa1_status == 0 and aa2_status == 0:
        return 0
    return 100000*drone_pos1[0] + 10000*drone_pos1[1]+1000*drone_pos2[0] + 100*drone_pos2[1] + 10*aa1_status + aa2_status

aa_positions = [
        (2,0),
        (3,2)
    ]

actions = {
        #0: "shoot first aa",
        #1: "shoot second aa",
        0: "moves up",
        1: "moves left",
        2: "moves down",
        3: "moves right"
    }
movement_delta = {
    0: (0,-1),
    1: (-1,0),
    2: (0,1),
    3: (1,0)
}
states = [-1, 0] #change
for x_coord1 in range(gridsize):
    for y_coord1 in range(gridsize):
        for x_coord2 in range(gridsize):
            for y_coord2 in range(gridsize):
                states.append(get_state_code((x_coord1, y_coord1),(x_coord2, y_coord2), 0, 1))
                states.append(get_state_code((x_coord1, y_coord1),(x_coord2, y_coord2), 1, 0))
                states.append(get_state_code((x_coord1, y_coord1),(x_coord2, y_coord2), 1, 1))

class CombatEnvironment:
    def __init__(self, grid_size=(6, 6), num_drones=2, num_defenses=2, cell_size=60):
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
            else:
                self.grid[entity.position] = None
                

    def step(self, action, num_drones, num_defenses):
        """
        Set drones and defences according to the newly provided coordinates.
        """
        num_defenses=2
        num_drones=2
        a_d = np.zeros((num_defenses,2))
        d_a = np.zeros((num_drones,2))

        # for i in range(num_defenses):
        #      a_d[i,:] = 0# self.defenses[i].aa_hit_prob(self.drones[0].position,self.drones[1].position)
        #      #print('aa'+str(i+1)+' shoots '+'drone'+str(a_d[i,1]+1))
        for i,a in enumerate(action):
            self.drones[i].position = tuple(t1 + t2 for t1, t2 in zip(self.drones[i].position, movement_delta[a]))
            b1 = (np.linalg.norm(np.array(self.drones[i].position) - np.array(aa_positions[0])))
            b2 = (np.linalg.norm(np.array(self.drones[i].position) - np.array(aa_positions[1])))
            print(b1,' b1', 'b2 ', b2)
            if(b1==0):
                self.defenses[0].status==0
                num_defenses=num_defenses-1
                
            if(b2==0):
                self.defenses[1].status==0
                num_defenses=num_defenses-1
                print('numdef ', num_defenses)

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
                    pygame.draw.circle(self.screen, (0, 255, 0), rect.center, self.cell_size // 4)  # Draw drones
                elif isinstance(self.grid[j, i], DefenseSystem):
                    pygame.draw.rect(self.screen, (255, 0, 0), rect.inflate(-20, -20))  # Draw defenses
        pygame.display.flip()  # Update the display
        if(self.drones[0].status==1 and self.drones[1].status==1):
            state = states.index(get_state_code(self.drones[0].position,self.drones[1].position,self.defenses[0].status,self.defenses[1].status))
            print(self.drones[0].position,self.drones[1].position,self.defenses[0].status,self.defenses[1].status)
            print(state) 
        else:
            state = -1
        
        return state

    def reset(self):
        """
        Reset the environment.
        """
        self.grid = np.zeros(self.grid_size, dtype=object)
        self.place_entities()