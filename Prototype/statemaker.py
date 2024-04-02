class StateMaker:
    def __init__(self, state, n, m):
        # Parsing the input state string
        positions = list(map(int, state.split(',')))
        self.agents = [positions[i:i+2] for i in range(0, 2*n, 2)]
        self.defenses = [positions[i:i+2] for i in range(2*n, 2*n+2*m, 2)]
        self.n = n
        self.m = m
        self.gridsize = 5

    def get_possible_moves(self, agent):
        # Define possible moves
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        possible_moves = []
        for dx, dy in directions:
            new_x, new_y = agent[0] + dx, agent[1] + dy
            # Check if move is within the grid
            if 0 <= new_x < self.gridsize and 0 <= new_y < self.gridsize:
                possible_moves.append((new_x, new_y))
        return possible_moves

    def generate_next_states(self):
        next_states = []
        all_moves = [self.get_possible_moves(agent) for agent in self.agents]

        def recurse(index, current_state):
            if index == len(all_moves):
                # Check for any attacks on defenses
                defenses_pos = [d[:] for d in self.defenses]  # Create a copy of the defenses positions
                for i, agent_pos in enumerate(current_state):
                    for j, defense_pos in enumerate(defenses_pos):
                        if agent_pos == tuple(defense_pos):
                            defenses_pos[j] = [-1, -1]

                state_str = ', '.join([f"{pos[0]}, {pos[1]}" for pos in (current_state + defenses_pos)])
                next_states.append(state_str)
                return

            for move in all_moves[index]:
                if move not in current_state:  # Ensure no overlap among agents
                    recurse(index + 1, current_state + [move])

        recurse(0, [])
        return next_states
