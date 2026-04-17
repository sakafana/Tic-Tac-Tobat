import time
import tkinter as tk
from tkinter import messagebox

class TicTacToePureMinimax:
    def __init__(self, root):
        self.root = root
        # Judul jendela disesuaikan agar jelas ini versi tanpa pruning
        self.root.title("Tic-Tac-Toe Murni Minimax")
        # Tema warna gelap (Dark Mode) agar menarik
        self.root.configure(bg='#2c3e50')
        
        self.board = [' ' for _ in range(9)]
        self.buttons = []
        # Variabel untuk mencatat statistik
        self.nodes_visited = 0
        self.setup_gui()

    def setup_gui(self):
        # Header Info: Menampilkan giliran
        self.info_label = tk.Label(self.root, text="Giliran Anda (X)", font=('Helvetica', 14, 'bold'), 
                                  bg='#2c3e50', fg='#ecf0f1', pady=10)
        self.info_label.grid(row=0, column=0, columnspan=3)

        # Membuat Grid Tombol 3x3
        for i in range(9):
            btn = tk.Button(self.root, text='', font=('Helvetica', 20, 'bold'), width=5, height=2,
                           bg='#34495e', fg='white', relief='flat',
                           # Menggunakan lambda agar fungsi tahu tombol mana yang diklik
                           command=lambda i=i: self.player_move(i))
            btn.grid(row=(i//3)+1, column=i%3, padx=5, pady=5)
            # Mengubah warna saat kursor mouse lewat di atasnya (hover effect)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#3e5871') if b['state'] == 'normal' else None)
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg='#34495e') if b['state'] == 'normal' else None)
            self.buttons.append(btn)

        # Area Statistik: Menampilkan waktu eksekusi dan node count
        # Menggunakan font Monospace (Courier) agar angka sejajar
        self.stats_label = tk.Label(self.root, text="Performa AI:\nTime: -\nNodes Visited: -", 
                                   font=('Courier', 10), bg='#2c3e50', fg='#bdc3c7', 
                                   justify='left', bd=1, relief='solid', padx=10, pady=5)
        self.stats_label.grid(row=4, column=0, columnspan=3, pady=15)

    def is_winner(self, b, p):
        # 8 Kombinasi kemenangan
        win = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        return any(b[x]==b[y]==b[z]==p for x,y,z in win)

    # --- LOGIKA CORE MINIMAX MURNI ---
    def minimax(self, board, depth, is_max):
        # Setiap kali fungsi ini dipanggil, hitung sebagai 1 node yang dikunjungi
        self.nodes_visited += 1
        
        # Mengecek kondisi terminal (akhir permainan)
        if self.is_winner(board, 'O'): return 10 - depth  # AI Menang
        if self.is_winner(board, 'X'): return depth - 10  # Pemain Menang
        if ' ' not in board: return 0                     # Seri

        if is_max:
            # Giliran AI (Maximizing)
            best_val = -float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'O'
                    # Memanggil rekursif untuk giliran lawan
                    value = self.minimax(board, depth + 1, False)
                    board[i] = ' '
                    best_val = max(best_val, value)
            return best_val
        else:
            # Giliran Pemain (Minimizing)
            best_val = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'X'
                    # Memanggil rekursif untuk giliran AI
                    value = self.minimax(board, depth + 1, True)
                    board[i] = ' '
                    best_val = min(best_val, value)
            return best_val

    def ai_move(self):
        self.info_label.config(text="AI Sedang Berpikir...", fg='#e74c3c')
        self.root.update() # Update GUI agar label berubah sebelum AI lag

        self.nodes_visited = 0 # Reset hitungan node
        start_time = time.time() # Mulai hitung waktu
        
        best_val = -float('inf')
        move = -1
        
        # Evaluasi semua langkah yang tersedia di level teratas
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                # Mulai pencarian penuh (tanpa alpha-beta)
                res = self.minimax(self.board, 0, False)
                self.board[i] = ' '
                
                if res > best_val:
                    best_val = res
                    move = i
        
        execution_time = time.time() - start_time # Waktu selesai

        # Terapkan langkah AI ke GUI
        if move != -1:
            self.board[move] = 'O'
            self.buttons[move].config(text='O', fg='#e74c3c', state='disabled', bg='#34495e')
            
            # Perbarui label statistik dengan data aktual
            self.stats_label.config(text=f"Performa AI (Minimax):\nTime: {execution_time:.4f}s\nNodes Visited: {self.nodes_visited:,}")
            self.info_label.config(text="Giliran Anda (X)", fg='#ecf0f1')

            # Cek apakah AI menang setelah melangkah
            if self.is_winner(self.board, 'O'):
                messagebox.showinfo("Game Over", "AI Menang!")
                self.reset_game()
            elif ' ' not in self.board:
                messagebox.showinfo("Game Over", "Permainan Seri!")
                self.reset_game()

    def player_move(self, i):
        # Validasi jika kotak kosong dan bukan giliran AI
        if self.board[i] == ' ':
            # Terapkan langkah pemain (X)
            self.board[i] = 'X'
            # Warna biru untuk pemain
            self.buttons[i].config(text='X', fg='#3498db', state='disabled', bg='#34495e')
            
            if self.is_winner(self.board, 'X'):
                messagebox.showinfo("Game Over", "Hebat! Anda Menang!")
                self.reset_game()
            elif ' ' not in self.board:
                messagebox.showinfo("Game Over", "Permainan Seri!")
                self.reset_game()
            else:
                # Jika belum berakhir, giliran AI
                self.ai_move()

    def reset_game(self):
        self.board = [' ' for _ in range(9)]
        self.info_label.config(text="Giliran Anda (X)", fg='#ecf0f1')
        for btn in self.buttons:
            btn.config(text='', state='normal', bg='#34495e')
        # Kosongkan statistik lama saat reset
        self.stats_label.config(text="Performa AI:\nTime: -\nNodes Visited: -")

if __name__ == "__main__":
    root = tk.Tk()
    # Atur agar jendela muncul di tengah layar (opsional, untuk kerapihan)
    root.eval('tk::PlaceWindow . center')
    game = TicTacToePureMinimax(root)
    root.mainloop()