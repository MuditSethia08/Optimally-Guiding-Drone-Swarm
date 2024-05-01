# agent.py
import numpy as np 

class Drone:
    def __init__(self, position,status):
        self.position = position
        self.status = status

    def drone_hit_prob(self,aa):
        return 1*np.e**-(np.linalg.norm(np.array(self.position) - np.array(aa)))