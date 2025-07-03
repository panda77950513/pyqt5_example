from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QColor, QPainter, QFont
from PyQt5.QtCore import Qt, QRect
import os

class ExportUtils:
    def __init__(self):
        pass

    def export_data(self, palette_data):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(None, "팔레트 내보내기", "",
                                                  "PNG 이미지 (*.png);;텍스트 파일 (*.txt)", options=options)
        if file_path:
            if file_path.endswith('.png'):
                self._export_as_image(file_path, palette_data)
            elif file_path.endswith('.txt'):
                self._export_as_text(file_path, palette_data)
            else:
                QMessageBox.warning(None, "내보내기 오류", "지원하지 않는 파일 형식입니다.")

    def _export_as_image(self, file_path, palette_data):
        try:
            # 이미지 크기 계산 (예시, 실제 팔레트 구성에 따라 조절 필요)
            # 각 색상 블록 높이 100, 너비 200, 여백 고려
            color_block_height = 100
            color_block_width = 200
            padding = 20
            text_height = 150 # 색상 정보 및 의미 텍스트를 위한 공간
            overall_sentiment_height = 100 # 종합 감성 설명을 위한 공간

            num_colors = len(palette_data['colors'])
            total_height = (color_block_height + text_height) * num_colors + overall_sentiment_height + padding * (num_colors + 2)
            total_width = color_block_width + padding * 2

            image = QImage(total_width, total_height, QImage.Format_ARGB32)
            image.fill(QColor(255, 255, 255)) # 흰색 배경

            painter = QPainter(image)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.TextAntialiasing)

            y_offset = padding

            # 종합 감성 설명 그리기
            painter.setFont(QFont("Arial", 12, QFont.Bold))
            painter.setPen(QColor(0, 0, 0)) # 검정색 펜
            overall_sentiment_rect = QRect(padding, y_offset, total_width - 2 * padding, overall_sentiment_height)
            painter.drawText(overall_sentiment_rect, Qt.AlignTop | Qt.AlignLeft | Qt.TextWordWrap, 
                             "종합 감성: " + palette_data['overall_sentiment'])
            y_offset += overall_sentiment_height + padding

            # 각 색상 블록 그리기
            for color_info in palette_data['colors']:
                color_hex = color_info['hex']
                color_rgb = color_info['rgb']
                color_meaning = color_info['meaning']

                # 색상 블록
                painter.fillRect(padding, y_offset, color_block_width, color_block_height, QColor(color_hex))
                painter.setPen(QColor(100, 100, 100)) # 테두리 색상
                painter.drawRect(padding, y_offset, color_block_width, color_block_height)

                # 텍스트 정보
                painter.setPen(QColor(0, 0, 0)) # 검정색 펜
                painter.setFont(QFont("Arial", 10))
                y_offset += color_block_height + 5
                painter.drawText(padding, y_offset, f"HEX: {color_hex}")
                y_offset += 20
                painter.drawText(padding, y_offset, f"RGB: {color_rgb}")
                y_offset += 20
                
                # 색상 의미 (줄바꿈 처리)
                meaning_rect = QRect(padding, y_offset, color_block_width, text_height - 45) # 남은 공간 활용
                painter.drawText(meaning_rect, Qt.AlignTop | Qt.AlignLeft | Qt.TextWordWrap, color_meaning)
                y_offset += text_height - 45 + padding # 다음 블록을 위한 여백

            painter.end()
            image.save(file_path)
            QMessageBox.information(None, "내보내기 성공", f"팔레트가 {os.path.basename(file_path)} (으)로 성공적으로 내보내졌습니다.")
        except Exception as e:
            QMessageBox.critical(None, "내보내기 오류", f"이미지 내보내기 중 오류가 발생했습니다: {e}")

    def _export_as_text(self, file_path, palette_data):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("--- 감성 컬러 팔레트 제안 ---\n\n")
                f.write(f"종합 감성 및 분위기: {palette_data['overall_sentiment']}\n\n")
                f.write("--- 컬러 팔레트 ---\n")
                for i, color_info in enumerate(palette_data['colors']):
                    f.write(f"\n색상 {i+1}:\n")
                    f.write(f"  HEX: {color_info['hex']}\n")
                    f.write(f"  RGB: {color_info['rgb']}\n")
                    f.write(f"  의미: {color_info['meaning']}\n")
                f.write("\n---------------------------\n")
            QMessageBox.information(None, "내보내기 성공", f"팔레트가 {os.path.basename(file_path)} (으)로 성공적으로 내보내졌습니다.")
        except Exception as e:
            QMessageBox.critical(None, "내보내기 오류", f"텍스트 내보내기 중 오류가 발생했습니다: {e}")