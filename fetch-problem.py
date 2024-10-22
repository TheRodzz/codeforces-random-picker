import requests
import random
import time

def get_random_problem(rating):
    """
    Fetch a random Codeforces problem with the specified rating.

    Args:
        rating (int): Desired problem rating

    Returns:
        dict: Problem information including name, rating, and URL
    """
    try:
        # Fetch all problems from Codeforces API
        response = requests.get("https://codeforces.com/api/problemset.problems")
        if response.status_code != 200:
            return "Error: Unable to fetch problems from Codeforces API"

        data = response.json()
        if data["status"] != "OK":
            return "Error: API request failed"

        # Filter problems by rating
        problems = data["result"]["problems"]
        matching_problems = [p for p in problems if p.get("rating") == rating]

        if not matching_problems:
            return f"No problems found with rating {rating}"

        # Select a random problem
        problem = random.choice(matching_problems)

        # Create problem URL
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

def main():
    try:
        rating = int(input("Enter the desired problem rating: "))
        if rating < 800 or rating > 3500:
            print("Please enter a rating between 800 and 3500")
            return

        print("\nFetching problem...")
        result = get_random_problem(rating)

        if isinstance(result, str):
            print(result)
        else:
            print("\nFound problem:")
            print(f"Name: {result['name']}")
            print(f"Rating: {result['rating']}")
            print(f"URL: {result['url']}")
            print("Tags:", ", ".join(result['tags']))

    except ValueError:
        print("Please enter a valid number")

if __name__ == "__main__":
    main()
