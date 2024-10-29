import webbrowser
import random
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                           QSpinBox, QTableWidget, QTableWidgetItem, QComboBox,
                           QHeaderView, QMessageBox, QTabWidget)
from src.data_fetcher import DataFetcher
from src.stats_page import StatsPage
from src.utils import get_available_browsers
from src.preferences import load_preferences, save_preferences, load_bookmarks, save_bookmarks
from src.themes import ThemeManager

class CodeforcesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.problems = []
        self.user_preferences = load_preferences()
        self.available_browsers = get_available_browsers()
        self.current_browser = self.user_preferences.get('browser', 'System Default')
        self.theme_manager = ThemeManager('Dark (Default)')
        self.initUI()
        self.setup_tabs()

    def initUI(self):
        self.setWindowTitle('Codeforces Problem Finder')
        self.setMinimumSize(800, 600)

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

        layout.addWidget(input_widget)

        # Theme and browser controls
        controls_widget = QWidget()
        controls_layout = QHBoxLayout(controls_widget)

        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self.theme_manager.get_theme_names())
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
        self.bookmarks = load_bookmarks()
    
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

    def fetch_problems(self):
        username = self.username_input.text()
        self.stats_page.update_username(username)
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
        self.current_browser = self.browser_combo.currentText()
        self.user_preferences['browser'] = self.current_browser
        save_preferences(self.user_preferences)

    def open_problem(self, index):
        row = index.row()
        problem = self.problems[row]
        self.open_in_browser(problem['url'])

    def open_random_problem(self):
        if self.problems:
            problem = random.choice(self.problems)
            self.open_in_browser(problem['url'])

    def open_in_browser(self, url):
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
    
    def change_theme(self, theme):
        self.theme_manager.apply_theme(theme)
        self.user_preferences['theme'] = theme
        save_preferences(self.user_preferences)

    def bookmark_problem(self):
        row = self.table.currentRow()
        if row != -1:
            problem = self.problems[row]
            self.bookmarks.append(problem)
            save_bookmarks(self.bookmarks)
            QMessageBox.information(self, "Bookmarked", f"Problem {problem['name']} bookmarked")