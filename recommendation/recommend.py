import os
import sys
import json
import numpy as np
import tensorflow as tf
from utility import count_problems_for_tags, benefit_array, get_sum_array, get_score, get_solved_ids

current_directory = os.path.dirname(__file__)
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(current_directory)

def recommend_problems(all_problems, skill):
    model_path = os.path.join(current_directory, 'Model', 'model_version_1.h5')
    model = tf.keras.models.load_model(model_path)

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
    recommended_problems = []
    
    tags = ['greedy', 'math', 'constructive', 'data structure', 'graph', 'dp', 'games']
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

    solved_ids = get_solved_ids()

    for problem in all_problems:
        if problem['_id'] in solved_ids:
            continue
        
        level = problem['level']
        problem_tags = problem['tags']
        
        priority_array = [0] * 7

        for i, tag in enumerate(tags):
            if tag in problem_tags:
                priority_array[i] = tag_priority[tag][level]
        
        score_array = get_sum_array(priority_array)
        
        # score = get_score(score_array) # if not using model

        # if using model
        score_array = np.array(score_array)
        score_array = score_array.reshape(1, -1)  # Reshape to (1, 4)
        score = model.predict(score_array)
        
        recommended_problems.append({"problem": problem, "score": score})

    recommended_problems.sort(key=lambda x: x["score"], reverse=True)

    recommended_problems = take_with_escape(recommended_problems)

    return recommended_problems


def take_with_escape(recommended_problems):
    selected_problems = []
    consecutive_count = 0
    last_level = None

    # Iterate through recommended_problems and populate selected_problems
    for problem_info in recommended_problems:
        problem = problem_info["problem"]
        level = problem["level"]
        
        if level != last_level:
            last_level = level
            consecutive_count = 0
        
        if consecutive_count < 20:
            selected_problems.append(problem_info)
            consecutive_count += 1
        else:
            continue
    
    return selected_problems


script_directory = os.path.dirname(os.path.abspath(__file__))
solved_problems_path = os.path.join(script_directory, 'solved_problems.json')
all_problems_path = os.path.join(script_directory, 'all_problems.json')
recommendations_path = os.path.join(script_directory, 'recommendations.json')
skillRating_path = os.path.join(script_directory, 'skillRating.json')

with open(all_problems_path, 'r') as all_problems_file:
    all_problems_data = json.load(all_problems_file)

with open(skillRating_path, 'r', encoding='utf-8') as file:
    data = json.load(file)  # Load the JSON content

skill = int(data)

recommendations = recommend_problems(all_problems_data, skill)

recommended_problems_only = [recommendation["problem"] for recommendation in recommendations]

with open(recommendations_path, 'w') as recommendations_file:
    json.dump(recommended_problems_only, recommendations_file, indent=4)