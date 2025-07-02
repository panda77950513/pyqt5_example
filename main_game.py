
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from game_assets.game_widget import GameWidget

class JumpGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Jump Game")
        self.setGeometry(200, 200, 400, 600)

        self.game_widget = GameWidget()
        self.setCentralWidget(self.game_widget)

        self.game_widget.setFocus()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = JumpGame()
    game.show()
    sys.exit(app.exec_())
