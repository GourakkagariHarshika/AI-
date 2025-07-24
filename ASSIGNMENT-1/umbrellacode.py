from collections import deque
from itertools import combinations

# === Define Person class ===
class Person:
    def __init__(self, name, time):
        self.name = name
        self.time = time

    def __repr__(self):
        return self.name

# === Define State class ===
class State:
    def __init__(self, left, right, umbrella_side, time_elapsed, path):
        self.left = left  # People on left
        self.right = right  # People on right
        self.umbrella_side = umbrella_side  # 'left' or 'right'
        self.time_elapsed = time_elapsed
        self.path = path  # List of actions taken

    def is_goal(self):
        return len(self.left) == 0  # All crossed

    def __hash__(self):
        return hash((tuple(sorted(p.name for p in self.left)), self.umbrella_side))

    def __eq__(self, other):
        return self.left == other.left and self.umbrella_side == other.umbrella_side

# === Define Problem class ===
class BridgeCrossing:
    def __init__(self):
        self.people = [
            Person("Amogh", 5),
            Person("Ameya", 10),
            Person("Grandmother", 20),
            Person("Grandfather", 25)
        ]
        self.max_time = 60
        self.initial_state = State(left=self.people.copy(), right=[], umbrella_side='left', time_elapsed=0, path=[])

    def get_successors(self, state):
        successors = []

        if state.umbrella_side == 'left':
            # Move 2 people from left to right
            for pair in combinations(state.left, 2):
                time_cost = max(p.time for p in pair)
                if state.time_elapsed + time_cost > self.max_time:
                    continue
                new_left = state.left.copy()
                new_right = state.right.copy()
                for p in pair:
                    new_left.remove(p)
                    new_right.append(p)
                new_path = state.path + [f"{[p.name for p in pair]} cross → ({time_cost} min)"]
                successors.append(State(new_left, new_right, 'right', state.time_elapsed + time_cost, new_path))

        else:
            # Move 1 person back from right to left
            for p in state.right:
                time_cost = p.time
                if state.time_elapsed + time_cost > self.max_time:
                    continue
                new_left = state.left.copy()
                new_right = state.right.copy()
                new_right.remove(p)
                new_left.append(p)
                new_path = state.path + [f"{p.name} returns ← ({time_cost} min)"]
                successors.append(State(new_left, new_right, 'left', state.time_elapsed + time_cost, new_path))

        return successors

    def bfs(self):
        visited = set()
        queue = deque([self.initial_state])

        while queue:
            current = queue.popleft()
            if current.is_goal() and current.time_elapsed <= self.max_time:
                return current
            if hash(current) in visited:
                continue
            visited.add(hash(current))
            for succ in self.get_successors(current):
                queue.append(succ)
        return None

    def dfs(self):
        visited = set()
        stack = [self.initial_state]

        while stack:
            current = stack.pop()
            print(f"Time: {current.time_elapsed}, Left: {[p.name for p in current.left]}, Right: {[p.name for p in current.right]}, Umbrella: {current.umbrella_side}")  # Debug
            if current.is_goal() and current.time_elapsed <= self.max_time:
                return current
            if hash(current) in visited:
                continue
            visited.add(hash(current))
            for succ in self.get_successors(current):
                stack.append(succ)
        return None


# === Run BFS and DFS ===
if __name__ == "__main__":
    problem = BridgeCrossing()

    print("BFS Solution (≤ 60 mins):")
    bfs_solution = problem.bfs()
    if bfs_solution:
        for step in bfs_solution.path:
            print(step)
        print(f" Total time: {bfs_solution.time_elapsed} minutes")
    else:
        print(" No BFS solution within 60 minutes.")

    print("\nDFS Solution (≤ 60 mins):")
    dfs_solution = problem.dfs()
    if dfs_solution:
        for step in dfs_solution.path:
            print(step)
        print(f" Total time: {dfs_solution.time_elapsed} minutes")
    else:
        print(" No DFS solution within 60 minutes.")

