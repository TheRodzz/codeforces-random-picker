import random
from collections import Counter
from statistics import median, stdev

# Define the number of recent contests to consider
N_RECENT_CONTESTS = 50

class RecommendationEngine:
    def __init__(self, submissions, all_problems):
        self.submissions = submissions
        self.solved_problem_ids = self._get_solved_problem_ids()
        self.all_problems = self._filter_recent_contests(all_problems)

    def _get_problem_id(self, problem):
        """
        Generate a unique problem ID from contestId and index.
        Handles both Latin (A-Z) and Cyrillic (А-Я) characters.
        """
        index = problem.get('index', 'А')  # Default to Cyrillic 'А'
        if not index:
            return problem.get('contestId', 0) * 100
            
        # Get the first character of the index
        first_char = index[0]
        
        # Handle Cyrillic characters
        if '\u0410' <= first_char <= '\u042F':  # Cyrillic uppercase range А-Я
            index_value = ord(first_char) - ord('А') + 1  # Convert 'А' to 1, 'Б' to 2, etc.
        # Handle Latin characters (as fallback)
        elif 'A' <= first_char <= 'Z':
            index_value = ord(first_char) - ord('A') + 1
        else:
            # If neither Cyrillic nor Latin, default to 1
            index_value = 1
            
        return problem.get('contestId', 0) * 100 + index_value

    def _get_solved_problem_ids(self):
        """Extract IDs of all problems that were successfully solved."""
        return {
            self._get_problem_id(submission['problem'])
            for submission in self.submissions
            if submission['verdict'] == "OK"
        }

    def _filter_recent_contests(self, problems):
        """Filter problems to only include those from recent contests and not already solved."""
        # Get unique contest IDs, sorted in descending order (most recent first)
        contest_ids = sorted(
            {problem.get('contestId') for problem in problems if problem.get('contestId') is not None},
            reverse=True
        )
        
        # Get the N most recent contest IDs
        recent_contest_ids = set(contest_ids[:N_RECENT_CONTESTS])
        
        # Filter problems to only include those from recent contests and not already solved
        return [
            problem for problem in problems
            if problem.get('contestId') in recent_contest_ids
            and self._get_problem_id(problem) not in self.solved_problem_ids
        ]

    def analyze_submissions(self):
        """Analyze submissions to get solved ratings and failed tags."""
        solved_ratings = []
        failed_tags = []
        
        for submission in self.submissions:
            problem = submission['problem']
            tags = problem.get('tags', [])
            rating = problem.get('rating')
            verdict = submission['verdict']
            
            if verdict == "OK" and rating:
                solved_ratings.append(rating)
            elif verdict != "OK":
                failed_tags.extend(tags)
                
        return solved_ratings, failed_tags

    def get_practice_recommendations(self):
        """Get recommendations for practice problems based on user's performance."""
        solved_ratings, failed_tags = self.analyze_submissions()
        
        if not solved_ratings:
            raise Exception("Not enough data to determine solved ratings.")
            
        rating_median = median(solved_ratings)
        rating_stdev = stdev(solved_ratings) if len(solved_ratings) > 1 else 0
        
        target_min = rating_median
        target_max = rating_median + rating_stdev
        
        # Find tags that appear in multiple failed submissions
        weak_tags = [
            tag for tag, count in Counter(failed_tags).items()
            if count > 1
        ]
        
        # Filter recommendations based on rating range and weak tags
        recommendations = [
            problem for problem in self.all_problems
            if problem.get('rating') 
            and target_min <= problem['rating'] <= target_max
            and any(tag in weak_tags for tag in problem.get('tags', []))
        ]
        
        return random.sample(recommendations, min(10, len(recommendations)))

    def get_warmup_recommendations(self):
        """Get recommendations for warmup problems below user's comfort level."""
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