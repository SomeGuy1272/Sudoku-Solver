import tkinter as tk
from tkinter import messagebox

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(
                    self.root,
                    width=2,
                    font=("Arial", 18),
                    justify='center',
                    bd=2,
                    relief='solid'
                )
                entry.grid(
                    row=i,
                    column=j,
                    padx=(2 if j % 3 == 0 and j != 0 else 1),
                    pady=(2 if i % 3 == 0 and i != 0 else 1)
                )
                entry.bind("<KeyRelease>", self.validate_input)
                self.entries[i][j] = entry

    def create_buttons(self):
        solve_button = tk.Button(self.root, text="Solve", command=self.solve_sudoku, font=("Arial", 12))
        solve_button.grid(row=9, column=0, columnspan=9, pady=10, ipadx=20)

    def validate_input(self, event):
        entry = event.widget
        value = entry.get()
        if value and (not value.isdigit() or int(value) < 1 or int(value) > 9):
            entry.delete(0, tk.END)

    def get_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                row.append(int(val) if val.isdigit() else 0)
            board.append(row)
        return board

    def display_board(self, board):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(board[i][j]))
                self.entries[i][j].config(bg="#ccffcc")  # light green

    def mark_unsolvable(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].config(bg="#ffcccc")  # light red

    def solve_sudoku(self):
        board = self.get_board()

        if not self.is_input_valid(board):
            messagebox.showerror("Invalid Input", "The board has conflicting entries. Please correct them.")
            return

        if solve(board):
            self.display_board(board)
        else:
            self.mark_unsolvable()
            messagebox.showerror("No Solution", "This board cannot be solved.")

    def is_input_valid(self, board):
        for i in range(9):
            for j in range(9):
                num = board[i][j]
                if num != 0:
                    board[i][j] = 0  # Temporarily remove to check validity
                    if not is_valid(board, num, (i, j)):
                        return False
                    board[i][j] = num
        return True


# --- Solver Logic ---
def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def is_valid(board, num, pos):
    row, col = pos
    for i in range(9):
        if board[row][i] == num and i != col:
            return False
        if board[i][col] == num and i != row:
            return False
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True

def solve(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for i in range(1, 10):
        if is_valid(board, i, (row, col)):
            board[row][col] = i
            if solve(board):
                return True
            board[row][col] = 0
    return False

# --- Launch App ---
if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()
