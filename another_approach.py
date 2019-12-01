import sqlite3
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
        return self.p1 and not self.p2


class simulation_system(Queue):
# _____________________INITIALISE SYSTEM_________________________________________________________
    def init_system(self):
        self.q = Queue()
        connection = sqlite3.connect('Simulation_data.db')
        cur = connection.cursor()
        cur.execute("SELECT id, arrival, duration FROM dataset ORDER BY arrival ASC")
        tasksList = cur.fetchall()
        print(tasksList)
        for i in tasksList:
            self.q.enqueue(i)
        self.clock = 0
        self.onHold = []
        self.processor1 = []
        self.processor2 = []
        self.processor3 = []
        connection.commit()
        connection.close()
        print("** SYSTEM INITIALISED **")
        return print(self.processor1)

# #######################Belows are the function prepared to run the system##########################################
    def assign_tasks(self, processor):
        if self.onHold:
            processor.append(self.onHold[0])
            print(f"** [{self.clock}] : Task [{processor[0][0]}] assigned to processor [1]")
            self.onHold.pop(0)
        else:
            processor.append(self.q.front())
            print(f"** [{self.clock}] : Task [{processor[0][0]}] assigned to processor [1]")
            self.q.dequeue()
        self.clock += processor[0][2]
        processor.append(self.clock)

    def task_processing(self, processor, anotherprocessor1, anotherprocessor2 ):
            EnteringItem = self.q.front()
            AssignedItem = processor[0]

            if len(self.onHold) >= 1 and AssignedItem[1] < anotherprocessor1[1] and AssignedItem[1] < anotherprocessor1[1] and AssignedItem[1] < EnteringItem[1]:
                if not len(anotherprocessor1) or AssignedItem[1] < anotherprocessor1[1]:
                    if not len(anotherprocessor2) and AssignedItem[1] < anotherprocessor2[1]:
                        self.clock = AssignedItem[1]
                        print(f"** [{self.clock}] : Task [{AssignedItem[0][0]}] completed.")
                        AssignedItem.clear()

            if len(self.onHold) > 0:
                EnteringItem = self.onHold[0]

            if EnteringItem[1] > AssignedItem[1]:
                if len(anotherprocessor1) and AssignedItem[1] > anotherprocessor1[1]:
                    if len(anotherprocessor2) and AssignedItem[1] > anotherprocessor2[1]:
                        self.clock = AssignedItem[1]
                        print(f"** [{self.clock}] : Task [{AssignedItem[0][0]}] completed.")
                        AssignedItem.clear()


    def entering_system(self):
            # entering
            EnteringItem = self.q.front()
            self.clock = EnteringItem[1]
            print(f"** [{self.clock}] : Task [{EnteringItem[0]}] with duration [{EnteringItem[2]}] enters the system.")

            # filtering
            pattern = re.compile(r"((?=.*[\d])(?=.*[a-z])(?=.*[A-Z])|(?=.*[\d])(?=.*[a-zA-Z])(?=.*[@#*&_-])|(?=.*[a-z])(?=.*[A-Z])(?=.*[@#*&_-])).*")
            if True:
                if pattern.match(EnteringItem[0]):
                    print(f"** Task [{EnteringItem[0]}] accepted.")

                else:
                    print(f"** Task [{EnteringItem[0]}] unfeasible and discarded.")
                    self.q.dequeue()
                    self.entering_system()


############################ run_system is a function really run the system###########################################
    def run_system(self):

        processor1 = self.processor1
        processor2 = self.processor2
        processor3 = self.processor3

        for i in range(1000):
                self.entering_system()
                # assigning
                if not len(self.processor1):
                    self.assign_tasks(processor1)

                if not len(self.processor2):
                    self.assign_tasks(processor2)

                if not len(self.processor3):
                    self.assign_tasks(processor3)

                else:
                    print(f'** Task [{self.q.front()[0]}] on hold')
                    self.onHold.append(self.q.front())
                    self.q.dequeue()
                # processing
                EnteringItem = self.q.front()
                processor = self.processor1
                AssignedItem = processor[0]
                anotherprocessor1 = self.processor2
                anotherprocessor2 = self.processor3
                if len(self.onHold) >= 1 and AssignedItem[1] < anotherprocessor1[1] and AssignedItem[1] < anotherprocessor1[1] and AssignedItem[1] < EnteringItem[1]:
                    if not len(anotherprocessor1) or AssignedItem[1] < anotherprocessor1[1]:
                        if not len(anotherprocessor2) and AssignedItem[1] < anotherprocessor2[1]:
                            self.clock = AssignedItem[1]
                            print(f"** [{self.clock}] : Task [{AssignedItem[0][0]}] completed.")
                            AssignedItem.clear()
                            if not len(self.processor1):
                                self.assign_tasks(processor1)

                            if not len(self.processor2):
                                self.assign_tasks(processor2)

                            if not len(self.processor3):
                                self.assign_tasks(processor3)
                            

                if len(self.onHold) > 0:
                    EnteringItem = self.onHold[0]

                if EnteringItem[1] > AssignedItem[1]:
                    if len(anotherprocessor1) and AssignedItem[1] > anotherprocessor1[1]:
                        if len(anotherprocessor2) and AssignedItem[1] > anotherprocessor2[1]:
                            self.clock = AssignedItem[1]
                            print(f"** [{self.clock}] : Task [{AssignedItem[0][0]}] completed.")
                            AssignedItem.clear()



                EnteringItem = self.q.front()
                processor = self.processor2
                AssignedItem = processor[0]
                anotherprocessor1 = self.processor3
                anotherprocessor2 = self.processor1
                if len(self.onHold) >= 1 and AssignedItem[1] < anotherprocessor1[1] and AssignedItem[1] < anotherprocessor1[1] and AssignedItem[1] < EnteringItem[1]:
                    if not len(anotherprocessor1) or AssignedItem[1] < anotherprocessor1[1]:
                        if not len(anotherprocessor2) and AssignedItem[1] < anotherprocessor2[1]:
                            self.clock = AssignedItem[1]
                            print(f"** [{self.clock}] : Task [{AssignedItem[0][0]}] completed.")
                            AssignedItem.clear()
                            if not len(self.processor1):
                                self.assign_tasks(processor1)

                            if not len(self.processor2):
                                self.assign_tasks(processor2)

                            if not len(self.processor3):
                                self.assign_tasks(processor3)
                            

                if len(self.onHold) > 0:
                    EnteringItem = self.onHold[0]

                if EnteringItem[1] > AssignedItem[1]:
                    if len(anotherprocessor1) and AssignedItem[1] > anotherprocessor1[1]:
                        if len(anotherprocessor2) and AssignedItem[1] > anotherprocessor2[1]:
                            self.clock = AssignedItem[1]
                            print(f"** [{self.clock}] : Task [{AssignedItem[0][0]}] completed.")
                            AssignedItem.clear()

                            
                EnteringItem = self.q.front()
                processor = self.processor3
                AssignedItem = processor[0]
                anotherprocessor1 = self.processor1
                anotherprocessor2 = self.processor2
                if len(self.onHold) >= 1 and AssignedItem[1] < anotherprocessor1[1] and AssignedItem[1] < anotherprocessor1[1] and AssignedItem[1] < EnteringItem[1]:
                    if not len(anotherprocessor1) or AssignedItem[1] < anotherprocessor1[1]:
                        if not len(anotherprocessor2) and AssignedItem[1] < anotherprocessor2[1]:
                            self.clock = AssignedItem[1]
                            print(f"** [{self.clock}] : Task [{AssignedItem[0][0]}] completed.")
                            AssignedItem.clear()
                            if not len(self.processor1):
                                self.assign_tasks(processor1)

                            if not len(self.processor2):
                                self.assign_tasks(processor2)

                            if not len(self.processor3):
                                self.assign_tasks(processor3)
                            

                if len(self.onHold) > 0:
                    EnteringItem = self.onHold[0]

                if EnteringItem[1] > AssignedItem[1]:
                    if len(anotherprocessor1) and AssignedItem[1] > anotherprocessor1[1]:
                        if len(anotherprocessor2) and AssignedItem[1] > anotherprocessor2[1]:
                            self.clock = AssignedItem[1]
                            print(f"** [{self.clock}] : Task [{AssignedItem[0][0]}] completed.")
                            AssignedItem.clear()



        print(f'** [{self.clock}] : SIMULATION COMPLETED. **')

simulation = simulation_system()
InitSystem = simulation.init_system()
Enter_system = simulation.run_system()
