

import sys
import markdown
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPlainTextEdit, QMessageBox, 
                             QFileDialog, QAction, QStatusBar, QLabel, QColorDialog, 
                             QInputDialog, QStackedWidget, QWidget, QToolBar, QFontDialog, 
                             QActionGroup, QStyle, QHBoxLayout, QTextBrowser)
from PyQt5.QtGui import QFont, QPainter, QPixmap, QPen, QImage, QIcon, QColor, QTextCursor
from PyQt5.QtCore import Qt, QPoint, QFileInfo, QSettings, pyqtSignal, QRect, QSize

# 줄 번호 표시 위젯
class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.editor.blockCountChanged.connect(self.update_width)
        self.editor.updateRequest.connect(self.update_area)
        self.editor.verticalScrollBar().valueChanged.connect(self.update_area)
        self.update_width()

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.editor.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def sizeHint(self):
        return QSize(self.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), Qt.lightGray)
        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top())
        bottom = top + int(self.editor.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.width(), self.fontMetrics().height(),
                                 Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + int(self.editor.blockBoundingRect(block).height())
            block_number += 1

    def update_width(self):
        self.editor.setViewportMargins(self.sizeHint().width(), 0, 0, 0)

    def update_area(self, rect, dy):
        if dy:
            self.scroll(0, dy)
        else:
            self.update(0, rect.y(), self.width(), rect.height())
        if rect.contains(self.rect()):
            self.update_width()

# 그림판 위젯
class DrawingCanvas(QWidget):
    modified = pyqtSignal()
    text_tool_clicked = pyqtSignal(QPoint)
    layer_changed = pyqtSignal() # 레이어 변경 시 시그널 발생

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StaticContents)
        self.layers = [] # QPixmap 객체 리스트
        self.active_layer_index = -1
        self.drawing, self.start_point, self.end_point = False, QPoint(), QPoint()
        self.tool, self.pen_color, self.pen_width = 'pen', QColor(Qt.black), 2
        self.fill_shapes = False
        
        self.add_layer() # 초기 레이어 추가

    def paintEvent(self, event):
        painter = QPainter(self)
        # 모든 보이는 레이어를 합쳐서 그림
        for layer_data in self.layers:
            if layer_data['visible']:
                painter.drawPixmap(self.rect(), layer_data['pixmap'])

        # 도형을 그리는 동안 임시로 화면에 표시
        if self.drawing and self.tool in ['line', 'rectangle', 'ellipse']:
            temp_painter = QPainter(self)
            temp_painter.setPen(QPen(self.pen_color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            if self.fill_shapes: temp_painter.setBrush(self.pen_color)
            rect = QRect(self.start_point, self.end_point).normalized()
            if self.tool == 'line': temp_painter.drawLine(self.start_point, self.end_point)
            elif self.tool == 'rectangle': temp_painter.drawRect(rect)
            elif self.tool == 'ellipse': temp_painter.drawEllipse(rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.tool == 'text':
                self.text_tool_clicked.emit(event.pos())
            else:
                self.start_point, self.end_point, self.drawing = event.pos(), event.pos(), True

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.drawing:
            self.end_point = event.pos()
            if self.tool in ['pen', 'eraser']:
                self.draw_line_to(self.end_point)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.drawing = False
            if self.tool in ['line', 'rectangle', 'ellipse']:
                self.draw_shape()
            self.modified.emit()
            self.update()

    def draw_line_to(self, end_point):
        if self.active_layer_index == -1: return
        painter = QPainter(self.layers[self.active_layer_index]['pixmap'])
        color = Qt.white if self.tool == 'eraser' else self.pen_color
        painter.setPen(QPen(color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(self.start_point, end_point)
        self.start_point = end_point

    def draw_shape(self):
        if self.active_layer_index == -1: return
        painter = QPainter(self.layers[self.active_layer_index]['pixmap'])
        painter.setPen(QPen(self.pen_color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        if self.fill_shapes: painter.setBrush(self.pen_color)
        rect = QRect(self.start_point, self.end_point).normalized()
        if self.tool == 'line': painter.drawLine(self.start_point, self.end_point)
        elif self.tool == 'rectangle': painter.drawRect(rect)
        elif self.tool == 'ellipse': painter.drawEllipse(rect)

    def draw_text(self, text, font, pos):
        if self.active_layer_index == -1: return
        painter = QPainter(self.layers[self.active_layer_index]['pixmap'])
        painter.setPen(self.pen_color)
        painter.setFont(font)
        painter.drawText(pos, text)
        self.modified.emit()
        self.update()

    def resizeEvent(self, event):
        new_width = self.width()
        new_height = self.height()
        
        for layer_data in self.layers:
            old_pixmap = layer_data['pixmap']
            if new_width > old_pixmap.width() or new_height > old_pixmap.height():
                new_pixmap = QPixmap(new_width, new_height)
                new_pixmap.fill(Qt.transparent) # 투명 배경으로 채움
                QPainter(new_pixmap).drawPixmap(0, 0, old_pixmap)
                layer_data['pixmap'] = new_pixmap
        super().resizeEvent(event)

    def clear_canvas(self): 
        # 현재 활성화된 레이어만 지우기
        if self.active_layer_index != -1:
            self.layers[self.active_layer_index]['pixmap'].fill(Qt.transparent)
            self.update()
            self.modified.emit()

    def clear_all_layers(self):
        # 모든 레이어 지우기 (새 파일, 모드 전환 시 사용)
        for layer_data in self.layers:
            layer_data['pixmap'].fill(Qt.transparent)
        self.update()
        self.modified.emit()

    def add_layer(self):
        # 레이어 추가 시 위젯의 현재 크기 또는 기본 크기 사용
        layer_size = self.size() if self.size().isValid() else QSize(800, 600)
        new_pixmap = QPixmap(layer_size)
        new_pixmap.fill(Qt.transparent) # 새 레이어는 투명하게 시작
        self.layers.append({'name': f'Layer {len(self.layers) + 1}', 'pixmap': new_pixmap, 'visible': True})
        self.active_layer_index = len(self.layers) - 1
        self.layer_changed.emit()
        self.modified.emit()
        self.update()

    def remove_layer(self, index):
        if len(self.layers) > 1 and 0 <= index < len(self.layers):
            del self.layers[index]
            if self.active_layer_index >= len(self.layers): # 활성 레이어가 삭제된 경우
                self.active_layer_index = len(self.layers) - 1
            self.layer_changed.emit()
            self.modified.emit()
            self.update()

    def set_active_layer(self, index):
        if 0 <= index < len(self.layers):
            self.active_layer_index = index
            self.layer_changed.emit()
            self.update()

    def toggle_layer_visibility(self, index):
        if 0 <= index < len(self.layers):
            self.layers[index]['visible'] = not self.layers[index]['visible']
            self.layer_changed.emit()
            self.update()

    def move_layer(self, from_index, to_index):
        if 0 <= from_index < len(self.layers) and 0 <= to_index < len(self.layers):
            layer = self.layers.pop(from_index)
            self.layers.insert(to_index, layer)
            if self.active_layer_index == from_index: # 활성 레이어 인덱스 업데이트
                self.active_layer_index = to_index
            elif from_index < self.active_layer_index <= to_index: # 다른 레이어 이동 시 활성 레이어 인덱스 조정
                self.active_layer_index -= 1
            elif to_index <= self.active_layer_index < from_index:
                self.active_layer_index += 1
            self.layer_changed.emit()
            self.modified.emit()
            self.update()

    def get_merged_pixmap(self):
        if not self.layers: return QPixmap(self.size() if self.size().isValid() else QSize(800, 600))
        merged_pixmap = QPixmap(self.layers[0]['pixmap'].size())
        merged_pixmap.fill(Qt.white) # 최종 이미지는 흰색 배경
        painter = QPainter(merged_pixmap)
        for layer_data in self.layers:
            if layer_data['visible']:
                painter.drawPixmap(0, 0, layer_data['pixmap'])
        return merged_pixmap

    def set_pixmap(self, pixmap):
        # 기존 레이어들을 모두 지우고 새 이미지로 단일 레이어 생성
        self.layers = []
        new_pixmap = QPixmap(pixmap.size())
        new_pixmap.fill(Qt.transparent)
        QPainter(new_pixmap).drawPixmap(0, 0, pixmap)
        self.layers.append({'name': 'Layer 1', 'pixmap': new_pixmap, 'visible': True})
        self.active_layer_index = 0
        self.layer_changed.emit()
        self.modified.emit()
        self.update()

    def set_pen_color(self, color): self.pen_color = color
    def set_pen_width(self, width): self.pen_width = width
    def set_tool(self, tool): self.tool = tool
    def set_fill_shapes(self, fill): self.fill_shapes = fill

class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("MySoft", "NotepadPlusPaint")
        self.current_file, self.current_mode = '', 'text'
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)

        # 중앙 위젯 설정 (StackedWidget)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 텍스트 에디터 컨테이너 (줄 번호 포함)
        self.text_editor_container = QWidget()
        self.text_editor_layout = QHBoxLayout(self.text_editor_container)
        self.text_editor_layout.setContentsMargins(0, 0, 0, 0)
        self.editor = QPlainTextEdit()
        self.editor.setFont(QFont('Arial', 12))
        self.line_number_area = LineNumberArea(self.editor)
        self.text_editor_layout.addWidget(self.line_number_area)
        self.text_editor_layout.addWidget(self.editor)

        # 마크다운 미리보기 위젯
        self.markdown_preview = QTextBrowser()
        self.markdown_preview.setOpenExternalLinks(True)

        # 텍스트 에디터와 마크다운 미리보기를 담을 레이아웃
        self.text_mode_layout_widget = QWidget()
        self.text_mode_layout = QHBoxLayout(self.text_mode_layout_widget)
        self.text_mode_layout.setContentsMargins(0,0,0,0)
        self.text_mode_layout.addWidget(self.text_editor_container)
        self.text_mode_layout.addWidget(self.markdown_preview)
        self.markdown_preview.hide() # 초기에는 숨김

        # 그림판 캔버스
        self.canvas = DrawingCanvas()

        # StackedWidget에 위젯 추가
        self.stacked_widget.addWidget(self.text_mode_layout_widget)
        self.stacked_widget.addWidget(self.canvas)

        self._create_actions()
        self._create_menus()
        self._create_toolbar()
        self._create_status_bar()
        self._connect_signals()
        
        self.load_settings()
        self.new_file(is_initial_start=True)

    def _create_actions(self):
        style = self.style()
        # File actions
        self.new_action = QAction(style.standardIcon(QStyle.SP_FileIcon), '새 파일', self)
        self.open_action = QAction(style.standardIcon(QStyle.SP_DirOpenIcon), '열기', self)
        self.save_action = QAction(style.standardIcon(QStyle.SP_DialogSaveButton), '저장', self)
        self.save_as_action = QAction('다른 이름으로 저장', self)
        self.exit_action = QAction('끝내기', self)
        # Edit actions
        self.undo_action = QAction(style.standardIcon(QStyle.SP_ArrowBack), '실행 취소', self)
        self.redo_action = QAction(style.standardIcon(QStyle.SP_ArrowForward), '다시 실행', self)
        self.cut_action = QAction('잘라내기', self)
        self.copy_action = QAction('복사', self)
        self.paste_action = QAction('붙여넣기', self)
        self.find_action = QAction('찾기', self)
        self.replace_action = QAction('바꾸기', self)
        self.go_to_line_action = QAction('줄 이동...', self)
        # Format actions
        self.font_action = QAction('글꼴', self)
        # Draw tool actions
        self.pen_action = QAction('펜', self, checkable=True); self.pen_action.setData('pen')
        self.eraser_action = QAction('지우개', self, checkable=True); self.eraser_action.setData('eraser')
        self.line_action = QAction('직선', self, checkable=True); self.line_action.setData('line')
        self.rect_action = QAction('사각형', self, checkable=True); self.rect_action.setData('rectangle')
        self.ellipse_action = QAction('원', self, checkable=True); self.ellipse_action.setData('ellipse')
        self.text_tool_action = QAction('텍스트', self, checkable=True); self.text_tool_action.setData('text')
        # Draw config actions
        self.pen_color_action = QAction('펜 색상', self)
        self.pen_width_action = QAction('펜 굵기', self)
        self.clear_canvas_action = QAction('캔버스 지우기', self)
        self.fill_shapes_action = QAction('도형 채우기', self, checkable=True)
        # Mode actions
        self.text_mode_action = QAction('텍스트 모드', self, checkable=True); self.text_mode_action.setData('text')
        self.draw_mode_action = QAction('그림판 모드', self, checkable=True); self.draw_mode_action.setData('draw')
        # View actions
        self.markdown_preview_action = QAction('마크다운 미리보기', self, checkable=True)
        # Layer actions
        self.add_layer_action = QAction('새 레이어', self)
        self.remove_layer_action = QAction('레이어 삭제', self)
        self.move_layer_up_action = QAction('레이어 위로', self)
        self.move_layer_down_action = QAction('레이어 아래로', self)
        self.toggle_layer_visibility_action = QAction('레이어 숨기기/보이기', self)

    def _create_menus(self):
        menu_bar = self.menuBar()
        # File menu
        file_menu = menu_bar.addMenu('파일')
        file_menu.addActions([self.new_action, self.open_action, self.save_action, self.save_as_action])
        file_menu.addSeparator()
        self.recent_files_menu = file_menu.addMenu("최근에 연 파일")
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)
        # Edit menu
        self.edit_menu = menu_bar.addMenu('편집')
        self.edit_menu.addActions([self.undo_action, self.redo_action, self.cut_action, self.copy_action, self.paste_action])
        self.edit_menu.addSeparator()
        self.edit_menu.addActions([self.find_action, self.replace_action, self.go_to_line_action])
        # Format menu
        self.format_menu = menu_bar.addMenu('서식')
        self.format_menu.addAction(self.font_action)
        # Draw menu
        self.draw_menu = menu_bar.addMenu('그리기')
        self.draw_tool_group = QActionGroup(self); self.draw_tool_group.setExclusive(True)
        for action in [self.pen_action, self.eraser_action, self.line_action, self.rect_action, self.ellipse_action, self.text_tool_action]:
            self.draw_tool_group.addAction(action)
        self.draw_menu.addActions(self.draw_tool_group.actions())
        self.draw_menu.addSeparator()
        self.draw_menu.addActions([self.pen_color_action, self.pen_width_action, self.clear_canvas_action, self.fill_shapes_action])
        # Mode menu
        mode_menu = menu_bar.addMenu('모드')
        self.mode_group = QActionGroup(self); self.mode_group.setExclusive(True)
        for action in [self.text_mode_action, self.draw_mode_action]:
            self.mode_group.addAction(action)
            mode_menu.addAction(action)
        # View menu
        view_menu = menu_bar.addMenu('보기')
        view_menu.addAction(self.markdown_preview_action)
        # Layer menu
        self.layer_menu = menu_bar.addMenu('레이어')
        self.layer_menu.addAction(self.add_layer_action)
        self.layer_menu.addAction(self.remove_layer_action)
        self.layer_menu.addSeparator()
        self.layer_menu.addAction(self.move_layer_up_action)
        self.layer_menu.addAction(self.move_layer_down_action)
        self.layer_menu.addSeparator()
        self.layer_select_menu = self.layer_menu.addMenu('레이어 선택')

    def _create_toolbar(self):
        toolbar = QToolBar("Main Toolbar"); self.addToolBar(toolbar)
        toolbar.addActions([self.new_action, self.open_action, self.save_action])
        toolbar.addSeparator()
        toolbar.addActions([self.undo_action, self.redo_action])

    def _create_status_bar(self):
        self.status_bar = QStatusBar(); self.setStatusBar(self.status_bar)
        self.main_status_label = QLabel(""); self.tool_status_label = QLabel("")
        self.status_bar.addPermanentWidget(self.main_status_label); self.status_bar.addPermanentWidget(self.tool_status_label)

    def _connect_signals(self):
        # File
        self.new_action.triggered.connect(self.new_file)
        self.open_action.triggered.connect(self.open_file)
        self.save_action.triggered.connect(self.save_file)
        self.save_as_action.triggered.connect(self.save_as_file)
        self.exit_action.triggered.connect(self.close)
        # Edit
        self.undo_action.triggered.connect(self.editor.undo); self.redo_action.triggered.connect(self.editor.redo)
        self.cut_action.triggered.connect(self.editor.cut); self.copy_action.triggered.connect(self.editor.copy); self.paste_action.triggered.connect(self.editor.paste)
        self.find_action.triggered.connect(self.find_text); self.replace_action.triggered.connect(self.replace_text)
        self.go_to_line_action.triggered.connect(self.go_to_line)
        # Format
        self.font_action.triggered.connect(self.change_font)
        # Draw
        self.draw_tool_group.triggered.connect(self.handle_tool_change)
        self.pen_color_action.triggered.connect(self.change_pen_color)
        self.pen_width_action.triggered.connect(self.change_pen_width)
        self.clear_canvas_action.triggered.connect(self.canvas.clear_canvas)
        self.fill_shapes_action.toggled.connect(self.canvas.set_fill_shapes)
        # Mode
        self.mode_group.triggered.connect(self.handle_mode_change)
        # View
        self.markdown_preview_action.toggled.connect(self.toggle_markdown_preview)
        # Layer
        self.add_layer_action.triggered.connect(self.canvas.add_layer)
        self.remove_layer_action.triggered.connect(lambda: self.canvas.remove_layer(self.canvas.active_layer_index))
        self.move_layer_up_action.triggered.connect(lambda: self.canvas.move_layer(self.canvas.active_layer_index, max(0, self.canvas.active_layer_index - 1)))
        self.move_layer_down_action.triggered.connect(lambda: self.canvas.move_layer(self.canvas.active_layer_index, min(len(self.canvas.layers) - 1, self.canvas.active_layer_index + 1)))
        # Widgets
        self.editor.textChanged.connect(lambda: self.setWindowModified(True))
        self.editor.textChanged.connect(self.update_status_bar) # 텍스트 변경 시 단어 수 업데이트
        self.editor.textChanged.connect(self.update_markdown_preview) # 마크다운 미리보기 업데이트
        self.editor.cursorPositionChanged.connect(self.update_status_bar)
        self.canvas.modified.connect(lambda: self.setWindowModified(True))
        self.canvas.text_tool_clicked.connect(self.handle_text_tool_click)
        self.canvas.layer_changed.connect(self.update_layer_menu)
        self.canvas.layer_changed.connect(self.update_status_bar)

    def handle_mode_change(self, action):
        new_mode = action.data()
        if self.current_mode == new_mode: return

        if not self.maybe_save():
            # User cancelled, revert the UI to the current mode's button
            if self.current_mode == 'text': self.text_mode_action.setChecked(True)
            else: self.draw_mode_action.setChecked(True)
            return

        self.current_mode = new_mode
        is_text_mode = (new_mode == 'text')
        self.stacked_widget.setCurrentWidget(self.text_mode_layout_widget if is_text_mode else self.canvas)
        self.edit_menu.setEnabled(is_text_mode)
        self.format_menu.setEnabled(is_text_mode)
        self.draw_menu.setEnabled(not is_text_mode)
        self.markdown_preview_action.setEnabled(is_text_mode)
        self.layer_menu.setEnabled(not is_text_mode) # 레이어 메뉴 활성화/비활성화
        if not is_text_mode: self.markdown_preview.hide() # 그림판 모드에서는 미리보기 숨김
        self.new_file(is_initial_start=True)

    def handle_tool_change(self, action):
        self.canvas.set_tool(action.data())
        self.update_status_bar()

    def handle_text_tool_click(self, pos):
        text, ok = QInputDialog.getText(self, '텍스트 입력', '캔버스에 그릴 텍스트를 입력하세요:')
        if not ok or not text: return

        font, ok = QFontDialog.getFont(self.editor.font(), self)
        if not ok: return

        self.canvas.draw_text(text, font, pos)
        self.setWindowModified(True)

    def toggle_markdown_preview(self, checked):
        if checked:
            self.markdown_preview.show()
            self.update_markdown_preview()
        else:
            self.markdown_preview.hide()

    def update_markdown_preview(self):
        if self.markdown_preview_action.isChecked() and self.current_mode == 'text':
            md_text = self.editor.toPlainText()
            html_text = markdown.markdown(md_text)
            self.markdown_preview.setHtml(html_text)

    def update_status_bar(self):
        if self.current_mode == 'text':
            cursor = self.editor.textCursor()
            line = cursor.blockNumber() + 1
            col = cursor.columnNumber() + 1
            word_count = len(self.editor.toPlainText().split())
            self.main_status_label.setText(f"Line: {line}  Col: {col}  Words: {word_count}")
            self.tool_status_label.setText("텍스트 모드")
        else:
            self.main_status_label.setText(f"Pen: {self.canvas.pen_color.name()}, {self.canvas.pen_width}px")
            fill_status = "채우기" if self.canvas.fill_shapes else "외곽선"
            layer_name = self.canvas.layers[self.canvas.active_layer_index]['name'] if self.canvas.active_layer_index != -1 else "N/A"
            layer_visibility = "보임" if self.canvas.layers[self.canvas.active_layer_index]['visible'] else "숨김"
            self.tool_status_label.setText(f"도구: {self.canvas.tool.capitalize()} ({fill_status}) | 레이어: {layer_name} ({layer_visibility})")

    def update_layer_menu(self):
        self.layer_select_menu.clear()
        for i, layer_data in enumerate(self.canvas.layers):
            action = QAction(f"{layer_data['name']} {'(활성)' if i == self.canvas.active_layer_index else ''} {'(숨김)' if not layer_data['visible'] else ''}", self)
            action.triggered.connect(lambda checked, index=i: self.canvas.set_active_layer(index))
            self.layer_select_menu.addAction(action)

            # 레이어 숨기기/보이기 액션 업데이트
            if i == self.canvas.active_layer_index:
                self.toggle_layer_visibility_action.setText(f"레이어 {'숨기기' if layer_data['visible'] else '보이기'}")
                # 기존 연결 해제 후 새 연결 (중복 연결 방지)
                try: self.toggle_layer_visibility_action.triggered.disconnect() 
                except TypeError: pass # 이미 연결 해제된 경우 무시
                self.toggle_layer_visibility_action.triggered.connect(lambda: self.canvas.toggle_layer_visibility(self.canvas.active_layer_index))

    def new_file(self, is_initial_start=False):
        if not is_initial_start and not self.maybe_save(): return
        if self.current_mode == 'text':
            self.editor.clear(); self.setWindowTitle("간단 메모장 - untitled.txt[*]")
        else:
            self.canvas.layers = [] # 모든 레이어 초기화
            self.canvas.add_layer() # 새 레이어 추가
            self.setWindowTitle("간단 메모장 - untitled.png[*]")
        self.current_file = ''; self.setWindowModified(False); self.update_status_bar()

    def open_file(self):
        if not self.maybe_save(): return
        fname, _ = QFileDialog.getOpenFileName(self, '파일 열기', '', "모든 지원 파일 (*.txt *.png *.jpg);;텍스트 (*.txt);;이미지 (*.png *.jpg)")
        if fname: self.load_file(fname)

    def load_file(self, fname):
        ext = QFileInfo(fname).suffix().lower()
        target_mode = 'text' if ext == 'txt' else 'draw' if ext in ['png', 'jpg', 'jpeg', 'bmp'] else None
        if target_mode is None: QMessageBox.warning(self, '경고', '지원하지 않는 파일 형식입니다.'); return
        
        # 모드 전환 (maybe_save를 건너뛰기 위해 직접 설정)
        self.current_mode = target_mode
        is_text_mode = (target_mode == 'text')
        self.stacked_widget.setCurrentWidget(self.text_mode_layout_widget if is_text_mode else self.canvas)
        (self.text_mode_action if is_text_mode else self.draw_mode_action).setChecked(True)
        self.edit_menu.setEnabled(is_text_mode); self.format_menu.setEnabled(is_text_mode)
        self.draw_menu.setEnabled(not is_text_mode)
        self.markdown_preview_action.setEnabled(is_text_mode)
        self.layer_menu.setEnabled(not is_text_mode) # 레이어 메뉴 활성화/비활성화
        if not is_text_mode: self.markdown_preview.hide()

        if target_mode == 'text':
            try:
                with open(fname, 'r', encoding='utf-8') as f: self.editor.setPlainText(f.read())
            except Exception as e: QMessageBox.critical(self, '오류', f'파일 열기 실패: {e}'); return
            self.update_markdown_preview()
        else:
            pixmap = QPixmap(fname)
            if pixmap.isNull(): QMessageBox.critical(self, '오류', '이미지 열기 실패'); return
            self.canvas.set_pixmap(pixmap) # 이미지를 새 레이어로 로드

        self.current_file = fname; self.setWindowModified(False)
        self.setWindowTitle(f"간단 메모장 - {QFileInfo(fname).fileName()}[*]")
        self.add_recent_file(fname)

    def save_file(self):
        if not self.current_file or not QFileInfo(self.current_file).exists(): return self.save_as_file()
        try:
            if self.current_mode == 'text':
                with open(self.current_file, 'w', encoding='utf-8') as f: f.write(self.editor.toPlainText())
            else:
                # 모든 보이는 레이어를 병합하여 저장
                self.canvas.get_merged_pixmap().save(self.current_file)
            self.setWindowModified(False)
            self.status_bar.showMessage(f'파일 저장됨: {self.current_file}', 3000)
            self.add_recent_file(self.current_file)
            return True
        except Exception as e: QMessageBox.critical(self, '오류', f'파일 저장 실패: {e}'); return False

    def save_as_file(self):
        filter = "텍스트 파일 (*.txt)" if self.current_mode == 'text' else "PNG 이미지 (*.png);;JPEG 이미지 (*.jpg)"
        fname, _ = QFileDialog.getSaveFileName(self, '다른 이름으로 저장', self.current_file or '', filter)
        if fname: self.current_file = fname; return self.save_file()
        return False

    def maybe_save(self):
        if not self.isWindowModified(): return True
        ret = QMessageBox.warning(self, "간단 메모장", "변경 내용을 저장하시겠습니까?", QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        if ret == QMessageBox.Save: return self.save_file()
        if ret == QMessageBox.Cancel: return False
        return True

    def change_pen_color(self): 
        color = QColorDialog.getColor(self.canvas.pen_color); 
        if color.isValid(): self.canvas.set_pen_color(color); self.update_status_bar()
    def change_pen_width(self): 
        width, ok = QInputDialog.getInt(self, '펜 굵기', '숫자 입력:', self.canvas.pen_width, 1, 50, 1); 
        if ok: self.canvas.set_pen_width(width); self.update_status_bar()
    def change_font(self): 
        font, ok = QFontDialog.getFont(self.editor.font()); 
        if ok: self.editor.setFont(font)

    def find_text(self):
        search_term, ok = QInputDialog.getText(self, '찾기', '찾을 내용:')
        if ok and search_term and not self.editor.find(search_term):
            QMessageBox.information(self, '찾기', f'\'{search_term}\'을(를) 찾을 수 없습니다.')

    def replace_text(self):
        find_term, ok1 = QInputDialog.getText(self, '바꾸기', '찾을 내용:')
        if not ok1 or not find_term: return
        replace_term, ok2 = QInputDialog.getText(self, '바꾸기', '바꿀 내용:')
        if not ok2: return
        new_text = self.editor.toPlainText().replace(find_term, replace_term)
        if self.editor.toPlainText() != new_text:
            self.editor.setPlainText(new_text)
            QMessageBox.information(self, '바꾸기', '모든 항목을 바꿨습니다.')
        else:
            QMessageBox.information(self, '바꾸기', '찾는 내용이 없습니다.')

    def go_to_line(self):
        line_number, ok = QInputDialog.getInt(self, "줄 이동", "이동할 줄 번호를 입력하세요:", 1, 1, self.editor.blockCount())
        if ok:
            cursor = QTextCursor(self.editor.document().findBlockByNumber(line_number - 1))
            self.editor.setTextCursor(cursor)

    def add_recent_file(self, fname):
        recent_files = self.settings.value("recentFiles", [], type=list)
        if fname in recent_files: recent_files.remove(fname)
        recent_files.insert(0, fname)
        self.settings.setValue("recentFiles", recent_files[:5])
        self.update_recent_files_menu()

    def update_recent_files_menu(self):
        self.recent_files_menu.clear()
        recent_files = self.settings.value("recentFiles", [], type=list)
        for fname in recent_files:
            action = QAction(QFileInfo(fname).fileName(), self)
            action.triggered.connect(lambda checked, name=fname: self.load_file(name))
            self.recent_files_menu.addAction(action)

    def load_settings(self):
        self.update_recent_files_menu()
        geom = self.settings.value("geometry")
        if geom: self.restoreGeometry(geom)
        else: self.setGeometry(100, 100, 800, 600)
        # Set initial mode UI
        self.text_mode_action.setChecked(True)
        self.edit_menu.setEnabled(True)
        self.format_menu.setEnabled(True)
        self.draw_menu.setEnabled(False)
        self.layer_menu.setEnabled(False) # 초기에는 레이어 메뉴 비활성화

    def closeEvent(self, event):
        if self.maybe_save():
            self.settings.setValue("geometry", self.saveGeometry())
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(app.style().standardIcon(QStyle.SP_FileIcon)))
    notepad = Notepad()
    notepad.show()
    sys.exit(app.exec_())