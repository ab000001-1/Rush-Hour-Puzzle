import sys
import heapq
from collections import deque

class RushHour:
    def __init__(self, vehicles):
        """Initialize the board."""
        self.vehicles = vehicles
        self.sizeof_board = 6

    def __lt__(self, other):
        return False

    def stateof_board(self):
        state = set()
        for vehicle, (x, y, orientation) in self.vehicles.items():
            length = 3 if vehicle in "OPQR" else 2
            if orientation == "H":
                state.update((x + i, y) for i in range(length))
            else:
                state.update((x, y + i) for i in range(length))
        return frozenset(state)

    def puzzle_completed(self):
        """Check if the red car (X) has reached the exit."""
        if "X" not in self.vehicles:
            return False
        x, y, orientation = self.vehicles["X"]
        return orientation == "H" and x + 2 >= self.sizeof_board  

    def pos_actions(self):
        """Generate all possible actions."""
        actions = []
        taken = self.stateof_board()

        for vehicle, (x, y, orientation) in self.vehicles.items():
            length = 3 if vehicle in "OPQR" else 2
            if orientation == "H":
                if x > 0 and (x - 1, y) not in taken:
                    diff_state = self.copy()
                    diff_state.vehicles[vehicle] = (x - 1, y, orientation)
                    actions.append((diff_state, f"{vehicle}L"))
                if x + length < self.sizeof_board and (x + length, y) not 
in taken:
                    diff_state = self.copy()
                    diff_state.vehicles[vehicle] = (x + 1, y, orientation)
                    actions.append((diff_state, f"{vehicle}R"))
            else:
                if y > 0 and (x, y - 1) not in taken:
                    diff_state = self.copy()
                    diff_state.vehicles[vehicle] = (x, y - 1, orientation)
                    actions.append((diff_state, f"{vehicle}U"))
                if y + length < self.sizeof_board and (x, y + length) not 
in taken:
                    diff_state = self.copy()
                    diff_state.vehicles[vehicle] = (x, y + 1, orientation)
                    actions.append((diff_state, f"{vehicle}D"))

        return actions

    def copy(self):
        return RushHour(self.vehicles.copy())

    def blocking_heuristic(self):
        """Returns the # of vehicles blocking the red car (X)."""
        if "X" not in self.vehicles:
            return float("inf")

        x, y, _ = self.vehicles["X"]
        blocking_count = 0

        for vehicle, (vx, vy, orientation) in self.vehicles.items():
            if vehicle != "X" and vy == y and vx > x:
                blocking_count += 1  

        return blocking_count

    def distance_heuristic(self):
        """Returns a combined heuristic."""
        return (5 - self.vehicles["X"][0]) + 2 * self.blocking_heuristic()

    def use_brute_force(self):
        """Solves the puzzle using brute force."""
        stack = [(self, [])]
        visited = set()
        visited.add(self.stateof_board())

        while stack:
            current, path = stack.pop()
            if current.puzzle_completed():
                return path, len(path), len(visited), current

            for diff_state, action in current.pos_actions():
                if diff_state.stateof_board() not in visited:
                    visited.add(diff_state.stateof_board())
                    stack.append((diff_state, path + [action]))

        return None, len(visited), len(visited), self

    def use_bfs(self):
        """Solves the puzzle using breadth-first search."""
        queue = deque([(self, [])])
        visited = set()
        visited.add(self.stateof_board())

        while queue:
            current, path = queue.popleft()
            if current.puzzle_completed():
                return path, len(path), len(visited), current

            for diff_state, action in current.pos_actions():
                if diff_state.stateof_board() not in visited:
                    visited.add(diff_state.stateof_board())
                    queue.append((diff_state, path + [action]))

        return None, None, len(visited), self

    def use_best_first(self, heuristic="blocking"):
        """Solves the puzzle using Best-First Search with a heuristic."""
        queue = []
        visited = set()

        initial_h_value = self.distance_heuristic() if heuristic == 
"distance" else self.blocking_heuristic()
        heapq.heappush(queue, (initial_h_value, 0, [], self))
        
        states_explored = 0

        while queue:
            h_value, depth, path, state = heapq.heappop(queue)
            if state.puzzle_completed():
                return path, depth, states_explored, state

            if state.stateof_board() in visited:
                continue

            visited.add(state.stateof_board())
            states_explored += 1

            for diff_state, action in state.pos_actions():
                if diff_state.stateof_board() not in visited:
                    new_h_value = diff_state.distance_heuristic() if 
heuristic == "distance" else diff_state.blocking_heuristic()
                    heapq.heappush(queue, (new_h_value, depth + 1, path + 
[action], diff_state))

        return None, states_explored, states_explored, self

    def display_board(self):
        """Displays the board state in a 6x6 grid."""
        grid = [["." for _ in range(self.sizeof_board)] for _ in 
range(self.sizeof_board)]
        for vehicle, (x, y, orientation) in self.vehicles.items():
            length = 3 if vehicle in "OPQR" else 2
            for i in range(length):
                if orientation == "H":
                    grid[y][x + i] = vehicle
                else:
                    grid[y + i][x] = vehicle

        for row in grid:
            print(" ".join(row))
        print()

def parse_input():
    """Reads input."""
    vehicles = {}
    for line in sys.stdin:
        line = line.strip()
        if len(line) < 4:
            continue
        vehicle = line[0]
        x = int(line[1])
        y = int(line[2])
        orientation = line[3]
        vehicles[vehicle] = (x, y, orientation)
    
    if "X" not in vehicles:
        raise ValueError("Error: Input file has to contain the red car 
('X').")
    
    return RushHour(vehicles)

if __name__ == "__main__":
    rush_hour = parse_input()
    print("Initial Board:")
    rush_hour.display_board()

    explore_stats = {}

    def display_solution(method_name, result):
        solution, depth, states_visited, final_state = result
        explore_stats[method_name] = states_visited
        print(f"\n{method_name}:")
        if solution:
            for action in solution:
                print(action)
        else:
            print("Solution: None")
        print(f"Depth: {depth}")
        print(f"States visited: {states_visited}")
        print("\nFinal Board State:")
        final_state.display_board()

    display_solution("Brute Force", rush_hour.use_brute_force())
    display_solution("BFS", rush_hour.use_bfs())
    display_solution("Best-First (Blocking Heuristic)", 
rush_hour.use_best_first("blocking"))
    display_solution("Best-First (Distance Heuristic)", 
rush_hour.use_best_first("distance"))

    print("\nSearch Space Comparison:")
    print(f"{'Algorithm':<30}{'States Explored'}")
    print("-" * 50)
    for method, nodes in explore_stats.items():
        print(f"{method:<30}{nodes}")

