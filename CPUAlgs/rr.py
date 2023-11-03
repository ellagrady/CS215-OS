import process

from collections import deque

# round robin algorithm
class RR:

    # initialize round robin object w/ number of processes, list of arrival times, list of burst times, and time quantum
    def __init__(self, numProcesses, arrivalTimes, burstTimes, timeQuantum):
        self.numProcesses = numProcesses
        self.arrivalTimes = arrivalTimes  # array of arrival times ordered by process id least to greatest, len = numProcesses
        self.burstTimes = burstTimes  # array of burst times ordered by process id least to greatest, len = numProcesses
        self.timeQuantum = timeQuantum
        self.processQueue = []

    # method to get list of process ids from 1-numProcesses
    def getProcessIDs(self):
        idArray = []
        for i in range(self.numProcesses):
            idArray.append(i + 1)
        return idArray

    # create the Process objects for each process in the RR object
    def createProcesses(self):
        processArray = []
        for i in range(self.numProcesses):
            processID = i + 1
            currentProcess = process.process(processID, self.arrivalTimes[i], self.burstTimes[i])
            processArray.append(currentProcess)
        processArray.sort(key=lambda x: x.arrivalTime)
        return processArray

    # return processQueue, for use in making diagram
    def makeQueue(self):
        return self.processQueue

    # calculate time it takes to complete each process following RR logic, return list of dictionaries
    def completionTimes(self):
        processArray = self.createProcesses()
        queue = deque(processArray)
        completionTimes = []  # To store the order of process completion
        currentTime = 0

        while queue:
            currentProcess = queue.popleft()
            if currentProcess.arrivalTime > currentTime:
                # Process arrives later, push it to the end of the queue
                currentTime = currentProcess.arrivalTime
                queue.append(currentProcess)
            else:
                if currentProcess.burstTime <= self.timeQuantum:
                    # Process completes within the time slice
                    completionTimes.append({currentProcess.processID: int(currentTime + currentProcess.burstTime)})
                    currentTime += currentProcess.burstTime
                else:
                    # Process still needs more time
                    completionTimes.append({currentProcess.processID: int(currentTime + self.timeQuantum)})
                    currentTime += self.timeQuantum
                    currentProcess.burstTime = currentProcess.burstTime - self.timeQuantum
                    queue.append(currentProcess)

        self.processQueue = completionTimes

        finalCompletionTimes = []

        for i in self.getProcessIDs():

            processList = []
            for process in completionTimes:
                if i == (list(process.keys())[0]):
                    processList.append(process)

            sortedProcesses = sorted(processList, key=lambda x: max (x.values()))
            maxTime = list(sortedProcesses[-1].values())[0]
            finalCompletionTimes.append({i: maxTime})
        return finalCompletionTimes

    # calculate the turn around times for each process, return list of dictionaries
    #   turnaround time = completion time - arrival time
    def turnAroundTimes(self):
        processArray = self.createProcesses()
        completionTimes = self.completionTimes()
        turnAroundTimes = []
        for i in processArray:
            for j in completionTimes:
                if i.processID == list(j.keys())[0]:
                    completionTime = j.get(i.processID)
                    arrivalTime = i.arrivalTime
                    turnaround = int(completionTime) - int(arrivalTime)
                    turnaroundProcess = {i.processID: turnaround}
                    turnAroundTimes.append(turnaroundProcess)
        return turnAroundTimes

    # from list of all processes' turn around times, calculate average
    def avgTAT(self):
        turnAroundTimes = self.turnAroundTimes()
        sumTAT = 0
        for currentProcess in turnAroundTimes:
            sumTAT += list(currentProcess.values())[0]

        avg = (sumTAT/self.numProcesses)
        return avg

    # calculate the waiting times for each process, return list of dictionaries
    #   waiting time = turnaround time - burst time
    def waitingTime(self):
        processArray = self.createProcesses()
        turnAroundTimes = self.turnAroundTimes()
        waitingTimes = []
        # for each process in the processArray and its corresponding burst time
        #   calculate waiting time = turn around time - burst time
        for i in processArray:
            for j in turnAroundTimes:
                if i.processID == list(j.keys())[0]:
                    turnaroundTime = j.get(i.processID)
                    burstTime = i.burstTime
                    waiting = turnaroundTime - burstTime
                    waitingProcess = {i.processID: waiting}
                    waitingTimes.append(waitingProcess)
        return waitingTimes

    # from list of all processes' turn around times, calculate average
    def avgWT(self):
        waitingTimes = self.waitingTime()
        turnAroundTimesArray = []
        sum = 0
        for currentProcess in waitingTimes:
            # turnAroundTimesArray.append(list(currentProcess.values())[0])
            sum += list(currentProcess.values())[0]

        avg = (sum/self.numProcesses)
        return avg

    # find total time taken to complete all processes
    #   schedule length = last process completion time - arrival time of first process
    def scheduleLength(self):
        processArray = self.createProcesses()
        completionTimes = self.completionTimes()
        lastProcess = max(completionTimes, key=lambda x: max(x.values()))
        startProcess = min(processArray, key=lambda x: x.arrivalTime)

        scheduleLength = (list(lastProcess.values())[0]) - startProcess.arrivalTime
        return scheduleLength

    # calculate throughput for completion of all processes
    #   throughput = number of processes/schedule length
    def throughput(self):
        scheduleLength = self.scheduleLength()
        throughputDec = self.numProcesses/scheduleLength
        throughput = str(self.numProcesses) + "/" + str(scheduleLength) + " (or " + str(throughputDec) + ")"
        return throughput

rr = RR(6, [0,1,2,3,4,6], [4,5,2,1,6,3], 3)
# print(rr.createProcesses())
print("completion times:", rr.completionTimes())
# print("turn around times:", rr.turnAroundTime())
# print("waiting times:", rr.waitingTime())
# print("schedule length:", rr.scheduleLength())
# print("throughput:", rr.throughput())
# print("average turn around time:", rr.avgTAT())
# print("average waiting time:", rr.avgWT())
