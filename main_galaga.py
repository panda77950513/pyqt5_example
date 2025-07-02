
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from galaga_assets.game_widget import GameWidget

class GalagaGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Galaga")
        self.game_widget = GameWidget()
        self.setCentralWidget(self.game_widget)
        self.game_widget.setFocus()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = GalagaGame()
    game.show()
    sys.exit(app.exec_())
