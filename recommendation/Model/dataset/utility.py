import json
import os
import random


def separate_training_and_validation():
    # Get the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Load the problems from problems.json
    problems_file_path = os.path.join(current_directory, 'problems.json')
    with open(problems_file_path, 'r') as f:
        problems = json.load(f)

    # List of tags to filter by
    desired_tags = ['greedy', 'math', 'constructive', 'data structure', 'graph', 'dp', 'games']

    # Separate problems into those that meet the tag criteria and those that don't
    valid_problems = []
    other_problems = []

    for problem in problems:
        if any(tag.lower() in desired_tags for tag in problem['tags']):
            valid_problems.append(problem)
        else:
            other_problems.append(problem)

    # Shuffle the list of valid problems and select 100 random problems
    random.shuffle(valid_problems)
    validation_problems = valid_problems[:200]

    # The remaining valid problems and those without the desired tags form the training set
    training_problems = valid_problems[200:] + other_problems

    # Write the validation problems to validation.json
    validation_file_path = os.path.join(current_directory, 'validation.json')
    with open(validation_file_path, 'w') as f:
        json.dump(validation_problems, f, indent=4)

    # Write the training problems to training.json
    training_file_path = os.path.join(current_directory, 'training.json')
    with open(training_file_path, 'w') as f:
        json.dump(training_problems, f, indent=4)






def random_select_for_training():
    # Get the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    training_folder_path = os.path.join(current_directory, 'training')

    # Load the problems from training.json
    training_file_path = os.path.join(current_directory, 'training.json')
    with open(training_file_path, 'r') as f:
        training_problems = json.load(f)

    # Separate problems into easy, mid, and hard
    easy_problems = []
    mid_problems = []
    hard_problems = []

    for problem in training_problems:
        level = problem['level'].lower()
        if level == 'easy':
            easy_problems.append(problem)
        elif level in ('mid', 'medium'):
            mid_problems.append(problem)
        elif level == 'hard':
            hard_problems.append(problem)

    # Ensure there are at least two problems in each category
    if len(easy_problems) < 2 or len(mid_problems) < 2 or len(hard_problems) < 2:
        raise ValueError("Each category must have at least two problems.")

    # Number of iterations
    num_iterations = 300

    for i in range(1, num_iterations + 1):
        
        num_easy = random.randint(2, min(30, len(easy_problems)))
        num_mid = random.randint(2, min(30, len(mid_problems)))
        num_hard = random.randint(2, min(30, len(hard_problems)))

        selected_easy = random.sample(easy_problems, num_easy)
        selected_mid = random.sample(mid_problems, num_mid)
        selected_hard = random.sample(hard_problems, num_hard)

        # Select one unique problem from each category for set_{i}_easy/mid/hard.json
        unique_easy = random.choice(selected_easy)
        unique_mid = random.choice(selected_mid)
        unique_hard = random.choice(selected_hard)

        # Prepare the final set for set_{i}.json by excluding the unique problems
        set_problems = selected_easy + selected_mid + selected_hard
        set_problems.remove(unique_easy)
        set_problems.remove(unique_mid)
        set_problems.remove(unique_hard)

        # File paths for the iteration
        set_file_path = os.path.join(training_folder_path, f'set_{i}.json')
        set_easy_file_path = os.path.join(training_folder_path, f'set_{i}_easy.json')
        set_mid_file_path = os.path.join(training_folder_path, f'set_{i}_mid.json')
        set_hard_file_path = os.path.join(training_folder_path, f'set_{i}_hard.json')

        # Write the selected problems for the complete set
        with open(set_file_path, 'w') as f:
            json.dump(set_problems, f, indent=4)

        # Write the unique problems to their respective files
        with open(set_easy_file_path, 'w') as f:
            json.dump([unique_easy], f, indent=4)

        with open(set_mid_file_path, 'w') as f:
            json.dump([unique_mid], f, indent=4)

        with open(set_hard_file_path, 'w') as f:
            json.dump([unique_hard], f, indent=4)





def random_select_for_validation():
    # Get the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    validation_folder_path = os.path.join(current_directory, 'validation')

    # Load the problems from validation.json
    validation_file_path = os.path.join(current_directory, 'validation.json')
    with open(validation_file_path, 'r') as f:
        validation_problems = json.load(f)

    # Separate problems into easy, mid, and hard
    easy_problems = []
    mid_problems = []
    hard_problems = []

    for problem in validation_problems:
        level = problem['level'].lower()
        if level == 'easy':
            easy_problems.append(problem)
        elif level in ('mid', 'medium'):
            mid_problems.append(problem)
        elif level == 'hard':
            hard_problems.append(problem)

    # Ensure there are at least two problems in each category
    if len(easy_problems) < 2 or len(mid_problems) < 2 or len(hard_problems) < 2:
        raise ValueError("Each category must have at least two problems.")

    # Number of iterations
    num_iterations = 200

    for i in range(1, num_iterations + 1):
        
        num_easy = random.randint(2, min(30, len(easy_problems)))
        num_mid = random.randint(2, min(30, len(mid_problems)))
        num_hard = random.randint(2, min(30, len(hard_problems)))

        selected_easy = random.sample(easy_problems, num_easy)
        selected_mid = random.sample(mid_problems, num_mid)
        selected_hard = random.sample(hard_problems, num_hard)

        # Select one unique problem from each category for set_{i}_easy/mid/hard.json
        unique_easy = random.choice(selected_easy)
        unique_mid = random.choice(selected_mid)
        unique_hard = random.choice(selected_hard)

        # Prepare the final set for set_{i}.json by excluding the unique problems
        set_problems = selected_easy + selected_mid + selected_hard
        set_problems.remove(unique_easy)
        set_problems.remove(unique_mid)
        set_problems.remove(unique_hard)

        # File paths for the iteration
        set_file_path = os.path.join(validation_folder_path, f'set_{i}.json')
        set_easy_file_path = os.path.join(validation_folder_path, f'set_{i}_easy.json')
        set_mid_file_path = os.path.join(validation_folder_path, f'set_{i}_mid.json')
        set_hard_file_path = os.path.join(validation_folder_path, f'set_{i}_hard.json')

        # Write the selected problems for the complete set
        with open(set_file_path, 'w') as f:
            json.dump(set_problems, f, indent=4)

        # Write the unique problems to their respective files
        with open(set_easy_file_path, 'w') as f:
            json.dump([unique_easy], f, indent=4)

        with open(set_mid_file_path, 'w') as f:
            json.dump([unique_mid], f, indent=4)

        with open(set_hard_file_path, 'w') as f:
            json.dump([unique_hard], f, indent=4)


def count_all_problems():
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Load the problems from problems.json
    problems_file_path = os.path.join(current_directory, 'problems.json')
    with open(problems_file_path, 'r') as f:
        problems = json.load(f)

    # Initialize a counter for non-empty links
    non_empty_links_count = 0

    # Iterate over each problem
    for problem in problems:
        # Check if the "link" field is not empty
        if problem.get("link", ""):
            non_empty_links_count += 1

    print("Number of problems with non-empty 'link' field:", non_empty_links_count)


# separate_training_and_validation()
random_select_for_training()
random_select_for_validation()
# count_all_problems()