from Visualisation import visualize_tasks, visualize_metrics
from Greedy import schedule_tasks_greedy
from TaskGeneration import generate_random_tasks
from Metrics import measure_metrics
# import matplotlib.pyplot as plt 
# from plotly.subplots import make_subplots
# import plotly.graph_objects as go
import time

# Task attributes
RESOURCE_LIMITS = {'A': 10, 'B': 10, 'C': 10, 'D': 10}

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


# Experiment setup
# num_tasks = [50, 100]


settings1 = {# experiments with number of tasks and max dependencies
    "simple1": (10, 0),
    "simple2": (50, 0),
    "medium1": (50, 0),
    "medium2": (100, 0),
    "complex1": (200, 0),
    "complex2": (500, 0),
    "complex3": (1000, 0)
} 
settings2 = {# experiments with number of tasks and max dependencies
    "simple1": (10, 2),
    "simple2": (50, 2),
    "medium1": (50, 2),
    "medium2": (100, 3),
    "complex1": (200, 3),
    "complex2": (500, 5),
    "complex3": (1000, 5)
}

# Run the experiment for Greedy approach
results = []

for experiment_name, (num_tasks, max_dependencies) in settings2.items():
    # Generate random tasks with specified number of tasks and max dependencies
    tasks = generate_random_tasks(num_tasks, RESOURCE_LIMITS, max_dependencies)
    start_time = time.time()
    schedule = schedule_tasks_greedy(tasks, RESOURCE_LIMITS)
    end_time = time.time()

    # visualise task
    visualize_tasks(tasks, schedule)
    
    # Measure metrics
    throughput, makespan, task_utilization_rate, priority_satisfaction, resource_utilization = measure_metrics(schedule, tasks, RESOURCE_LIMITS)
    # print(f"DEBUG3: {resource_utilization}")
    execution_time = end_time - start_time
    
    # Append results with experiment name for identification
    results.append((num_tasks, throughput, makespan, task_utilization_rate, priority_satisfaction, resource_utilization, execution_time))

# Visualize the results
visualize_metrics(results)