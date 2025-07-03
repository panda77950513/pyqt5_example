
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class SettingsMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        title_label = QLabel("설정")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Add settings options here (e.g., sound volume, key bindings)
        # For now, just a placeholder
        placeholder_label = QLabel("설정 메뉴 내용이 여기에 표시됩니다.")
        placeholder_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(placeholder_label)

        back_button = QPushButton("뒤로가기")
        back_button.setFixedSize(150, 40)
        # back_button.clicked.connect(self.parent_window.show_main_menu) # To be connected
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)
