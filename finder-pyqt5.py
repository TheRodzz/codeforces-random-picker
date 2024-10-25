import sys
import json
import requests
from datetime import datetime, timedelta
import os.path
from typing import List, Dict
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QLabel, QLineEdit, QPushButton,
                           QSpinBox, QTableWidget, QTableWidgetItem, QHeaderView,
                           QComboBox, QMessageBox, QCheckBox)
from PyQt5.QtCore import Qt, QTimer

class ProblemFinder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cache_file = "problems_cache.json"
        self.cache_expiry = 24 * 60 * 60  # 24 hours in seconds
        self.problems_data = []
        self.filtered_problems = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Codeforces Problem Finder')
        self.setGeometry(100, 100, 1200, 800)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        # Input controls
        input_layout = QHBoxLayout()
        
        # Username input
        username_layout = QVBoxLayout()
        username_label = QLabel('Codeforces Username:')
        self.username_input = QLineEdit()
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

        # Fetch button
        self.fetch_button = QPushButton('Fetch Problems')
        self.fetch_button.clicked.connect(self.fetch_problems)
        input_layout.addWidget(self.fetch_button)

        layout.addLayout(input_layout)

        # Sorting controls
        sort_layout = QHBoxLayout()
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
        layout.addLayout(sort_layout)

        # Problems table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            'Contest ID', 'Index', 'Name', 'Rating', 'Solved Count', 'Link'
        ])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        layout.addWidget(self.table)

        main_widget.setLayout(layout)

    def load_cache(self) -> Dict:
        if not os.path.exists(self.cache_file):
            return {}
        
        with open(self.cache_file, 'r') as f:
            cache = json.load(f)
            
        # Check if cache is expired
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

        try:
            # Load cache first
            cache = self.load_cache()
            if cache:
                problems_data = cache.get('data', {}).get('problems', [])
                solved_problems = cache.get('data', {}).get('solved_problems', set())
            else:
                # Fetch problems from API
                problems_response = requests.get('https://codeforces.com/api/problemset.problems')
                if problems_response.status_code != 200:
                    raise Exception('Failed to fetch problems')
                
                problems_data = problems_response.json()['result']['problems']
                
                # Fetch user's solved problems
                user_response = requests.get(f'https://codeforces.com/api/user.status?handle={username}')
                if user_response.status_code != 200:
                    raise Exception('Failed to fetch user data')
                
                solved_problems = set(
                    f"{submission['problem']['contestId']}{submission['problem']['index']}"
                    for submission in user_response.json()['result']
                    if submission['verdict'] == 'OK'
                )

                # Cache the data
                self.save_cache({
                    'problems': problems_data,
                    'solved_problems': list(solved_problems)
                })

            # Filter problems based on criteria
            min_rating = self.min_rating.value()
            max_rating = self.max_rating.value()
            contest_limit = self.contest_limit.value()

            # Sort contests by ID to get the latest ones
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

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error fetching data: {str(e)}')
        
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
    ex = ProblemFinder()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()