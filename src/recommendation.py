import random
from collections import Counter
from statistics import median, stdev

class RecommendationEngine:
    def __init__(self, submissions, all_problems):
        self.submissions = submissions
        self.all_problems = all_problems

    def analyze_submissions(self):
        solved_ratings = []
        failed_tags = []

        for submission in self.submissions:
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
        solved_ratings, failed_tags = self.analyze_submissions()

        if not solved_ratings:
            raise Exception("Not enough data to determine solved ratings.")

        rating_median = median(solved_ratings)
        rating_stdev = stdev(solved_ratings) if len(solved_ratings) > 1 else 0
        target_min = rating_median
        target_max = rating_median + rating_stdev

        weak_tags = [tag for tag, count in Counter(failed_tags).items() if count > 1]
        
        recommendations = [
            problem for problem in self.all_problems
            if problem.get('rating') and target_min <= problem['rating'] <= target_max
            and any(tag in weak_tags for tag in problem['tags'])
        ]

        return random.sample(recommendations, min(10, len(recommendations)))

    def get_warmup_recommendations(self):
        solved_ratings, _ = self.analyze_submissions()

        if not solved_ratings:
            raise Exception("Not enough data to determine solved ratings.")

        rating_median = median(solved_ratings)
        rating_stdev = stdev(solved_ratings) if len(solved_ratings) > 1 else 0
        comfort_max = rating_median - rating_stdev

        recommendations = [
            problem for problem in self.all_problems
            if problem.get('rating') and problem['rating'] <= comfort_max
        ]

        return random.sample(recommendations, min(10, len(recommendations)))