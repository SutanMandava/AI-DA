import numpy as np
import copy

class EightPuzzle:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
    
    def heuristic(self, state, method='manhattan'):
        if method == 'manhattan':
            distance = 0
            for i in range(3):
                for j in range(3):
                    value = state[i][j]
                    if value != 0:
                        goal_x, goal_y = np.where(self.goal_state == value)
                        distance += abs(i - goal_x[0]) + abs(j - goal_y[0])
            return distance
        elif method == 'misplaced':
            return np.sum(state != self.goal_state) - 1

    def get_neighbors(self, state):
        neighbors = []
        blank_pos = np.argwhere(state == 0)[0]
        x, y = blank_pos

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                neighbor = copy.deepcopy(state)
                neighbor[x][y], neighbor[nx][ny] = neighbor[nx][ny], neighbor[x][y]
                neighbors.append(neighbor)
        return neighbors

    def hill_climbing(self, heuristic_method='manhattan'):
        current_state = self.initial_state
        current_heuristic = self.heuristic(current_state, heuristic_method)

        steps = [current_state]
        while True:
            neighbors = self.get_neighbors(current_state)
            neighbor_heuristics = [self.heuristic(n, heuristic_method) for n in neighbors]

            best_heuristic = min(neighbor_heuristics)
            if best_heuristic >= current_heuristic:
                break

            best_index = neighbor_heuristics.index(best_heuristic)
            current_state = neighbors[best_index]
            current_heuristic = best_heuristic
            steps.append(current_state)

            if np.array_equal(current_state, self.goal_state):
                break

        return steps, current_heuristic

initial_state = np.array([[2, 8, 3], [1, 6, 4], [7, 0, 5]])
goal_state = np.array([[1, 2, 3], [8, 0, 4], [7, 6, 5]])

puzzle = EightPuzzle(initial_state, goal_state)
steps, final_heuristic = puzzle.hill_climbing('manhattan')

print("Steps to solution:")
for step in steps:
    print(step, "\n")
print("Final Heuristic Value:", final_heuristic)
