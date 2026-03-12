import tkinter as tk

class NQueenGUI:
    def __init__(self, root, n=8, cell_size=60, delay=300):
        self.root = root
        self.n = n
        self.cell_size = cell_size
        self.delay = delay  # delay dalam milidetik

        self.board = [[0 for _ in range(n)] for _ in range(n)]
        self.solving = False

        self.root.title(f"Visualisasi Backtracking N-Queen ({n}x{n})")

        canvas_width = n * cell_size
        canvas_height = n * cell_size

        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        self.canvas.pack(pady=10)

        self.status_label = tk.Label(root, text="Tekan tombol Mulai", font=("Arial", 12))
        self.status_label.pack()

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.start_button = tk.Button(button_frame, text="Mulai", command=self.start_solving)
        self.start_button.grid(row=0, column=0, padx=5)

        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_board)
        self.reset_button.grid(row=0, column=1, padx=5)

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.n):
            for col in range(self.n):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = "#F0D9B5" if (row + col) % 2 == 0 else "#B58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                if self.board[row][col] == 1:
                    self.canvas.create_text(
                        x1 + self.cell_size // 2,
                        y1 + self.cell_size // 2,
                        text="♛",
                        font=("Arial", int(self.cell_size / 2)),
                    )

    def is_safe(self, row, col):
        # cek kolom ke atas
        for i in range(row):
            if self.board[i][col] == 1:
                return False

        # cek diagonal kiri atas
        i, j = row - 1, col - 1
        while i >= 0 and j >= 0:
            if self.board[i][j] == 1:
                return False
            i -= 1
            j -= 1

        # cek diagonal kanan atas
        i, j = row - 1, col + 1
        while i >= 0 and j < self.n:
            if self.board[i][j] == 1:
                return False
            i -= 1
            j += 1

        return True

    def start_solving(self):
        if not self.solving:
            self.solving = True
            self.start_button.config(state="disabled")
            self.status_label.config(text="Mencari solusi...")
            self.solve_step(0, 0)

    def solve_step(self, row, start_col):
        if row == self.n:
            self.draw_board()
            self.status_label.config(text="Solusi ditemukan!")
            self.solving = False
            self.start_button.config(state="normal")
            return

        for col in range(start_col, self.n):
            if self.is_safe(row, col):
                self.board[row][col] = 1
                self.draw_board()
                self.status_label.config(text=f"Meletakkan ratu di baris {row}, kolom {col}")

                self.root.after(
                    self.delay,
                    lambda r=row, c=col: self.continue_after_place(r, c)
                )
                return

        self.backtrack(row)

    def continue_after_place(self, row, col):
        self.solve_step(row + 1, 0)

    def backtrack(self, row):
        if row == 0:
            self.status_label.config(text="Tidak ada solusi.")
            self.solving = False
            self.start_button.config(state="normal")
            return

        prev_row = row - 1

        for col in range(self.n - 1, -1, -1):
            if self.board[prev_row][col] == 1:
                self.board[prev_row][col] = 0
                self.draw_board()
                self.status_label.config(text=f"Backtrack dari baris {prev_row}, kolom {col}")

                self.root.after(
                    self.delay,
                    lambda r=prev_row, c=col: self.solve_step(r, c + 1)
                )
                return

    def reset_board(self):
        self.board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.solving = False
        self.start_button.config(state="normal")
        self.status_label.config(text="Papan di-reset. Tekan tombol Mulai")
        self.draw_board()


if __name__ == "__main__":
    root = tk.Tk()
    app = NQueenGUI(root, n=8, cell_size=60, delay=300)
    root.mainloop()
