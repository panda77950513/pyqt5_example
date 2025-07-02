# game_widget.py

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont, QPen
from PyQt5.QtCore import Qt, QTimer, QRectF
from .game_map import TILE_SIZE, MAP_WIDTH, MAP_HEIGHT, EMPTY, WALL, BLOCK, ROUND_DATA
from .game_logic import GameState

class GameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE + 50) # 맵 크기 + 상단 UI 공간
        self.current_round = 1
        self.game_state = None
        print("GameWidget: __init__ 호출됨")
        self.init_game()

    def init_game(self):
        print(f"GameWidget: init_game 호출됨 (라운드: {self.current_round})")
        try:
            self.game_state = GameState(ROUND_DATA[self.current_round])
            print("GameWidget: GameState 객체 생성 성공")
        except KeyError as e:
            print(f"GameWidget: ROUND_DATA[{self.current_round}] 키 오류 발생: {e}")
            print("게임 데이터를 로드할 수 없습니다. 라운드 번호를 확인하세요.")
            self.game_over = True # 게임 오버 상태로 전환하여 더 이상 진행되지 않도록 함
            return
        except Exception as e:
            print(f"GameWidget: GameState 객체 생성 중 알 수 없는 오류 발생: {e}")
            self.game_over = True
            return

        self.game_over = False
        self.game_cleared = False

        self.keys_pressed = set()

        # 타이머는 init_game에서 항상 초기화
        if not hasattr(self, 'game_timer'): # 최초 1회만 생성
            self.game_timer = QTimer(self)
            self.game_timer.timeout.connect(self.game_loop)
        self.game_timer.start(1000 // 60) # 약 60 FPS
        print("GameWidget: 게임 타이머 시작됨")

    def game_loop(self):
        if self.game_over or self.game_cleared:
            return

        # 플레이어 이동 처리
        if not self.game_state.player.is_moving:
            if Qt.Key_Left in self.keys_pressed:
                self.game_state.move_player(-1, 0)
            elif Qt.Key_Right in self.keys_pressed:
                self.game_state.move_player(1, 0)
            elif Qt.Key_Up in self.keys_pressed:
                self.game_state.move_player(0, -1)
            elif Qt.Key_Down in self.keys_pressed:
                self.game_state.move_player(0, 1)

        self.game_state.update_game_state()

        if self.game_state.game_over:
            self.game_over = True
            self.game_timer.stop()
        elif self.game_state.round_cleared:
            self.current_round += 1
            if self.current_round <= len(ROUND_DATA): # 다음 라운드가 있다면
                print(f"GameWidget: 라운드 {self.current_round} 로드 중...")
                self.init_game() # 다음 라운드 로드
            else:
                self.game_cleared = True
                self.game_timer.stop()

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # game_state가 아직 초기화되지 않았다면 검은 화면을 그리고 반환
        if self.game_state is None:
            painter.setBrush(QBrush(QColor(0, 0, 0)))
            painter.drawRect(self.rect())
            return

        # 배경
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.drawRect(self.rect())

        # 상단 정보 바
        painter.setBrush(QBrush(QColor(50, 50, 50)))
        painter.drawRect(0, 0, self.width(), 50)
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(QFont('Arial', 14))
        painter.drawText(10, 30, f"Score: {self.game_state.player.score}")
        painter.drawText(int(self.width() / 2 - 40), 30, f"Round: {self.current_round}")
        painter.drawText(self.width() - 100, 30, f"Lives: {self.game_state.player.lives}")

        # 맵 그리기 (상단 정보 바 아래부터)
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                tile_type = self.game_state.current_map[y][x]
                rect = QRectF(x * TILE_SIZE, y * TILE_SIZE + 50, TILE_SIZE, TILE_SIZE)
                if tile_type == WALL:
                    painter.setBrush(QBrush(QColor(100, 100, 200))) # 벽
                    painter.drawRect(rect)
                elif tile_type == EMPTY:
                    painter.setBrush(QBrush(QColor(0, 0, 0))) # 빈 공간
                    painter.drawRect(rect)

        # 블록 그리기
        painter.setBrush(QBrush(QColor(150, 200, 255))) # 얼음 블록
        for block in self.game_state.ice_blocks:
            pixel_x, pixel_y = block.get_pixel_pos()
            painter.drawRect(pixel_x, pixel_y + 50, TILE_SIZE, TILE_SIZE)

        # 적 그리기
        painter.setBrush(QBrush(QColor(255, 100, 100))) # 적
        for enemy in self.game_state.enemies:
            pixel_x, pixel_y = enemy.get_pixel_pos()
            painter.drawEllipse(pixel_x, pixel_y + 50, TILE_SIZE, TILE_SIZE)

        # 플레이어 그리기
        painter.setBrush(QBrush(QColor(0, 255, 0))) # 플레이어
        pixel_x, pixel_y = self.game_state.player.get_pixel_pos()
        painter.drawEllipse(pixel_x, pixel_y + 50, TILE_SIZE, TILE_SIZE)

        # 게임 오버 화면
        if self.game_over:
            painter.setBrush(QBrush(QColor(0, 0, 0, 150))) # 반투명 검은색
            painter.drawRect(0, 0, self.width(), self.height())
            painter.setPen(QPen(QColor(255, 255, 255)))
            painter.setFont(QFont('Arial', 40, QFont.Bold))
            painter.drawText(self.rect(), Qt.AlignCenter, "GAME OVER\nPress 'R' to Restart")
        
        # 게임 클리어 화면
        if self.game_cleared:
            painter.setBrush(QBrush(QColor(0, 0, 0, 150))) # 반투명 검은색
            painter.drawRect(0, 0, self.width(), self.height())
            painter.setPen(QPen(QColor(255, 255, 255)))
            painter.setFont(QFont('Arial', 40, QFont.Bold))
            painter.drawText(self.rect(), Qt.AlignCenter, "GAME CLEARED!\nPress 'R' to Play Again")

    def keyPressEvent(self, event):
        if self.game_over or self.game_cleared:
            if event.key() == Qt.Key_R:
                self.current_round = 1 # 라운드 초기화
                self.init_game()
            return
            
        self.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):
        if event.key() in self.keys_pressed:
            self.keys_pressed.remove(event.key())