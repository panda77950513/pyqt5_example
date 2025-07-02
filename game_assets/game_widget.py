import random
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont, QPen
from PyQt5.QtCore import Qt, QTimer
from .game_logic import Player, Platform, MovingPlatform, Hazard, MOVE_SPEED

class GameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_game()

    def init_game(self):
        self.player = Player()
        self.platforms = []
        self.hazards = []
        self.camera_y = 0
        self.score = 0
        self.max_height = self.height()
        self.game_over = False

        self.last_platform_y = self.height() - 50
        self.generate_initial_platforms()

        self.keys_pressed = set()

        if not hasattr(self, 'timer'):
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.game_loop)
            self.timer.start(16) # 약 60 FPS

    def generate_initial_platforms(self):
        # 시작 발판
        self.platforms.append(Platform(100, self.height() - 50, 200, 20))
        # 초기 발판들 생성
        for _ in range(10):
            self.generate_new_platform()

    def generate_new_platform(self):
        x = random.randint(0, self.width() - 100)
        y = self.last_platform_y - random.randint(80, 120)
        platform_type = random.choice(['static', 'moving', 'hazard'])

        if platform_type == 'static':
            self.platforms.append(Platform(x, y, 100, 20))
        elif platform_type == 'moving':
            self.platforms.append(MovingPlatform(x, y, 100, 20))
        elif platform_type == 'hazard' and self.score > 500: # 점수가 500 이상일 때부터 장애물 등장
            self.hazards.append(Hazard(x, y + 5, 100, 10))
        
        self.last_platform_y = y

    def game_loop(self):
        if self.game_over:
            return

        # 플레이어 이동
        if Qt.Key_Left in self.keys_pressed:
            self.player.move(-MOVE_SPEED)
        if Qt.Key_Right in self.keys_pressed:
            self.player.move(MOVE_SPEED)

        # 플레이어 및 움직이는 발판 업데이트
        self.player.update(self.platforms)
        for p in self.platforms:
            if isinstance(p, MovingPlatform):
                p.update()

        # 카메라 스크롤 및 점수
        if self.player.rect.top() < self.max_height:
            self.max_height = self.player.rect.top()
            self.score = int((self.height() - self.max_height) / 10)
        
        if self.player.rect.top() < self.height() / 2:
            self.camera_y = self.player.rect.top() - self.height() / 2

        # 새로운 발판 생성
        while self.last_platform_y > self.camera_y - 50:
            self.generate_new_platform()

        # 게임 오버 조건 확인
        if self.player.rect.top() > self.camera_y + self.height():
            self.game_over = True
        
        for h in self.hazards:
            if self.player.rect.intersects(h.rect):
                self.game_over = True
                break

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(0, -self.camera_y)

        # 배경
        painter.setBrush(QBrush(QColor(210, 230, 255)))
        painter.drawRect(self.rect().translated(0, int(self.camera_y)))

        # 플레이어
        painter.setBrush(QBrush(QColor(255, 100, 100)))
        painter.drawRect(self.player.rect)

        # 발판
        painter.setBrush(QBrush(QColor(100, 200, 100)))
        for p in self.platforms:
            painter.drawRect(p.rect)

        # 장애물
        painter.setBrush(QBrush(QColor(255, 0, 0)))
        for h in self.hazards:
            painter.drawRect(h.rect)

        # 점수 표시
        painter.resetTransform() # 카메라 시점 리셋
        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.setFont(QFont('Arial', 20))
        painter.drawText(10, 30, f"Score: {self.score}")

        # 게임 오버 화면
        if self.game_over:
            painter.setBrush(QBrush(QColor(0, 0, 0, 150))) # 반투명 검은색
            painter.drawRect(self.rect())
            painter.setPen(QPen(QColor(255, 255, 255)))
            painter.setFont(QFont('Arial', 30, QFont.Bold))
            painter.drawText(self.rect(), Qt.AlignCenter, "Game Over\nPress 'R' to Restart")

    def keyPressEvent(self, event):
        if self.game_over and event.key() == Qt.Key_R:
            self.init_game()
            return
            
        self.keys_pressed.add(event.key())
        if event.key() == Qt.Key_Space:
            self.player.jump()

    def keyReleaseEvent(self, event):
        if event.key() in self.keys_pressed:
            self.keys_pressed.remove(event.key())