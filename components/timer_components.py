
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTimeEdit
from PyQt5.QtCore import QTimer, QTime, Qt

class TimerWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 레이아웃 설정
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # 시간 표시 라벨
        self.time_label = QLabel("00:00:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        font = self.time_label.font()
        font.setPointSize(50)
        font.setBold(True)
        self.time_label.setFont(font)
        layout.addWidget(self.time_label)

        # 시간 설정
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("hh:mm:ss")
        layout.addWidget(self.time_edit, alignment=Qt.AlignCenter)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        self.start_pause_button = QPushButton("Start")
        self.reset_button = QPushButton("Reset")
        button_layout.addWidget(self.start_pause_button)
        button_layout.addWidget(self.reset_button)
        layout.addLayout(button_layout)

        # 타이머 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.is_running = False

        # 버튼 연결
        self.start_pause_button.clicked.connect(self.toggle_start_pause)
        self.reset_button.clicked.connect(self.reset_timer)

    def toggle_start_pause(self):
        if not self.is_running:
            if self.time_edit.time() == QTime(0, 0, 0):
                return # 시간이 설정되지 않으면 시작하지 않음
            self.timer.start(1000)
            self.is_running = True
            self.start_pause_button.setText("Pause")
            self.time_edit.setEnabled(False)
        else:
            self.timer.stop()
            self.is_running = False
            self.start_pause_button.setText("Start")

    def reset_timer(self):
        self.timer.stop()
        self.is_running = False
        self.time_edit.setEnabled(True)
        self.time_label.setText(self.time_edit.time().toString("hh:mm:ss"))
        self.start_pause_button.setText("Start")

    def update_time(self):
        current_time = QTime.fromString(self.time_label.text(), "hh:mm:ss")
        if current_time == QTime(0, 0, 0):
            self.timer.stop()
            self.is_running = False
            self.start_pause_button.setText("Start")
            self.time_edit.setEnabled(True)
            # 여기에 알림 기능 추가 가능 (예: 소리 재생)
            return
        
        new_time = current_time.addSecs(-1)
        self.time_label.setText(new_time.toString("hh:mm:ss"))
