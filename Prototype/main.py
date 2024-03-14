import pygame
from environment import CombatEnvironment
import numpy as np

def main():
    env = CombatEnvironment()
    num_drones = 2  # Adjust this based on the number of drones in your environment
    state_size = 3 * num_drones
    action_size = len(env.action_space)
    agent = env.agent

    episodes = 1000
    batch_size = 32

    for e in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, state_size])

        for time_step in range(500):
            env.render()

            action = agent.act(state)
            next_state, reward, done = env.step([env.action_space[action]])
            next_state = np.reshape(next_state, [1, state_size])

            agent.remember(state, action, reward, next_state, done)
            state = next_state

            if done:
                print(f"Episode: {e+1}/{episodes}, Score: {time_step}")
                break

            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

    pygame.quit()

if __name__ == "__main__":
    main()
