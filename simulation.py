import sqlite3
import re

class Queue(object):
    def __init__(self):
        self.p1 = []
        self.p2 = []

    def enqueue(self, item):#O(1)
        self.p1.append(item)

    def dequeue(self):      #O(1)
        self.front()
        return self.p2.pop()

    def front(self):        #O(1) : this is a fuction this system required but built-in module doesn't have
        if not self.p2:
            while self.p1:
                    self.p2.append(self.p1.pop())
        return self.p2[-1]

    def isEmpty(self):
        return not self.p1 and not self.p2

class simulation_system(Queue):

########################################INITIALISE SYSTEM######################################################################################################################

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

# #######################Belows are the function prepared to run the system#####################################################################################################


    def entering_system(self):
            # entering
            EnteringItem = self.q.front()
            self.clock = EnteringItem[1]
            print(f"** [{self.clock}] : Task [{EnteringItem[0]}] with duration [{EnteringItem[2]}] enters the system.")

            # filtering
            pattern = re.compile(r"((?=.*[\d])(?=.*[a-z])(?=.*[A-Z])|(?=.*[\d])(?=.*[a-zA-Z])(?=.*[@#*&_-])|(?=.*[a-z])(?=.*[A-Z])(?=.*[@#*&_-])).*")
            if True:
                if pattern.match(EnteringItem[0]):
                    print(f"** Task [{EnteringItem[0]}] accepted.\n")
                    self.taskAcceptButNotYetAssignedOrHold = 1
                else:
                    print(f"** Task [{EnteringItem[0]}] unfeasible and discarded.\n")
                    self.q.dequeue()

    def assign_tasks(self, processor, num):

        #assigning if tasks onHold
        if self.onHold:
            processor.append(self.onHold[0])
            print(f"** [{self.clock}] : Task [{processor[0][0]}] assigned to processor [{num}]")
            self.onHold.pop(0)

        #assigning if nothing is onHold
        else:
            processor.append(self.q.front())
            self.q.dequeue()
            print(f"** [{self.clock}] : Task [{processor[0][0]}] assigned to processor [{num}]")
            self.taskAcceptButNotYetAssignedOrHold = 0
        processor.append(self.clock + processor[0][2])

        #processing by processor
    def completing (self, processor):
        self.clock = processor[1]
        print(f"** [{self.clock}] : Task [{processor[0][0]}] completed.")
        processor.clear()


################################## run_system is actually running the system#######################################################################################################
    def run_system(self):

            processor1 = self.processor1
            processor2 = self.processor2
            processor3 = self.processor3

            completion_time1 = 110#These are default values for comparison when nothing in processor 1 or 2 or 3.
            completion_time2 = 111#These values will be set back to default when a task completed.
            completion_time3 = 112#

            self.taskAcceptButNotYetAssignedOrHold = 0 # when a task get accepted but not yet assigned or onHold, it increases to 1.

            ################################################### Start - Let tasks enter##############################################################
            while not self.q.isEmpty(): # loop until queue is empty
                firstItem = self.q.front()

                #completion time for each processors should be greater than the first item's arrival in the queue if the first item needs to enter the system.
                if self.q.front()[1] <= completion_time1 and firstItem[1] <= completion_time2 and firstItem[1] <= completion_time3:
                    if  firstItem[1] <= completion_time1 and firstItem[1] <= completion_time2 and firstItem[1] <= completion_time3:
                        if self.onHold:
                            if onHold_completion_time <= firstItem[1]:
                                pass
                        self.entering_system()


            #################################################### assigning tasks#################################################################

                #if nothing is in processors and tasks got accepted or onhold and the first Item's arrival in the queue less than or equal to processors' completion time:

                if not len(processor1) and self.taskAcceptButNotYetAssignedOrHold:
                    if firstItem[1] <= completion_time1 and firstItem[1] <= completion_time2 and firstItem[1] <= completion_time3:
                        self.assign_tasks(processor1, 1)
                        completion_time1 = processor1[1]

                if not len(processor2) and self.taskAcceptButNotYetAssignedOrHold:
                    if firstItem[1] <= completion_time1 and firstItem[1] <= completion_time2 and firstItem[1] <= completion_time3:
                        self.assign_tasks(processor2, 2)
                        completion_time2 = processor2[1]

                if not len(processor3) and self.taskAcceptButNotYetAssignedOrHold:
                    if firstItem[1] <= completion_time1 and firstItem[1] <= completion_time2 and firstItem[1] <= completion_time3:
                        self.assign_tasks(processor3, 3)
                        completion_time3 = processor3[1]

                #if processors are full, onHold
                if len(self.processor1) and len(self.processor2) and len(self.processor3) and self.taskAcceptButNotYetAssignedOrHold:
                    print(f'** Task [{firstItem[0]}] on hold\n')
                    self.onHold.append(firstItem)
                    onHold_completion_time = self.clock + self.onHold[0][2]
                    self.taskAcceptButNotYetAssignedOrHold = 0
                    self.q.dequeue()

            ################################################# processing tasks###################################################

                #comparing the completion time among processors
                if completion_time1 <= firstItem[1] and completion_time1 <= completion_time2 and completion_time1 <= completion_time3:
                        self.completing (processor1)
                        completion_time1 = 110

                if completion_time2 <= firstItem[1] and completion_time2 <= completion_time3 and completion_time2 <= completion_time1:
                    if completion_time2 < completion_time3:
                        self.completing (processor2)
                        completion_time2 = 111

                if completion_time3 <= firstItem[1] and completion_time3 <= completion_time1 and completion_time3 <= completion_time2:
                        self.completing (processor3)
                        completion_time3 = 112

###########################################clear tasks that remain in processors and onHold  while the queue is empty############################################################

            while len(processor1) or len(processor2) or len(processor3):

                if completion_time1 <= completion_time2 and completion_time1 <= completion_time3:
                    self.completing(processor1)
                    completion_time1 = 110
                    if self.onHold:
                        self.assign_tasks(processor1, 1)
                        completion_time1 = processor1[1]

                if completion_time2 <= completion_time3 and completion_time2 <= completion_time1:
                    self.completing(processor2)
                    completion_time2 = 111
                    if self.onHold:
                        self.assign_tasks(processor2, 1)
                        completion_time2 = processor2[1]

                if completion_time3 <= completion_time1 and completion_time3 <= completion_time2:
                    self.completing(processor3)
                    completion_time3 = 112
                    if self.onHold:
                        self.assign_tasks(processor3, 1)
                        completion_time3 = processor3[1]


##########################################################Ending##############################################################################################

    def end (self):

        print(f'** [{self.clock}] : SIMULATION COMPLETED. **')

#####################################################Class instantiation######################################################################################
simulation = simulation_system()
InitSystem = simulation.init_system()
Enter_system = simulation.run_system()
end_system = simulation.end()
