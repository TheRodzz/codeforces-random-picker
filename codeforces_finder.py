import tkinter as tk
from tkinter import ttk, messagebox
import requests
from threading import Thread
import webbrowser
from datetime import datetime
import random
import subprocess
import sys
import os

class CodeforcesGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Codeforces Problem Finder")
        self.root.geometry("1000x800")
        self.root.configure(padx=20, pady=20)

        # Style configuration
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TLabel', padding=5)
        style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))

        # Header
        header = ttk.Label(
            root, 
            text="Codeforces Problem Finder", 
            style='Header.TLabel'
        )
        header.pack(pady=10)


        # Settings frame
        self.settings_frame = ttk.Frame(root)
        self.settings_frame.pack(fill='x', pady=10)

        # Rating range frame
        rating_frame = ttk.LabelFrame(self.settings_frame, text="Rating Range")
        rating_frame.pack(side='left', padx=10, fill='x', expand=True)

        # Rating range inputs
        self.ratings = [800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 
                       1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 
                       2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 
                       3200, 3300, 3400, 3500]

        ttk.Label(rating_frame, text="From:").pack(side='left', padx=5)
        self.rating_from = ttk.Combobox(
            rating_frame,
            values=self.ratings,
            width=8
        )
        self.rating_from.set("800")
        self.rating_from.pack(side='left', padx=5)

        ttk.Label(rating_frame, text="To:").pack(side='left', padx=5)
        self.rating_to = ttk.Combobox(
            rating_frame,
            values=self.ratings,
            width=8
        )
        self.rating_to.set("3500")
        self.rating_to.pack(side='left', padx=5)

        # Sort options frame
        sort_frame = ttk.LabelFrame(self.settings_frame, text="Sort By")
        sort_frame.pack(side='left', padx=10, fill='x', expand=True)

        self.sort_var = tk.StringVar(value="rating")
        sort_options = [
            ("Rating", "rating"),
            ("Contest ID", "contestId"),
            ("Solved Count", "solvedCount"),
            ("Difficulty", "rating")
        ]

        for text, value in sort_options:
            ttk.Radiobutton(
                sort_frame,
                text=text,
                value=value,
                variable=self.sort_var
            ).pack(side='left', padx=5)

        # Order direction
        self.order_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            sort_frame,
            text="Ascending",
            variable=self.order_var
        ).pack(side='left', padx=5)

        # Show tags checkbox
        self.show_tags_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.settings_frame,
            text="Show Tags",
            variable=self.show_tags_var,
            command=self.update_problems_display
        ).pack(side='left', padx=10)

        # Find button
        self.find_button = ttk.Button(
            root,
            text="Find Problems",
            command=self.find_problems_thread
        )
        self.find_button.pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(
            root,
            mode='indeterminate',
            length=400
        )
        self.progress.pack(pady=10)

        # Create Treeview for problems
        self.create_problem_tree()

        # Store problems data
        self.problems_data = []
        self.solved_problems = set()

        # Random button (moved to bottom)
        self.random_button = ttk.Button(
            root,
            text="Pick Random Problem",
            command=self.pick_random_problem
        )
        self.random_button.pack(pady=10)
        from codeforces_enhancements import CodeforcesEnhancements
        self.enhancements = CodeforcesEnhancements(self)
        
    def pick_random_problem(self):
        """Pick a random problem from the displayed list and open it."""
        if self.problems_data:
            random_problem = random.choice(self.problems_data)
            contest_id = random_problem['contestId']
            index = random_problem['index']
            url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
            webbrowser.open(url)
        else:
            self.show_error("No problems found. Please perform a search first.")
    def create_problem_tree(self):
        """Create and configure the Treeview for displaying problems."""
        columns = ('name', 'rating', 'solved_count', 'tags')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        
        # Configure columns
        self.tree.heading('name', text='Problem Name', command=lambda: self.sort_problems('name'))
        self.tree.heading('rating', text='Rating', command=lambda: self.sort_problems('rating'))
        self.tree.heading('solved_count', text='Solved Count', command=lambda: self.sort_problems('solvedCount'))
        self.tree.heading('tags', text='Tags', command=lambda: self.sort_problems('tags'))

        # Set column widths
        self.tree.column('name', width=300)
        self.tree.column('rating', width=100)
        self.tree.column('solved_count', width=100)
        self.tree.column('tags', width=400)

        # Add scrollbars
        scrollbar_y = ttk.Scrollbar(self.root, orient='vertical', command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(self.root, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Create a frame for browser buttons
        browser_frame = ttk.Frame(self.root)
        
        # Create browser-specific buttons
        firefox_button = ttk.Button(
            browser_frame,
            text="Open in Firefox",
            command=lambda: self.open_problem_in_browser('firefox')
        )
        chrome_button = ttk.Button(
            browser_frame,
            text="Open in Chrome",
            command=lambda: self.open_problem_in_browser('chrome')
        )

        # Pack browser buttons
        firefox_button.pack(side='left', padx=5)
        chrome_button.pack(side='left', padx=5)

        # Pack everything
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x.pack(side='bottom', fill='x')
        self.tree.pack(fill='both', expand=True)
        browser_frame.pack(pady=10)
    def get_browser_path(self, browser):
        """Get the path to the browser executable based on the operating system."""
        if sys.platform.startswith('win'):  # Windows
            if browser == 'chrome':
                paths = [
                    os.path.join(os.environ.get('PROGRAMFILES', ''), 'Google/Chrome/Application/chrome.exe'),
                    os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Google/Chrome/Application/chrome.exe')
                ]
            else:  # firefox
                paths = [
                    os.path.join(os.environ.get('PROGRAMFILES', ''), 'Mozilla Firefox/firefox.exe'),
                    os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Mozilla Firefox/firefox.exe')
                ]
        elif sys.platform.startswith('darwin'):  # macOS
            if browser == 'chrome':
                paths = ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome']
            else:  # firefox
                paths = ['/Applications/Firefox.app/Contents/MacOS/firefox']
        else:  # Linux
            if browser == 'chrome':
                paths = ['google-chrome', 'google-chrome-stable']
            else:  # firefox
                paths = ['firefox']

        # For Linux, try to find the browser in PATH
        if not sys.platform.startswith('win') and not sys.platform.startswith('darwin'):
            for path in paths:
                try:
                    return subprocess.check_output(['which', path]).decode().strip()
                except subprocess.CalledProcessError:
                    continue

        # For Windows and macOS, check if the paths exist
        else:
            for path in paths:
                if os.path.exists(path):
                    return path

        return None
    
    def open_problem_in_browser(self, browser):
        """Open the selected problem in the specified browser."""
        selected_items = self.tree.selection()
        if not selected_items:
            self.show_error("Please select a problem first")
            return

        selected_item = selected_items[0]
        contest_id, index = self.tree.item(selected_item)['tags']
        url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"

        browser_path = self.get_browser_path(browser)
        if browser_path:
            try:
                if sys.platform.startswith('win'):
                    subprocess.Popen([browser_path, url])
                else:
                    subprocess.Popen([browser_path, '-new-tab', url])
            except subprocess.SubprocessError:
                self.show_error(f"Failed to open {browser}. Using default browser instead.")
                webbrowser.open(url)
        else:
            self.show_error(f"{browser.title()} not found. Using default browser instead.")
            webbrowser.open(url)

    def pick_random_problem(self):
        """Pick a random problem from the displayed list and open it."""
        if self.problems_data:
            random_problem = random.choice(self.problems_data)
            contest_id = random_problem['contestId']
            index = random_problem['index']
            url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
            
            # Show a dialog to choose the browser
            dialog = tk.Toplevel(self.root)
            dialog.title("Choose Browser")
            dialog.geometry("200x100")
            dialog.transient(self.root)
            
            ttk.Button(
                dialog,
                text="Open in Firefox",
                command=lambda: self.open_random_problem(url, 'firefox', dialog)
            ).pack(pady=5)
            
            ttk.Button(
                dialog,
                text="Open in Chrome",
                command=lambda: self.open_random_problem(url, 'chrome', dialog)
            ).pack(pady=5)
        else:
            self.show_error("No problems found. Please perform a search first.")

    def open_random_problem(self, url, browser, dialog):
        """Open the random problem in the specified browser and close the dialog."""
        browser_path = self.get_browser_path(browser)
        if browser_path:
            try:
                if sys.platform.startswith('win'):
                    subprocess.Popen([browser_path, url])
                else:
                    subprocess.Popen([browser_path, '-new-tab', url])
            except subprocess.SubprocessError:
                self.show_error(f"Failed to open {browser}. Using default browser instead.")
                webbrowser.open(url)
        else:
            self.show_error(f"{browser.title()} not found. Using default browser instead.")
            webbrowser.open(url)
        dialog.destroy()

    def get_user_solved_problems(self, username):
        """Fetch solved problems for a given username."""
        try:
            response = requests.get(f"https://codeforces.com/api/user.status?handle={username}")
            if response.status_code != 200:
                return "Error: Unable to fetch user data from Codeforces API"
            
            data = response.json()
            if data["status"] != "OK":
                return "Error: Invalid username or API request failed"
            
            # Get unique problems that were solved (verdict="OK")
            solved = {
                f"{submission['problem']['contestId']},{submission['problem']['index']}"
                for submission in data["result"]
                if submission["verdict"] == "OK"
            }
            
            return solved
            
        except requests.exceptions.RequestException:
            return "Error: Network error occurred"
        except (KeyError, ValueError):
            return "Error: Invalid response format from API"

    def get_problems(self, rating_from, rating_to):
        """Fetch problems from Codeforces API within rating range."""
        try:
            response = requests.get("https://codeforces.com/api/problemset.problems")
            if response.status_code != 200:
                return "Error: Unable to fetch problems from Codeforces API"
            
            data = response.json()
            if data["status"] != "OK":
                return "Error: API request failed"
            
            problems = data["result"]["problems"]
            statistics = data["result"]["problemStatistics"]

            # Create solved count dictionary
            solved_counts = {
                f"{stat['contestId']},{stat['index']}": stat.get('solvedCount', 0)
                for stat in statistics
            }

            # Filter problems by rating range and unsolved status
            matching_problems = [
                {**p, 'solvedCount': solved_counts.get(f"{p['contestId']},{p['index']}", 0)}
                for p in problems
                if p.get('rating') is not None 
                and rating_from <= p['rating'] <= rating_to
                and f"{p['contestId']},{p['index']}" not in self.solved_problems
            ]
            
            return matching_problems
            
        except requests.exceptions.RequestException:
            return "Error: Network error occurred"
        except (KeyError, ValueError):
            return "Error: Invalid response format from API"

    def find_problems_thread(self):
        """Start a new thread to fetch problems."""
        self.find_button.config(state='disabled')
        self.progress.start()
        Thread(target=self.find_problems).start()

    def find_problems(self):
        """Fetch and display problems."""
        try:
            username = self.username_var.get().strip()
            if username:
                solved_result = self.get_user_solved_problems(username)
                if isinstance(solved_result, str):
                    self.show_error(solved_result)
                    return
                self.solved_problems = solved_result
                if hasattr(self, 'enhancements'):
                    self.enhancements.update_user_profile()
            else:
                self.solved_problems = set()

            rating_from = int(self.rating_from.get())
            rating_to = int(self.rating_to.get())
            
            if rating_from > rating_to:
                self.show_error("'From' rating must be less than or equal to 'To' rating")
                return
                
            result = self.get_problems(rating_from, rating_to)
            
            if isinstance(result, str):
                self.show_error(result)
            else:
                self.problems_data = result
                self.update_problems_display()
                
                if hasattr(self, 'enhancements'):
                    self.enhancements.update_difficulty_histogram()
                
        except ValueError:
            self.show_error("Please enter valid ratings")
        finally:
            self.root.after(0, self.cleanup_after_search)
            
    def show_info(self, message):
        """Display info message."""
        messagebox.showinfo("Information", message)
        
    def update_problems_display(self):
        """Update the problems displayed in the Treeview."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Sort problems
        sort_key = self.sort_var.get()
        reverse = not self.order_var.get()
        
        sorted_problems = sorted(
            self.problems_data,
            key=lambda x: (x.get(sort_key, 0) if sort_key != 'name' else x['name']),
            reverse=reverse
        )

        # Add problems to treeview
        for problem in sorted_problems:
            tags = ', '.join(problem['tags']) if self.show_tags_var.get() else ''
            self.tree.insert('', 'end', values=(
                problem['name'],
                problem['rating'],
                problem.get('solvedCount', 'N/A'),
                tags
            ), tags=(str(problem['contestId']), problem['index']))

    def open_problem(self, event):
        """Open the selected problem in web browser."""
        selected_item = self.tree.selection()[0]
        contest_id, index = self.tree.item(selected_item)['tags']
        url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
        webbrowser.open(url)

    def cleanup_after_search(self):
        """Reset UI elements after search completes."""
        self.find_button.config(state='normal')
        self.progress.stop()

    def show_info(self, message):
        """Display info message."""
        messagebox.showinfo("Information", message)

    def show_error(self, message):
        """Display error message."""
        messagebox.showerror("Error", message)

def main():
    root = tk.Tk()
    app = CodeforcesGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()