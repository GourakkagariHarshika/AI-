from collections import deque

class RabbitLeap:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal

    def get_moves(self, state):
        moves = []
        index = state.index('_')  # position of the empty space

        # Move left or right: swap '_' with adjacent rabbit
        for delta in [-1, -2, 1, 2]:  # single step or jump
            new_index = index + delta
            if 0 <= new_index < len(state):
                # valid jump logic
                if abs(delta) == 1 or (abs(delta) == 2 and state[index + delta // 2] != '_'):
                    new_state = state.copy()
                    new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
                    moves.append(new_state)
        return moves

    def bfs(self):
        visited = set()
        queue = deque([(self.start, [self.start])])

        while queue:
            current, path = queue.popleft()
            state_tuple = tuple(current)

            if state_tuple in visited:
                continue
            visited.add(state_tuple)

            if current == self.goal:
                return path

            for move in self.get_moves(current):
                queue.append((move, path + [move]))
        return None

    def dfs(self):
        visited = set()
        stack = [(self.start, [self.start])]

        while stack:
            current, path = stack.pop()
            state_tuple = tuple(current)

            if state_tuple in visited:
                continue
            visited.add(state_tuple)

            if current == self.goal:
                return path

            for move in self.get_moves(current):
                stack.append((move, path + [move]))
        return None


def print_path(path):
    if not path:
        print("No solution found.")
        return
    for step in path:
        print(''.join(step))
    print(f"Steps: {len(path) - 1}")


# Initial and goal state
start_state = ['E', 'E', 'E', '_', 'W', 'W', 'W']
goal_state = ['W', 'W', 'W', '_', 'E', 'E', 'E']

# Create solver
solver = RabbitLeap(start_state, goal_state)

# Run BFS
print("BFS Solution:")
bfs_path = solver.bfs()
print_path(bfs_path)

# Run DFS
print("\nDFS Solution:")
dfs_path = solver.dfs()
print_path(dfs_path)

