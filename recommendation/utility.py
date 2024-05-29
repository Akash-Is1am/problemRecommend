import os
import json
import math


# Initialize the tags list
tags = ['greedy', 'math', 'constructive', 'data structure', 'graph', 'dp', 'games']


# Function to get the current script's directory
def get_current_directory():
    return os.path.dirname(__file__)


def get_solved_ids():
    current_directory = os.path.dirname(os.path.abspath(__file__))  # Current script directory
    solved_problems_path = os.path.join(current_directory, 'solved_problems.json')  # Solved problems file path
    
    with open(solved_problems_path, 'r') as file:
        solved_problem_ids = json.load(file)  # List of solved problem IDs

    solved_ids = {}

    for id in solved_problem_ids:
        solved_ids[id] = '1'
    
    return solved_ids
    


# Function to count easy, mid, and hard problem counts for a list of tags
def count_problems_for_tags():
    # Initialize the tag counts dictionary
    tag_counts = {tag: {"Easy": 0, "Medium": 0, "Hard": 0} for tag in tags}
    
    # Define the current directory and file paths
    current_directory = os.path.dirname(os.path.abspath(__file__))  # Current script directory
    solved_problems_path = os.path.join(current_directory, 'solved_problems.json')  # Solved problems file path
    all_problems_path = os.path.join(current_directory, 'all_problems.json')  # All problems file path
    
    # Load the solved problem IDs
    with open(solved_problems_path, 'r') as file:
        solved_problem_ids = json.load(file)  # List of solved problem IDs

    # Load all problems
    with open(all_problems_path, 'r') as file:
        all_problems = json.load(file)  # List of all problems

    # Create a lookup dictionary for all problems based on their ID
    all_problems_lookup = {problem['_id']: problem for problem in all_problems}

    # Count the problems based on their level and tags
    for solved_id in solved_problem_ids:
        if solved_id in all_problems_lookup:
            problem = all_problems_lookup[solved_id]
            level = problem.get('level', '')
            if level not in ["Easy", "Medium", "Hard"]:
                continue  # Skip if the level is not recognized

            # Increment the count for each tag that matches the predefined tags
            for tag in tags:
                if tag in problem.get('tags', []):
                    tag_counts[tag][level] += 1

    return tag_counts

skill_problem_distribution = [
    [30, 1, 0.04],    # Skill level 0
    [20, 1.2, 0.1],    # Skill level 1
    [15, 1.5, 0.4],    # Skill level 2
    [8, 2.2, 0.8],    # Skill level 3
    [4, 6, 1],    # Skill level 4
    [3, 10, 3],    # Skill level 5
    [1, 15, 10],    # Skill level 6
    [0.7, 12, 9],    # Skill level 7
    [0.4,  8, 5],    # Skill level 8
    [0.1,  10, 11],    # Skill level 9
    [0.01,  15, 20],    # Skill level 10
]

def benefit_array(easy, mid, hard, skill):
    ratio_total = 0
    for _ in range(3):
        ratio_total = ratio_total + skill_problem_distribution[skill][_]
    
    solved_total = easy + mid + hard
    
    easy_exp = solved_total * skill_problem_distribution[skill][0] / ratio_total
    mid_exp = solved_total * skill_problem_distribution[skill][1] / ratio_total
    hard_exp = solved_total * skill_problem_distribution[skill][2] / ratio_total

    diff_easy = max(0, easy_exp - easy)
    diff_mid = max(0, mid_exp - mid)
    diff_hard = max(0, hard_exp - hard)

    ans = [diff_easy, diff_mid, diff_hard]

    if diff_easy + diff_mid + diff_hard == 0:
        ans = []
        for _ in range(3):
            ans.append(skill_problem_distribution[skill][_])

    return ans

def get_sum_array(priority_array):
    n = len(priority_array)  # Length of the array
    total_sum = sum(priority_array)  # Calculate the sum
    average = total_sum / n  # Calculate the average
    max_value = max(priority_array)  # Get the maximum value

    # Calculate variance for standard deviation
    variance = sum((x - average) ** 2 for x in priority_array) / n
    standard_deviation = math.sqrt(variance)  # Calculate the standard deviation

    return [total_sum, average, max_value, standard_deviation]



def get_score(sum_array):
    total_sum = sum_array[0]  # Retrieve the sum
    average = sum_array[1]  # Retrieve the average
    max_value = sum_array[2]  # Retrieve the maximum value
    standard_deviation = sum_array[3]  # Retrieve the standard deviation

    # Calculate the score using the given formula
    score = (total_sum * 1) + (max_value * 1.5) + (standard_deviation * 0.5) + (average * 1)
    return score
