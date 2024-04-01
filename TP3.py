import tkinter as tk
from tkinter import messagebox, ttk
import math

# Définition des symboles pour le joueur humain et l'ordinateur
EMPTY = ' '
HUMAN = 'X'
COMPUTER = 'O'


class TicTacToeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")

        self.starting_player = tk.StringVar(value="me")

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        ttk.Label(self.frame, text="Choisissez qui commence:").pack()
        ttk.Radiobutton(self.frame, text="Moi", variable=self.starting_player, value="me").pack()
        ttk.Radiobutton(self.frame, text="IA", variable=self.starting_player, value="ai").pack()

        ttk.Button(self.frame, text="Commencer", command=self.start_game).pack()

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        self.board = [[EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY]]

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = HUMAN
        self.computer_player = COMPUTER

    def create_board_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.board_frame, text='', font=('Helvetica', 24), width=5, height=2,
                                               command=lambda row=i, col=j: self.on_button_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def start_game(self):
        self.frame.destroy()
        self.create_board_buttons()
        if self.starting_player.get() == "ai":
            self.current_player = COMPUTER
            self.computer_move()

    def on_button_click(self, row, col):
        if self.board[row][col] == EMPTY and self.current_player == HUMAN:
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_winner(self.current_player):
                messagebox.showinfo("Fin de partie", f"Le joueur {self.current_player} a gagné!")
                self.reset_game()
            elif self.game_over():
                messagebox.showinfo("Fin de partie", "Match nul!")
                self.reset_game()
            else:
                self.current_player = COMPUTER
                self.computer_move()

    def computer_move(self):
        best_score = -math.inf
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    self.board[i][j] = self.computer_player
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = EMPTY
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            row, col = best_move
            self.board[row][col] = self.computer_player
            self.buttons[row][col].config(text=self.computer_player)

            if self.check_winner(self.computer_player):
                messagebox.showinfo("Fin de partie", f"Le joueur {self.computer_player} a gagné!")
                self.reset_game()
            elif self.game_over():
                messagebox.showinfo("Fin de partie", "Match nul!")
                self.reset_game()
            else:
                self.current_player = HUMAN

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner(COMPUTER):
            return 1
        elif self.check_winner(HUMAN):
            return -1
        elif self.game_over():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == EMPTY:
                        board[i][j] = COMPUTER
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = EMPTY
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == EMPTY:
                        board[i][j] = HUMAN
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = EMPTY
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        # Vérification des lignes et des colonnes
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or all(self.board[j][i] == player for j in range(3)):
                return True
        # Vérification des diagonales
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def game_over(self):
        return self.check_winner(HUMAN) or self.check_winner(COMPUTER) or not any(
            EMPTY in row for row in self.board)

    def reset_game(self):
        self.board = [[EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY]]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=EMPTY)
        self.current_player = HUMAN

    def run(self):
        self.root.mainloop()


# Démarrage de l'interface graphique
if __name__ == "__main__":
    game = TicTacToeGUI()
    game.run()
