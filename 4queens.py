class FourQueensProblem:
    def __init__(self):
        self.size = 4

    def place_queen(self, state, row, col):
        state.append((row, col))

    def is_safe(self, state, row, col):
        for qr, qc in state:
            if qr == row or qc == col or abs(qr - row) == abs(qc - col):
                return False
        return True

    def is_goal(self, state):
        return len(state) == self.size

    def get_successors(self, state):
        successors = []
        for col in range(self.size):
            row = len(state)  # Place the queen on the next available row
            if self.is_safe(state, row, col):
                successors.append(state + [(row, col)])
        return successors


def bfs(problem):
    queue = [([], [])]  # Chaque élément est un tuple contenant (état, étapes)
    solutions = []
    while queue:
        current_state, steps = queue.pop(0)
        if problem.is_goal(current_state):
            solutions.append((current_state, steps))
            continue
        successors = problem.get_successors(current_state)
        for successor in successors:
            queue.append((successor, steps + [successor[-1]]))  # Ajouter la dernière reine placée à l'étape
    return solutions


def dfs(problem):
    stack = [([], [])]  # Chaque élément est un tuple contenant (état, étapes)
    solutions = []
    while stack:
        current_state, steps = stack.pop()
        if problem.is_goal(current_state):
            solutions.append((current_state, steps))
            continue
        successors = problem.get_successors(current_state)
        for successor in successors:
            stack.append((successor, steps + [successor[-1]]))  # Ajouter la dernière reine placée à l'étape
    return solutions


def print_solution(solution):
    if solution:
        for sol_num, (state, steps) in enumerate(solution, 1):
            print(f"Solution {sol_num}:")
            board = [['.' for _ in range(4)] for _ in range(4)]
            for row, col in state:
                board[row][col] = 'Q'
            for row in board:
                print(' '.join(row))
            print("Trouvé avec:", len(steps), "étapes")
            print("Étapes:")
            for step in steps:
                print("- Placer une reine à la ligne", step[0], "et colonne", step[1])
            print()
    else:
        print("Pas de solution trouvée.")


if __name__ == "__main__":
    problem = FourQueensProblem()

    print("Solutions BFS:")
    bfs_solutions = bfs(problem)
    print_solution(bfs_solutions)

    print()

    print("Solutions DFS:")
    dfs_solutions = dfs(problem)
    print_solution(dfs_solutions)
