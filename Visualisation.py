import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import numpy as np

# Task visualization
def visualize_tasks(tasks, schedule):
    if not schedule:
        return 0  # Return 0 for empty schedule
    
    # Create a figure with 4 subplots (one for each task type)
    fig, axs = plt.subplots(4, 1, figsize=(12, 12), sharex=True)

    # Get unique task types
    task_types = ['A', 'B', 'C', 'D']

    # Determine unique priorities and create a color map
    unique_priorities = sorted(set(task.priority for task in tasks))
    num_priorities = len(unique_priorities)
    
    # Create a blue-to-white color map
    cmap = plt.get_cmap('Blues', num_priorities)  # Blue colormap

    # Plot the tasks for each task type
    for i, task_type in enumerate(task_types):
        ax = axs[i]
        for task_id, start_time, end_time in schedule:
            task = next(t for t in tasks if t.task_id == task_id)
            if task.task_type == task_type:
                # Get the index for the color based on task priority
                priority_index = unique_priorities.index(task.priority)
                color = cmap(priority_index)  # Get color from the colormap
                ax.barh(task_id, end_time - start_time, left=start_time, height=0.4, color=color)
                ax.text(start_time + 0.5 * (end_time - start_time), task_id, str(task.task_id), 
                        va='center', ha='center', color='white')

        # Set labels and title for each subplot
        ax.set_title(f'Task Type {task_type} Execution Timeline')
        ax.set_ylabel('Task ID')
        ax.set_xlim(0, max(end_time for _, start_time, end_time in schedule) + 1)  # Extend x-axis for visibility
        ax.grid(True)

    # Set the x-axis label for the entire figure
    plt.xlabel('Time')

    # Adjust layout
    plt.tight_layout()

    # Show the plot
    # plt.show()

def visualize_resource_utilization(resource_utilization):
    # Create a figure with subplots
    # print(f"DEBUG: {resource_utilization}")
    num_resources = len(resource_utilization[-1])
    fig, axs = plt.subplots(num_resources, 1, figsize=(10, 3.5 * num_resources), sharex=True)

    # Calculate the number of time points based on the length of the utilization lists
    time_points = list(range(max(len(res) for res in resource_utilization[-1].values())))

    # Define intervals for x-ticks for better readability
    step = max(1, len(time_points) // 10)  # Show up to 10 ticks
    x_ticks = list(range(0, len(time_points), step))  # Convert to a list of indices
    x_tick_labels = [str(time_points[i]) for i in x_ticks]  # Use list comprehension to get labels

    # Plot each resource utilization in its own subplot
    for i, (label, res) in enumerate(resource_utilization[-1].items()):
        axs[i].plot(time_points[:len(res)], res, label=label)

        # Highlight periods where utilization is over 95%
        for j in range(len(res)):
            if res[j] > 95:
                axs[i].axvspan(time_points[j], time_points[j] + 1, color='red', alpha=0.3)

        axs[i].set_title(f'Resource Utilization for {label}')
        axs[i].set_ylabel('Utilization (%)')
        axs[i].set_ylim(0, 100)  # Set y-limits to 0-100% for better readability
        axs[i].grid()
        axs[i].legend()

    plt.xlabel('Time')
    plt.xticks(x_ticks, x_tick_labels)  # Set x-ticks to the defined intervals
    plt.tight_layout()  # Adjust layout to prevent overlapping
    # plt.show()


import matplotlib.pyplot as plt

def visualize_metrics(results, algorithms):
    """
    Visualizes the metrics measured in the experiment.

    Args:
        results (dict): A dictionary where keys are algorithm names and values are lists of tuples containing the experiment results.
        algorithms (list): A list of algorithm names for plotting.
    """
    plt.figure(figsize=(16, 8))

    metrics = ['Throughput', 'Makespan', 'Task Utilization Rate', 'Priority Satisfaction', 'Average Waiting Time', 'Execution Time']
    
    for i, metric in enumerate(metrics):
        plt.subplot(2, 3, i + 1)

        for algorithm in algorithms:
            x = [r[0] for r in results[algorithm]]  # Number of tasks
            y = [r[i + 1] for r in results[algorithm]]  # Offset by 1 since the first element is num_tasks
            
            # Check if y has valid values before plotting
            if all(isinstance(value, (int, float)) for value in y):
                plt.plot(x, y, label=algorithm)
            else:
                print(f"Invalid data for {algorithm}: {metric}{y}")

        plt.title(metric)
        plt.xlabel('Number of Tasks')
        plt.ylabel(metric)
        plt.legend()

    plt.tight_layout()
    plt.show()