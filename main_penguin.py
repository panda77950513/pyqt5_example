
# main_penguin.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from penguin_assets.game_widget import GameWidget

class PenguinBrothersGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Penguin Brothers")
        self.game_widget = GameWidget()
        self.setCentralWidget(self.game_widget)
        self.game_widget.setFocus() # 키보드 입력을 받기 위해 포커스 설정

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = PenguinBrothersGame()
    game.show()
    sys.exit(app.exec_())
