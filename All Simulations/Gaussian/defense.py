# defense.py
import numpy as np

class DefenseSystem:
    def __init__(self, position, status):
        self.position = position
        self.status = status
            
    def aa_hit_prob(self,drone_pos1,drone_pos2):
        d1 = np.linalg.norm(np.array(drone_pos1) - np.array(self.position))
        d2 = np.linalg.norm(np.array(drone_pos2) - np.array(self.position))
        p1 = 0.5*np.e**(-(10**2)*((d1-2)**2))
        p2 = 0.5*np.e**(-(10**2)*((d2-2)**2))
        if(p1>p2):
            return [p1,0]
        elif(p1<p2):
            return [p2,1]
        elif(p1==p2):
            a = np.random.choice([0,1],p=[0.5, 0.5])
            if(a==0):
                return [p1*self.status,0]
            elif(a==1):
                return [p2*self.status,1]