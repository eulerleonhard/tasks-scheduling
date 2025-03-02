# Task Scheduling Project

## Overview
This repository contains experiments on various algorithms for solving the task scheduling problem. The focus is evaluating different approaches to efficiently schedule tasks while considering constraints such as resource limits, dependencies, and execution times.

## Files Included
- **Greedy.py**: Implementation of a greedy algorithm for scheduling tasks.
- **Metrics.py**: Module to calculate and evaluate various performance metrics.
- **TaskGeneration.py**: Script for generating **Task** objects.
- **Visualisation.py**: Tools for visualizing scheduling results and metrics.
- **experiments.py**: Script to run experiments with different algorithms and configurations.
- **results/**: Directory containing output data and experiment visualisations.

## Metrics
In this project, we consider the following metrics to evaluate the performance of the scheduling algorithms:

1. **Throughput**:
  - Definition: The total work units completed per hour.
  - Importance: This metric directly measures how effectively the algorithm utilizes available resources to complete tasks.

2. **Makespan**:
  - Definition: The total time required to complete all tasks.
  - Importance: A lower makespan indicates a more efficient scheduling algorithm.

5. **Resource Utilization**:
   - Definition: The percentage of available resources used during the scheduling process.
   - Importance: High resource utilization is desirable as it indicates effective use of available resources.

6. **Task Utilization Rate**:
  - Definition: The ratio of the actual time tasks are running to the total available time.
  - Importance: This metric helps assess how well the algorithm is keeping tasks busy, especially under resource constraints.

5. **Average Wait Time**:
   - Definition: The average time that tasks spend waiting in the queue before execution.
   - Importance: Lower average wait times indicate better responsiveness of the scheduling algorithm.
  
6. **Priority Satisfaction**:
  - Definition: The percentage of high-priority tasks that are completed before lower-priority tasks.
  - Importance: Measures how well the algorithm adheres to the priority rules, which is crucial for stakeholder satisfaction.

7. **Execution Time**:
  - Definition: The time taken by the algorithm to produce a schedule.
  - Importance: A faster execution time is preferable, especially in dynamic environments where tasks may frequently change.

## Getting Started
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/eulerleonhard/tasks-scheduling.git
   cd tasks-scheduling
   ```

2. **Install Requirements**:
   Make sure to install any necessary dependencies. You may use `pip` to install required packages.

3. **Run Experiments**:
   Execute the `experiments.py` script to run the scheduling algorithms and generate results.
   ```bash
   python experiments.py
   ```

---

Feel free to explore the repository and experiment with the algorithms to enhance your understanding of task scheduling!
