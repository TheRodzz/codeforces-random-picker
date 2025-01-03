from PyQt5.QtCore import QThread, pyqtSignal
import requests
from src.recommendation import RecommendationEngine

class DataFetcher(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, username, min_rating, max_rating, contest_limit, tags=None, recommendation_type=None):
        super().__init__()
        self.username = username
        self.min_rating = min_rating
        self.max_rating = max_rating
        self.contest_limit = contest_limit
        self.tags = tags
        self.recommendation_type = recommendation_type
        self.CODEFORCES_API_URL = 'https://codeforces.com/api'

    def run(self):
        try:
            if self.recommendation_type == 'practice':
                problems = self.get_practice_recommendations()
            elif self.recommendation_type == 'warmup':
                problems = self.get_warmup_recommendations()
            else:
                problems = self.get_problems()
            if problems:
                self.finished.emit(problems)
            else:
                self.error.emit("No problems found matching the criteria")
        except Exception as e:
            self.error.emit(str(e))

    def get_user_submissions(self):
        url = f"{self.CODEFORCES_API_URL}/user.status?handle={self.username}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Failed to fetch user submissions")
        return response.json()['result']

    def get_unsolved_problems(self):
        url = f"{self.CODEFORCES_API_URL}/problemset.problems"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Failed to fetch unsolved problems")
        problems_data = response.json()['result']['problems']
        return [{
            'name': problem.get('name'),
            'rating': problem.get('rating', 0),
            'contestId': problem.get('contestId'),
            'index': problem.get('index'),
            'tags': problem.get('tags', []),
            'url': f"https://codeforces.com/problemset/problem/{problem.get('contestId')}/{problem.get('index')}"
        } for problem in problems_data]

    def get_practice_recommendations(self):
        submissions = self.get_user_submissions()
        all_problems = self.get_unsolved_problems()
        recommendation_engine = RecommendationEngine(submissions, all_problems)
        return recommendation_engine.get_practice_recommendations()

    def get_warmup_recommendations(self):
        submissions = self.get_user_submissions()
        all_problems = self.get_unsolved_problems()
        recommendation_engine = RecommendationEngine(submissions, all_problems)
        return recommendation_engine.get_warmup_recommendations()

    def get_problems(self):
        # Get solved problems for the user
        solved_problems = self.get_solved_problems()
        
        # Fetch all problems
        all_problems = self.get_unsolved_problems()
        
        # Filter problems based on criteria
        return self.filter_problems(all_problems, solved_problems)

    def get_solved_problems(self):
        user_url = f"{self.CODEFORCES_API_URL}/user.status?handle={self.username}"
        user_response = requests.get(user_url)
        if user_response.status_code != 200:
            raise Exception("Failed to fetch user data")
        
        solved_problems = set()
        for submission in user_response.json()['result']:
            if submission['verdict'] == 'OK':
                problem = submission['problem']
                solved_problems.add(f"{problem.get('contestId')}_{problem.get('index')}")
        
        return solved_problems

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
                problem_id not in solved_problems and
                (not self.tags or any(tag in problem.get('tags', []) for tag in self.tags))):
                
                if contest_id not in seen_contest_ids:
                    seen_contest_ids.add(contest_id)
                
                filtered_problems.append(problem)
        
        return filtered_problems