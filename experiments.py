from Visualisation import visualize_tasks, visualize_metrics
from Greedy import schedule_tasks_greedy
from TaskGeneration import generate_random_tasks
from Metrics import measure_metrics
from IntegerLinearProgramming import schedule_tasks_ilp
import time

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
    # "complex4": (2000, 10)
}

# Initialize a dictionary to hold results for each algorithm
results = {
    'Greedy': [],
    'ILP-Based': [],
    # Add other algorithms here
}

algorithms = ['Greedy', 'ILP-Based']  # List of algorithms for comparison

for experiment_name, (num_tasks, max_dependencies) in settings2.items():
    # Generate random tasks with specified number of tasks and max dependencies
    tasks = generate_random_tasks(num_tasks, RESOURCE_LIMITS, max_dependencies)

    # Test Greedy Algorithm
    start_time = time.time()
    schedule_greedy = schedule_tasks_greedy(tasks, RESOURCE_LIMITS)
    end_time = time.time()

    # visualise task
    # visualize_tasks(tasks, schedule_greedy)

    # Measure metrics for Greedy
    throughput, makespan, task_utilization_rate, priority_satisfaction, resource_utilization, task_avg_wait_time = measure_metrics(schedule_greedy, tasks, RESOURCE_LIMITS)
    execution_time = end_time - start_time

    # Append results for Greedy
    results['Greedy'].append((num_tasks, throughput, makespan, task_utilization_rate, priority_satisfaction, task_avg_wait_time, execution_time))

    # Test ILP-Based Algorithm
    start_time = time.time()
    schedule_priority = schedule_tasks_ilp(tasks, RESOURCE_LIMITS)
    end_time = time.time()

    # visualise task
    # visualize_tasks(tasks, schedule_priority)

    # Measure metrics for ILP-Based
    throughput, makespan, task_utilization_rate, priority_satisfaction, resource_utilization, task_avg_wait_time = measure_metrics(schedule_priority, tasks, RESOURCE_LIMITS)
    execution_time = end_time - start_time

    # Append results for ILP-Based
    results['ILP-Based'].append((num_tasks, throughput, makespan, task_utilization_rate, priority_satisfaction, task_avg_wait_time, execution_time))

# Visualize the results
visualize_metrics(results, algorithms)