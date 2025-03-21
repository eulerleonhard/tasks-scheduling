import random
import pandas as pd

# Task attributes
TASK_TYPES = ['A', 'B', 'C', 'D']
TASK_STATUS = ['Running', 'Not Running']

class Task:
  def __init__(self, task_id, task_type, status, min_start_time, length, priority, resource_req, dependencies, num_dependencies):
    self.task_id = task_id # Unique ID of a task
    self.task_type = task_type # Type of the task
    self.status = status
    self.min_start_time = min_start_time
    self.length = length
    self.priority = priority
    self.resource_req = resource_req
    self.dependencies = dependencies
    self.num_dependencies = num_dependencies

  def __str__(self):
    return (f"Task ID: {self.task_id}, Type: {self.task_type}, Status: {self.status}, "
            f"Min Start Time: {self.min_start_time}, Length: {self.length}, "
            f"Priority: {self.priority}, Resource Requirement: {self.resource_req}, "
            f"Dependencies: {self.dependencies}")
  
def generate_random_tasks(num_tasks, resource_limits, max_dependencies=0):
    '''
    Generate a list of tasks with random attributes.

    Parameters:
    num_tasks (int): The number of tasks to generate.
    resource_limits (dict): A dictionary with task types as keys and their max resource limits as values.

    Returns:
    list: A list of Task objects.
    '''
    tasks = []

    for i in range(num_tasks):
        task_status = random.choice(TASK_STATUS)
        task_type = random.choice(TASK_TYPES)
        length = random.randint(1, 5)
        priority = random.randint(1, 10)

        # Ensure resource_req is within a valid range
        max_resource = resource_limits[task_type]
        resource_req = random.randint(1, max_resource-1) if max_resource > 0 else 0
        
        min_start_time = random.randint(0, 10)

        # Determine the number of dependencies (up to max_dependencies) based on previously created tasks
        num_dependencies = random.randint(0, min(i, max_dependencies))
        dependencies = random.sample([f'T{j}' for j in range(i)], k=num_dependencies)

        task = Task(
            task_id=f'T{i}',
            task_type=task_type,
            status=task_status,
            length=length,
            priority=priority,
            resource_req=resource_req,
            min_start_time=min_start_time,
            dependencies=dependencies,
            num_dependencies=num_dependencies
        )
        
        tasks.append(task)

    # Create a DataFrame to hold task data
    data = {
        "Task ID": [task.task_id for task in tasks],
        "Task Type": [task.task_type for task in tasks],
        "Status": [task.status for task in tasks],
        "Length": [task.length for task in tasks],
        "Priority": [task.priority for task in tasks],
        "Resource Requirement": [task.resource_req for task in tasks],
        "Min Start Time": [task.min_start_time for task in tasks],
        "Dependencies": [", ".join(task.dependencies) for task in tasks],
        "Number of Dependencies": [task.num_dependencies for task in tasks]
    }

    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    csv_filename = "tasks_dataset.csv"
    df.to_csv(csv_filename, index=False)

    # Show statistics of the dataset
    print("Dataset Statistics:")
    print(df.describe(include='all'))

    return tasks