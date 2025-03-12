from pulp import LpProblem, LpVariable, LpBinary, LpMaximize, lpSum, LpStatus, PULP_CBC_CMD

def schedule_tasks_ilp(tasks, resource_limits):
    # Create a linear programming problem
    prob = LpProblem("Task_Scheduling", LpMaximize)

    # Create a binary variable for each task and time slot
    task_vars = {}
    max_time_horizon = max(task.length + task.min_start_time for task in tasks)

    for task in tasks:
        for start_time in range(max_time_horizon - task.length + 1):
            if start_time >= task.min_start_time:
                task_vars[(task.task_id, start_time)] = LpVariable(f"task_{task.task_id}_{start_time}", cat=LpBinary)

    # Objective function: maximize total priority
    prob += lpSum(task.priority * task_vars[(task.task_id, start_time)]
                  for task in tasks
                  for start_time in range(max_time_horizon - task.length + 1)
                  if (task.task_id, start_time) in task_vars)

    # Resource constraints
    for start_time in range(max_time_horizon):
        for task_type in resource_limits:
            prob += lpSum(task_vars[(task.task_id, start_time)] * task.resource_req
                          for task in tasks if task.task_type == task_type
                          if (task.task_id, start_time) in task_vars) <= resource_limits[task_type]

    # Dependency constraints
    for task in tasks:
        for dep in task.dependencies:
            for start_time in range(max_time_horizon - task.length + 1):
                if start_time >= task.min_start_time:
                    prob += lpSum(task_vars[(dep, dep_start)]
                                 for dep_start in range(max(0, start_time - next(t for t in tasks if t.task_id == dep).length + 1), start_time + 1)
                                 if (dep, dep_start) in task_vars) <= 1

    # Solve the problem with an efficient solver
    prob.solve(PULP_CBC_CMD(msg=0, timeLimit=300))  # Set a time limit if needed

    # Check the status of the solution
    if LpStatus[prob.status] == 'Optimal':
        schedule = []
        for task in tasks:
            for start_time in range(max_time_horizon - task.length + 1):
                if (task.task_id, start_time) in task_vars and task_vars[(task.task_id, start_time)].varValue == 1:
                    end_time = start_time + task.length
                    schedule.append((task.task_id, start_time, end_time))
        return schedule
    else:
        return "No optimal solution found"