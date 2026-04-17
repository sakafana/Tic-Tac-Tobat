import time
import tkinter as tk
from tkinter import messagebox

class TicTacToeAlphaBeta:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe Versi Alpha-Beta Prunning")
        self.root.configure(bg='#2c3e50')
        
        self.board = [' ' for _ in range(9)]
        self.buttons = []
        self.nodes_visited = 0
        self.setup_gui()

    def setup_gui(self):
        # Header Info
        self.info_label = tk.Label(self.root, text="Giliran Anda (X)", font=('Helvetica', 14, 'bold'), 
                                  bg='#2c3e50', fg='#ecf0f1', pady=10)
        self.info_label.grid(row=0, column=0, columnspan=3)

        # Grid Buttons
        for i in range(9):
            btn = tk.Button(self.root, text='', font=('Helvetica', 20, 'bold'), width=5, height=2,
                           bg='#34495e', fg='white', relief='flat',
                           command=lambda i=i: self.player_move(i))
            btn.grid(row=(i//3)+1, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        # Stats Area
        self.stats_label = tk.Label(self.root, text="Stats: -\nNodes: -", font=('Courier', 10),
                                   bg='#2c3e50', fg='#bdc3c7', justify='left')
        self.stats_label.grid(row=4, column=0, columnspan=3, pady=10)

    def is_winner(self, b, p):
        win = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        return any(b[x]==b[y]==b[z]==p for x,y,z in win)

    def minimax_ab(self, board, depth, alpha, beta, is_max):
        self.nodes_visited += 1
        if self.is_winner(board, 'O'): return 10 - depth
        if self.is_winner(board, 'X'): return depth - 10
        if ' ' not in board: return 0

        if is_max:
            val = -float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'O'
                    val = max(val, self.minimax_ab(board, depth+1, alpha, beta, False))
                    board[i] = ' '
                    alpha = max(alpha, val)
                    if beta <= alpha: break
            return val
        else:
            val = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'X'
                    val = min(val, self.minimax_ab(board, depth+1, alpha, beta, True))
                    board[i] = ' '
                    beta = min(beta, val)
                    if beta <= alpha: break
            return val

    def ai_move(self):
        self.nodes_visited = 0
        start = time.time()
        best_val = -float('inf')
        move = -1
        
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                res = self.minimax_ab(self.board, 0, -float('inf'), float('inf'), False)
                self.board[i] = ' '
                if res > best_val:
                    best_val = res
                    move = i
        
        duration = time.time() - start
        if move != -1:
            self.board[move] = 'O'
            self.buttons[move].config(text='O', fg='#e74c3c', state='disabled')
            self.stats_label.config(text=f"Time: {duration:.4f}s\nNodes: {self.nodes_visited}")
            
            if self.is_winner(self.board, 'O'):
                messagebox.showinfo("Result", "AI Menang!")
                self.reset_game()
            elif ' ' not in self.board:
                messagebox.showinfo("Result", "Seri!")
                self.reset_game()

    def player_move(self, i):
        if self.board[i] == ' ':
            self.board[i] = 'X'
            self.buttons[i].config(text='X', fg='#3498db', state='disabled')
            
            if self.is_winner(self.board, 'X'):
                messagebox.showinfo("Result", "Anda Menang!")
                self.reset_game()
            elif ' ' not in self.board:
                messagebox.showinfo("Result", "Seri!")
                self.reset_game()
            else:
                self.ai_move()

    def reset_game(self):
        self.board = [' ' for _ in range(9)]
        for btn in self.buttons:
            btn.config(text='', state='normal')

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeAlphaBeta(root)
    root.mainloop()