
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QTimer, Qt
from components.styles import STYLESHEET
from components.clock_components import CircleClock, WorldClockList
from components.stopwatch_components import StopwatchWidget
from components.alarm_components import AlarmWidget
from components.timer_components import TimerWidget

class ClockApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Clock')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(STYLESHEET)

        # 메인 위젯 및 레이아웃
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 탭 바
        tabs = QTabWidget()
        tabs.addTab(self.create_clock_tab(), "Clock")
        tabs.addTab(AlarmWidget(), "Alarm")
        tabs.addTab(StopwatchWidget(), "Stopwatch")
        tabs.addTab(TimerWidget(), "Timer")
        main_layout.addWidget(tabs)

    def create_clock_tab(self):
        clock_tab = QWidget()
        layout = QVBoxLayout(clock_tab)

        # 중앙 원형 시계
        self.circle_clock = CircleClock()
        layout.addWidget(self.circle_clock, alignment=Qt.AlignCenter)

        # 세계 시간 목록
        self.world_clock_list = WorldClockList()
        layout.addWidget(self.world_clock_list)

        # 하단 버튼
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)
        set_clock_button = QPushButton("Set Clock")
        layout.addWidget(set_clock_button, alignment=Qt.AlignCenter)

        # 타이머 설정
        timer = QTimer(self)
        timer.timeout.connect(self.update_times)
        timer.start(1000) # 1초마다 업데이트

        return clock_tab

    def update_times(self):
        self.circle_clock.update()
        self.world_clock_list.update_clocks()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClockApp()
    window.show()
    sys.exit(app.exec_())
