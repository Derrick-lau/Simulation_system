import sqlite3
from multiprocessing import Process
import re

class Queue(object):
    def __init__(self):
        self.p1 = []
        self.p2 = []

    def enqueue(self, item):
        self.p1.append(item)

    def dequeue(self):
        self.front()
        return self.p2.pop()

    def front(self):
        if not self.p2:
            while self.p1:
                    self.p2.append(self.p1.pop())
        return self.p2[-1]

    def isEmpty(self):
        return not self.p1 and not self.p2


class simulation_system(Queue):

    def init_system(self):
        self.q = Queue()
        connection = sqlite3.connect('Simulation_data.db')
        cur = connection.cursor()
        cur.execute("SELECT * FROM dataset ORDER BY arrival ASC")
        tasksList = cur.fetchall()
        print(tasksList)
        for i in tasksList:
            self.q.enqueue(i)
        self.clock = 0
        self.onHold = 0
        self.processor1 = []
        self.processor2 = []
        self.processor3 = []
        connection.commit()
        connection.close()
        return print("** SYSTEM INITIALISED **")

    def enter_system(self):
        if self.q.isEmpty() is False:
            EnteringItem = self.q.front()
            self.clock = EnteringItem[1]
            print(f"** [{self.clock}] : Task [{EnteringItem[0]}] with duration [{EnteringItem[2]}] enters the system.")
            pattern = re.compile(r"((?=.*[\d])(?=.*[a-z])(?=.*[A-Z])|(?=.*[\d])(?=.*[a-zA-Z])(?=.*[@#*&_-])|(?=.*[a-z])(?=.*[A-Z])(?=.*[@#*&_-])).*")
            if pattern.match(EnteringItem[0]):
                print(f"** Task [{EnteringItem[0]}] accepted.")
                self.assign_processor()
            else:
                print(f"** Task [{EnteringItem[0]}] unfeasible and discarded.")
                self.q.dequeue()
                self.enter_system()
        else:
            self.complete_tasks()

    def assign_processor(self):
        EnteringItem = self.q.front()
        if len(self.processor1) == 0:
                print(f"** [{self.clock}] : Task [{EnteringItem[0]}] assigned to processor [1]")
                self.processor1.append(self.q.front())
                self.q.dequeue()
                self.complete_tasks()

        elif len(self.processor2) == 0:
                print(f"** [{self.clock}] : Task [{EnteringItem[0]}] assigned to processor [2]")
                self.processor2.append(self.q.front())
                self.q.dequeue()
                self.complete_tasks2()

        elif len(self.processor3) == 0:
                print(f"** [{self.clock}] : Task [{EnteringItem[0]}] assigned to processor [3]")
                self.processor3.append(self.q.front())
                self.q.dequeue()
                self.complete_tasks3()

        elif self.onHold == 0:
            print(f'** Task [{EnteringItem[0]}] on hold')
            self.onHold = 1
            self.complete_tasks()

    def complete_tasks(self):
        try:
            EnteringItem = self.q.front()
            AssignedItem1 = self.processor1[0]

            if self.onHold == 1:
                print(f"** [{self.clock}] : Task [{AssignedItem1[0]}] completed.")
                self.processor1.pop()
                self.onHold = 0
                self.assign_processor()

            elif EnteringItem[1] > AssignedItem1[1] + AssignedItem1[2]:
                print(f"** [{self.clock}] : Task [{AssignedItem1[0]}] completed.")
                self.processor1.pop()
                self.enter_system()

            else:
                self.enter_system()
        except:
            self.complete_tasks2()

    def complete_tasks2(self):
        try:
            EnteringItem = self.q.front()
            AssignedItem2 = self.processor2[0]
            if self.onHold == 1:
                print(f"** [{self.clock}] : Task [{AssignedItem2[0]}] completed.")
                self.processor2.pop()
                self.onHold = 0
                self.assign_processor()

            elif EnteringItem[1] > AssignedItem2[1] + AssignedItem2[2]:
                print(f"** [{self.clock}] : Task [{AssignedItem2[0]}] completed.")
                self.processor2.pop()
                self.enter_system()
            else:
                self.enter_system()
        except:
            self.complete_tasks3()

    def complete_tasks3(self):
        try:
            EnteringItem = self.q.front()
            AssignedItem3 = self.processor3[0]
            if self.onHold == 1:
                print(f"** [{self.clock}] : Task [{AssignedItem3[0]}] completed.")
                self.processor3.pop()
                self.onHold = 0
                self.assign_processor()

            elif EnteringItem[1] > AssignedItem3[1] + AssignedItem3[2]:
                print(f"** [{self.clock}] : Task [{AssignedItem3[0]}] completed.")
                self.processor3.pop()
                self.enter_system()

            else:
                self.enter_system()
        except:
            print(f"[{self.clock}] : SIMULATION COMPLETED.")




Simulation = simulation_system()
InitSystem = Simulation.init_system()
StartSystem = Simulation.enter_system()