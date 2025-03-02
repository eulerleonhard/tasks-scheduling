from threading import Lock, Thread
import heapq

class Task:
    def __init__(self, task_id, task_type, status, min_start_time, length, priority, resource_req, dependencies):
        self.task_id = task_id
        self.task_type = task_type
        self.status = status
        self.min_start_time = min_start_time
        self.length = length
        self.priority = priority
        self.resource_req = resource_req
        self.dependencies = dependencies

def schedule_tasks_greedy(tasks, resource_limits, task_types=['A', 'B', 'C', 'D']):
    # Sort tasks by priority (descending) and min_start_time (ascending)
    tasks.sort(key=lambda t: (-t.priority, t.min_start_time))

    # Initialize resource usage for each task type
    resource_usage = {task_type: 0 for task_type in task_types}

    # Initialize a priority queue to keep track of running tasks for each task type
    running_tasks = {task_type: [] for task_type in task_types}
    running_task_ids = {task_type: set() for task_type in task_types}  # Track running task IDs

    # Initialize a lock for each task type to prevent race conditions
    locks = {task_type: Lock() for task_type in task_types}

    # Initialize the schedule
    schedule = []

    # Function to update resource usage
    def update_resource_usage(task_type, amount):
        resource_usage[task_type] += amount

    # Define the scheduling function for each task type
    def schedule_task_type(task_type):
        current_time = 0

        while True:
            eligible_tasks = []
            with locks[task_type]:  # Lock access to this task type
                for task in tasks:
                    if task.task_type == task_type and task.status == 'Not Running':
                        # Check if all dependencies are met
                        if all(dep_id not in running_task_ids[task.task_type] for dep_id in task.dependencies):
                            # Check if resources are available
                            if resource_usage[task_type] + task.resource_req <= resource_limits[task_type]:
                                eligible_tasks.append(task)

            if not eligible_tasks:
                break  # No more tasks can be scheduled

            # Try to schedule as many eligible tasks as possible without exceeding resource limits
            current_batch = []
            total_resource_req = 0

            for task in eligible_tasks:
                if total_resource_req + task.resource_req <= resource_limits[task_type]:
                    # Assign start and end times
                    start_time = max(task.min_start_time, current_time)
                    end_time = start_time + task.length
                    schedule.append((task.task_id, start_time, end_time))

                    # Update resource usage for this task
                    total_resource_req += task.resource_req
                    current_batch.append((task, end_time))  # Store both task and end time

            # If we can schedule tasks, update their status and resource usage
            if current_batch:
                for task, end_time in current_batch:
                    update_resource_usage(task.task_type, task.resource_req)
                    task.status = 'Running'
                    running_task_ids[task.task_type].add(task.task_id)  # Track running task ID
                    heapq.heappush(running_tasks[task.task_type], (end_time, task.task_id))

            # Update the current time to the next event (completion of the earliest task)
            if running_tasks[task_type]:
                current_time = min(end_time for end_time, _ in running_tasks[task_type])
            else:
                break  # No running tasks, exit the loop

            # Remove completed tasks from the running tasks priority queue
            while running_tasks[task_type] and running_tasks[task_type][0][0] <= current_time:
                _, completed_task_id = heapq.heappop(running_tasks[task_type])
                # Update the resource usage for the completed task
                completed_task = next((t for t in tasks if t.task_id == completed_task_id), None)
                if completed_task:
                    update_resource_usage(task_type, -completed_task.resource_req)
                    completed_task.status = 'Completed'  # Update task status
                    running_task_ids[task.task_type].remove(completed_task_id)  # Remove completed task ID

    # Schedule tasks for each task type concurrently using threads
    threads = []
    for task_type in task_types:
        t = Thread(target=schedule_task_type, args=(task_type,))
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()

    return schedule