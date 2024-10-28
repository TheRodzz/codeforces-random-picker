from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QFrame, QScrollArea)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import requests
from collections import defaultdict
import numpy as np

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
        
        # Create scroll area for charts
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        charts_widget = QWidget()
        charts_layout = QHBoxLayout(charts_widget)
        
        # Tags pie chart
        tags_frame = QFrame()
        tags_frame.setFrameStyle(QFrame.StyledPanel)
        tags_layout = QVBoxLayout(tags_frame)
        self.tags_canvas = FigureCanvas(plt.Figure(figsize=(8, 8)))
        tags_layout.addWidget(self.tags_canvas)
        charts_layout.addWidget(tags_frame)
        
        # Rating distribution bar chart
        rating_frame = QFrame()
        rating_frame.setFrameStyle(QFrame.StyledPanel)
        rating_layout = QVBoxLayout(rating_frame)
        self.rating_canvas = FigureCanvas(plt.Figure(figsize=(10, 6)))
        rating_layout.addWidget(self.rating_canvas)
        charts_layout.addWidget(rating_frame)
        
        scroll_area.setWidget(charts_widget)
        layout.addWidget(scroll_area)
        
        # Stats summary
        self.stats_label = QLabel()
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setStyleSheet("font-size: 14px; margin: 10px;")
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
                f"Total Problems Solved: {total_solved} | "
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
        
        # Create figure with white background
        self.tags_canvas.figure.set_facecolor('white')
        
        # Create gridspec with more space for legend
        gs = self.tags_canvas.figure.add_gridspec(1, 2, width_ratios=[1, 1.2])
        
        # Create pie chart
        ax_pie = self.tags_canvas.figure.add_subplot(gs[0])
        ax_pie.set_facecolor('white')
        
        # Sort tags by count
        sorted_tags = dict(sorted(tags_data.items(), key=lambda x: x[1], reverse=True))
        
        # Calculate percentages
        total = sum(sorted_tags.values())
        
        # Create distinct colors using qualitative colormaps
        num_tags = len(sorted_tags)
        if num_tags <= 20:
            colors = plt.cm.Set3(np.linspace(0, 1, 12))[:num_tags]  # Using Set3 for better visibility
        else:
            colors1 = plt.cm.Set3(np.linspace(0, 1, 12))
            colors2 = plt.cm.Paired(np.linspace(0, 1, 12))
            colors = np.vstack((colors1, colors2))
            colors = colors[:num_tags]
        
        # Create pie chart without labels
        ax_pie.pie(sorted_tags.values(),
                colors=colors,
                wedgeprops=dict(width=0.6),  # Slightly wider donut
                labels=["" for _ in sorted_tags])
                # autopct=lambda pct: f'{pct:.1f}%' if pct > 4 else '')  # Only show percentages > 4%
        
        # Add title
        ax_pie.set_title("Problem Tags Distribution", pad=10, size=12, weight='bold')
        
        # Create custom legend
        ax_legend = self.tags_canvas.figure.add_subplot(gs[1])
        ax_legend.set_facecolor('white')
        ax_legend.axis('off')
        
        # Create legend entries with more compact format
        legend_elements = []
        legend_labels = []
        for (tag, count), color in zip(sorted_tags.items(), colors):
            percentage = (count / total) * 100
            if percentage > 1.0:  # Only show tags with more than 1% representation
                legend_elements.append(plt.Rectangle((0, 0), 1, 1, fc=color))
                legend_labels.append(f'{tag} ({count})')  # Simplified legend text
        
        # Add legend with better positioning and smaller font
        ax_legend.legend(legend_elements, legend_labels,
                        loc='center left',
                        bbox_to_anchor=(0, 0.5),
                        frameon=False,
                        fontsize=8,
                        ncol=1 if len(legend_labels) > 15 else 2)  # Use 2 columns if fewer items
        
        # Adjust layout with more padding
        self.tags_canvas.figure.tight_layout(pad=1.5)
        
        # Draw the updated chart
        self.tags_canvas.draw()
        
        
    def update_rating_chart(self, rating_data):
        # Clear previous figure
        self.rating_canvas.figure.clear()
        
        # Create figure with white background
        self.rating_canvas.figure.set_facecolor('white')
        ax = self.rating_canvas.figure.add_subplot(111)
        ax.set_facecolor('white')
        
        # Create rating ranges from 800 to max rating in steps of 100
        max_rating = max(rating_data.keys(), default=3500)  # Using default for Python 3.4+
        rating_ranges = list(range(800, max_rating + 100, 100))  # Ensure max_rating is included
        
        # **Force inclusion of all intermediate ratings by initializing range_counts with all ranges**
        range_counts = {r: 0 for r in rating_ranges}
        
        # Group problems into rating ranges
        for rating, count in rating_data.items():
            if rating >= 800:  # Only consider problems rated 800+
                range_start = (rating // 100) * 100
                if range_start in range_counts:  # Safety check
                    range_counts[range_start] += count
        
        # Prepare data for plotting
        heights = [range_counts[r] for r in rating_ranges]
        
        # Create gradient colors
        colors = plt.cm.viridis(np.linspace(0, 0.9, len(rating_ranges)))
        
        # Create bars with gradient colors and rounded corners
        bars = ax.bar(rating_ranges, heights, width=80, color=colors)
        
        # Add value labels on top of each bar
        for bar, height in zip(bars, heights):
            if height > 0:  # Only show label if there are problems
                ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')
            # **Optional: Show 0 for empty ranges if desired**
            # else:
            #     ax.text(bar.get_x() + bar.get_width()/2., 0,
            #            '0',
            #            ha='center', va='bottom')
        
        # Customize the chart
        ax.set_title("Problems Solved by Rating", pad=20, size=14, weight='bold')
        ax.set_xlabel("Problem Rating", size=12)
        ax.set_ylabel("Number of Problems", size=12)
        
        # Ensure all x-axis labels are shown
        ax.set_xticks(rating_ranges)
        ax.tick_params(axis='x', rotation=45)
        
        # Add grid for better readability
        ax.grid(True, axis='y', linestyle='--', alpha=0.3)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Set background color
        ax.set_facecolor('white')
        
        # Adjust layout to prevent label cutoff
        self.rating_canvas.figure.tight_layout()
        
        self.rating_canvas.draw()