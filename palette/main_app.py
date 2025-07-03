
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QFrame, QScrollArea
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtCore import Qt

from color_generator import ColorGenerator
from export_utils import ExportUtils
from styles import get_app_palette, get_stylesheet

class ColorPaletteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.color_generator = ColorGenerator()
        self.export_utils = ExportUtils()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("감성 컬러 팔레트 제안 도구")
        self.setGeometry(100, 100, 1000, 700) # 초기 창 크기 조정

        # 애플리케이션 팔레트 및 스타일시트 적용
        self.setPalette(get_app_palette())
        self.setStyleSheet(get_stylesheet())

        # 메인 레이아웃
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # 좌측 컨트롤 패널
        control_panel_layout = QVBoxLayout()
        control_panel_layout.setContentsMargins(20, 20, 20, 20)
        control_panel_layout.setSpacing(15)

        # 제목
        title_label = QLabel("감성 컬러 팔레트 생성기")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        control_panel_layout.addWidget(title_label)

        # 설명
        desc_label = QLabel("원하는 감성 키워드나 설명을 입력하세요.")
        desc_label.setFont(QFont("Arial", 10))
        control_panel_layout.addWidget(desc_label)

        # 텍스트 입력 필드
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("예: 차분함, 열정적, 여름날 해변의 시원하고 활기찬 느낌...")
        self.text_input.setFixedHeight(100)
        control_panel_layout.addWidget(self.text_input)

        # 팔레트 생성 버튼
        generate_button = QPushButton("팔레트 생성")
        generate_button.clicked.connect(self.generate_palette)
        control_panel_layout.addWidget(generate_button)

        # 내보내기 버튼
        export_button = QPushButton("팔레트 내보내기")
        export_button.clicked.connect(self.export_palette)
        control_panel_layout.addWidget(export_button)

        control_panel_layout.addStretch(1)

        main_layout.addLayout(control_panel_layout, 1) # 좌측 패널이 1/3 공간 차지

        # 우측 결과 표시 영역
        result_panel_layout = QVBoxLayout()
        result_panel_layout.setContentsMargins(20, 20, 20, 20)
        result_panel_layout.setSpacing(15)

        # 팔레트 시각화 영역
        palette_display_label = QLabel("생성된 컬러 팔레트")
        palette_display_label.setFont(QFont("Arial", 14, QFont.Bold))
        result_panel_layout.addWidget(palette_display_label)

        self.palette_frames_layout = QVBoxLayout() # 각 색상 프레임을 담을 레이아웃
        self.palette_scroll_area = QScrollArea()
        self.palette_scroll_area.setWidgetResizable(True)
        self.palette_scroll_area_content = QWidget()
        self.palette_scroll_area_content.setLayout(self.palette_frames_layout)
        self.palette_scroll_area.setWidget(self.palette_scroll_area_content)
        result_panel_layout.addWidget(self.palette_scroll_area, 3) # 팔레트 시각화 영역이 더 많은 공간 차지

        # 종합 감성 설명 영역
        overall_sentiment_label = QLabel("종합 감성 및 분위기")
        overall_sentiment_label.setFont(QFont("Arial", 14, QFont.Bold))
        result_panel_layout.addWidget(overall_sentiment_label)

        self.overall_sentiment_text = QTextEdit()
        self.overall_sentiment_text.setReadOnly(True)
        self.overall_sentiment_text.setFixedHeight(100)
        result_panel_layout.addWidget(self.overall_sentiment_text)

        main_layout.addLayout(result_panel_layout, 2) # 우측 패널이 2/3 공간 차지

    def generate_palette(self):
        keyword = self.text_input.toPlainText()
        if not keyword:
            self.overall_sentiment_text.setText("키워드를 입력해주세요.")
            return

        # 기존 팔레트 프레임 제거
        for i in reversed(range(self.palette_frames_layout.count())):
            widget = self.palette_frames_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # 컬러 팔레트 생성
        palette_data = self.color_generator.generate_palette(keyword)

        if not palette_data:
            self.overall_sentiment_text.setText("해당 키워드에 대한 팔레트를 찾을 수 없습니다. 다른 키워드를 시도해보세요.")
            return

        # 각 색상 시각화 및 설명 추가
        for color_info in palette_data['colors']:
            color_hex = color_info['hex']
            color_rgb = color_info['rgb']
            color_meaning = color_info['meaning']

            color_frame = QFrame()
            color_frame.setFrameShape(QFrame.Box)
            color_frame.setFrameShadow(QFrame.Raised)
            color_frame.setLineWidth(1)
            color_frame.setStyleSheet(f"background-color: {color_hex}; border: 1px solid #555;")
            color_frame.setFixedHeight(120)

            frame_layout = QVBoxLayout()
            color_frame.setLayout(frame_layout)

            hex_label = QLabel(f"HEX: {color_hex}")
            rgb_label = QLabel(f"RGB: {color_rgb}")
            meaning_label = QLabel(color_meaning)
            meaning_label.setWordWrap(True)

            hex_label.setStyleSheet("color: white; background: rgba(0,0,0,0.5); padding: 2px;")
            rgb_label.setStyleSheet("color: white; background: rgba(0,0,0,0.5); padding: 2px;")
            meaning_label.setStyleSheet("color: white; background: rgba(0,0,0,0.5); padding: 2px;")

            frame_layout.addWidget(hex_label)
            frame_layout.addWidget(rgb_label)
            frame_layout.addWidget(meaning_label)
            frame_layout.addStretch(1)

            self.palette_frames_layout.addWidget(color_frame)

        # 종합 감성 설명 업데이트
        self.overall_sentiment_text.setText(palette_data['overall_sentiment'])

    def export_palette(self):
        keyword = self.text_input.toPlainText()
        if not keyword:
            self.overall_sentiment_text.setText("먼저 팔레트를 생성해주세요.")
            return

        # 현재 표시된 팔레트 정보를 가져와서 내보내기 유틸리티에 전달
        # 이 부분은 실제 팔레트 데이터 구조에 따라 조정 필요
        # 예시: self.color_generator.get_last_generated_palette()
        # 지금은 간단히 텍스트 필드에서 키워드를 가져와서 다시 생성하는 방식으로 처리
        palette_data = self.color_generator.generate_palette(keyword) # 다시 생성 (비효율적, 개선 필요)

        if palette_data:
            self.export_utils.export_data(palette_data)
        else:
            self.overall_sentiment_text.setText("내보낼 팔레트 데이터가 없습니다.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Emotional Color Palette Proposer")
    app.setApplicationVersion("1.0.0")

    ex = ColorPaletteApp()
    ex.show()
    sys.exit(app.exec_())
