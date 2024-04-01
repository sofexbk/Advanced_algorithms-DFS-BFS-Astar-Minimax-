import tkinter as tk
from tkinter import messagebox
import heapq

# Fonction d'estimation heuristique (nombre de cases mal placées)
def heuristic(state, goal_state):
    misplaced = sum(1 for i in range(3) for j in range(3) if state[i][j] != goal_state[i][j])
    return misplaced

# Déplacements légaux
def get_neighbors(state):
    neighbors = []
    zero_i, zero_j = None, None
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j] == 0:
                zero_i, zero_j = i, j
                break
        if zero_i is not None:
            break

    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for move in moves:
        new_i, new_j = zero_i + move[0], zero_j + move[1]
        if 0 <= new_i < len(state) and 0 <= new_j < len(state[0]):
            new_state = [row[:] for row in state]
            new_state[zero_i][zero_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[zero_i][zero_j]
            neighbors.append(new_state)

    return neighbors

# Algorithme A* avec enregistrement des étapes
def a_star(start_state, goal_state):
    heap = [(heuristic(start_state, goal_state), 0, start_state, [])]
    heapq.heapify(heap)
    visited = set()

    while heap:
        _, cost, current_state, path = heapq.heappop(heap)

        if current_state == goal_state:
            return cost, path

        if tuple(map(tuple, current_state)) in visited:
            continue

        visited.add(tuple(map(tuple, current_state)))

        for neighbor in get_neighbors(current_state):
            heapq.heappush(heap, (heuristic(neighbor, goal_state) + cost + 1, cost + 1, neighbor, path + [neighbor]))

    return float('inf'), []  # Impossible to reach goal state

# Fonction pour afficher l'état du jeu dans une fenêtre Tkinter
def display_state(state, window):
    for i in range(len(state)):
        for j in range(len(state[0])):
            label = tk.Label(window, text=str(state[i][j]), font=("Arial", 16), width=4, height=2)
            label.grid(row=i, column=j, padx=5, pady=5)

# Fonction pour afficher les étapes de la solution enchaînées avec un délai
def display_solution(solution, window, index):
    if index < len(solution):
        display_state(solution[index], window)
        window.after(1000, display_solution, solution, window, index + 1)
    else:
        window.destroy()

# Fonction principale pour l'interaction avec l'utilisateur
def main():
    print("Entrez les nombres de 0 à 8 pour former l'état initial du jeu de taquin :")
    start_state = []
    for _ in range(3):
        row = list(map(int, input().split()))
        start_state.append(row)

    print("Entrez les nombres de 0 à 8 pour former l'état final du jeu de taquin :")
    goal_state = []
    for _ in range(3):
        row = list(map(int, input().split()))
        goal_state.append(row)

    print("\nÉtat initial du jeu de taquin :")
    window = tk.Tk()
    display_state(start_state, window)

    steps, solution = a_star(start_state, goal_state)
    if steps == float('inf'):
        messagebox.showinfo("Erreur", "État initial non solvable.")
    else:
        print("\nNombre de coups pour atteindre l'état final :", steps)
        print("\nAffichage de l'état initial...")

        window.after(1500, display_solution, solution, window, 0)
        window.mainloop()

if __name__ == "__main__":
    main()
