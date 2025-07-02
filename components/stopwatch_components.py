
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget
from PyQt5.QtCore import QTimer, QTime, Qt

class StopwatchWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 레이아웃 설정
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # 시간 표시 라벨
        self.time_label = QLabel("00:00.000")
        self.time_label.setAlignment(Qt.AlignCenter)
        font = self.time_label.font()
        font.setPointSize(50)
        font.setBold(True)
        self.time_label.setFont(font)
        layout.addWidget(self.time_label)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        self.start_pause_button = QPushButton("Start")
        self.lap_button = QPushButton("Lap")
        self.reset_button = QPushButton("Reset")
        button_layout.addWidget(self.start_pause_button)
        button_layout.addWidget(self.lap_button)
        button_layout.addWidget(self.reset_button)
        layout.addLayout(button_layout)

        # 랩 타임 리스트
        self.lap_list = QListWidget()
        layout.addWidget(self.lap_list)

        # 타이머 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.stopwatch_time = QTime(0, 0, 0)
        self.is_running = False

        # 버튼 연결
        self.start_pause_button.clicked.connect(self.toggle_start_pause)
        self.reset_button.clicked.connect(self.reset_stopwatch)
        self.lap_button.clicked.connect(self.record_lap_time)
        self.lap_button.setEnabled(False)

    def toggle_start_pause(self):
        if not self.is_running:
            self.timer.start(1)
            self.is_running = True
            self.start_pause_button.setText("Pause")
            self.lap_button.setEnabled(True)
        else:
            self.timer.stop()
            self.is_running = False
            self.start_pause_button.setText("Start")

    def reset_stopwatch(self):
        self.timer.stop()
        self.is_running = False
        self.stopwatch_time.setHMS(0, 0, 0, 0)
        self.time_label.setText("00:00.000")
        self.start_pause_button.setText("Start")
        self.lap_list.clear()
        self.lap_button.setEnabled(False)

    def update_time(self):
        self.stopwatch_time = self.stopwatch_time.addMSecs(1)
        self.time_label.setText(self.stopwatch_time.toString("mm:ss.zzz"))

    def record_lap_time(self):
        if self.is_running:
            lap_time = self.time_label.text()
            self.lap_list.insertItem(0, lap_time)
