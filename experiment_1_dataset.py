from Visualisation import visualize_tasks, visualize_metrics, visualize_pipeline
from Greedy import schedule_tasks_greedy
from TaskGeneration import generate_random_tasks
from Metrics import measure_metrics
from IntegerLinearProgramming import schedule_tasks_ilp
import time
import pandas as pd
import random

from MetaheuristicAlgorithms import genetic_algorithm

# Task attributes
RESOURCE_LIMITS = {'A': 23, 'B': 17, 'C': 19, 'D': 11}

# Generate random tasks
# tasks = generate_random_tasks(num_tasks=100, resource_limits=RESOURCE_LIMITS, max_dependencies=2)

# Print out the tasks
# print("Generated Tasks:")
# for task in tasks:
#     print(task)

# Schedule the tasks
# schedule = schedule_tasks_greedy(tasks, resource_limits=RESOURCE_LIMITS)

# # Print the schedule
# print("\nSchedule:")
# for task_id, start_time, end_time in schedule:
#     print(f"Task {task_id}: start={start_time}, end={end_time}")

# visualise task
# visualize_tasks(tasks, schedule)

# Define a dictionary of algorithms
ALGORITHMS = {
    'Greedy': schedule_tasks_greedy,
    'ILP-Based': schedule_tasks_ilp,
    'Genetic-Algorithm': genetic_algorithm,
    # Add other algorithms here
}

# Initialize a dictionary to hold results for each algorithm
results = {algo_name: [] for algo_name in ALGORITHMS}

def run_experiment(tasks, resource_limits, algorithms, num_tasks):
    for algo_name in algorithms:
        algo_func = ALGORITHMS[algo_name]
        start_time = time.time()
        schedule = algo_func(tasks, resource_limits)
        end_time = time.time()

        # visualise task
        # if algo_name == "Genetic-Algorithm":
        #     visualize_tasks(tasks, schedule, num_tasks)

        # Measure metrics
        weighted_throughput, makespan, task_utilization_rate, priority_satisfaction, resource_utilization, task_avg_wait_time = measure_metrics(schedule, tasks, resource_limits)
        execution_time = end_time - start_time

        # Append results
        results[algo_name].append((num_tasks, weighted_throughput, makespan, task_utilization_rate, priority_satisfaction, task_avg_wait_time, execution_time))

    return results

# Experiment setup
# Generate the dataset as a list
dataset = generate_random_tasks(2000, RESOURCE_LIMITS, 10)
visualize_tasks(dataset)

num_tasks = [10, 20, 50, 100, 200, 500, 1000, 2000]

for num in num_tasks:
    # Select a random sample of 'num' tasks from the list
    tasks = random.sample(dataset, num)
    # print(f"type: {type(tasks)}")
    results = run_experiment(tasks, RESOURCE_LIMITS, list(ALGORITHMS.keys()), num)

visualize_metrics(results, list(ALGORITHMS.keys()))