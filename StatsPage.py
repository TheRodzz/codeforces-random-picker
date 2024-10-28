from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QFrame)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import requests
from collections import defaultdict

class StatsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.username = ""
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        self.username_label = QLabel("User Stats")
        self.username_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(self.username_label)
        
        # Refresh button
        self.refresh_btn = QPushButton("Refresh Stats")
        self.refresh_btn.clicked.connect(self.refresh_stats)
        header_layout.addWidget(self.refresh_btn)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Create frames for charts
        charts_layout = QHBoxLayout()
        
        # Tags pie chart
        tags_frame = QFrame()
        tags_frame.setFrameStyle(QFrame.StyledPanel)
        tags_layout = QVBoxLayout(tags_frame)
        self.tags_canvas = FigureCanvas(plt.Figure(figsize=(6, 6)))
        tags_layout.addWidget(self.tags_canvas)
        charts_layout.addWidget(tags_frame)
        
        # Rating distribution bar chart
        rating_frame = QFrame()
        rating_frame.setFrameStyle(QFrame.StyledPanel)
        rating_layout = QVBoxLayout(rating_frame)
        self.rating_canvas = FigureCanvas(plt.Figure(figsize=(8, 6)))
        rating_layout.addWidget(self.rating_canvas)
        charts_layout.addWidget(rating_frame)
        
        layout.addLayout(charts_layout)
        
        # Stats summary
        self.stats_label = QLabel()
        self.stats_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.stats_label)
        
        self.setLayout(layout)
        
    def update_username(self, username):
        self.username = username
        self.username_label.setText(f"Stats for {username}")
        self.refresh_stats()
        
    def refresh_stats(self):
        if not self.username:
            return
            
        try:
            # Fetch user submission data
            submissions = self.fetch_user_submissions()
            if not submissions:
                return
                
            # Process the data
            tags_data, rating_data = self.process_submissions(submissions)
            
            # Update charts
            self.update_tags_chart(tags_data)
            self.update_rating_chart(rating_data)
            
            # Update summary stats
            total_solved = len({(sub['problem']['contestId'], sub['problem']['index']) 
                              for sub in submissions if sub['verdict'] == 'OK'})
            max_rating = max((sub['problem'].get('rating', 0) for sub in submissions 
                            if sub['verdict'] == 'OK' and 'rating' in sub['problem']), default=0)
            
            self.stats_label.setText(
                f"Total Problems Solved: {total_solved}\n"
                f"Maximum Rating Solved: {max_rating}"
            )
            
        except Exception as e:
            self.stats_label.setText(f"Error fetching stats: {str(e)}")
    
    def fetch_user_submissions(self):
        url = f"https://codeforces.com/api/user.status?handle={self.username}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['result']
        return None
        
    def process_submissions(self, submissions):
        # Process tags
        tags_counter = defaultdict(int)
        # Process ratings
        rating_counter = defaultdict(int)
        
        # Track unique problems
        solved_problems = set()
        
        for submission in submissions:
            if submission['verdict'] == 'OK':
                problem = submission['problem']
                problem_id = (problem['contestId'], problem['index'])
                
                # Only count each problem once
                if problem_id not in solved_problems:
                    solved_problems.add(problem_id)
                    
                    # Count tags
                    for tag in problem.get('tags', []):
                        tags_counter[tag] += 1
                    
                    # Count ratings
                    if 'rating' in problem:
                        rating = problem['rating']
                        rating_counter[rating] += 1
        
        return dict(tags_counter), dict(rating_counter)
    
    def update_tags_chart(self, tags_data):
        # Clear previous figure
        self.tags_canvas.figure.clear()
        
        # Create pie chart
        ax = self.tags_canvas.figure.add_subplot(111)
        
        # Sort tags by count and take top 10
        sorted_tags = dict(sorted(tags_data.items(), key=lambda x: x[1], reverse=True)[:10])
        
        ax.pie(sorted_tags.values(), labels=sorted_tags.keys(), autopct='%1.1f%%')
        ax.set_title("Top 10 Tags Distribution")
        
        self.tags_canvas.draw()
    
    def update_rating_chart(self, rating_data):
        # Clear previous figure
        self.rating_canvas.figure.clear()
        
        # Create bar chart
        ax = self.rating_canvas.figure.add_subplot(111)
        
        # Create rating ranges from 800 to max rating in steps of 100
        max_rating = max(rating_data.keys()) if rating_data else 3500
        rating_ranges = range(800, max_rating + 100, 100)
        
        # Group problems into rating ranges
        range_counts = defaultdict(int)
        for rating, count in rating_data.items():
            if rating >= 800:  # Only consider problems rated 800+
                range_start = (rating // 100) * 100
                range_counts[range_start] += count
        
        # Prepare data for plotting
        heights = [range_counts.get(r, 0) for r in rating_ranges]
        ax.bar(rating_ranges, heights)
        
        # Customize the chart
        ax.set_title("Problems Solved by Rating")
        ax.set_xlabel("Problem Rating")
        ax.set_ylabel("Number of Problems")
        ax.tick_params(axis='x', rotation=45)
        
        # Adjust layout to prevent label cutoff
        self.rating_canvas.figure.tight_layout()
        self.rating_canvas.draw()