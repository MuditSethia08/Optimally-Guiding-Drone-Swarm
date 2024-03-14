class StateMaker:
    def __init__(self, state):
        # Parsing the input state string
        positions = list(map(int, state.split(',')))
        self.a1 = positions[:2]
        self.a2 = positions[2:4]
        self.d1 = positions[4:6]
        self.d2 = positions[6:]

    def get_possible_moves(self, agent):
        # Define possible moves
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        possible_moves = []
        for dx, dy in directions:
            new_x, new_y = agent[0] + dx, agent[1] + dy
            # Check if move is within the grid
            if 0 <= new_x < 5 and 0 <= new_y < 5:
                possible_moves.append((new_x, new_y))
        return possible_moves

    def generate_next_states(self):
        next_states = []
        a1_moves = self.get_possible_moves(self.a1)
        a2_moves = self.get_possible_moves(self.a2)

        for a1_move in a1_moves:
            for a2_move in a2_moves:
                # Ensure agents do not overlap
                if a1_move != a2_move:
                    # Copy the original defense positions
                    d1_pos = list(self.d1)
                    d2_pos = list(self.d2)

                    # Check if agents attack the defenses
                    if a1_move == tuple(d1_pos):
                        d1_pos = [-1, -1]
                    elif a1_move == tuple(d2_pos):
                        d2_pos = [-1, -1]
                    if a2_move == tuple(d1_pos):
                        d1_pos = [-1, -1]
                    elif a2_move == tuple(d2_pos):
                        d2_pos = [-1, -1]

                    state_str = f"{a1_move[0]}, {a1_move[1]}, {a2_move[0]}, {a2_move[1]}, {d1_pos[0]}, {d1_pos[1]}, {d2_pos[0]}, {d2_pos[1]}"
                    next_states.append(state_str)
        return next_states
