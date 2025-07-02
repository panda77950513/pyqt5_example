
import random

class GameLogic:
    def __init__(self, size=4):
        self.size = size
        self.grid = [[0] * size for _ in range(size)]
        self.score = 0
        self.game_over = False
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4

    def move(self, direction):
        moved = False
        if direction == 'up':
            self.grid, moved = self._move_vertical(self.grid)
        elif direction == 'down':
            reversed_grid = self.grid[::-1]
            reversed_grid, moved = self._move_vertical(reversed_grid)
            self.grid = reversed_grid[::-1]
        elif direction == 'left':
            transposed_grid = [list(row) for row in zip(*self.grid)]
            transposed_grid, moved = self._move_vertical(transposed_grid)
            self.grid = [list(row) for row in zip(*transposed_grid)]
        elif direction == 'right':
            transposed_grid = [list(row) for row in zip(*self.grid)]
            reversed_transposed_grid = [row[::-1] for row in transposed_grid]
            reversed_transposed_grid, moved = self._move_vertical(reversed_transposed_grid)
            self.grid = [list(row)[::-1] for row in zip(*reversed_transposed_grid)]

        if moved:
            self.add_new_tile()
            if not self.moves_left():
                self.game_over = True
        return moved

    def _move_vertical(self, grid):
        moved = False
        for c in range(self.size):
            new_col = []
            for r in range(self.size):
                if grid[r][c] != 0:
                    new_col.append(grid[r][c])
            
            merged_col = []
            i = 0
            while i < len(new_col):
                if i + 1 < len(new_col) and new_col[i] == new_col[i+1]:
                    merged_col.append(new_col[i] * 2)
                    self.score += new_col[i] * 2
                    i += 2
                else:
                    merged_col.append(new_col[i])
                    i += 1
            
            merged_col.extend([0] * (self.size - len(merged_col)))
            
            for r in range(self.size):
                if grid[r][c] != merged_col[r]:
                    moved = True
                grid[r][c] = merged_col[r]
        return grid, moved

    def moves_left(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 0:
                    return True
                if r + 1 < self.size and self.grid[r][c] == self.grid[r+1][c]:
                    return True
                if c + 1 < self.size and self.grid[r][c] == self.grid[r][c+1]:
                    return True
        return False

    def restart(self):
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.game_over = False
        self.add_new_tile()
        self.add_new_tile()
