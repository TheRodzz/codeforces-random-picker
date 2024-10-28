import requests

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