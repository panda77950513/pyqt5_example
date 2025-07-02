
# game_widget.py

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QFont
from PyQt5.QtCore import Qt, QTimer, QPointF
from .constants import *
from .game_logic import Game

class GameWidget(QWidget):
    def __init__(self):
        super().__init__()
        print("GameWidget: __init__ 호출됨")
        self.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        try:
            self.game = Game()
            print("GameWidget: Game 객체 생성 성공")
        except Exception as e:
            print(f"GameWidget: Game 객체 생성 중 오류 발생: {e}")
            # 오류 발생 시 게임 종료를 위해 QApplication 종료
            QApplication.instance().quit()
            return

        self.keys_pressed = {'up': False, 'down': False, 'left': False, 'right': False, 'space': False}

        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.game_loop)
        self.game_timer.start(1000 // FPS)
        print("GameWidget: 게임 타이머 시작됨")

    def game_loop(self):
        try:
            # print("GameWidget: game_loop 호출됨") # 너무 자주 출력되므로 주석 처리
            self.game.update(self.keys_pressed)
            self.update() # Redraw the widget
        except Exception as e:
            print(f"GameWidget: game_loop 중 오류 발생: {e}")
            self.game_timer.stop()
            QApplication.instance().quit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw field
        painter.setBrush(QBrush(QColor(*COLOR_FIELD)))
        painter.drawRect(FIELD_X, FIELD_Y, FIELD_WIDTH, FIELD_HEIGHT)

        # Draw field lines
        painter.setPen(QPen(QColor(*COLOR_LINE), 2))
        painter.drawRect(FIELD_X, FIELD_Y, FIELD_WIDTH, FIELD_HEIGHT) # Outer boundary
        painter.drawLine(int(SCREEN_WIDTH / 2), FIELD_Y, int(SCREEN_WIDTH / 2), FIELD_Y + FIELD_HEIGHT) # Halfway line
        painter.drawEllipse(QPointF(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 60, 60) # Center circle

        # Draw goals
        painter.setBrush(QBrush(QColor(*COLOR_GOAL)))
        painter.drawRect(FIELD_X - GOAL_WIDTH, int(FIELD_Y + FIELD_HEIGHT / 2 - GOAL_HEIGHT / 2), GOAL_WIDTH, GOAL_HEIGHT) # Left goal
        painter.drawRect(FIELD_X + FIELD_WIDTH, int(FIELD_Y + FIELD_HEIGHT / 2 - GOAL_HEIGHT / 2), GOAL_WIDTH, GOAL_HEIGHT) # Right goal

        # Draw players
        for team in [self.game.red_team, self.game.blue_team]:
            for player in team.players:
                painter.setBrush(QBrush(QColor(*player.color)))
                painter.drawEllipse(int(player.pos.x() - player.radius), int(player.pos.y() - player.radius), player.radius * 2, player.radius * 2)

        # Draw ball
        painter.setBrush(QBrush(QColor(*self.game.ball.color)))
        painter.drawEllipse(int(self.game.ball.pos.x() - self.game.ball.radius), int(self.game.ball.pos.y() - self.game.ball.radius), self.game.ball.radius * 2, self.game.ball.radius * 2)

        # Draw score
        painter.setPen(QPen(QColor(*COLOR_LINE)))
        painter.setFont(QFont('Arial', 24, QFont.Bold))
        painter.drawText(int(SCREEN_WIDTH / 2 - 50), 40, f"{self.game.score_red} - {self.game.score_blue}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left: self.keys_pressed['left'] = True
        elif event.key() == Qt.Key_Right: self.keys_pressed['right'] = True
        elif event.key() == Qt.Key_Up: self.keys_pressed['up'] = True
        elif event.key() == Qt.Key_Down: self.keys_pressed['down'] = True
        elif event.key() == Qt.Key_Space: self.keys_pressed['space'] = True

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Left: self.keys_pressed['left'] = False
        elif event.key() == Qt.Key_Right: self.keys_pressed['right'] = False
        elif event.key() == Qt.Key_Up: self.keys_pressed['up'] = False
        elif event.key() == Qt.Key_Down: self.keys_pressed['down'] = False
        elif event.key() == Qt.Key_Space: self.keys_pressed['space'] = False
