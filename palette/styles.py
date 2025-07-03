
from PyQt5.QtGui import QColor, QPalette

def get_app_palette():
    palette = QPalette()
    # Dark theme colors
    palette.setColor(QPalette.Window, QColor(53, 53, 53)) # Background
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255)) # Text color
    palette.setColor(QPalette.Base, QColor(25, 25, 25)) # Input fields background
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255)) # General text
    palette.setColor(QPalette.Button, QColor(70, 70, 70)) # Button background
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255)) # Button text
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218)) # Selection highlight
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0)) # Selected text color
    return palette

def get_stylesheet():
    return """
    QWidget {
        background-color: #353535;
        color: #FFFFFF;
        font-family: Arial;
    }

    QLabel {
        color: #FFFFFF;
    }

    QPushButton {
        background-color: #4A4A4A;
        color: #FFFFFF;
        border: 1px solid #555555;
        padding: 8px 15px;
        border-radius: 5px;
        font-size: 14px;
    }

    QPushButton:hover {
        background-color: #5A5A5A;
    }

    QPushButton:pressed {
        background-color: #3A3A3A;
    }

    QTextEdit {
        background-color: #2A2A2A;
        color: #FFFFFF;
        border: 1px solid #555555;
        padding: 5px;
        border-radius: 5px;
    }

    QScrollArea {
        border: none;
    }

    QFrame {
        border: 1px solid #555555;
        border-radius: 5px;
        background-color: #4A4A4A;
    }

    /* Scrollbar styling */
    QScrollBar:vertical {
        border: 1px solid #4A4A4A;
        background: #353535;
        width: 10px;
        margin: 0px 0px 0px 0px;
    }
    QScrollBar::handle:vertical {
        background: #5A5A5A;
        min-height: 20px;
        border-radius: 5px;
    }
    QScrollBar::add-line:vertical {
        border: none;
        background: none;
    }
    QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
    """
