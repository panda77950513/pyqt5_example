
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from .styles import TILE_COLORS

class GameBoard(QWidget):
    def __init__(self, size=4):
        super().__init__()
        self.setObjectName("GameBoard")
        self.size = size
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(15)
        self.tiles = [[QLabel() for _ in range(size)] for _ in range(size)]
        self.init_board()

    def init_board(self):
        for r in range(self.size):
            for c in range(self.size):
                tile = self.tiles[r][c]
                tile.setObjectName("Tile")
                tile.setAlignment(Qt.AlignCenter)
                self.grid_layout.addWidget(tile, r, c)

    def update_board(self, grid):
        for r in range(self.size):
            for c in range(self.size):
                value = grid[r][c]
                tile = self.tiles[r][c]
                bg_color, text_color = TILE_COLORS.get(value, TILE_COLORS[2048])
                tile.setText(str(value) if value != 0 else "")
                tile.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
