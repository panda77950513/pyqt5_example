
# main_soccer.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from soccer_assets.game_widget import GameWidget

class SoccerGameApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3v3 Soccer")
        self.game_widget = GameWidget()
        self.setCentralWidget(self.game_widget)
        self.game_widget.setFocus() # 키보드 입력을 받기 위해 포커스 설정

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = SoccerGameApp()
    game.show()
    sys.exit(app.exec_())
