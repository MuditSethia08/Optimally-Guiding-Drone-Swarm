# agent.py
import numpy as np 

class Drone:
    def __init__(self, position,status):
        self.position = position
        self.status = status
    
    def drone_hit_prob(self, aa):
        d = np.linalg.norm(np.array(self.position) - np.array(aa))
        return np.e**(-0.75*d)