import process


"""
Class SRTF
Usage for Shortest Remaining Time First CPU algorithm

Attributes:
    numProcesses - int, number of processes
    arrivalTimes - list, listing arrival times of each process ordered process 1 -> numProcesses
    burstTimes - list, listing burst times of each process ordered process 1 -> numProcesses

Methods:
    getProcessIDs() - returns list of process ids (id 1 -> id numProcesses)
    createProcesses() - creates and returns list of process objects
    srtf() - calculates and returns list of processes order
    makeQueue() - returns processQueue, for use in making diagram in GUI
    completionTimes() - calculates and returns list of dictionaries representing processes' completion times
    turnAroundTimes() - calculates and returns list of dictionaries representing processes' turnaround times
    avgTAT() - calculates and returns average turnaround time from turnAroundTimes()
    waitingTime() - calculates and returns list of dictionaries representing processes' waiting times
    avgWT() - calculates and returns average waiting time from waitingTime()
    scheduleLength() - calculates and returns schedule length of CPU and the processes
    throughput() - calculates and returns throughput of CPU
"""
class SRTF:

    """
    initialize SRTF object

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
            currentProcess = process.process(id, self.arrivalTimes[i], self.burstTimes[i], self.burstTimes[i])
            processArray.append(currentProcess)
        processArray.sort(key=lambda x: x.arrivalTime)
        return processArray

    """
    Calculates processesOrder, returns list of dictionaries
    
    Returns:
        processesOrder - list of dictionaries ({id: time process stops running at}), 
            not completion times but accounts for preemptive nature
    """
    def srtf(self):
        processArray = self.createProcesses()
        completedProcesses = []
        inProgressProcesses = []
        processesOrder = []  # fill with dictionary items {id: start time}
        time = 0  # current time
        processOne = processArray[0]
        if processOne.arrivalTime > 0 and {"null" : ("0 -> " + str(processOne.arrivalTime))} not in self.processQueue:
            self.processQueue.append({"null": ("0 -> " + str(processOne.arrivalTime))})
        while len(completedProcesses) < self.numProcesses:
            # add arrived processes to list of in progress processes
            for current in processArray:
                if current.arrivalTime <= time and current not in inProgressProcesses and current not in completedProcesses:
                    inProgressProcesses.append(current)
                # if no processes currently running, advance time
                if not inProgressProcesses:
                    time += 1
                else:  # sort in progress processes by time remaining
                    inProgressProcesses.sort(key=lambda x: x.remainingTime)

                    # current process is executed for one time unit
                    currentProcess = inProgressProcesses[0]
                    currentProcess.remainingTime -= 1
                    processesOrder.append({currentProcess.processID: time})
                    if {currentProcess.processID: time+1} not in self.processQueue:
                        self.processQueue.append({currentProcess.processID: time+1})

                    # once process is completed, it's removed from list of in progress processes
                    if currentProcess.remainingTime == 0:
                        inProgressProcesses.remove(currentProcess)
                        completedProcesses.append(currentProcess)
                        if {currentProcess.processID: time+1} not in self.processQueue:
                            self.processQueue.append({currentProcess.processID: time+1})

                    time += 1

        return processesOrder

    """
    Returns queue of processes, to be used for diagram created in GUI

    Returns: 
        processQueue - list of processes as they enter CPU (regardless of being finished)
    """
    def makeQueue(self):
        return self.processQueue

    """
    Calculates completion times for each process using srtf() fn, returns as list of dictionaries

    Returns: 
        completionTimes - list of dicts ({processID: completionTime}), represents completion times for each process
    """
    def completionTimes(self):
        processesOrder = self.srtf()
        processArray = self.createProcesses()
        completionTimes = []
        for currentProcess in processArray:
            eachProcess = []
            for partProcess in processesOrder:
                if list(partProcess.keys())[0] == currentProcess.processID:
                    partProcess[currentProcess.processID] = (partProcess.get(currentProcess.processID) + 1)
                    eachProcess.append(partProcess)
            completionTimes.append(eachProcess[-1])
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
        sumTAT = 0
        for currentProcess in turnAroundTimes:
            sumTAT += list(currentProcess.values())[0]

        avg = (sumTAT / self.numProcesses)
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
        sumWT = 0
        for currentProcess in waitingTimes:
            sumWT += list(currentProcess.values())[0]

        avg = (sumWT / self.numProcesses)
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
        firstProcess = processArray[0].arrivalTime
        lastProcess = list(max(completionTimes, key=lambda x: max(x.values())).values())[0]  # time stored in arrival time of process
        scheduleLength = lastProcess - firstProcess
        return scheduleLength

    """
    Calculate throughput
        throughput = numProcesses/scheduleLength

    Returns:
        throughput - int, processes to time ratio
    """
    def throughput(self):
        scheduleLength = self.scheduleLength()
        throughputDec = self.numProcesses/scheduleLength
        throughput = str(self.numProcesses) + "/" + str(scheduleLength) + " (or " + str(throughputDec) + ")"
        return throughput


srtf = SRTF(6, [0, 1, 2, 3, 4, 5], [7, 5, 3, 1, 2, 1])
print("processesOrder:", srtf.srtf())
print("completionTimes:", srtf.completionTimes())
print("turn around times:", srtf.turnAroundTimes())
print("avg TAT:", srtf.avgTAT())
print("waiting times:", srtf.waitingTime())
print("avg WT:", srtf.avgWT())
print("schedule length:", srtf.scheduleLength())
print("throughput:", srtf.throughput())




