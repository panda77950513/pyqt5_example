import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QLinearGradient
from PyQt5.QtCore import Qt, QTimer, QDateTime, QPointF, QRectF
import pytz
from datetime import datetime

class CircleClock(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(300, 300)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        side = min(self.width(), self.height())
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 320.0, side / 320.0)

        # 그라데이션 테두리
        gradient = QLinearGradient(QPointF(-150, -150), QPointF(150, 150))
        gradient.setColorAt(0.0, QColor("#FF0080"))
        gradient.setColorAt(1.0, QColor("#FF4D4D"))
        pen = QPen(gradient, 10)
        painter.setPen(pen)
        painter.drawEllipse(-145, -145, 290, 290)

        # 시간 및 날짜 텍스트
        painter.setPen(QColor(255, 255, 255))
        font = QFont('Segoe UI', 40, QFont.Bold)
        painter.setFont(font)
        current_time = QDateTime.currentDateTime().toString('hh:mm')
        painter.drawText(QRectF(-100, -50, 200, 100), Qt.AlignCenter, current_time)

        font.setPointSize(14)
        painter.setFont(font)
        current_date = QDateTime.currentDateTime().toString('dddd dd MMMM')
        painter.drawText(QRectF(-100, 20, 200, 50), Qt.AlignCenter, current_date)

class WorldClockList(QListWidget):
    def __init__(self):
        super().__init__()
        self.timezones = ['UTC', 'Asia/Tokyo', 'Australia/Queensland', 'Europe/Barcelona', 'Africa/Dakar']
        self.update_clocks()

    def update_clocks(self):
        self.clear()
        utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
        for tz_name in self.timezones:
            try:
                timezone = pytz.timezone(tz_name)
                local_time = utc_now.astimezone(timezone)
                city = tz_name.split('/')[-1].replace('_', ' ')
                time_str = local_time.strftime('%H:%M')
                item_text = f"{city}: {time_str}"
                self.addItem(QListWidgetItem(item_text))
            except pytz.UnknownTimeZoneError:
                print(f"Unknown timezone: {tz_name}")