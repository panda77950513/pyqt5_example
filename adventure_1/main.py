
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor

import pygame

from game.game_engine import GameEngine
from ui.main_menu import MainMenu

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("레바의 모험: 심연의 유산")
        self.setGeometry(100, 100, 1280, 720) # 게임 해상도에 맞게 조정

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.game_engine = None
        self.main_menu = MainMenu(self)
        self.layout.addWidget(self.main_menu)

        self.set_dark_theme()

        # PyQt5 키 코드를 Pygame 키 코드로 매핑
        self._qt_to_pygame_key_map = {
            Qt.Key_Left: pygame.K_LEFT,
            Qt.Key_Right: pygame.K_RIGHT,
            Qt.Key_Space: pygame.K_SPACE,
            Qt.Key_Z: pygame.K_z,
        }

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(70, 70, 70))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        self.setPalette(palette)

        self.setStyleSheet("""
            QPushButton {
                background-color: #4A4A4A;
                color: #FFFFFF;
                border: 1px solid #555555;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #5A5A5A;
            }
            QPushButton:pressed {
                background-color: #3A3A3A;
            }
            QLabel {
                color: #FFFFFF;
            }
        """)

    def start_game(self):
        if self.game_engine is None:
            self.game_engine = GameEngine(self.central_widget) # Pass central_widget for Pygame embedding
            self.layout.removeWidget(self.main_menu)
            self.main_menu.hide()
            self.layout.addWidget(self.game_engine.get_pygame_widget()) # Get the QWidget from GameEngine
            self.game_engine.start_game_loop()
            self.setFocus() # 게임 시작 시 메인 윈도우에 포커스 설정

    def show_main_menu(self):
        if self.game_engine:
            self.game_engine.stop_game_loop()
            self.layout.removeWidget(self.game_engine.get_pygame_widget())
            self.game_engine = None
        self.layout.addWidget(self.main_menu)
        self.main_menu.show()

    def keyPressEvent(self, event):
        if self.game_engine and self.game_engine.game_active:
            qt_key = event.key()
            print(f"MainWindow: Key Pressed - Qt Key: {qt_key}")
            if qt_key in self._qt_to_pygame_key_map:
                pygame_key = self._qt_to_pygame_key_map[qt_key]
                pygame_event = pygame.event.Event(pygame.KEYDOWN, key=pygame_key)
                self.game_engine.handle_key_event(pygame_event)
            else:
                print(f"MainWindow: Unmapped Qt Key: {qt_key}")
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if self.game_engine and self.game_engine.game_active:
            qt_key = event.key()
            print(f"MainWindow: Key Released - Qt Key: {qt_key}")
            if qt_key in self._qt_to_pygame_key_map:
                pygame_key = self._qt_to_pygame_key_map[qt_key]
                pygame_event = pygame.event.Event(pygame.KEYUP, key=pygame_key)
                self.game_engine.handle_key_event(pygame_event)
            else:
                print(f"MainWindow: Unmapped Qt Key: {qt_key}")
        super().keyReleaseEvent(event)

    def closeEvent(self, event):
        if self.game_engine:
            self.game_engine.stop_game_loop()
        pygame.quit()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
