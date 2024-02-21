# agent.py

class Drone:
    def __init__(self, position, health=100, attack_power=10, range=2):
        self.position = position
        self.health = health
        self.attack_power = attack_power
        self.range = range

    def act(self, action, environment):
        # Implement the logic for drone actions (move, attack)
        pass
