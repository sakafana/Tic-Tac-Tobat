import time
import random
import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

class TicTacTobat:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Tobat - Ultimate AI")
        self.root.geometry("450x750")
        self.root.configure(bg='#2c3e50')
        
        self.settings_file = "settings.json"
        self.load_settings()
        self.main_menu()

    def load_settings(self):
        default = {
            "Classic": True, "Infinite": True, "Trap": True, "Clash": True,
            "score_x": 0, "score_o": 0
        }
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r") as f:
                    self.data = json.load(f)
                    if "score_x" not in self.data: self.data["score_x"] = 0
                    if "score_o" not in self.data: self.data["score_o"] = 0
            except: self.data = default
        else: self.data = default
        
        self.show_rules = self.data
        self.score_x = self.data["score_x"]
        self.score_o = self.data["score_o"]

    def save_settings(self):
        self.data["score_x"] = self.score_x
        self.data["score_o"] = self.score_o
        with open(self.settings_file, "w") as f:
            json.dump(self.data, f)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="TIC TAC TOBAT", font=('Helvetica', 28, 'bold'),
                 bg='#2c3e50', fg='#f1c40f', pady=30).pack()
        
        modes = [("Classic Mode", "Classic", "#3498db"),
                 ("Infinite Mode (FIFO)", "Infinite", "#9b59b6"),
                 ("Hidden Trap Mode", "Trap", "#e67e22"),
                 ("Clash Mode (Blind)", "Clash", "#1abc9c")]

        for text, mode, color in modes:
            tk.Button(self.root, text=text, font=('Helvetica', 12, 'bold'), bg=color, fg='white', 
                      width=25, height=2, relief='flat', command=lambda m=mode: self.start_game_flow(m)).pack(pady=10)

        tk.Button(self.root, text="Reset Skor", font=('Helvetica', 10), bg='#95a5a6', fg='white', 
                  command=self.reset_score).pack(pady=10)
        tk.Button(self.root, text="Keluar Program", font=('Helvetica', 12), bg='#e74c3c', fg='white', 
                  width=25, height=2, relief='flat', command=self.root.quit).pack(pady=20)

    def reset_score(self):
        self.score_x, self.score_o = 0, 0
        self.save_settings()
        messagebox.showinfo("Reset", "Skor telah dikosongkan.")

    def start_game_flow(self, mode):
        if self.show_rules.get(mode, True): self.display_rules(mode)
        else: self.launch_mode(mode)

    def display_rules(self, mode):
        self.clear_screen()
        rules_text = {
            "Classic": "Aturan Standar: Hubungkan 3 simbol untuk menang.",
            "Infinite": "Aturan Infinite: Maksimal 3 simbol. Langkah ke-4 menghapus langkah ke-1.",
            "Trap": "Aturan Trap: Siapa pun yang menginjak jebakan, simbolnya hancur!",
            "Clash": "Aturan Clash: Pilih kotak bersamaan. Menang instan jika terbentuk 3 jajar!"
        }
        tk.Label(self.root, text=f"CARA BERMAIN: {mode}", font=('Helvetica', 14, 'bold'), bg='#2c3e50', fg='#f1c40f', pady=20).pack()
        tk.Label(self.root, text=rules_text[mode], font=('Helvetica', 11), bg='#2c3e50', fg='#ecf0f1', wraplength=350).pack(pady=20)
        self.var_rule = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Jangan tampilkan aturan ini lagi", variable=self.var_rule, bg='#2c3e50', fg='#bdc3c7').pack()
        tk.Button(self.root, text="MULAI", font=('Helvetica', 12, 'bold'), bg='#27ae60', fg='white', width=20, 
                  command=lambda: self.confirm_rules(mode)).pack(pady=20)

    def confirm_rules(self, mode):
        if self.var_rule.get(): self.show_rules[mode] = False
        self.save_settings()
        self.launch_mode(mode)

    def launch_mode(self, mode):
        self.clear_screen()
        self.current_mode = mode
        self.game_board = [' ' for _ in range(9)]
        
        # 1. Gambar Header & Score Terlebih Dahulu
        header = tk.Frame(self.root, bg='#2c3e50')
        header.pack(fill='x', padx=10, pady=5)
        tk.Button(header, text="← Menu", bg='#34495e', fg='white', command=self.main_menu).pack(side='left')
        self.score_label = tk.Label(header, text=f"Player (X): {self.score_x}  |  AI (O): {self.score_o}", 
                                   font=('Courier', 12, 'bold'), bg='#2c3e50', fg='#f1c40f')
        self.score_label.pack(side='right')

        # 2. Gambar Frame Papan
        frame = tk.Frame(self.root, bg='#2c3e50')
        frame.pack(pady=20)
        self.game_btns = []
        for i in range(9):
            btn = tk.Button(frame, text='', font=('Helvetica', 20, 'bold'), width=5, height=2,
                           bg='#34495e', fg='white', command=lambda i=i: self.handle_click(i))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.game_btns.append(btn)
        
        # Paksa GUI untuk memproses perubahan tampilan (Clear screen & Drawing board)
        self.root.update()

        # 3. Baru Munculkan Dialog Trap Jika Mode Trap
        if mode == "Trap":
            p_trap = simpledialog.askinteger("Trap", "Pasang jebakan Anda (1-9):", minvalue=1, maxvalue=9)
            if p_trap is None:
                self.main_menu()
                return
            self.p_trap = p_trap - 1
            self.ai_trap = random.choice([i for i in range(9) if i != self.p_trap])
            self.traps = {self.p_trap: "Pemain", self.ai_trap: "AI"}
            # Tandai jebakan sendiri pada UI
            self.game_btns[self.p_trap].config(highlightbackground="orange", highlightthickness=2)
        
        if mode == "Infinite": self.q_x, self.q_o = [], []

    def handle_click(self, i):
        if self.game_board[i] != ' ' and self.current_mode != "Clash": return
        if self.current_mode == "Classic": self.play_classic(i)
        elif self.current_mode == "Infinite": self.play_infinite(i)
        elif self.current_mode == "Trap": self.play_trap(i)
        elif self.current_mode == "Clash": self.play_clash(i)

    def play_classic(self, i):
        self.game_board[i] = 'X'; self.update_ui()
        if self.check_end('X'): return
        self.ai_move()

    def play_infinite(self, i):
        if len(self.q_x) >= 3:
            old = self.q_x.pop(0); self.game_board[old] = ' '
        self.game_board[i] = 'X'; self.q_x.append(i); self.update_ui()
        if self.check_end('X'): return
        move = self.get_best_move(self.game_board)
        if move != -1:
            if len(self.q_o) >= 3:
                old = self.q_o.pop(0); self.game_board[old] = ' '
            self.game_board[move] = 'O'; self.q_o.append(move); self.update_ui(); self.check_end('O')

    def play_trap(self, i):
        if i in self.traps:
            messagebox.showwarning("BOOM!", f"Bidak hancur terkena jebakan {self.traps[i]}!"); del self.traps[i]
            self.ai_move_trap(); return
        self.game_board[i] = 'X'; self.update_ui()
        if self.check_end('X'): return
        self.ai_move_trap()

    def ai_move_trap(self):
        move = self.get_best_move(self.game_board)
        if move != -1:
            if move in self.traps:
                messagebox.showinfo("AI TRAPPED", f"AI hancur terkena jebakan {self.traps[move]}!"); del self.traps[move]
            else:
                self.game_board[move] = 'O'; self.update_ui(); self.check_end('O')

    def play_clash(self, i):
        p_move, a_move = i, self.get_best_move(self.game_board)
        if p_move == a_move:
            winner = self.open_suit_window()
            if winner == "Player": self.game_board[p_move] = 'X'
            elif winner == "AI": self.game_board[a_move] = 'O'
        else:
            self.game_board[p_move] = 'X'
            if a_move != -1: self.game_board[a_move] = 'O'
        self.update_ui()
        win_x, win_o = self.is_winner(self.game_board, 'X'), self.is_winner(self.game_board, 'O')
        if win_x and win_o: messagebox.showinfo("Clash Result", "Seri."); self.launch_mode("Clash")
        elif win_x: self.process_win('X')
        elif win_o: self.process_win('O')
        elif ' ' not in self.game_board: messagebox.showinfo("Draw", "Seri!"); self.launch_mode("Clash")

    def open_suit_window(self):
        suit_win = tk.Toplevel(self.root); suit_win.title("Suit!"); suit_win.geometry("300x250")
        res = {"val": "Draw"}; choices = ["Batu", "Gunting", "Kertas"]
        def set_suit(p_choice):
            ai = random.choice(choices)
            if p_choice == ai: res["val"] = "Draw"
            elif (p_choice=="Batu" and ai=="Gunting") or (p_choice=="Gunting" and ai=="Kertas") or (p_choice=="Kertas" and ai=="Batu"):
                res["val"] = "Player"
            else: res["val"] = "AI"
            messagebox.showinfo("Result", f"Anda: {p_choice}\nAI: {ai}\nWinner: {res['val']}"); suit_win.destroy()
        tk.Label(suit_win, text="Terjadi Clash! Pilih Senjatamu:").pack(pady=10)
        for c in choices: tk.Button(suit_win, text=c, width=15, command=lambda x=c: set_suit(x)).pack(pady=5)
        self.root.wait_window(suit_win); return res["val"]

    def ai_move(self):
        move = self.get_best_move(self.game_board)
        if move != -1: self.game_board[move] = 'O'; self.update_ui(); self.check_end('O')

    def get_best_move(self, board):
        best_val, move = -float('inf'), -1
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'; res = self.minimax_ab(board, 0, -float('inf'), float('inf'), False); board[i] = ' '
                if res > best_val: best_val = res; move = i
        return move

    def minimax_ab(self, board, depth, alpha, beta, is_max):
        if self.is_winner(board, 'O'): return 10 - depth
        if self.is_winner(board, 'X'): return depth - 10
        if ' ' not in board or depth > 5: return 0
        if is_max:
            val = -float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'O'; val = max(val, self.minimax_ab(board, depth+1, alpha, beta, False)); board[i] = ' '
                    alpha = max(alpha, val)
                    if beta <= alpha: break
            return val
        else:
            val = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'X'; val = min(val, self.minimax_ab(board, depth+1, alpha, beta, True)); board[i] = ' '
                    beta = min(beta, val)
                    if beta <= alpha: break
            return val

    def is_winner(self, b, p):
        win = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        return any(b[a]==b[b_]==b[c]==p for a,b_,c in win)

    def update_ui(self):
        for i in range(9):
            char = self.game_board[i]
            self.game_btns[i].config(text=char)
            if char == 'X': self.game_btns[i].config(fg='#3498db')
            elif char == 'O': self.game_btns[i].config(fg='#e74c3c')

    def check_end(self, last_player):
        if self.is_winner(self.game_board, last_player): self.process_win(last_player); return True
        if ' ' not in self.game_board: messagebox.showinfo("Game Over", "Seri!"); self.launch_mode(self.current_mode); return True
        return False

    def process_win(self, winner):
        if winner == 'X': self.score_x += 1; msg = "Anda Menang!"
        else: self.score_o += 1; msg = "AI Menang!"
        self.save_settings(); messagebox.showinfo("Game Over", msg); self.launch_mode(self.current_mode)

if __name__ == "__main__":
    root = tk.Tk(); app = TicTacTobat(root); root.mainloop()