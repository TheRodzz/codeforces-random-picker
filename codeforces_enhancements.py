import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3

class CodeforcesEnhancements:
    def __init__(self, parent_app):
        self.app = parent_app
        self.db_path = 'codeforces_cache.db'
        self.setup_database()
        
        # Add username frame before the rating frame
        self.create_username_frame()
        self.create_profile_frame()
        self.create_analytics_frame()
        self.setup_bookmarks()
        
    def setup_database(self):
        """Initialize SQLite database for caching and bookmarks."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS problems_cache
                    (problem_id TEXT PRIMARY KEY, data TEXT, timestamp DATETIME)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS bookmarks
                    (problem_id TEXT PRIMARY KEY, user_id TEXT,
                     added_date DATETIME, notes TEXT)''')
        
        conn.commit()
        conn.close()

    def create_username_frame(self):
        """Create username input frame."""
        username_frame = ttk.LabelFrame(self.app.settings_frame, text="Username")
        username_frame.pack(side='left', padx=10, fill='x', expand=True, before=self.app.settings_frame.winfo_children()[0])
        
        self.app.username_var = tk.StringVar()
        self.app.username_entry = ttk.Entry(
            username_frame,
            textvariable=self.app.username_var,
            width=20
        )
        self.app.username_entry.pack(side='left', padx=5)
    
    def create_profile_frame(self):
        """Create and populate user profile section."""
        profile_frame = ttk.LabelFrame(self.app.root, text="User Profile")
        profile_frame.pack(fill='x', pady=10, after=self.app.root.winfo_children()[0])
        
        # Profile labels
        self.profile_labels = {
            'rating': ttk.Label(profile_frame, text="Rating: --"),
            'rank': ttk.Label(profile_frame, text="Rank: --"),
            'solved': ttk.Label(profile_frame, text="Problems Solved: --"),
            'streak': ttk.Label(profile_frame, text="Current Streak: --")
        }
        
        for label in self.profile_labels.values():
            label.pack(side='left', padx=10)
            
        # Refresh button
        ttk.Button(
            profile_frame,
            text="Refresh Profile",
            command=self.update_user_profile
        ).pack(side='right', padx=10)
    def create_analytics_frame(self):
        """Create analytics section with difficulty histogram."""
        self.analytics_frame = ttk.LabelFrame(self.app.root, text="Analytics")
        self.analytics_frame.pack(fill='both', expand=True, pady=10)
        
        # Create difficulty histogram
        fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(fig, master=self.analytics_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def update_user_profile(self):
        """Fetch and update user profile information."""
        username = self.app.username_var.get().strip()
        if not username:
            return
            
        try:
            response = requests.get(f"https://codeforces.com/api/user.info?handles={username}")
            data = response.json()
            
            if data['status'] == 'OK':
                user = data['result'][0]
                self.profile_labels['rating'].config(
                    text=f"Rating: {user.get('rating', '--')}")
                self.profile_labels['rank'].config(
                    text=f"Rank: {user.get('rank', '--')}")
                
                # Update solved problems count
                solved = len(self.app.solved_problems)
                self.profile_labels['solved'].config(
                    text=f"Problems Solved: {solved}")
                
                # Calculate streak
                streak = self.calculate_streak(username)
                self.profile_labels['streak'].config(
                    text=f"Current Streak: {streak} days")
                
                # Update difficulty histogram
                self.update_difficulty_histogram()
                
        except Exception as e:
            self.app.show_error(f"Failed to update profile: {str(e)}")
    
    def calculate_streak(self, username: str) -> int:
        """Calculate current problem-solving streak."""
        try:
            response = requests.get(
                f"https://codeforces.com/api/user.status?handle={username}")
            data = response.json()
            
            if data['status'] != 'OK':
                return 0
                
            submissions = data['result']
            if not submissions:
                return 0
            
            # Sort submissions by time
            submissions.sort(key=lambda x: x['creationTimeSeconds'], reverse=True)
            
            current_date = datetime.now().date()
            streak = 0
            seen_dates = set()
            
            for submission in submissions:
                sub_date = datetime.fromtimestamp(
                    submission['creationTimeSeconds']).date()
                
                # Break if we find a gap in the streak
                if current_date - sub_date > timedelta(days=1):
                    break
                    
                if sub_date not in seen_dates and submission['verdict'] == 'OK':
                    seen_dates.add(sub_date)
                    streak += 1
                    current_date = sub_date
            
            return streak
            
        except Exception:
            return 0
    
    def update_difficulty_histogram(self):
        """Update the difficulty distribution histogram."""
        if not self.app.problems_data:  # Changed from self.problems_data to self.app.problems_data
            return
            
        # Clear previous plot
        self.ax.clear()
        
        # Get difficulty distribution
        difficulties = [p['rating'] for p in self.app.problems_data if 'rating' in p]  # Changed to self.app.problems_data
        
        if difficulties:
            self.ax.hist(difficulties, bins=20, edgecolor='black')
            self.ax.set_title('Problem Difficulty Distribution')
            self.ax.set_xlabel('Difficulty Rating')
            self.ax.set_ylabel('Number of Problems')
            self.canvas.draw()
    
    def setup_bookmarks(self):
        """Initialize bookmarks functionality."""
        # Add bookmark button to tree context menu
        self.app.tree.bind('<Button-3>', self.show_context_menu)
        
        # Create context menu
        self.context_menu = tk.Menu(self.app.root, tearoff=0)
        self.context_menu.add_command(
            label="Bookmark Problem",
            command=self.bookmark_selected_problem
        )
    
    def show_context_menu(self, event):
        """Show context menu on right click."""
        item = self.app.tree.identify_row(event.y)
        if item:
            self.app.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def bookmark_selected_problem(self):
        """Add selected problem to bookmarks."""
        selected = self.app.tree.selection()
        if not selected:
            return
            
        item = selected[0]
        contest_id, index = self.app.tree.item(item)['tags']
        problem_id = f"{contest_id},{index}"
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        try:
            c.execute('''INSERT INTO bookmarks (problem_id, user_id, added_date)
                        VALUES (?, ?, ?)''',
                     (problem_id, self.app.username_var.get(), datetime.now()))
            conn.commit()
            self.app.show_info("Problem bookmarked successfully!")
            
        except sqlite3.IntegrityError:
            self.app.show_info("This problem is already bookmarked!")
            
        finally:
            conn.close()

# Extension method for the main app
def show_info(self, message):
    """Display info message."""
    messagebox.showinfo("Information", message)