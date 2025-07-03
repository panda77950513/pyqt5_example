
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, QTime

class StopwatchWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('Stopwatch.ui', self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

        self.time = QTime(0, 0, 0)
        self.is_running = False

        self.pushButton.clicked.connect(self.toggle_start_pause)
        self.pushButton_2.clicked.connect(self.reset_stopwatch)
        self.pushButton_3.clicked.connect(self.record_lap_time)

        self.setWindowTitle('Stopwatch')
        self.show()

    def toggle_start_pause(self):
        if not self.is_running:
            self.timer.start(1)  # Update every millisecond
            self.is_running = True
            self.pushButton.setText('Pause')
        else:
            self.timer.stop()
            self.is_running = False
            self.pushButton.setText('Start')

    def reset_stopwatch(self):
        self.timer.stop()
        self.is_running = False
        self.time.setHMS(0, 0, 0, 0)
        self.label.setText('00.000')
        self.pushButton.setText('Start')
        self.listWidget.clear()

    def update_time(self):
        self.time = self.time.addMSecs(1)
        self.label.setText(self.time.toString('ss.zzz'))

    def record_lap_time(self):
        if self.is_running:
            lap_time = self.label.text()
            self.listWidget.addItem(lap_time)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StopwatchWindow()
    sys.exit(app.exec_())
