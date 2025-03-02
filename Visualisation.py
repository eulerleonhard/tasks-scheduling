import matplotlib.pyplot as plt

# Task visualization
def visualize_tasks(tasks, schedule):
    # Create a figure with 4 subplots (one for each task type)
    fig, axs = plt.subplots(4, 1, figsize=(12, 12), sharex=True)

    # Get unique task types
    task_types = ['A', 'B', 'C', 'D']

    # Plot the tasks for each task type
    for i, task_type in enumerate(task_types):
        ax = axs[i]
        for task_id, start_time, end_time in schedule:
            task = next(t for t in tasks if t.task_id == task_id)
            if task.task_type == task_type:
                ax.barh(task_id, end_time - start_time, left=start_time, height=0.4, color='black')
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
    plt.show()


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
    plt.show()

def visualize_metrics(results):
    """
    Visualizes the metrics measured in the experiment.

    Args:
        results (list): A list of tuples containing the experiment results (number of tasks, throughput, makespan, task_utilization_rate, priority_satisfaction, resource_utilization, execution_time).
    """
    x = [r[0] for r in results]
    throughput = [r[1] for r in results]
    makespan = [r[2] for r in results]
    task_utilization_rate = [r[3] for r in results]
    priority_satisfaction = [r[4] for r in results]
    resource_utilization = [r[5] for r in results]
    # print(f"DEBUG: {resource_utilization}")
    execution_time = [r[6] for r in results]
    task_avg_wait_time = [r[7] for r in results]
    
    plt.figure(figsize=(16, 8))

    plt.subplot(2, 3, 1)
    plt.plot(x, throughput)
    plt.title('Throughput')
    plt.xlabel('Number of Tasks')
    plt.ylabel('Throughput')

    plt.subplot(2, 3, 2)
    plt.plot(x, makespan)
    plt.title('Makespan')
    plt.xlabel('Number of Tasks')
    plt.ylabel('Makespan')

    plt.subplot(2, 3, 3)
    plt.plot(x, task_utilization_rate)
    plt.title('Task Utilization Rate')
    plt.xlabel('Number of Tasks')
    plt.ylabel('Task Utilization Rate')

    plt.subplot(2, 3, 4)
    plt.plot(x, priority_satisfaction)
    plt.title('Priority Satisfaction')
    plt.xlabel('Number of Tasks')
    plt.ylabel('Priority Satisfaction')

    plt.subplot(2, 3, 5)
    plt.plot(x, task_avg_wait_time)
    plt.title('Average waiting time of task before execution')
    plt.xlabel('Number of Tasks')
    plt.ylabel('Waiting Time')

    plt.subplot(2, 3, 6)
    plt.plot(x, execution_time)
    plt.title('Execution Time')
    plt.xlabel('Number of Tasks')
    plt.ylabel('Execution Time (seconds)')

    plt.tight_layout()
    plt.show()

    visualize_resource_utilization(resource_utilization)

    # visualize_resource_utilization_heatmap(resource_utilization)