import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import random

class Drone:
    def __init__(self, position):
        self.position = position
        self.health = 100


