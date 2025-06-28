import pygame as p
import random as r
from copy import deepcopy
import time as t

class Sudoku:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solved_board = [[0 for _ in range(9)] for _ in range(9)]  # Board to store the solved state
        self.generate_full_sudoku()

    def draw_grid(self, highlight=None):  # Add offset_x parameter
        WIN.fill(WHITE)
        for i in range(9):
            for j in range(9):
                num = self.board[i][j]
                # Display solved number if the cell is empty and highlighted
                if num != 0:
                    color = HIGHLIGHT_COLOR if highlight and (i, j) == highlight else BLACK
                    text = FONT.render(str(num), True, color)
                    # Center the text with an added horizontal offset
                    text_rect = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
                    WIN.blit(text, text_rect)
                elif highlight and (i, j) == highlight:
                    # Highlight empty cell if selected
                    p.draw.rect(WIN, HIGHLIGHT_COLOR, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
    
        # Draw grid lines
        for i in range(10):
            thickness = 3 if i % 3 == 0 else 1
            p.draw.line(WIN, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), thickness)
            p.draw.line(WIN, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), thickness)
        p.display.update()


        # Draw grid lines
        for i in range(10):
            thickness = 3 if i % 3 == 0 else 1
            p.draw.line(WIN, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), thickness)
            p.draw.line(WIN, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), thickness)
        p.display.update()

    def is_valid(self, row, col, num):
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def solve_sudoku(self, animate=True):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(row, col, num):
                            self.board[row][col] = num
                            if self.solve_sudoku(animate):
                                return True
                            self.board[row][col] = 0
                    return False
        return True

    def generate_full_sudoku(self):
        def fill_sudoku():
            for row in range(9):
                for col in range(9):
                    if self.board[row][col] == 0:
                        r.shuffle(numbers)
                        for num in numbers:
                            if self.is_valid(row, col, num):
                                self.board[row][col] = num
                                if fill_sudoku():
                                    return True
                                self.board[row][col] = 0
                        return False
            return True

        numbers = list(range(1, 10))
        fill_sudoku()
        self.solved_board = [row[:] for row in self.board]  # Store the solved board for reference

    def count_solutions(self):
        count = [0]
        def backtrack():
            if count[0] > 1:
                return
            for row in range(9):
                for col in range(9):
                    if self.board[row][col] == 0:
                        for num in range(1, 10):
                            if self.is_valid(row, col, num):
                                self.board[row][col] = num
                                backtrack()
                                self.board[row][col] = 0
                        return
            count[0] += 1
        backtrack()
        return count[0]

    def randomize_and_remove(self, num_hints=30):
        puzzle = deepcopy(self.board)
        cells = [(i, j) for i in range(9) for j in range(9)]
        r.shuffle(cells)
        while len(cells) > r.randint(50, 80) - num_hints:
            row, col = cells.pop()
            original_value = puzzle[row][col]
            puzzle[row][col] = 0
            self.board = puzzle
            if self.count_solutions() != 1:
                puzzle[row][col] = original_value
        self.board = puzzle

    def random_fill(self):
        """Randomly fill the solved board with a delay for visual effect."""
        # Clear the current board before filling
        self.board = [[0 for _ in range(9)] for _ in range(9)]

        cells = [(i, j) for i in range(9) for j in range(9) if self.solved_board[i][j] != 0]
        r.shuffle(cells)  # Shuffle cells for random order
        
        for row, col in cells:
            self.board[row][col] = self.solved_board[row][col]
            self.draw_grid()  # Draw the grid after placing each number
            t.sleep(0.035)

p.init()
p.font.init()  # Ensure the font system is initialized

WIDTH, HEIGHT = 801, 801
CELL_SIZE = WIDTH // 9
WIN = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("sussy file5_.exe")
WHITE = (15, 15, 15)
BLACK = (200, 200, 200)
HIGHLIGHT_COLOR = (200, 0, 0)

try:
    FONT = p.font.SysFont("arial", 60)
except Exception as e:
    print(f"Error loading font: {e}")
    FONT = p.font.SysFont("arial", 60)

def main():
    running = True
    selected_cell = None  # Variable to store the selected cell
    sudoku = Sudoku()
    sudoku.randomize_and_remove(num_hints=30)
    sudoku.solve_sudoku()

    # Use the random fill method to show the solved numbers
    sudoku.random_fill()

    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            if event.type == p.MOUSEBUTTONDOWN:
                # Get mouse position and calculate the cell
                mouse_x, mouse_y = event.pos
                col = mouse_x // CELL_SIZE
                row = mouse_y // CELL_SIZE
                if sudoku.board[row][col] == 0:  # Only allow selection of empty cells
                    selected_cell = (row, col)
        
        # Drawing the grid with highlighting the selected cell
        sudoku.draw_grid(highlight=selected_cell)

        if selected_cell:
            row, col = selected_cell
            # Place the solved number from the solved board in the selected cell
            if sudoku.solved_board[row][col] != 0:
                sudoku.board[row][col] = sudoku.solved_board[row][col]
                selected_cell = None  # Reset the selected cell after placing the number

    p.quit()

if __name__ == "__main__":
    main()