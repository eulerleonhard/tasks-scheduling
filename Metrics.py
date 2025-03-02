# Metrics calculation functions
def calculate_throughput(schedule):
    """
    Calculates the throughput of the schedule.
    Throughput is defined as the number of tasks completed per time unit.

    Args:
        schedule (list): A list of tuples (task_id, start_time, end_time) representing the schedule.

    Returns:
        float: The throughput of the schedule.
    """
    completed_tasks = len(schedule)  # Count of completed tasks

    if completed_tasks == 0:
        return 0.0  # Avoid division by zero

    start_times = [start_time for _, start_time, _ in schedule]
    end_times = [end_time for _, _, end_time in schedule]

    total_time = max(end_times) - min(start_times)

    return completed_tasks / total_time if total_time > 0 else 0.0

def calculate_makespan(schedule):
    """
    Calculates the makespan of the schedule.
    Makespan is defined as the total time from the start of the first task to the completion of the last task.

    Args:
        schedule (list): A list of tuples (task_id, start_time, end_time) representing the schedule.

    Returns:
        float: The makespan of the schedule.
    """
    return max(end_time for _, _, end_time in schedule)

def calculate_task_utilization_rate(schedule, tasks):
    """
    Calculates the task utilization rate of the schedule.
    Task utilization rate is defined as the ratio of the actual time tasks are running to the total available time.

    Args:
        schedule (list): A list of tuples (task_id, start_time, end_time) representing the schedule.
        tasks (list): A list of Task objects.

    Returns:
        float: The task utilization rate of the schedule.
    """
    total_time = max(end_time for _, _, end_time in schedule)
    total_task_time = sum(task.length for task in tasks)
    return total_task_time / (len(tasks) * total_time)

def calculate_priority_satisfaction(schedule, tasks):
    """
    Calculates the priority satisfaction of the schedule.
    Priority satisfaction is defined as the percentage of high-priority tasks that are completed before lower-priority tasks.

    Args:
        schedule (list): A list of tuples (task_id, start_time, end_time) representing the schedule.
        tasks (list): A list of Task objects.

    Returns:
        float: The priority satisfaction of the schedule.
    """
    high_priority_tasks = [task for task in tasks if task.priority >= 3]
    high_priority_completed = sum(1 for task_id, _, _ in schedule if any(task.task_id == task_id for task in high_priority_tasks))
    return high_priority_completed / len(high_priority_tasks)

def calculate_resource_utilization(schedule, tasks, resource_limits):
    """
    Calculates the resource utilization over time for each task type.
    Resource utilization is defined as the percentage of resource capacity used at each point in time for each task type.

    Args:
        schedule (list): A list of tuples (task_id, start_time, end_time) representing the schedule.
        tasks (list): A list of Task objects.
        resource_limits (dict): A dictionary of resource limits for each task type.

    Returns:
        dict: A dictionary where keys are task types and values are lists containing the resource utilization percentage over time.
    """
    # Initialize resource utilization tracking
    utilization = {task_type: [] for task_type in resource_limits.keys()}
    current_usage = {task_type: 0 for task_type in resource_limits.keys()}

    # Track the time intervals based on schedule
    time_points = set()
    for _, start_time, end_time in schedule:
        time_points.add(start_time)
        time_points.add(end_time)

    # Sort time points
    time_points = sorted(time_points)

    # Create a time index for utilization calculations
    for t in time_points:
        # Reset current usage at each time point
        for task_id, start_time, end_time in schedule:
            task = next((t for t in tasks if t.task_id == task_id), None)
            if start_time <= t < end_time:
                current_usage[task.task_type] += task.resource_req

        # Calculate utilization for each task type
        for task_type in resource_limits.keys():
            utilization[task_type].append(current_usage[task_type] / resource_limits[task_type] * 100)

        # Reset usage for the next time point
        for task_id, start_time, end_time in schedule:
            task = next((t for t in tasks if t.task_id == task_id), None)
            if start_time <= t < end_time:
                current_usage[task.task_type] -= task.resource_req
    # print(f"DEBUG1: {utilization}")
    return utilization

def calculate_average_wait_time(tasks, schedule):
    wait_times = {task.task_id: 0 for task in tasks}  # Initialize wait times for each task

    for task_id, start_time, end_time in schedule:
        task = next((t for t in tasks if t.task_id == task_id), None)
        if task:
            # Calculate wait time for each task
            wait_time = max(0, start_time - task.min_start_time)
            wait_times[task_id] += wait_time

    # Calculate average wait time
    total_wait_time = sum(wait_times.values())
    average_wait_time = total_wait_time / len(tasks) if tasks else 0
    return average_wait_time

def measure_metrics(schedule, tasks, resource_limits):
    """
    Measures the various metrics for the given schedule, tasks, and resource limits.

    Args:
        schedule (list): A list of tuples (task_id, start_time, end_time) representing the schedule.
        tasks (list): A list of Task objects.
        resource_limits (dict): A dictionary of resource limits for each task type.

    Returns:
        tuple: A tuple containing the measured metrics (throughput, makespan, task_utilization_rate, priority_satisfaction, resource_utilization).
    """
    throughput = calculate_throughput(schedule)
    makespan = calculate_makespan(schedule)
    task_utilization_rate = calculate_task_utilization_rate(schedule, tasks)
    priority_satisfaction = calculate_priority_satisfaction(schedule, tasks)
    resource_utilization = calculate_resource_utilization(schedule, tasks, resource_limits)
    task_avg_wait_time = calculate_average_wait_time(tasks, schedule)
    # print(f"DEBUG2: {resource_utilization}")
    return throughput, makespan, task_utilization_rate, priority_satisfaction, resource_utilization, task_avg_wait_time

