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
        return not self.p1 and not self.p2

class simulation_system(Queue):

# _________________________________INITIALISE SYSTEM_________________________________________________________

    def init_system(self):
        self.q = Queue()
        connection = sqlite3.connect('Simulation_data.db')
        cur = connection.cursor()
        cur.execute("SELECT id, arrival, duration FROM dataset ORDER BY arrival ASC")
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

# _________________________________FILTER TASKS_____________________________________________________
    def enter_system(self):
        if not self.q.isEmpty():
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
                self.complete_tasks()
        else:
            self.endpoint1()
# _________________________________ASSIGN TASKS TO PROCESSORS________________________________________________________
    def assign_tasks(self, processor, num):
        if self.onHold:
            processor.append(self.onHold[0])
            print(f"** [{self.clock}] : Task [{processor[0][0]}] assigned to processor [{num}]")
            self.onHold.pop(0)
        else:
            processor.append(self.q.front())
            print(f"** [{self.clock}] : Task [{processor[0][0]}] assigned to processor [{num}]")
            self.q.dequeue()
        self.clock += processor[0][2]
        processor.append(self.clock)
        self.complete_tasks()

    def assign_processor(self):
        EnteringItem = self.q.front()
        if not len(self.processor1):
            processor = self.processor1
            self.assign_tasks(processor, 1)
        elif not len(self.processor2):
            processor = self.processor2
            self.assign_tasks(processor, 2)
        elif not len(self.processor3):
            processor = self.processor3
            self.assign_tasks(processor, 3)
        else:
            print(f'** Task [{EnteringItem[0]}] on hold')
            self.onHold.append(self.q.front())
            self.q.dequeue()
            self.complete_tasks()
# _________________________________PROCESSING____________________________________________________________________________________________
    def processing(self, AssignedItem):
        self.clock = AssignedItem[1]
        print(f"** [{self.clock}] : Task [{AssignedItem[0][0]}] completed.")
        AssignedItem.clear()

    def complete_tasks(self):
        try:
            EnteringItem = self.q.front()
            AssignedItem = self.processor1
            if len(self.onHold) >= 1 and AssignedItem[1] < self.processor2[1] and AssignedItem[1] < self.processor2[1] and AssignedItem[1] < EnteringItem[1]:
                if len(self.processor2) and AssignedItem[1] > self.processor2[1]:
                    self.complete_tasks2()
                if len(self.processor3) and AssignedItem[1] > self.processor3[1]:
                    self.complete_tasks3()
                self.processing(AssignedItem)
                self.assign_processor()

            if len(self.onHold) > 0:
                EnteringItem = self.onHold[0]

            if EnteringItem[1] > AssignedItem[1]:
                if len(self.processor2) and AssignedItem[1] > self.processor2[1]:
                    self.complete_tasks2()
                if len(self.processor3) and AssignedItem[1] > self.processor3[1]:
                    self.complete_tasks3()
                self.clock = AssignedItem[1]
                self.processing(AssignedItem)
                self.complete_tasks2()

            else:
                self.complete_tasks2()
        except:
            self.complete_tasks2()

    def complete_tasks2(self):
        try:
            EnteringItem = self.q.front()
            AssignedItem = self.processor2
            if len(self.onHold) >= 1 and AssignedItem[1] < self.processor1[1] and AssignedItem[1] < self.processor3[1] and AssignedItem[1] < EnteringItem[1]:
                if len(self.processor3) and AssignedItem[1] > self.processor3[1]:
                    self.complete_tasks3()
                self.processing(AssignedItem)
                self.assign_processor()

            if len(self.onHold) > 0:
                EnteringItem = self.onHold[0]

            if EnteringItem[1] > AssignedItem[1]:
                if len(self.processor3) and AssignedItem[1] > self.processor3[1]:
                    self.complete_tasks3()
                self.processing(AssignedItem)
                self.complete_tasks3()
            else:
                self.complete_tasks3()
        except:
            self.complete_tasks3()

    def complete_tasks3(self):
        try:
            EnteringItem = self.q.front()
            AssignedItem = self.processor3
            if len(self.onHold) and AssignedItem[1] < self.processor2[1] and AssignedItem[1] < self.processor1[1] and AssignedItem[1] < EnteringItem[1]:
                if len(self.processor1) and AssignedItem[1] > self.processor1[1]:
                    self.complete_tasks()
                self.processing(AssignedItem)
                self.assign_processor()

            if len(self.onHold):
                EnteringItem = self.onHold[0]

            if EnteringItem[1] > AssignedItem[1]:
                if len(self.processor1) and AssignedItem[1] > self.processor1[1]:
                    self.complete_tasks()
                self.processing(AssignedItem)
                self.complete_tasks()
            else:
                self.enter_system()
        except:
            self.enter_system()

# _________________________________LAST TASKS PROCESSING WHEN EVERYTASKS ARE DEQUEUED__________________________________________
    def onHoldEnd(self, processor, num):
        processor.append(self.onHold[0])
        print(f"** [{self.clock}] : Task [{processor[0][0]}] assigned to processor [{num}]")
        self.onHold.pop(0)
        self.clock += processor[0][2]
        processor.append(self.clock)

    def processorEnd(self, processor):
        self.clock = processor[1]
        print(f"** [{self.clock}] : Task [{processor[0][0]}] completed.")
        processor.clear()

    def endpoint1(self):
            processor = self.processor1
            if len(processor):
                if len(self.processor2) and processor[1] > self.processor2[1]:
                    self.endpoint2()
                if len(self.processor3) and processor[1] > self.processor3[1]:
                    self.endpoint3()
                self.processorEnd(processor)
            if self.onHold:
                self.onHoldEnd(processor, 1)
            if len(self.processor2):
                self.endpoint2()
            if len(self.processor3):
                self.endpoint3()

    def endpoint2(self):
            processor = self.processor2
            if len(processor):
                if len(self.processor3) and processor[1] > self.processor3[1]:
                    self.endpoint3()
                if len(self.processor1) and processor[1] > self.processor1[1]:
                    self.endpoint1()
                self.processorEnd(processor)
            if self.onHold:
                self.onHoldEnd(processor, 2)
            if len(self.processor3):
                self.endpoint3()
            if len(self.processor1):
                self.endpoint1()

    def endpoint3(self):
            processor = self.processor3
            if len(processor):
                if len(self.processor1) and processor[1] > self.processor1[1]:
                    self.endpoint1()
                if len(self.processor2) and processor[1] > self.processor2[1]:
                    self.endpoint2()
                self.processorEnd(processor)
            if self.onHold:
                self.onHoldEnd(processor, 3)
            if len(self.processor1):
                self.endpoint1()
            if len(self.processor2):
                self.endpoint2()

# _________________________________SYSTEM ENDED______________________________________________________
    def ending(self):
        print(f'** [{self.clock}] : SIMULATION COMPLETED. **')

# _________________________________RUN SYSTEM_____________________________________________
Simulation = simulation_system()
try:
    InitSystem = Simulation.init_system()
    StartSystem = Simulation.enter_system()
except:
    pass
EndSystem = Simulation.ending()
