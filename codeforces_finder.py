import sys
import random
import json
import shutil
import os
import webbrowser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                           QSpinBox, QTableWidget, QTableWidgetItem, QComboBox,
                           QHeaderView, QStyleFactory, QCheckBox, 
                           QMessageBox,QTabWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

from DataFetcher import DataFetcher
from StatsPage import StatsPage

class CodeforcesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.problems = []
        self.dark_mode = True  
        self.user_preferences = self.load_preferences()
        self.available_browsers = self.get_available_browsers()
        self.current_browser = self.user_preferences.get('browser', 'System Default')
        self.initUI()
        self.setup_tabs()

    def get_default_browser_name(self):
        """Get the name of the default system browser"""
        # Try to get the default browser name based on the platform
        if sys.platform == 'darwin':  # macOS
            # Check if Safari is the default
            if os.path.exists('/Applications/Safari.app'):
                return 'Safari'
        elif sys.platform == 'win32':  # Windows
            import winreg
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                  r'SOFTWARE\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice') as key:
                    browser_reg = winreg.QueryValueEx(key, 'ProgId')[0]
                    
                    if 'Chrome' in browser_reg:
                        return 'Chrome'
                    elif 'Firefox' in browser_reg:
                        return 'Firefox'
                    elif 'Edge' in browser_reg:
                        return 'Edge'
                    elif 'Safari' in browser_reg:
                        return 'Safari'
                    elif 'Opera' in browser_reg:
                        return 'Opera'
            except:
                pass
        else:  # Linux
            # Try to detect the default browser using xdg-settings
            try:
                browser = os.popen('xdg-settings get default-web-browser').read().strip()
                if 'firefox' in browser.lower():
                    return 'Firefox'
                elif 'chrome' in browser.lower():
                    return 'Chrome'
                elif 'chromium' in browser.lower():
                    return 'Chromium'
                elif 'safari' in browser.lower():
                    return 'Safari'
                elif 'opera' in browser.lower():
                    return 'Opera'
                elif 'edge' in browser.lower():
                    return 'Edge'
            except:
                pass
            
            # Alternative method for Linux: check if common browsers are installed
            browsers_commands = {
                'firefox': 'Firefox',
                'google-chrome': 'Chrome',
                'chromium': 'Chromium',
                'opera': 'Opera',
                'microsoft-edge': 'Edge'
            }
            
            for cmd, name in browsers_commands.items():
                if shutil.which(cmd):
                    return name
                
        return 'System Browser'  # Fallback name if we can't detect the specific browser

    def get_available_browsers(self):
        """Get list of available browsers on the system"""
        browsers = {}
        
        # Add default browser first
        default_name = self.get_default_browser_name()
        browsers[f'{default_name} (Default)'] = ''
        
        # Try to detect common browsers
        try:
            # Check for Firefox
            if shutil.which('firefox'):
                try:
                    webbrowser.get('firefox')
                    browsers['Firefox'] = 'firefox'
                except webbrowser.Error:
                    pass

            # Check for Chrome
            chrome_cmd = 'google-chrome' if sys.platform.startswith('linux') else 'chrome'
            if shutil.which(chrome_cmd):
                try:
                    webbrowser.get('chrome')
                    browsers['Chrome'] = 'chrome'
                except webbrowser.Error:
                    pass

            # Check for Chromium on Linux
            if sys.platform.startswith('linux') and shutil.which('chromium'):
                try:
                    webbrowser.get('chromium')
                    browsers['Chromium'] = 'chromium'
                except webbrowser.Error:
                    pass

            # Check for Safari on macOS
            if sys.platform == 'darwin' and os.path.exists('/Applications/Safari.app'):
                try:
                    webbrowser.get('safari')
                    browsers['Safari'] = 'safari'
                except webbrowser.Error:
                    pass

            # Check for Edge
            edge_cmd = 'microsoft-edge' if sys.platform.startswith('linux') else 'edge'
            if shutil.which(edge_cmd):
                try:
                    webbrowser.get('edge')
                    browsers['Edge'] = 'edge'
                except webbrowser.Error:
                    pass

            # Check for Opera
            if shutil.which('opera'):
                try:
                    webbrowser.get('opera')
                    browsers['Opera'] = 'opera'
                except webbrowser.Error:
                    pass

        except Exception as e:
            print(f"Error detecting browsers: {e}")
            
        return browsers

    def initUI(self):
        self.setWindowTitle('Codeforces Problem Finder')
        self.setMinimumSize(800, 600)

        # Set dark mode by default
        self.apply_dark_mode()

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Input controls
        input_widget = QWidget()
        input_layout = QHBoxLayout(input_widget)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Codeforces Username")
        self.username_input.setText(self.user_preferences.get('username', ''))
        input_layout.addWidget(self.username_input)

        # Rating range inputs
        self.min_rating = QSpinBox()
        self.min_rating.setRange(800, 3500)
        self.min_rating.setValue(self.user_preferences.get('min_rating', 800))
        self.max_rating = QSpinBox()
        self.max_rating.setRange(800, 3500)
        self.max_rating.setValue(self.user_preferences.get('max_rating', 3500))
        
        input_layout.addWidget(QLabel("Rating Range:"))
        input_layout.addWidget(self.min_rating)
        input_layout.addWidget(QLabel("to"))
        input_layout.addWidget(self.max_rating)

        # Contest limit input
        self.contest_limit = QSpinBox()
        self.contest_limit.setRange(1, 1000)
        self.contest_limit.setValue(self.user_preferences.get('contest_limit', 100))
        input_layout.addWidget(QLabel("Contest Limit:"))
        input_layout.addWidget(self.contest_limit)

        # Fetch button
        self.fetch_button = QPushButton("Fetch Problems")
        self.fetch_button.clicked.connect(self.fetch_problems)
        input_layout.addWidget(self.fetch_button)

        # Dark mode toggle
        self.dark_mode_toggle = QCheckBox("Dark Mode")
        self.dark_mode_toggle.setChecked(self.dark_mode)
        self.dark_mode_toggle.stateChanged.connect(self.toggle_dark_mode)
        input_layout.addWidget(self.dark_mode_toggle)

        layout.addWidget(input_widget)

        # Theme and browser controls
        controls_widget = QWidget()
        controls_layout = QHBoxLayout(controls_widget)

        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark (Default)", "Light", "Monokai", "Solarized"])
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        controls_layout.addWidget(QLabel("Theme:"))
        controls_layout.addWidget(self.theme_combo)

        # Browser selection
        controls_layout.addWidget(QLabel("Open in Browser:"))
        self.browser_combo = QComboBox()
        self.browser_combo.addItems(self.available_browsers.keys())
        
        # Set the previously selected browser if it exists
        if self.current_browser:
            index = self.browser_combo.findText(self.current_browser)
            if index >= 0:
                self.browser_combo.setCurrentIndex(index)
        
        controls_layout.addWidget(self.browser_combo)
        self.browser_combo.currentTextChanged.connect(self.save_browser_preference)

        layout.addWidget(controls_widget)

        # Sorting controls
        sort_widget = QWidget()
        sort_layout = QHBoxLayout(sort_widget)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Rating ↑", "Rating ↓", "Name A-Z", "Name Z-A", "Contest ID ↑", "Contest ID ↓"])
        self.sort_combo.currentIndexChanged.connect(self.sort_problems)
        sort_layout.addWidget(QLabel("Sort by:"))
        sort_layout.addWidget(self.sort_combo)

        # Random problem button
        self.random_button = QPushButton("Open Random Problem")
        self.random_button.clicked.connect(self.open_random_problem)
        sort_layout.addWidget(self.random_button)

        # Bookmark button
        self.bookmark_button = QPushButton("Bookmark Problem")
        self.bookmark_button.clicked.connect(self.bookmark_problem)
        sort_layout.addWidget(self.bookmark_button)

        layout.addWidget(sort_widget)

        # Problems table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Rating", "Contest ID", "Index", "Tags"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.doubleClicked.connect(self.open_problem)
        layout.addWidget(self.table)

        # Status bar
        self.statusBar().showMessage('Ready')

        # Load bookmarks
        self.bookmarks = self.load_bookmarks()
    
    def setup_tabs(self):
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create main problem finder page
        self.problem_finder_page = QWidget()
        self.problem_finder_page.setLayout(self.centralWidget().layout())
        
        # Create stats page
        self.stats_page = StatsPage()
        
        # Add tabs
        self.tab_widget.addTab(self.problem_finder_page, "Problem Finder")
        self.tab_widget.addTab(self.stats_page, "User Stats")
        
        # Set tab widget as central widget
        self.setCentralWidget(self.tab_widget)

    def apply_dark_mode(self):
        """Apply dark mode styling"""
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

    def toggle_dark_mode(self, state):
        app = QApplication.instance()
        if state:
            self.apply_dark_mode()
        else:
            app.setStyle(QStyleFactory.create("Fusion"))
            app.setPalette(app.style().standardPalette())

    def fetch_problems(self):
        username = self.username_input.text()
        self.stats_page.update_username(username)  # Add this line
        self.statusBar().showMessage('Fetching problems...')
        self.fetch_button.setEnabled(False)
        self.table.setRowCount(0)
        
        self.fetcher = DataFetcher(
            username,
            self.min_rating.value(),
            self.max_rating.value(),
            self.contest_limit.value()
        )
        self.fetcher.finished.connect(self.update_problems)
        self.fetcher.error.connect(self.show_error)
        self.fetcher.start()

    def update_problems(self, problems):
        self.problems = problems
        self.display_problems()
        self.fetch_button.setEnabled(True)
        self.statusBar().showMessage(f'Found {len(problems)} problems')

    def show_error(self, error_message):
        self.statusBar().showMessage(f'Error: {error_message}')
        self.fetch_button.setEnabled(True)

    def display_problems(self):
        self.table.setRowCount(len(self.problems))
        for i, problem in enumerate(self.problems):
            self.table.setItem(i, 0, QTableWidgetItem(problem['name']))
            self.table.setItem(i, 1, QTableWidgetItem(str(problem['rating'])))
            self.table.setItem(i, 2, QTableWidgetItem(str(problem['contestId'])))
            self.table.setItem(i, 3, QTableWidgetItem(problem['index']))
            self.table.setItem(i, 4, QTableWidgetItem(', '.join(problem['tags'])))

    def sort_problems(self):
        sort_type = self.sort_combo.currentText()
        if sort_type == "Rating ↑":
            self.problems.sort(key=lambda x: x['rating'])
        elif sort_type == "Rating ↓":
            self.problems.sort(key=lambda x: x['rating'], reverse=True)
        elif sort_type == "Name A-Z":
            self.problems.sort(key=lambda x: x['name'])
        elif sort_type == "Name Z-A":
            self.problems.sort(key=lambda x: x['name'], reverse=True)
        elif sort_type == "Contest ID ↑":
            self.problems.sort(key=lambda x: x['contestId'])
        elif sort_type == "Contest ID ↓":
            self.problems.sort(key=lambda x: x['contestId'], reverse=True)
        
        self.display_problems()

    def save_browser_preference(self):
        """Save the selected browser to user preferences"""
        self.current_browser = self.browser_combo.currentText()
        self.user_preferences['browser'] = self.current_browser
        self.save_preferences()

    def open_problem(self, index):
        row = index.row()
        problem = self.problems[row]
        self.open_in_browser(problem['url'])

    def open_random_problem(self):
        if self.problems:
            problem = random.choice(self.problems)
            self.open_in_browser(problem['url'])

    def open_in_browser(self, url):
        """Open URL in the selected browser"""
        browser_name = self.browser_combo.currentText()
        browser_key = self.available_browsers.get(browser_name)
        
        try:
            if browser_key:
                # Use specific browser
                try:
                    browser = webbrowser.get(browser_key)
                    browser.open(url)
                except webbrowser.Error:
                    webbrowser.open(url)  # Fallback to default browser
            else:
                # Use system default browser
                webbrowser.open(url)
        except Exception as e:
            QMessageBox.warning(
                self,
                "Browser Error",
                f"Failed to open browser: {str(e)}\nFalling back to default browser."
            )
            webbrowser.open(url)
    
    def load_preferences(self):
        try:
            with open("preferences.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
      
    def change_theme(self, theme):
        if theme == "Light":
            self.apply_light_mode()
        elif theme == "Monokai":
            self.apply_monokai_mode()
        elif theme == "Solarized":
            self.apply_solarized_mode()
        else:
            self.apply_dark_mode()

    def apply_light_mode(self):
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

    def apply_monokai_mode(self):
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

    def bookmark_problem(self):
        row = self.table.currentRow()
        if row!= -1:
            problem = self.problems[row]
            self.bookmarks.append(problem)
            self.save_bookmarks()
            QMessageBox.information(self, "Bookmarked", f"Problem {problem['name']} bookmarked")

    def load_preferences(self):
        try:
            with open("preferences.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_preferences(self):
        with open("preferences.json", "w") as f:
            json.dump(self.user_preferences, f)

    def load_bookmarks(self):
        try:
            with open("bookmarks.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_bookmarks(self):
        with open("bookmarks.json", "w") as f:
            json.dump(self.bookmarks, f)
            
def main():
    app = QApplication(sys.argv)
    ex = CodeforcesApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()