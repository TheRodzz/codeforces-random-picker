import sys
import json
import requests
import webbrowser
import random
from datetime import datetime, timedelta
import os.path
from typing import List, Dict
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QLabel, QLineEdit, QPushButton,
                           QSpinBox, QTableWidget, QTableWidgetItem, QHeaderView,
                           QComboBox, QMessageBox, QCheckBox, QFrame, QStyleFactory,
                           QStatusBar)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor

class StyledWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #2c3e50;
                font-weight: bold;
                font-size: 12px;
            }
            QLineEdit, QSpinBox, QComboBox {
                padding: 6px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
                min-height: 25px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
            QTableWidget {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 8px;
                border: none;
            }
        """)

class ProblemFinder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cache_file = "problems_cache.json"
        self.cache_expiry = 24 * 60 * 60  # 24 hours in seconds
        self.problems_data = []
        self.filtered_problems = []
        self.selected_browser = "default"
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Codeforces Problem Finder')
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #f5f5f5;")

        # Create main widget and layout
        main_widget = StyledWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_label = QLabel('Codeforces Problem Finder')
        header_label.setStyleSheet("""
            font-size: 24px;
            color: #2c3e50;
            font-weight: bold;
            padding: 10px;
        """)
        layout.addWidget(header_label, alignment=Qt.AlignCenter)

        # Create a frame for input controls
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        input_layout = QHBoxLayout(input_frame)
        input_layout.setSpacing(20)

        # Username input
        username_layout = QVBoxLayout()
        username_label = QLabel('Codeforces Username:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username...")
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        input_layout.addLayout(username_layout)

        # Rating range inputs
        rating_layout = QVBoxLayout()
        rating_label = QLabel('Rating Range:')
        rating_range_layout = QHBoxLayout()
        self.min_rating = QSpinBox()
        self.min_rating.setRange(800, 3500)
        self.min_rating.setValue(800)
        self.max_rating = QSpinBox()
        self.max_rating.setRange(800, 3500)
        self.max_rating.setValue(3500)
        rating_range_layout.addWidget(self.min_rating)
        rating_range_layout.addWidget(QLabel('-'))
        rating_range_layout.addWidget(self.max_rating)
        rating_layout.addWidget(rating_label)
        rating_layout.addLayout(rating_range_layout)
        input_layout.addLayout(rating_layout)

        # Contest limit input
        contest_limit_layout = QVBoxLayout()
        contest_limit_label = QLabel('Last N Contests:')
        self.contest_limit = QSpinBox()
        self.contest_limit.setRange(1, 1000)
        self.contest_limit.setValue(100)
        contest_limit_layout.addWidget(contest_limit_label)
        contest_limit_layout.addWidget(self.contest_limit)
        input_layout.addLayout(contest_limit_layout)

        # Browser selection
        browser_layout = QVBoxLayout()
        browser_label = QLabel('Browser:')
        self.browser_combo = QComboBox()
        self.browser_combo.addItems(['Default', 'Chrome', 'Firefox', 'Safari', 'Edge'])
        browser_layout.addWidget(browser_label)
        browser_layout.addWidget(self.browser_combo)
        input_layout.addLayout(browser_layout)

        # Buttons layout
        buttons_layout = QVBoxLayout()
        self.fetch_button = QPushButton('Fetch Problems')
        self.fetch_button.clicked.connect(self.fetch_problems)
        self.random_button = QPushButton('Open Random Problem')
        self.random_button.clicked.connect(self.open_random_problem)
        self.random_button.setEnabled(False)
        buttons_layout.addWidget(self.fetch_button)
        buttons_layout.addWidget(self.random_button)
        input_layout.addLayout(buttons_layout)

        layout.addWidget(input_frame)

        # Sorting controls in a frame
        sort_frame = QFrame()
        sort_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        sort_layout = QHBoxLayout(sort_frame)
        sort_layout.addWidget(QLabel('Sort by:'))
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(['Rating', 'Solved Count', 'Contest ID', 'Problem Index'])
        sort_layout.addWidget(self.sort_combo)
        
        self.sort_order = QComboBox()
        self.sort_order.addItems(['Ascending', 'Descending'])
        sort_layout.addWidget(self.sort_order)
        
        sort_button = QPushButton('Sort')
        sort_button.clicked.connect(self.sort_problems)
        sort_layout.addWidget(sort_button)
        sort_layout.addStretch()
        
        layout.addWidget(sort_frame)

        # Problems table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            'Contest ID', 'Index', 'Name', 'Rating', 'Solved Count', 'Link'
        ])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #dcdcdc;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        layout.addWidget(self.table)

        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.setStyleSheet("""
            QStatusBar {
                background-color: #34495e;
                color: white;
                padding: 5px;
            }
        """)

        main_widget.setLayout(layout)

    def open_random_problem(self):
        if not self.filtered_problems:
            QMessageBox.warning(self, 'Error', 'No problems available to choose from')
            return

        problem = random.choice(self.filtered_problems)
        link = f"https://codeforces.com/problemset/problem/{problem['contestId']}/{problem['index']}"
        
        browser = self.browser_combo.currentText().lower()
        try:
            if browser == 'default':
                webbrowser.open(link)
            else:
                webbrowser.get(browser).open(link)
            self.statusBar.showMessage(f'Opened problem {problem["name"]} in {browser} browser', 5000)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to open browser: {str(e)}')

    def load_cache(self) -> Dict:
        if not os.path.exists(self.cache_file):
            return {}
        
        with open(self.cache_file, 'r') as f:
            cache = json.load(f)
            
        if datetime.now().timestamp() - cache.get('timestamp', 0) > self.cache_expiry:
            return {}
            
        return cache

    def save_cache(self, data: Dict):
        cache_data = {
            'timestamp': datetime.now().timestamp(),
            'data': data
        }
        with open(self.cache_file, 'w') as f:
            json.dump(cache_data, f)

    def fetch_problems(self):
        username = self.username_input.text().strip()
        if not username:
            QMessageBox.warning(self, 'Error', 'Please enter a username')
            return

        self.fetch_button.setEnabled(False)
        self.fetch_button.setText('Fetching...')
        self.statusBar.showMessage('Fetching problems...')

        try:
            cache = self.load_cache()
            if cache:
                problems_data = cache.get('data', {}).get('problems', [])
                solved_problems = cache.get('data', {}).get('solved_problems', set())
            else:
                problems_response = requests.get('https://codeforces.com/api/problemset.problems')
                if problems_response.status_code != 200:
                    raise Exception('Failed to fetch problems')
                
                problems_data = problems_response.json()['result']['problems']
                
                user_response = requests.get(f'https://codeforces.com/api/user.status?handle={username}')
                if user_response.status_code != 200:
                    raise Exception('Failed to fetch user data')
                
                solved_problems = set(
                    f"{submission['problem']['contestId']}{submission['problem']['index']}"
                    for submission in user_response.json()['result']
                    if submission['verdict'] == 'OK'
                )

                self.save_cache({
                    'problems': problems_data,
                    'solved_problems': list(solved_problems)
                })

            min_rating = self.min_rating.value()
            max_rating = self.max_rating.value()
            contest_limit = self.contest_limit.value()

            contest_ids = sorted(set(p['contestId'] for p in problems_data), reverse=True)[:contest_limit]
            
            self.problems_data = [
                problem for problem in problems_data
                if (problem.get('rating', 0) >= min_rating and
                    problem.get('rating', 0) <= max_rating and
                    problem['contestId'] in contest_ids and
                    f"{problem['contestId']}{problem['index']}" not in solved_problems)
            ]

            self.filtered_problems = self.problems_data.copy()
            self.update_table()
            self.random_button.setEnabled(True)
            self.statusBar.showMessage(f'Found {len(self.filtered_problems)} problems', 5000)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error fetching data: {str(e)}')
            self.statusBar.showMessage('Error fetching problems', 5000)
        
        finally:
            self.fetch_button.setEnabled(True)
            self.fetch_button.setText('Fetch Problems')

    def sort_problems(self):
        sort_by = self.sort_combo.currentText()
        ascending = self.sort_order.currentText() == 'Ascending'

        if sort_by == 'Rating':
            key = lambda x: x.get('rating', 0)
        elif sort_by == 'Solved Count':
            key = lambda x: x.get('solvedCount', 0)
        elif sort_by == 'Contest ID':
            key = lambda x: x['contestId']
        else:  # Problem Index
            key = lambda x: x['index']

        self.filtered_problems.sort(key=key, reverse=not ascending)
        self.update_table()
        self.statusBar.showMessage(f'Sorted by {sort_by} ({self.sort_order.currentText()})', 3000)

    def update_table(self):
        self.table.setRowCount(0)
        self.table.setRowCount(len(self.filtered_problems))

        for row, problem in enumerate(self.filtered_problems):
            self.table.setItem(row, 0, QTableWidgetItem(str(problem['contestId'])))
            self.table.setItem(row, 1, QTableWidgetItem(problem['index']))
            self.table.setItem(row, 2, QTableWidgetItem(problem['name']))
            self.table.setItem(row, 3, QTableWidgetItem(str(problem.get('rating', 'N/A'))))
            self.table.setItem(row, 4, QTableWidgetItem(str(problem.get('solvedCount', 'N/A'))))
            
            link = f"https://codeforces.com/problemset/problem/{problem['contestId']}/{problem['index']}"
            link_item = QTableWidgetItem(link)
            link_item.setData(Qt.UserRole, link)
            self.table.setItem(row, 5, link_item)

def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    ex = ProblemFinder()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()