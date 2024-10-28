from PyQt5.QtWidgets import (QApplication,QStyleFactory)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

def apply_dark_mode():
    app = QApplication.instance()
    app.setStyle(QStyleFactory.create("Fusion"))
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

def apply_light_mode():
    app = QApplication.instance()
    app.setStyle(QStyleFactory.create("Fusion"))
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

def apply_monokai_mode():
    app = QApplication.instance()
    app.setStyle(QStyleFactory.create("Fusion"))
    palette = QPalette()
    
    # Monokai Color Scheme
    background = QColor(39, 40, 34)  # Background
    foreground = QColor(248, 248, 242)  # Foreground
    gray = QColor(102, 102, 102)  # Gray
    light_gray = QColor(170, 170, 170)  # Light Gray
    orange = QColor(255, 184, 108)  # Orange
    pink = QColor(255, 105, 180)  # Pink
    yellow = QColor(240, 230, 140)  # Yellow
    green = QColor(80, 200, 120)  # Green
    cyan = QColor(80, 200, 220)  # Cyan
    blue = QColor(80, 120, 220)  # Blue
    purple = QColor(140, 120, 200)  # Purple

    palette.setColor(QPalette.Window, background)
    palette.setColor(QPalette.WindowText, foreground)
    palette.setColor(QPalette.Base, background)
    palette.setColor(QPalette.AlternateBase, background)
    palette.setColor(QPalette.ToolTipBase, foreground)
    palette.setColor(QPalette.ToolTipText, background)
    palette.setColor(QPalette.Text, foreground)
    palette.setColor(QPalette.Button, background)
    palette.setColor(QPalette.ButtonText, foreground)
    palette.setColor(QPalette.BrightText, orange)
    palette.setColor(QPalette.Link, blue)
    palette.setColor(QPalette.Highlight, green)
    palette.setColor(QPalette.HighlightedText, background)
    app.setPalette(palette)

def apply_solarized_mode():
    app = QApplication.instance()
    app.setStyle(QStyleFactory.create("Fusion"))
    palette = QPalette()
    
    # Solarized Color Scheme
    base03 = QColor(236, 239, 244)  # Light background
    base02 = QColor(147, 161, 161)  # Medium background
    base01 = QColor(88, 110, 117)   # Dark background
    base00 = QColor(42, 57, 66)     # Light foreground
    base0 = QColor(60, 76, 90)      # Medium foreground
    base1 = QColor(83, 104, 120)    # Dark foreground
    yellow = QColor(181, 137, 0)    # Yellow
    orange = QColor(203, 75, 22)    # Orange
    red = QColor(197, 15, 31)       # Red
    magenta = QColor(136, 23, 152)  # Magenta
    cyan = QColor(58, 151, 165)     # Cyan
    green = QColor(35, 148, 109)    # Green

    palette.setColor(QPalette.Window, base03)
    palette.setColor(QPalette.WindowText, base00)
    palette.setColor(QPalette.Base, base02)
    palette.setColor(QPalette.AlternateBase, base03)
    palette.setColor(QPalette.ToolTipBase, base00)
    palette.setColor(QPalette.ToolTipText, base03)
    palette.setColor(QPalette.Text, base00)
    palette.setColor(QPalette.Button, base02)
    palette.setColor(QPalette.ButtonText, base00)
    palette.setColor(QPalette.BrightText, red)
    palette.setColor(QPalette.Link, cyan)
    palette.setColor(QPalette.Highlight, green)
    palette.setColor(QPalette.HighlightedText, base03)
    app.setPalette(palette)