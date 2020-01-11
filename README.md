# python_simulation_system

Run "simulation_data.py" first to generate a dataset that contains 10000 tasks.
Then run "simulation.py" to process the tasks.

"simulation_data.py" randomly generates a simulation data, according to certain criterias. A simulation dataset contains 10000 tasks. The code stores the dataset in sqlite3.

"simulation.py" simulates the processing system that acquires the tasks from the database and stores them in a queue. The system check on the task IDs is carried out using regular expressions. At each step of the simulation, the
simulation clock is updated to the next significant event, e.g.,task arrival, task processing completion.


