
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class MainMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter) # Center align widgets
        layout.setSpacing(20)

        title_label = QLabel("레바의 모험: 심연의 유산")
        title_label.setFont(QFont("Arial", 36, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        start_button = QPushButton("게임 시작")
        start_button.setFixedSize(200, 50)
        start_button.clicked.connect(self.parent_window.start_game)
        layout.addWidget(start_button, alignment=Qt.AlignCenter)

        settings_button = QPushButton("설정")
        settings_button.setFixedSize(200, 50)
        # settings_button.clicked.connect(self.show_settings) # To be implemented
        layout.addWidget(settings_button, alignment=Qt.AlignCenter)

        exit_button = QPushButton("게임 종료")
        exit_button.setFixedSize(200, 50)
        exit_button.clicked.connect(self.parent_window.close)
        layout.addWidget(exit_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)
