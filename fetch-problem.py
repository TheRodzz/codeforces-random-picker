import tkinter as tk
from tkinter import ttk, messagebox
import requests
import random
import webbrowser
from threading import Thread

class CodeforcesGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Codeforces Problem Finder")
        self.root.geometry("600x400")
        self.root.configure(padx=20, pady=20)

        # Style configuration
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TLabel', padding=5)
        style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))

        # Header
        header = ttk.Label(
            root, 
            text="Codeforces Random Problem Finder", 
            style='Header.TLabel'
        )
        header.pack(pady=10)

        # Rating frame
        rating_frame = ttk.Frame(root)
        rating_frame.pack(fill='x', pady=10)

        ttk.Label(
            rating_frame, 
            text="Problem Rating:"
        ).pack(side='left', padx=5)

        # Create rating dropdown with common Codeforces ratings
        self.ratings = [800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 
                       1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 
                       2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 
                       3200, 3300, 3400, 3500]
        
        self.rating_var = tk.StringVar(value="1400")
        rating_dropdown = ttk.Combobox(
            rating_frame, 
            textvariable=self.rating_var,
            values=self.ratings,
            width=10
        )
        rating_dropdown.pack(side='left', padx=5)

        # Find button
        self.find_button = ttk.Button(
            root,
            text="Find Problem",
            command=self.find_problem_thread
        )
        self.find_button.pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(
            root,
            mode='indeterminate',
            length=400
        )
        self.progress.pack(pady=10)

        # Result frame
        self.result_frame = ttk.Frame(root)
        self.result_frame.pack(fill='both', expand=True, pady=10)

        # Problem details
        self.problem_name = ttk.Label(
            self.result_frame,
            text="",
            wraplength=500
        )
        self.problem_name.pack(pady=5)

        self.problem_rating = ttk.Label(
            self.result_frame,
            text=""
        )
        self.problem_rating.pack(pady=5)

        self.problem_tags = ttk.Label(
            self.result_frame,
            text="",
            wraplength=500
        )
        self.problem_tags.pack(pady=5)

        # Open in browser button (initially hidden)
        self.open_button = ttk.Button(
            self.result_frame,
            text="Open in Browser",
            command=self.open_in_browser
        )
        self.current_url = None

    def get_random_problem(self, rating):
        """Fetch a random Codeforces problem with the specified rating."""
        try:
            response = requests.get("https://codeforces.com/api/problemset.problems")
            if response.status_code != 200:
                return "Error: Unable to fetch problems from Codeforces API"
            
            data = response.json()
            if data["status"] != "OK":
                return "Error: API request failed"
            
            problems = data["result"]["problems"]
            matching_problems = [p for p in problems if p.get("rating") == rating]
            
            if not matching_problems:
                return f"No problems found with rating {rating}"
            
            problem = random.choice(matching_problems)
            problem_url = f"https://codeforces.com/problemset/problem/{problem['contestId']}/{problem['index']}"
            
            return {
                "name": problem["name"],
                "rating": problem["rating"],
                "url": problem_url,
                "tags": problem.get("tags", [])
            }
            
        except requests.exceptions.RequestException:
            return "Error: Network error occurred"
        except (KeyError, ValueError):
            return "Error: Invalid response format from API"

    def find_problem_thread(self):
        """Start a new thread to fetch the problem."""
        self.find_button.config(state='disabled')
        self.progress.start()
        Thread(target=self.find_problem).start()

    def find_problem(self):
        """Fetch and display a random problem."""
        try:
            rating = int(self.rating_var.get())
            result = self.get_random_problem(rating)
            
            if isinstance(result, str):
                self.show_error(result)
            else:
                self.display_problem(result)
                
        except ValueError:
            self.show_error("Please enter a valid rating")
        finally:
            self.root.after(0, self.cleanup_after_search)

    def display_problem(self, problem):
        """Display the problem details in the GUI."""
        def update_ui():
            self.problem_name.config(
                text=f"Problem: {problem['name']}"
            )
            self.problem_rating.config(
                text=f"Rating: {problem['rating']}"
            )
            self.problem_tags.config(
                text=f"Tags: {', '.join(problem['tags'])}"
            )
            self.current_url = problem['url']
            self.open_button.pack(pady=10)
        
        self.root.after(0, update_ui)

    def cleanup_after_search(self):
        """Reset UI elements after search completes."""
        self.find_button.config(state='normal')
        self.progress.stop()

    def show_error(self, message):
        """Display error message."""
        messagebox.showerror("Error", message)

    def open_in_browser(self):
        """Open the problem in default web browser."""
        if self.current_url:
            webbrowser.open(self.current_url)

def main():
    root = tk.Tk()
    app = CodeforcesGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()