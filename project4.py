        #  TIC TAC TOE GAME


import tkinter as tk
from tkinter import messagebox
import random



class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.mode = None  # "single" or "two"
        self.current_player = "X"
        self.board = [""] * 9
        self.scores = {"X": 0, "O": 0}

        self.create_mode_selection()

    def create_mode_selection(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(self.root, text="Choose Game Mode", font=("Arial", 16))
        label.pack(pady=20)

        single_btn = tk.Button(self.root, text="Single Player (vs Computer)", font=("Arial", 12),
                               command=lambda: self.start_game("single"))
        single_btn.pack(pady=10)

        multi_btn = tk.Button(self.root, text="Two Player", font=("Arial", 12),
                              command=lambda: self.start_game("two"))
        multi_btn.pack(pady=10)

    def start_game(self, mode):
        self.mode = mode
        self.board = [""] * 9
        self.current_player = "X"
        self.create_game_ui()

    def create_game_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.buttons = []
        for i in range(9):
            button = tk.Button(self.root, text="", font=("Arial", 24), width=5, height=2,
                               command=lambda i=i: self.on_click(i))
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(button)

        self.status = tk.Label(self.root, text=f"Player {self.current_player}'s turn", font=("Arial", 14))
        self.status.grid(row=3, column=0, columnspan=3, pady=10)

        self.score_label = tk.Label(self.root, text=self.get_score_text(), font=("Arial", 12), fg="blue")
        self.score_label.grid(row=4, column=0, columnspan=3)

        self.reset_btn = tk.Button(self.root, text="Restart", command=self.reset_game, font=("Arial", 12))
        self.reset_btn.grid(row=5, column=0, columnspan=1, pady=10)

        self.mode_btn = tk.Button(self.root, text="Change Mode", command=self.create_mode_selection, font=("Arial", 12))
        self.mode_btn.grid(row=5, column=2, columnspan=1, pady=10)

    def get_score_text(self):
        return f"Score — X: {self.scores['X']}  |  O: {self.scores['O']}"

    def on_click(self, index):
        if self.board[index] == "" and not self.check_winner():
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)

            winner = self.check_winner()
            if winner:
                self.status.config(text=f"🎉 Player {winner} wins!")
                self.scores[winner] += 1
                self.score_label.config(text=self.get_score_text())
                messagebox.showinfo("Game Over", f"Player {winner} wins!")
                return
            elif "" not in self.board:
                self.status.config(text="It's a draw!")
                messagebox.showinfo("Game Over", "It's a draw!")
                return

            self.current_player = "O" if self.current_player == "X" else "X"
            self.status.config(text=f"Player {self.current_player}'s turn")

            if self.mode == "single" and self.current_player == "O":
                self.root.after(500, self.computer_move)

    def computer_move(self):
        available = [i for i, val in enumerate(self.board) if val == ""]
        if available:
            move = random.choice(available)
            self.on_click(move)

    def check_winner(self):
        wins = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        for combo in wins:
            a, b, c = combo
            if self.board[a] == self.board[b] == self.board[c] != "":
                return self.board[a]
        return None

    def reset_game(self):
        self.board = [""] * 9
        self.current_player = "X"
        for button in self.buttons:
            button.config(text="")
        self.status.config(text=f"Player {self.current_player}'s turn")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
