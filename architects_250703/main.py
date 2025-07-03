import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QListWidget, QListWidgetItem, QPushButton, QStackedWidget,
                             QTextBrowser)
from PyQt5.QtGui import QPixmap, QColor, QFont
from PyQt5.QtCore import Qt, QSize, pyqtSignal

import architect_db as db # Assuming architect_db.py is in the same directory

class ImagePlaceholder(QLabel):
    def __init__(self, width=150, height=150, parent=None):
        QLabel.__init__(self, parent)
        self.setFixedSize(width, height)
        self.setStyleSheet("background-color: white; border: 1px solid lightgray;")
        self.setAlignment(Qt.AlignCenter)
        self.setText("No Image") # Optional text

    def set_image(self, image_path):
        if image_path:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                self.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.setText("") # Remove text if image is loaded
            else:
                self.setText("Image Load Failed")
                self.clear()
        else:
            self.setText("No Image")
            self.clear()

class ArchitectListView(QWidget):
    architect_selected = pyqtSignal(int) # Signal to emit architect ID

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.layout = QVBoxLayout(self)
        self.title_label = QLabel("Architects")
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.architect_list_widget = QListWidget()
        self.architect_list_widget.itemClicked.connect(self._on_architect_clicked)
        self.layout.addWidget(self.architect_list_widget)

    def load_architects(self):
        self.architect_list_widget.clear()
        architects = db.get_architects()
        for arch in architects:
            item = QListWidgetItem(f"{arch[1]} ({arch[4]})") # Name (Nationality)
            item.setData(Qt.UserRole, arch[0]) # Store architect ID
            self.architect_list_widget.addItem(item)

    def _on_architect_clicked(self, item):
        architect_id = item.data(Qt.UserRole)
        self.architect_selected.emit(architect_id)

class ArchitectDetailView(QWidget):
    back_requested = pyqtSignal() # Signal to go back to architect list
    building_selected = pyqtSignal(int) # Signal to emit building ID

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.layout = QVBoxLayout(self)

        self.back_button = QPushButton("← Back to Architects")
        self.back_button.clicked.connect(self.back_requested.emit)
        self.layout.addWidget(self.back_button)

        self.architect_name_label = QLabel()
        self.architect_name_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.layout.addWidget(self.architect_name_label)

        self.architect_image = ImagePlaceholder(200, 200) # Larger placeholder
        self.layout.addWidget(self.architect_image)

        self.architect_bio = QTextBrowser()
        self.architect_bio.setReadOnly(True)
        self.layout.addWidget(self.architect_bio)

        self.buildings_label = QLabel("Buildings:")
        self.buildings_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.layout.addWidget(self.buildings_label)

        self.building_list_widget = QListWidget()
        self.building_list_widget.itemClicked.connect(self._on_building_clicked)
        self.layout.addWidget(self.building_list_widget)

    def load_architect_details(self, architect_id):
        architects = db.get_architects() # Re-fetch to find by ID
        architect = next((a for a in architects if a[0] == architect_id), None)
        if architect:
            self.architect_name_label.setText(f"{architect[1]} ({architect[4]})")
            bio_text = f"Born: {architect[2] or 'N/A'}\n" \
                       f"Died: {architect[3] or 'N/A'}\n" \
                       f"Bio: {architect[5] or 'N/A'}"
            self.architect_bio.setText(bio_text)
            self.architect_image.set_image(architect[6]) # Set architect image

            self.building_list_widget.clear()
            buildings = db.get_buildings_by_architect(architect_id)
            for bld in buildings:
                item = QListWidgetItem(bld[2]) # Building Name
                item.setData(Qt.UserRole, bld[0]) # Store building ID
                self.building_list_widget.addItem(item)

    def _on_building_clicked(self, item):
        building_id = item.data(Qt.UserRole)
        self.building_selected.emit(building_id)

class BuildingDetailView(QWidget):
    back_requested = pyqtSignal(int) # Signal to emit architect ID to go back

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.layout = QVBoxLayout(self)

        self.back_button = QPushButton("← Back to Architect")
        self.back_button.clicked.connect(self._on_back_clicked)
        self.layout.addWidget(self.back_button)

        self.building_name_label = QLabel()
        self.building_name_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.layout.addWidget(self.building_name_label)

        self.building_image = ImagePlaceholder(300, 250) # Larger placeholder
        self.layout.addWidget(self.building_image)

        self.building_details = QTextBrowser()
        self.building_details.setReadOnly(True)
        self.layout.addWidget(self.building_details)

        self.current_architect_id = -1 # To store architect ID for back navigation

    def load_building_details(self, building_id):
        # Fetch all buildings and find the one by ID
        all_buildings = db.get_all_buildings()
        building = next((b for b in all_buildings if b[0] == building_id), None)
        if building:
            self.current_architect_id = building[1] # Store architect ID
            self.building_name_label.setText(building[2]) # Building Name
            details_text = f"Location: {building[3] or 'N/A'}\n" \
                           f"Year Completed: {building[4] or 'N/A'}\n" \
                           f"Description: {building[5] or 'N/A'}"
            self.building_details.setText(details_text)
            self.building_image.set_image(building[6]) # Set building image

    def _on_back_clicked(self):
        self.back_requested.emit(self.current_architect_id)


class ArchitectApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Architects & Buildings DB")
        self.setGeometry(100, 100, 1000, 800) # Set initial window size

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.architect_list_view = ArchitectListView(self)
        self.architect_detail_view = ArchitectDetailView(self)
        self.building_detail_view = BuildingDetailView(self)

        self.stacked_widget.addWidget(self.architect_list_view)
        self.stacked_widget.addWidget(self.architect_detail_view)
        self.stacked_widget.addWidget(self.building_detail_view)

        self._connect_signals()
        self.architect_list_view.load_architects() # Load initial data

        # Apply some basic styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333;
                padding: 5px;
            }
            QLabel#title_label {
                background-color: #e0e0e0;
                border-bottom: 1px solid #ccc;
                margin-bottom: 10px;
            }
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #aaddff;
                color: black;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QTextBrowser {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: white;
                padding: 10px;
            }
        """)

    def _connect_signals(self):
        self.architect_list_view.architect_selected.connect(self.show_architect_details)
        self.architect_detail_view.back_requested.connect(self.show_architect_list)
        self.architect_detail_view.building_selected.connect(self.show_building_details)
        self.building_detail_view.back_requested.connect(self.show_architect_details)

    def show_architect_list(self):
        self.architect_list_view.load_architects() # Refresh list in case of changes
        self.stacked_widget.setCurrentWidget(self.architect_list_view)

    def show_architect_details(self, architect_id):
        self.architect_detail_view.load_architect_details(architect_id)
        self.stacked_widget.setCurrentWidget(self.architect_detail_view)

    def show_building_details(self, building_id):
        self.building_detail_view.load_building_details(building_id)
        self.stacked_widget.setCurrentWidget(self.building_detail_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Ensure the database is created before running the app
    db.create_tables()
    window = ArchitectApp()
    window.show()
    sys.exit(app.exec_())