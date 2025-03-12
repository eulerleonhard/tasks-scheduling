'''
Overview of Genetic Algorithms
    Genetic Algorithms are inspired by the process of natural selection.
    They are used to find optimal or near-optimal solutions to complex
        problems through processes mimicking biological evolution. 
    The core components of a GA include:

        Population: A set of potential solutions (individuals).
        Fitness Function: A way to evaluate how good each solution is.
        Selection: Choosing the best solutions to create the next generation.
        Crossover: Combining parts of two solutions to create new ones.
        Mutation: Making small random changes to solutions to maintain diversity.
'''


import random

import random

def create_individual(tasks, max_time_horizon):
    """
    Create a random schedule for the given tasks.
    
    Parameters:
    - tasks: List of tasks to schedule.
    - max_time_horizon: The latest time by which tasks can be scheduled.

    Returns:
    A list of tuples, each containing a task ID and its start time.
    """
    schedule = []
    for task in tasks:
        # Randomly select a start time for each task within allowed limits
        start_time = random.randint(task.min_start_time, max_time_horizon - task.length)
        schedule.append((task.task_id, start_time))  # Append (task_id, start_time) to schedule
    return schedule

def fitness(schedule, tasks, resource_limits):
    """
    Evaluate the fitness of a schedule based on priority, resource limits, and dependencies.
    
    Parameters:
    - schedule: The current schedule to evaluate.
    - tasks: List of tasks for reference.
    - resource_limits: Dictionary of resource limits.

    Returns:
    Total priority score of the schedule (higher is better).
    """
    total_priority = 0
    # Initialize resource usage tracking
    resource_usage = {key: 0 for key in resource_limits.keys()}
    end_times = {}  # To track when tasks finish

    for task_id, start_time in schedule:
        # Get the task details from the task list
        task = next(t for t in tasks if t.task_id == task_id)
        end_time = start_time + task.length  # Calculate end time of the task
        
        # Check if adding this task exceeds resource limits
        resource_usage[task.task_type] += task.resource_req
        if resource_usage[task.task_type] > resource_limits[task.task_type]:
            return 0  # Return 0 fitness if resource limits are exceeded
        
        # Check if all dependencies for this task are satisfied
        for dep in task.dependencies:
            dep_end_time = end_times.get(dep)
            if dep_end_time is None or dep_end_time > start_time:
                return 0  # Return 0 fitness if a dependency is not satisfied

        # Adjust total priority (lower number means higher priority)
        total_priority -= task.priority
        end_times[task_id] = end_time  # Record the end time of the task
        
    return total_priority  # Return total priority score

def crossover(parent1, parent2):
    """
    Create two offspring schedules from two parent schedules.
    
    Parameters:
    - parent1: First parent schedule.
    - parent2: Second parent schedule.

    Returns:
    Two new child schedules created through crossover.
    """
    crossover_point = random.randint(1, len(parent1) - 1)  # Choose a random crossover point
    # Create children by combining segments from both parents
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2  # Return the two new child schedules

def mutate(individual, tasks, max_time_horizon):
    """
    Randomly mutate a schedule to introduce diversity.
    
    Parameters:
    - individual: The schedule to mutate.
    - tasks: List of tasks for reference.
    - max_time_horizon: The latest time by which tasks can be scheduled.

    Returns:
    None (modifies the individual in place).
    """
    if random.random() < 0.1:  # 10% chance of mutation
        task_to_mutate = random.choice(individual)  # Select a random task to mutate
        task_id = task_to_mutate[0]
        task = next(t for t in tasks if t.task_id == task_id)  # Get the task details
        # Generate a new random start time within allowed limits
        new_start_time = random.randint(task.min_start_time, max_time_horizon - task.length)
        # Update the individual's schedule with the new start time
        individual[individual.index(task_to_mutate)] = (task_id, new_start_time)

def genetic_algorithm(tasks, resource_limits, population_size=100, generations=100):
    """
    Run the genetic algorithm to optimize task scheduling.
    
    Parameters:
    - tasks: List of tasks to schedule.
    - resource_limits: Dictionary of resource limits.
    - population_size: Number of individuals in the population.
    - generations: Number of generations to evolve.

    Returns:
    The best schedule found after all generations.
    """
    max_time_horizon = max(task.length + task.min_start_time for task in tasks)  # Calculate max time

    # Create initial population of random schedules
    population = [create_individual(tasks, max_time_horizon) for _ in range(population_size)]

    for generation in range(generations):
        # Evaluate the fitness of each individual in the population
        fitness_scores = [(individual, fitness(individual, tasks, resource_limits)) for individual in population]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)  # Sort by fitness score
        
        # Select the top half of individuals as parents for the next generation
        selected_parents = fitness_scores[:population_size // 2]

        # Prepare for the next generation
        next_generation = []
        while len(next_generation) < population_size:
            # Select two parents randomly from the selected parents
            parent1, parent2 = random.choices(selected_parents, k=2)
            children = crossover(parent1[0], parent2[0])  # Create children from parents
            for child in children:
                mutate(child, tasks, max_time_horizon)  # Apply mutation
                next_generation.append(child)  # Add child to next generation

        population = next_generation  # Update the population for the next generation

    # Get the best solution from the final population
    best_schedule = max(population, key=lambda ind: fitness(ind, tasks, resource_limits))
    
    # Convert the best schedule to the expected format (task_id, end_time, start_time)
    final_schedule = []
    for task_id, start_time in best_schedule:
        task = next(t for t in tasks if t.task_id == task_id)  # Get task details
        end_time = start_time + task.length  # Calculate end time
        final_schedule.append((task_id, end_time, start_time))  # Append to final schedule
    
    return final_schedule  # Return the final optimized schedule