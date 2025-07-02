
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTimeEdit, QListWidget, QListWidgetItem, QCheckBox
from PyQt5.QtCore import QTime, Qt

class AlarmWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 레이아웃 설정
        layout = QVBoxLayout(self)

        # 알람 설정 부분
        add_alarm_layout = QHBoxLayout()
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("hh:mm")
        self.add_button = QPushButton("Add Alarm")
        add_alarm_layout.addWidget(self.time_edit)
        add_alarm_layout.addWidget(self.add_button)
        layout.addLayout(add_alarm_layout)

        # 알람 목록
        self.alarm_list = QListWidget()
        layout.addWidget(self.alarm_list)

        # 버튼 연결
        self.add_button.clicked.connect(self.add_alarm)

    def add_alarm(self):
        time = self.time_edit.time()
        item = QListWidgetItem(self.alarm_list)
        widget = self.create_alarm_item_widget(time)
        item.setSizeHint(widget.sizeHint())
        self.alarm_list.addItem(item)
        self.alarm_list.setItemWidget(item, widget)

    def create_alarm_item_widget(self, time):
        widget = QWidget()
        layout = QHBoxLayout(widget)

        time_label = QLabel(time.toString("hh:mm"))
        font = time_label.font()
        font.setPointSize(20)
        time_label.setFont(font)

        checkbox = QCheckBox()
        checkbox.setChecked(True)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_alarm(widget))

        layout.addWidget(time_label)
        layout.addStretch()
        layout.addWidget(checkbox)
        layout.addWidget(delete_button)

        return widget

    def delete_alarm(self, widget):
        for i in range(self.alarm_list.count()):
            item = self.alarm_list.item(i)
            if self.alarm_list.itemWidget(item) == widget:
                self.alarm_list.takeItem(i)
                break
