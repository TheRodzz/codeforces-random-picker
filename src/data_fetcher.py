
from PyQt5.QtCore import QThread, pyqtSignal

import requests
from collections import Counter
from statistics import median, stdev
import random

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
        self.CODEFORCES_API_URL='https://codeforces.com/api'

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

    def analyze_submissions(self, submissions):
        solved_ratings = []
        failed_tags = []

        for submission in submissions:
            problem = submission['problem']
            tags = problem.get('tags', [])
            rating = problem.get('rating')
            verdict = submission['verdict']
            
            if verdict == "OK":
                if rating:
                    solved_ratings.append(rating)
            else:
                failed_tags.extend(tags)
        
        return solved_ratings, failed_tags

    def get_practice_recommendations(self):
        submissions = self.get_user_submissions()
        solved_ratings, failed_tags = self.analyze_submissions(submissions)

        if not solved_ratings:
            raise Exception("Not enough data to determine solved ratings.")

        rating_median = median(solved_ratings)
        rating_stdev = stdev(solved_ratings) if len(solved_ratings) > 1 else 0
        target_min = rating_median
        target_max = rating_median + rating_stdev

        weak_tags = [tag for tag, count in Counter(failed_tags).items() if count > 1]
        
        all_problems = self.get_unsolved_problems()
        recommendations = [
            problem for problem in all_problems
            if problem.get('rating') and target_min <= problem['rating'] <= target_max
            and any(tag in weak_tags for tag in problem['tags'])
        ]

        return random.sample(recommendations, min(10, len(recommendations)))

    def get_warmup_recommendations(self):
        submissions = self.get_user_submissions()
        solved_ratings, _ = self.analyze_submissions(submissions)

        if not solved_ratings:
            raise Exception("Not enough data to determine solved ratings.")

        rating_median = median(solved_ratings)
        rating_stdev = stdev(solved_ratings) if len(solved_ratings) > 1 else 0
        comfort_max = rating_median - rating_stdev

        all_problems = self.get_unsolved_problems()
        recommendations = [
            problem for problem in all_problems
            if problem.get('rating') and problem['rating'] <= comfort_max
        ]

        return random.sample(recommendations, min(10, len(recommendations)))

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