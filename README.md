

# Overview
A simulation system processing 10000 tasks with 3 processors.

# Features
- This system acquires tasks from the database and stores them in a queue which was built with linked list. 

- The system check on the task IDs is carried out using Regular Expressions. 

- At each step of the simulation, the simulation clock is updated to the next significant event, e.g.,task arrival, task processing completion.

- "simulation_data.py" randomly generates a simulation data, according to certain criterias. A simulation dataset contains 10000 tasks. The code stores the dataset in sqlite3.

# Setup & Installation
1.Run "simulation_data.py" first to generate a dataset that contains 10000 tasks.

2.Then run "simulation.py" to process the tasks.


