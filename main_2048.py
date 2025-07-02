import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from assets_2048.styles import STYLESHEET
from assets_2048.game_logic import GameLogic
from assets_2048.game_board import GameBoard

class Game2048(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2048")
        self.setGeometry(200, 200, 500, 600)
        self.setObjectName("MainWindow")
        self.setStyleSheet(STYLESHEET)

        self.game_logic = GameLogic()

        # 메인 위젯 및 레이아웃
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 상단 UI (제목, 점수, 재시작 버튼)
        top_layout = QHBoxLayout()
        title = QLabel("2048")
        title.setObjectName("TitleLabel")
        self.score_label = QLabel(f"SCORE\n{self.game_logic.score}")
        self.score_label.setObjectName("ScoreLabel")
        self.score_label.setAlignment(Qt.AlignCenter)
        restart_button = QPushButton("Restart")
        restart_button.setObjectName("RestartButton")
        restart_button.clicked.connect(self.restart_game)
        top_layout.addWidget(title)
        top_layout.addStretch()
        top_layout.addWidget(self.score_label)
        top_layout.addWidget(restart_button)
        main_layout.addLayout(top_layout)

        # 게임 보드
        self.game_board = GameBoard()
        main_layout.addWidget(self.game_board)

        self.update_ui()

    def update_ui(self):
        self.game_board.update_board(self.game_logic.grid)
        self.score_label.setText(f"SCORE\n{self.game_logic.score}")
        if self.game_logic.game_over:
            self.show_game_over_message()

    def keyPressEvent(self, event):
        # 키보드 이벤트는 더 이상 사용하지 않음
        pass

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and hasattr(self, 'drag_start_pos'):
            self.drag_end_pos = event.pos()
            dx = self.drag_end_pos.x() - self.drag_start_pos.x()
            dy = self.drag_end_pos.y() - self.drag_start_pos.y()

            if abs(dx) > abs(dy): # 좌우 드래그
                if dx > 0:
                    direction = 'right'
                else:
                    direction = 'left'
            else: # 상하 드래그
                if dy > 0:
                    direction = 'down'
                else:
                    direction = 'up'
            
            # 드래그 거리가 너무 짧으면 무시
            if abs(dx) > 10 or abs(dy) > 10:
                if self.game_logic.move(direction):
                    self.update_ui()
            
            del self.drag_start_pos # 시작 위치 초기화

    def restart_game(self):
        self.game_logic.restart()
        self.update_ui()

    def show_game_over_message(self):
        msg_box = QMessageBox()
        msg_box.setText("Game Over!")
        msg_box.setInformativeText(f"Your score is {self.game_logic.score}.\nWould you like to play again?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.Yes)
        ret = msg_box.exec_()
        if ret == QMessageBox.Yes:
            self.restart_game()
        else:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game2048()
    game.show()
    sys.exit(app.exec_())