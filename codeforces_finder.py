import sys
import random
import requests
import webbrowser
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                           QSpinBox, QTableWidget, QTableWidgetItem, QComboBox,
                           QHeaderView, QStyle, QStyleFactory, QCheckBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPalette, QColor

class DataFetcher(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, username, min_rating, max_rating, contest_limit):
        super().__init__()
        self.username = username
        self.min_rating = min_rating
        self.max_rating = max_rating
        self.contest_limit = contest_limit

    def run(self):
        try:
            problems = self.get_problems()
            if problems:
                self.finished.emit(problems)
            else:
                self.error.emit("No problems found matching the criteria")
        except Exception as e:
            self.error.emit(str(e))

    def get_problems(self):
        # Get solved problems for the user
        solved_problems = self.get_solved_problems()
        
        # Fetch all problems
        all_problems = self.fetch_all_problems()
        
        # Filter problems based on criteria
        return self.filter_problems(all_problems, solved_problems)

    def get_solved_problems(self):
        user_url = f"https://codeforces.com/api/user.status?handle={self.username}"
        user_response = requests.get(user_url)
        if user_response.status_code != 200:
            raise Exception("Failed to fetch user data")
        
        solved_problems = set()
        for submission in user_response.json()['result']:
            if submission['verdict'] == 'OK':
                problem = submission['problem']
                solved_problems.add(f"{problem.get('contestId')}_{problem.get('index')}")
        
        return solved_problems

    def fetch_all_problems(self):
        problems_url = "https://codeforces.com/api/problemset.problems"
        problems_response = requests.get(problems_url)
        if problems_response.status_code != 200:
            raise Exception("Failed to fetch problems")
        
        problems_data = problems_response.json()['result']['problems']
        return [{
            'name': problem.get('name'),
            'rating': problem.get('rating', 0),
            'contestId': problem.get('contestId'),
            'index': problem.get('index'),
            'tags': problem.get('tags', []),
            'url': f"https://codeforces.com/problemset/problem/{problem.get('contestId')}/{problem.get('index')}"
        } for problem in problems_data]

    def filter_problems(self, all_problems, solved_problems):
        filtered_problems = []
        seen_contest_ids = set()
        
        for problem in all_problems:
            if len(seen_contest_ids) >= self.contest_limit:
                break
            
            contest_id = problem.get('contestId')
            problem_id = f"{contest_id}_{problem.get('index')}"
            
            if (problem.get('rating', 0) >= self.min_rating and 
                problem.get('rating', 0) <= self.max_rating and
                problem_id not in solved_problems):
                
                if contest_id not in seen_contest_ids:
                    seen_contest_ids.add(contest_id)
                
                filtered_problems.append(problem)
        
        return filtered_problems

class CodeforcesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.problems = []
        self.dark_mode = True  # Changed to True for default dark mode
        self.initUI()
        
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
        input_layout.addWidget(self.username_input)

        # Rating range inputs
        self.min_rating = QSpinBox()
        self.min_rating.setRange(800, 3500)
        self.min_rating.setValue(800)
        self.max_rating = QSpinBox()
        self.max_rating.setRange(800, 3500)
        self.max_rating.setValue(3500)
        
        input_layout.addWidget(QLabel("Rating Range:"))
        input_layout.addWidget(self.min_rating)
        input_layout.addWidget(QLabel("to"))
        input_layout.addWidget(self.max_rating)

        # Contest limit input
        self.contest_limit = QSpinBox()
        self.contest_limit.setRange(1, 1000)
        self.contest_limit.setValue(100)
        input_layout.addWidget(QLabel("Contest Limit:"))
        input_layout.addWidget(self.contest_limit)

        # Fetch button
        self.fetch_button = QPushButton("Fetch Problems")
        self.fetch_button.clicked.connect(self.fetch_problems)
        input_layout.addWidget(self.fetch_button)

        # Dark mode toggle - set checked by default
        self.dark_mode_toggle = QCheckBox("Dark Mode")
        self.dark_mode_toggle.setChecked(True)  # Set checked by default
        self.dark_mode_toggle.stateChanged.connect(self.toggle_dark_mode)
        input_layout.addWidget(self.dark_mode_toggle)

        layout.addWidget(input_widget)

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

        self.statusBar().showMessage('Ready')

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
        self.statusBar().showMessage('Fetching problems...')
        self.fetch_button.setEnabled(False)
        self.table.setRowCount(0)
        
        self.fetcher = DataFetcher(
            self.username_input.text(),
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

    def open_problem(self, index):
        row = index.row()
        problem = self.problems[row]
        webbrowser.open(problem['url'])

    def open_random_problem(self):
        if self.problems:
            problem = random.choice(self.problems)
            webbrowser.open(problem['url'])

def main():
    app = QApplication(sys.argv)
    ex = CodeforcesApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()