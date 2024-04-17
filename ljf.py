import process

"""
Class LJF
Usage for Longest Job First CPU algorithm

Attributes:
    numProcesses - int, number of processes
    arrivalTimes - list, listing arrival times of each process ordered process 1 -> numProcesses
    burstTimes - list, listing burst times of each process ordered process 1 -> numProcesses

Methods:
    getProcessIDs() - returns list of process ids (id 1 -> id numProcesses)
    createProcesses() - creates and returns list of process objects
    makeQueue() - returns processQueue, for use in making diagram in GUI
    completionTimes() - calculates and returns list of dictionaries representing processes' completion times
    turnAroundTimes() - calculates and returns list of dictionaries representing processes' turnaround times
    avgTAT() - calculates and returns average turnaround time from turnAroundTimes()
    waitingTime() - calculates and returns list of dictionaries representing processes' waiting times
    avgWT() - calculates and returns average waiting time from waitingTime()
    scheduleLength() - calculates and returns schedule length of CPU and the processes
    throughput() - calculates and returns throughput of CPU
"""
class LJF:
    """
    initialize LJF object

    Args:
        numProcesses - int, number of processes
        arrivalTimes - list, listing arrival times of each process ordered process 1 -> numProcesses
        burstTimes - list, listing burst times of each process ordered process 1 -> numProcesses
    """
    def __init__(self, numProcesses, arrivalTimes, burstTimes):
        self.numProcesses = numProcesses
        self.arrivalTimes = arrivalTimes  # array of arrival times ordered by process id least to greatest, len = numProcesses
        self.burstTimes = burstTimes  # array of burst times ordered by process id least to greatest, len = numProcesses
        self.processQueue = []

    """
    Returns array of processIds, calculated from entered numProcesses (1 to numProcesses)

    Returns: 
        idArray - list of ints, represents ids of all processes (1 to numProcesses)
    """
    def getProcessIDs(self):
        idArray = []
        for i in range(self.numProcesses):
            idArray.append(i + 1)
        return idArray

    """
    create the processes, return array of processes

    Returns: 
        processArray - list of process objects
    """
    def createProcesses(self):
        processArray = []
        for i in range(self.numProcesses):
            id = i + 1
            currentProcess = process.process(id, self.arrivalTimes[i], self.burstTimes[i])
            processArray.append(currentProcess)
        processArray.sort(key=lambda x: x.arrivalTime)
        return processArray

    """
    Returns queue of processes, to be used for diagram created in GUI

    Returns: 
        processQueue - list of processes as they enter CPU (regardless of being finished)
    """
    def makeQueue(self):
        return self.processQueue

    """
    Calculates completion times for each process, returns as list of dictionaries

    Returns: 
        completionTimes - list of dicts ({processID: completionTime}), represents completion times for each process
    """
    def completionTimes(self):
        processArray = self.createProcesses()
        completionTimes = []
        # handle process with processId 1
        processOne = processArray[0]
        completedTime = processOne.arrivalTime + processOne.burstTime
        completedProcess = {processOne.processID: completedTime}
        completionTimes.append(completedProcess)
        # add completed process to processQueue
        if completedProcess not in self.processQueue:
            if processOne.arrivalTime > 0 and {"null": ("0 -> " + str(processOne.arrivalTime))} not in self.processQueue:
                self.processQueue.append({"null": ("0 -> " + str(processOne.arrivalTime))})
            self.processQueue.append(completedProcess)
        processArray.remove(processOne)
        # for all other processes
        while len(processArray) > 0:
            longestBurst = max(processArray, key=lambda x: x.burstTime)
            completedTime += longestBurst.burstTime
            completedProcess = {longestBurst.processID: completedTime}
            if completedProcess not in self.processQueue:
                self.processQueue.append(completedProcess)
            completionTimes.append(completedProcess)
            processArray.remove(longestBurst)
        return completionTimes

    """
    Calculate turnaround times for each process, returns as list of dictionaries
        TAT = completion time - arrival time

    Returns:
        turnAroundTimes - list of dictionaries ({processID: TAT}), represents TAT for each process
    """
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

    """
    Calculates average TAT from turnaround times list

    Returns:
        avg - int, average TAT from turnAroundTimes() results
    """
    def avgTAT(self):
        turnAroundTimes = self.turnAroundTimes()
        sum = 0
        for currentProcess in turnAroundTimes:
            sum += list(currentProcess.values())[0]

        avg = (sum / self.numProcesses)
        return avg

    """
    Calculate wait times, returns as list of dictionaries
        WT = TAT - burst time

    Returns: 
        waitingTimes - list of dictionaries ({processID: WT}), representing wait time of each process
    """
    def waitingTime(self):
        processArray = self.createProcesses()
        turnAroundTimes = self.turnAroundTimes()
        waitingTimes = []
        for i in processArray:
            for j in turnAroundTimes:
                if i.processID == list(j.keys())[0]:
                    turnaroundTime = j.get(i.processID)
                    burstTime = i.burstTime
                    waiting = turnaroundTime - burstTime
                    waitingProcess = {i.processID: waiting}
                    waitingTimes.append(waitingProcess)
        return waitingTimes

    """
    Calculate average wait time from waiting times list

    Returns: 
        avg - average from results of waitingTime()
    """
    def avgWT(self):
        waitingTimes = self.waitingTime()
        turnAroundTimesArray = []
        sum = 0
        for currentProcess in waitingTimes:
            # turnAroundTimesArray.append(list(currentProcess.values())[0])
            sum += list(currentProcess.values())[0]

        avg = (sum / self.numProcesses)
        return avg

    """ 
    Calculate length of CPU action
        scheduleLength = last process completion time - first process arrival time

    Returns:
        scheduleLength - int, total length of time CPU is in action
    """
    def scheduleLength(self):
        processArray = self.createProcesses()
        completionTimes = self.completionTimes()
        lastProcess = max(completionTimes, key=lambda x: max(x.values()))
        startProcess = min(processArray, key=lambda x: x.arrivalTime)

        scheduleLength = (list(lastProcess.values())[0]) - startProcess.arrivalTime
        return scheduleLength

    """
   Calculate throughput
       throughput = numProcesses/scheduleLength

   Returns:
       throughput - int, processes to time ratio
   """
    def throughput(self):
        scheduleLength = self.scheduleLength()
        throughputDec = self.numProcesses / scheduleLength
        throughput = str(self.numProcesses) + "/" + str(scheduleLength) + " (or " + str(throughputDec) + ")"
        return throughput


ljf = LJF(5, [1, 2, 3, 4, 5], [7, 5, 1, 2, 8])
print("completion times:", ljf.completionTimes())
print("turn around times:", ljf.turnAroundTimes())
print("waiting times:", ljf.waitingTime())
print("schedule length:", ljf.scheduleLength())
print("throughput:", ljf.throughput())
print("average turn around time:", ljf.avgTAT())
print("average waiting time:", ljf.avgWT())