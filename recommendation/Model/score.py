import os
import json
import math


# Initialize the tags list
tags = ['greedy', 'math', 'constructive', 'data structure', 'graph', 'dp', 'games']


# Function to get the current script's directory
def get_current_directory():
    return os.path.dirname(__file__)

# Function to count easy, mid, and hard problem counts for a list of tags
def count_problems_for_tags():
    # Initialize the tag counts dictionary
    global tags
    tag_counts = {tag: {"Easy": 0, "Medium": 0, "Hard": 0} for tag in tags}
    
    # Define the current directory and file paths
    current_directory = os.path.dirname(os.path.abspath(__file__))
    solved_problems_path = os.path.join(current_directory, 'dataset', 'temp_solve.json')
    
    # Load the solved problem IDs
    with open(solved_problems_path, 'r') as file:
      solved_problems = json.load(file)  # List of solved problem

    for problem in solved_problems:
      problem_tags = problem.get("tags", [])
      level = problem.get("level", "Unknown")  # Default to 'Unknown' if 'level' key is missing

      if level in ["Easy", "Medium", "Hard"]:
        for tag in problem_tags:
          if tag in tag_counts:  # Ensure the tag is in the expected list
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


def get_priority_array(tag_priority):
  
  current_directory = os.path.dirname(os.path.abspath(__file__))
  new_problem_path = os.path.join(current_directory, 'dataset', 'temp_new.json')

  with open(new_problem_path, 'r') as file:
    new_problem = json.load(file)
  
  priority_array = [0] * 7
  
  for problem in new_problem:
    level = problem['level']
    problem_tags = problem['tags']
    for i, tag in enumerate(tags):
      if tag in problem_tags:
        priority_array[i] = tag_priority[tag][level]
  
  return priority_array


def get_sum_array(skill):
    
    tag_counts = count_problems_for_tags()
    tag_priority = {}
    
    for tag in tags:
      easy_count = tag_counts[tag]['Easy']
      medium_count = tag_counts[tag]['Medium']
      hard_count = tag_counts[tag]['Hard']

      result_array = benefit_array(easy_count, medium_count, hard_count, skill)

      tag_priority[tag] = {
        'Easy': result_array[0],
        'Medium': result_array[1],
        'Hard': result_array[2]
      }

    priority_array = get_priority_array(tag_priority)

    n = len(priority_array)  # Length of the array
    total_sum = sum(priority_array)  # Calculate the sum
    average = total_sum / n  # Calculate the average
    max_value = max(priority_array)  # Get the maximum value

    variance = sum((x - average) ** 2 for x in priority_array) / n
    standard_deviation = math.sqrt(variance)

    return [total_sum, average, max_value, standard_deviation]



def get_score(sum_array):
    total_sum = sum_array[0]  # Retrieve the sum
    average = sum_array[1]  # Retrieve the average
    max_value = sum_array[2]  # Retrieve the maximum value
    standard_deviation = sum_array[3]  # Retrieve the standard deviation

    # Calculate the score using the given formula
    score = (total_sum * 1) + (max_value * 1.5) + (standard_deviation * 0.5) + (average * 1)
    return score
