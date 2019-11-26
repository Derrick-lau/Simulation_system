import queue
import sqlite3
import multiprocessing
import time
import re

class simulation_system(object):
    def init_system(self):
        self.system = queue.Queue()
        return print("** SYSTEM INITIALISED **")

    def system_acquireData(self):
        connection = sqlite3.connect('Simulation_data.db')
        cur = connection.cursor() 
        cur.execute("SELECT * FROM dataset")  
        tasks = cur.fetchall()
        pattern = re.compile(r"((?=.*[\d])(?=.*[a-z])(?=.*[A-Z])|(?=.*[\d])(?=.*[a-zA-Z])(?=.*[@''#*&-])|(?=.*[a-z])(?=.*[A-Z])(?=.*[@''#*&-])).*")
        for i in tasks:
            print(f"** [{time.perf_counter()}] : Task [{i[0]}] with duration [{i[2]}] enters the system.")
        for i in tasks:
            if pattern.match(i[0]):
                print(f"** Task [{i[0]}] accepted.")
                self.system.put(i)
            else:
                print(f"** Task [{i[0]}] unfeasible and discarded.")
        connection.commit()
        connection.close()
    
    def assign_processor(self):
        onHold = []
        p1 = multiprocessing.Process(target=self.system.get)
        p2 = multiprocessing.Process(target=self.system.get)
        p3 = multiprocessing.Process(target=self.system.get)
        p1.start()
        p2.start()
        p3.start()

        while not self.system.empty():
            onHold.append(self.system.get())
        print(onHold)

    # Then, the task needs to be assigned to a processor. If a processor is
# available, then the task is assigned to it, the processor is busy for the whole
# duration of the task and it becomes available when it ends. Otherwise,
# the task must be put on hold and assigned to the first available processor
# according to a FIFO strategy.
# When a task is put on hold the message displayed is:
# ** Task [TASK ID] on hold.
# On the other hand, when a task is assigned to a processor the following
# message is displayed:
# ** [CLOCK] : Task [TASK ID] assigned to processor [PROCESSOR #].
# where [PROCESSOR #] is the processor number, i.e., either 1, 2 or 3.
# When a task is completed, the message displayed is:
# 3
# ** [CLOCK] : Task [TASK ID] completed.
 
    def system_end(self):
        return print( f"** [{time.perf_counter()}] : SIMULATION COMPLETED. **")

Simulation = simulation_system()
InitSystem = Simulation.init_system()
EnterSystem = Simulation.system_acquireData()
AssignProcessors = Simulation.assign_processor()
SystemEnd =  Simulation.system_end()