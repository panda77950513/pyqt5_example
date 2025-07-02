
STYLESHEET = """
/* 전체적인 위젯 스타일 */
QWidget {
    background-color: #2E2E2E; /* 다크 그레이 배경 */
    color: #FFFFFF; /* 흰색 텍스트 */
    font-family: 'Segoe UI', Arial, sans-serif;
}

/* 탭 위젯 스타일 */
QTabWidget::pane {
    border: 1px solid #444444;
    border-top: none;
}

QTabBar::tab {
    background-color: #2E2E2E;
    color: #B0B0B0; /* 비활성 탭 텍스트 색상 */
    padding: 10px 20px;
    border: 1px solid #444444;
    border-bottom: none;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #4A4A4A; /* 활성 탭 배경 */
    color: #FFFFFF; /* 활성 탭 텍스트 */
    border-bottom: 2px solid qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #FF0080, stop:1 #FF4D4D);
}

QTabBar::tab:hover {
    background-color: #3E3E3E;
}

/* 버튼 스타일 */
QPushButton {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #FF0080, stop:1 #FF4D4D);
    color: white;
    border: none;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    border-radius: 15px;
}

QPushButton:hover {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #FF2090, stop:1 #FF6D6D);
}

QPushButton:pressed {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #E00070, stop:1 #E03D3D);
}

/* 리스트 위젯 스타일 */
QListWidget {
    background-color: #3A3A3A;
    border: 1px solid #555555;
    border-radius: 10px;
    padding: 5px;
    font-size: 14px;
}

QListWidget::item {
    padding: 8px;
    color: #E0E0E0;
}

QListWidget::item:hover {
    background-color: #4A4A4A;
}

/* 라벨 스타일 */
QLabel {
    color: #FFFFFF;
}

/* 시간 편집 위젯 스타일 */
QTimeEdit {
    background-color: #3A3A3A;
    color: #FFFFFF;
    border: 1px solid #555555;
    padding: 5px;
    font-size: 16px;
}

/* 체크박스 스타일 */
QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 2px solid #888888;
    border-radius: 5px;
}

QCheckBox::indicator:checked {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #FF0080, stop:1 #FF4D4D);
    border: 2px solid #FF0080;
}
"""
