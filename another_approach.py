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
        try:
            return self.p2[-1]
        except:
            return self.p2[0]

    def isEmpty(self):
        return not self.p1 and not self.p2


class simulation_system(Queue):
# _____________________INITIALISE SYSTEM_________________________________________________________
    def init_system(self):
        self.q = Queue()
        connection = sqlite3.connect('Simulation_data.db')
        cur = connection.cursor()
        cur.execute("SELECT * FROM dataset ORDER BY arrival ASC")
        tasksList = cur.fetchall()
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
        try:
            EnteringItem = self.q.front()
            AssignedItem = processor

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
            else:
                self.entering_system()
        except:
            self.entering_system()

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

    def run_system(self):

        processor1 = self.processor1
        processor2 = self.processor2
        processor3 = self.processor3

        try:
            for i in range(100):
                self.entering_system()
                # assigning
                if not len(self.processor1):
                    self.assign_tasks(processor1)

                elif not len(self.processor2):
                    self.assign_tasks(processor2)

                elif not len(self.processor3):
                    self.assign_tasks(processor3)

                else:
                    print(f'** Task [{self.q.front()[0]}] on hold')
                    self.onHold.append(self.q.front())
                    self.q.dequeue()

                # processing
                self.task_processing(processor1, processor2, processor3)
                self.task_processing(processor2, processor3, processor1)
                self.task_processing(processor3, processor1, processor2)

        except:
            try:
                self.endpoint1()
            except:
                print(f'** [{self.clock}] : SIMULATION COMPLETED. **')

    def endpoint1(self):

        if len(self.processor1):
            if len(self.processor2) and self.processor1[1] > self.processor2[1]:
                self.endpoint2()
            if len(self.processor3) and self.processor1[1] > self.processor3[1]:
                self.endpoint3()
            self.clock = self.processor1[1]
            print(f"** [{self.clock}] : Task [{self.processor1[0][0]}] completed.")
            self.processor1.clear()
        elif self.onHold:
            self.processor1.append(self.onHold[0])
            print(f"** [{self.clock}] : Task [{self.processor1[0][0]}] assigned to processor [1]")
            self.onHold.pop(0)
            self.clock += self.processor1[0][2]
            self.processor1.append(self.clock)
        elif len(self.processor2):
            self.endpoint2()
        elif len(self.processor3):
            self.endpoint3()



    def endpoint2(self):
        if len(self.processor2):
            if len(self.processor3) and self.processor2[1] > self.processor3[1]:
                self.endpoint3()
            self.clock = self.processor2[1]
            print(f"** [{self.clock}] : Task [{self.processor2[0][0]}] completed.")
            self.processor2.clear()
        elif self.onHold:
            self.processor2.append(self.onHold[0])
            print(f"** [{self.clock}] : Task [{self.processor2[0][0]}] assigned to processor [2]")
            self.onHold.pop(0)
            self.clock += self.processor2[0][2]
            self.processor2.append(self.clock)
        if len(self.processor3):
            self.endpoint3()
        if len(self.processor1):
            self.endpoint1()

    def endpoint3(self):
        if len(self.processor3):
            self.clock = self.processor3[1]
            print(f"** [{self.clock}] : Task [{self.processor3[0][0]}] completed.")
            self.processor3.clear()
        elif self.onHold:
            self.processor3.append(self.onHold[0])
            print(f"** [{self.clock}] : Task [{self.processor3[0][0]}] assigned to processor [3]")
            self.onHold.pop(0)
            self.clock += self.processor3[0][2]
            self.processor3.append(self.clock)
        if len(self.processor2):
            self.endpoint2()
        if len(self.processor1):
            self.endpoint1()




simulation = simulation_system()
InitSystem = simulation.init_system()
Enter_system = simulation.run_system()









