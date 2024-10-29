from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

class ThemeManager:
    def __init__(self, initial_theme):
        self.themes = {
            "Dark (Default)": self.apply_dark_mode,
            "Light": self.apply_light_mode,
            "Monokai": self.apply_monokai_mode,
            "Solarized": self.apply_solarized_mode,
            "Solarized Dark": self.apply_solarized_dark_mode,
            "Dracula": self.apply_dracula_mode,
            "Nord": self.apply_nord_mode,
            "Gruvbox": self.apply_gruvbox_mode,
            "One Dark": self.apply_one_dark_mode
        }
        self.current_theme = initial_theme
        self.apply_theme(initial_theme)

    def get_theme_names(self):
        return list(self.themes.keys())

    def apply_theme(self, theme):
        self.current_theme = theme
        self.themes[theme]()

    def apply_dark_mode(self):
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()

        # Dark Mode Color Scheme
        background = QColor(53, 53, 53)
        foreground = Qt.white
        base = QColor(25, 25, 25)
        alternate_base = QColor(53, 53, 53)
        tool_tip_base = Qt.white
        tool_tip_text = Qt.white
        text = Qt.white
        button = QColor(53, 53, 53)
        button_text = Qt.white
        bright_text = Qt.red
        link = QColor(42, 130, 218)
        highlight = QColor(42, 130, 218)
        highlighted_text = Qt.black

        palette.setColor(QPalette.Window, background)
        palette.setColor(QPalette.WindowText, foreground)
        palette.setColor(QPalette.Base, base)
        palette.setColor(QPalette.AlternateBase, alternate_base)
        palette.setColor(QPalette.ToolTipBase, tool_tip_base)
        palette.setColor(QPalette.ToolTipText, tool_tip_text)
        palette.setColor(QPalette.Text, text)
        palette.setColor(QPalette.Button, button)
        palette.setColor(QPalette.ButtonText, button_text)
        palette.setColor(QPalette.BrightText, bright_text)
        palette.setColor(QPalette.Link, link)
        palette.setColor(QPalette.Highlight, highlight)
        palette.setColor(QPalette.HighlightedText, highlighted_text)
        app.setPalette(palette)

    def apply_light_mode(self):
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()

        # Light Mode Color Scheme
        background = QColor(240, 240, 240)
        foreground = Qt.black
        base = QColor(255, 255, 255)
        alternate_base = QColor(240, 240, 240)
        tool_tip_base = Qt.white
        tool_tip_text = Qt.white
        text = Qt.black
        button = QColor(240, 240, 240)
        button_text = Qt.black
        bright_text = Qt.red
        link = QColor(42, 130, 218)
        highlight = QColor(42, 130, 218)
        highlighted_text = Qt.black

        palette.setColor(QPalette.Window, background)
        palette.setColor(QPalette.WindowText, foreground)
        palette.setColor(QPalette.Base, base)
        palette.setColor(QPalette.AlternateBase, alternate_base)
        palette.setColor(QPalette.ToolTipBase, tool_tip_base)
        palette.setColor(QPalette.ToolTipText, tool_tip_text)
        palette.setColor(QPalette.Text, text)
        palette.setColor(QPalette.Button, button)
        palette.setColor(QPalette.ButtonText, button_text)
        palette.setColor(QPalette.BrightText, bright_text)
        palette.setColor(QPalette.Link, link)
        palette.setColor(QPalette.Highlight, highlight)
        palette.setColor(QPalette.HighlightedText, foreground)
        app.setPalette(palette)

    def apply_monokai_mode(self):
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()

        # Monokai Color Scheme
        background = QColor(39, 40, 34)
        foreground = QColor(248, 248, 242)
        gray = QColor(102, 102, 102)
        light_gray = QColor(170, 170, 170)
        orange = QColor(255, 184, 108)
        pink = QColor(255, 105, 180)
        yellow = QColor(240, 230, 140)
        green = QColor(80, 200, 120)
        cyan = QColor(80, 200, 220)
        blue = QColor(80, 120, 220)
        purple = QColor(140, 120, 200)

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
        palette.setColor(QPalette.HighlightedText, foreground)
        app.setPalette(palette)

    def apply_solarized_mode(self):
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

    def apply_solarized_dark_mode(self):
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()

        # Solarized Dark Color Scheme
        base03 = QColor(0, 43, 54)  # Dark background
        base02 = QColor(7, 54, 66)  # Medium dark background
        base01 = QColor(88, 110, 117)  # Light dark background
        base00 = QColor(101, 123, 131)  # Dark foreground
        base0 = QColor(131, 148, 150)  # Medium dark foreground
        base1 = QColor(147, 161, 161)  # Light dark foreground
        yellow = QColor(181, 137, 0)  # Yellow
        orange = QColor(203, 75, 22)  # Orange
        red = QColor(220, 50, 47)  # Red
        magenta = QColor(211, 54, 130)  # Magenta
        violet = QColor(108, 113, 196)  # Violet
        blue = QColor(38, 139, 210)  # Blue
        cyan = QColor(42, 161, 152)  # Cyan
        green = QColor(135, 153, 0)  # Green

        palette.setColor(QPalette.Window, base03)
        palette.setColor(QPalette.WindowText, base0)
        palette.setColor(QPalette.Base, base02)
        palette.setColor(QPalette.AlternateBase, base03)
        palette.setColor(QPalette.ToolTipBase, base0)
        palette.setColor(QPalette.ToolTipText, base03)
        palette.setColor(QPalette.Text, base0)
        palette.setColor(QPalette.Button, base02)
        palette.setColor(QPalette.ButtonText, base0)
        palette.setColor(QPalette.BrightText, red)
        palette.setColor(QPalette.Link, blue)
        palette.setColor(QPalette.Highlight, green)
        palette.setColor(QPalette.HighlightedText, base03)
        app.setPalette(palette)

    def apply_dracula_mode(self):
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()

        # Dracula Color Scheme
        background = QColor(40, 42, 54)
        foreground = QColor(248, 248, 242)
        comment = QColor(98, 114, 164)
        cyan = QColor(139, 233, 253)
        green = QColor(80, 250, 123)
        orange = QColor(255, 184, 108)
        pink = QColor(255, 121, 198)
        purple = QColor(189, 147, 249)
        red = QColor(255, 85, 85)
        yellow = QColor(241, 250, 140)

        palette.setColor(QPalette.Window, background)
        palette.setColor(QPalette.WindowText, foreground)
        palette.setColor(QPalette.Base, background)
        palette.setColor(QPalette.AlternateBase, QColor(44, 44, 44))
        palette.setColor(QPalette.ToolTipBase, foreground)
        palette.setColor(QPalette.ToolTipText, background)
        palette.setColor(QPalette.Text, foreground)
        palette.setColor(QPalette.Button, background)
        palette.setColor(QPalette.ButtonText, foreground)
        palette.setColor(QPalette.BrightText, red)
        palette.setColor(QPalette.Link, purple)
        palette.setColor(QPalette.Highlight, pink)
        palette.setColor(QPalette.HighlightedText, background)
        app.setPalette(palette)

    def apply_nord_mode(self):
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()

        # Nord Color Scheme
        nord0 = QColor(46, 52, 64)
        nord1 = QColor(59, 66, 76)
        nord2 = QColor(73, 80, 87)
        nord3 = QColor(216, 222, 233)
        nord4 = QColor(143, 141, 138)
        nord5 = QColor(229, 233, 240)
        nord6 = QColor(143, 188, 187)
        nord7 = QColor(136, 192, 208)
        nord8 = QColor(129, 151, 205)
        nord9 = QColor(208, 135, 112)
        nord10 = QColor(207, 126, 112)
        nord11 = QColor(243, 139, 34)
        nord12 = QColor(163, 190, 140)
        nord13 = QColor(191, 97, 106)
        nord14 = QColor(180, 142, 173)
        nord15 = QColor(237, 208, 152)

        palette.setColor(QPalette.Window, nord0)
        palette.setColor(QPalette.WindowText, nord3)
        palette.setColor(QPalette.Base, nord0)
        palette.setColor(QPalette.AlternateBase, nord1)
        palette.setColor(QPalette.ToolTipBase, nord3)
        palette.setColor(QPalette.ToolTipText, nord0)
        palette.setColor(QPalette.Text, nord3)
        palette.setColor(QPalette.Button, nord0)
        palette.setColor(QPalette.ButtonText, nord3)
        palette.setColor(QPalette.BrightText, nord10)
        palette.setColor(QPalette.Link, nord7)
        palette.setColor(QPalette.Highlight, nord12)
        palette.setColor(QPalette.HighlightedText, nord0)
        app.setPalette(palette)

    def apply_gruvbox_mode(self):
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()

        # Gruvbox Color Scheme
        dark0 = QColor(38, 35, 32)
        dark1 = QColor(50, 47, 45)
        dark2 = QColor(62, 59, 57)
        dark3 = QColor(72, 69, 66)
        dark4 = QColor(83, 80, 77)
        dark5 = QColor(95, 92, 89)
        dark6 = QColor(107, 105, 102)
        light0 = QColor(253, 246, 227)
        light1 = QColor(237, 232, 212)
        light2 = QColor(218, 212, 193)
        light3 = QColor(200, 195, 178)
        light4 = QColor(181, 177, 161)
        light5 = QColor(163, 160, 144)
        light6 = QColor(144, 142, 126)
        red = QColor(235, 84, 104)
        green = QColor(150, 181, 106)
        yellow = QColor(215, 164, 63)
        blue = QColor(115, 145, 195)
        purple = QColor(178, 133, 192)
        aqua = QColor(145, 181, 181)
        orange = QColor(222, 137, 65)

        palette.setColor(QPalette.Window, dark0)
        palette.setColor(QPalette.WindowText, light0)
        palette.setColor(QPalette.Base, dark0)
        palette.setColor(QPalette.AlternateBase, dark1)
        palette.setColor(QPalette.ToolTipBase, light0)
        palette.setColor(QPalette.ToolTipText, dark0)
        palette.setColor(QPalette.Text, light0)
        palette.setColor(QPalette.Button, dark0)
        palette.setColor(QPalette.ButtonText, light0)
        palette.setColor(QPalette.BrightText, red)
        palette.setColor(QPalette.Link, blue)
        palette.setColor(QPalette.Highlight, green)
        palette.setColor(QPalette.HighlightedText, dark0)
        app.setPalette(palette)

    def apply_one_dark_mode(self):
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()

        # One Dark Color Scheme
        background = QColor(30, 30, 30)
        foreground = QColor(248, 248, 242)
        comment = QColor(102, 102, 102)
        cyan = QColor(102, 217, 239)
        green = QColor(163, 190, 140)
        orange = QColor(255, 184, 108)
        pink = QColor(255, 121, 198)
        purple = QColor(189, 147, 249)
        red = QColor(255, 85, 85)
        yellow = QColor(241, 250, 140)

        palette.setColor(QPalette.Window, background)
        palette.setColor(QPalette.WindowText, foreground)
        palette.setColor(QPalette.Base, background)
        palette.setColor(QPalette.AlternateBase, QColor(36, 36, 36))
        palette.setColor(QPalette.ToolTipBase, foreground)
        palette.setColor(QPalette.ToolTipText, background)
        palette.setColor(QPalette.Text, foreground)
        palette.setColor(QPalette.Button, background)
        palette.setColor(QPalette.ButtonText, foreground)
        palette.setColor(QPalette.BrightText, red)
        palette.setColor(QPalette.Link, purple)
        palette.setColor(QPalette.Highlight, pink)
        palette.setColor(QPalette.HighlightedText, foreground)
        app.setPalette(palette)