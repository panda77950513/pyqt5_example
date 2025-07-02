
# 2048 게임을 위한 스타일시트

STYLESHEET = """
QWidget#MainWindow {
    background-color: #FAF8EF;
}

QLabel#TitleLabel {
    font-size: 80px;
    font-weight: bold;
    color: #776E65;
}

QLabel#ScoreLabel {
    font-size: 18px;
    font-weight: bold;
    color: #EFEFEF;
    background-color: #BBADA0;
    padding: 15px;
    border-radius: 5px;
}

QPushButton#RestartButton {
    font-size: 18px;
    font-weight: bold;
    color: #F9F6F2;
    background-color: #8F7A66;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
}

QPushButton#RestartButton:hover {
    background-color: #9F8B77;
}

QWidget#GameBoard {
    background-color: #BBADA0;
    border-radius: 10px;
}

QLabel.Tile {
    font-size: 45px;
    font-weight: bold;
    border-radius: 5px;
}
"""

TILE_COLORS = {
    0: ("#CDC1B4", "#776E65"),
    2: ("#EEE4DA", "#776E65"),
    4: ("#EDE0C8", "#776E65"),
    8: ("#F2B179", "#F9F6F2"),
    16: ("#F59563", "#F9F6F2"),
    32: ("#F67C5F", "#F9F6F2"),
    64: ("#F65E3B", "#F9F6F2"),
    128: ("#EDCF72", "#F9F6F2"),
    256: ("#EDCC61", "#F9F6F2"),
    512: ("#EDC850", "#F9F6F2"),
    1024: ("#EDC53F", "#F9F6F2"),
    2048: ("#EDC22E", "#F9F6F2"),
}
