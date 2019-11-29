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

# _____________________INITIALISE SYSTEM_________________________________________________________
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
        self.onHold = []
        self.processor1 = []
        self.processor2 = []
        self.processor3 = []
        connection.commit()
        connection.close()
        return print("** SYSTEM INITIALISED **")

# ________________________FILTER TASKS_____________________________________________________
    
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
    def assign_cons(self, processor):
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
        self.complete_tasks()

    def assign_processor(self):
        EnteringItem = self.q.front()
        processor1 = self.processor1
        processor2 = self.processor2
        processor3 = self.processor3
        if len(self.processor1) == 0:
            self.assign_cons(processor1)
        elif len(self.processor2) == 0:
            self.assign_cons(processor2)
        elif len(self.processor3) == 0:
            self.assign_cons(processor3)
        else:
            print(f'** Task [{EnteringItem[0]}] on hold')
            self.onHold.append(self.q.front())
            self.q.dequeue()
            self.complete_tasks()

# ____________________________________PROCESSING____________________________________________________________________________________________
    def processing(self, processor, anotherprocessor1, anotherprocessor2, goAnotherP1, goAnotherP2 ):
        EnteringItem = self.q.front()
        AssignedItem = processor

        if len(self.onHold) >= 1 and AssignedItem[1] < anotherprocessor1[1] and AssignedItem1[1] < anotherprocessor1[1] and AssignedItem1[1] < EnteringItem[1]:
            if len(anotherprocessor1) and AssignedItem[1] > self.processor2[1]:
                goAnotherP1()
            if len(anotherprocessor2) and AssignedItem[1] > anotherprocessor2[1]:
                goAnotherP2()
            self.clock = AssignedItem[1]
            print(f"** [{self.clock}] : Task [{AssignedItem[0][0]}] completed.")
            AssignedItem.clear()
            self.assign_processor()

        if len(self.onHold) > 0:
            EnteringItem = self.onHold[0]

        if EnteringItem[1] > AssignedItem[1]:
            if len(anotherprocessor1) and AssignedItem[1] > anotherprocessor1[1]:
                goAnotherP1()
            if len(anotherprocessor2) and AssignedItem[1] > anotherprocessor2[1]:
                goAnotherP2()
            self.clock = AssignedItem[1]
            print(f"** [{self.clock}] : Task [{AssignedItem[0][0]}] completed.")
            processor.clear()
            goAnotherP1()
        else:
            goAnotherP1()

    def complete_tasks(self):
        try:
            processor = self.processor1
            anotherprocessor1 = self.processor2
            anotherprocessor2 = self.processor3
            goAnotherP1 = self.complete_tasks2
            goAnotherP2 = self.complete_tasks3
            processing(processor, anotherprocessor1, anotherprocessor2, goAnotherP1, goAnotherP2)
        except:
            self.complete_tasks2()

    def complete_tasks2(self):
        try:
            processor = self.processor2
            anotherprocessor1 = self.processor3
            anotherprocessor2 = self.processor1
            goAnotherP1 = self.complete_tasks3
            goAnotherP2 = self.complete_tasks
            processing(processor, anotherprocessor1, anotherprocessor2, goAnotherP1, goAnotherP2)
        except:
            self.complete_tasks3()

    def complete_tasks3(self):
        try:
            EnteringItem = self.q.front()
            AssignedItem3 = self.processor3
            if len(self.onHold) and AssignedItem3[1] < self.processor2[1] and AssignedItem3[1] < self.processor1[1] and AssignedItem3[1] < EnteringItem[1]:
                if len(self.processor1) and AssignedItem3[1] > self.processor1[1]:
                    self.complete_tasks()
                self.clock = AssignedItem3[1]
                print(f"** [{self.clock}] : Task [{AssignedItem3[0][0]}] completed.")
                self.processor3.clear()
                self.assign_processor()

            if len(self.onHold):
                EnteringItem = self.onHold[0]

            if EnteringItem[1] > AssignedItem3[1]:
                if len(self.processor1) and AssignedItem3[1] > self.processor1[1]:
                    self.complete_tasks()
                self.clock = AssignedItem3[1]
                print(f"** [{self.clock}] : Task [{AssignedItem3[0][0]}] completed.")
                self.processor3.clear()
                self.complete_tasks()
            else:
                self.enter_system()
        except:
            self.enter_system()

# _________________________________PROCESSING WHEN QUEUE IS EMPTY__________________________________________
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

# _______________________________________________SYSTEM ENDED______________________________________________________
    def ending(self):
        print(f'** [{self.clock}] : SIMULATION COMPLETED. **')

# _____________________________________________START SYSTEM_____________________________________________
Simulation = simulation_system()
InitSystem = Simulation.init_system()

StartSystem = Simulation.enter_system()
EndSystem = Simulation.ending()

















