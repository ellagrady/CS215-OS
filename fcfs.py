import process

"""
Class FCFS
Usage for First Come First Serve CPU algorithm

Attributes:
    numProcesses - int, number of processes
    arrivalTimes - list, listing arrival times of each process ordered process 1 -> numProcesses
    burstTimes - list, listing burst times of each process ordered process 1 -> numProcesses
    contextSwitch - int, context switch value

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
    cpuEfficiency() - calculates and returns the efficiency of the CPU
"""
class FCFS:
    """
    initialize FCFS object

    Args:
        numProcesses - int, number of processes
        arrivalTimes - list, listing arrival times of each process ordered process 1 -> numProcesses
        burstTimes - list, listing burst times of each process ordered process 1 -> numProcesses
        contextSwitch - int, context switch value
    """

    def __init__(self, numProcesses, arrivalTimes, burstTimes, contextSwitch):
        self.numProcesses = numProcesses
        self.arrivalTimes = arrivalTimes  # array of arrival times ordered by process id least to greatest, len = numProcesses
        self.burstTimes = burstTimes  # array of burst times ordered by process id least to greatest, len = numProcesses
        self.contextSwitch = contextSwitch
        self.processQueue = []

    """
    Returns array of processIds, calculated from entered numProcesses (1 to numProcesses)
    
    Returns: 
        idArray - list of ints, represents ids of all processes (1 to numProcesses)
    """

    # return array of processIDs, calculated from entered numProcesses (1 to numProcesses)
    def getProcessIDs(self):
        idArray = []
        for i in range(self.numProcesses):
            idArray.append(i + 1)
        return idArray

    """
    create the processes, return array of processes, sorted by arrival times least to greatest
    
    Returns: 
        processArray - list of process objects
    """

    def createProcesses(self):
        processArray = []
        for i in range(self.numProcesses):
            id = i + 1
            currentProcess = process.process(id, self.arrivalTimes[i], self.burstTimes[i], None, self.contextSwitch)
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
        # make processes
        processArray = self.createProcesses()
        completionTimes = []
        processOne = processArray[0]
        completedTime = int(processArray[0].contextSwitch + processArray[0].arrivalTime + processArray[0].burstTime)
        completed = {processArray[0].processID: completedTime}
        # include waiting time if first process arrival time is not at 0
        if processOne.arrivalTime > 0 and {"null": ("0 -> " + str(processOne.arrivalTime))} not in self.processQueue:
            self.processQueue.append({"null": ("0 -> " + str(processOne.arrivalTime))})

            # keep track of processes for diagram
            if completed not in self.processQueue:
                if self.contextSwitch == 0:
                    self.processQueue.append(completed)
                else:
                    self.processQueue.append({"context switch": str(processOne.arrivalTime) + " -> " + str(
                        int(processOne.arrivalTime + self.contextSwitch))})
                    self.processQueue.append(completed)
        # if first process arrives at 0
        elif processOne.arrivalTime == 0 and completed not in self.processQueue:
            if self.contextSwitch == 0:
                self.processQueue.append(completed)
            else:
                self.processQueue.append({"context switch": ("0 -> " + str(int(self.contextSwitch)))})
                self.processQueue.append(completed)
        completionTimes.append(completed)
        processArray.remove(processArray[0])

        # for all other processes
        while len(processArray) > 0:
            currentProcess = processArray[0]
            completedTime += int(currentProcess.contextSwitch + currentProcess.burstTime)
            completed = {currentProcess.processID: completedTime}
            completionTimes.append(completed)
            # context switch set to 0, not worry about adding to diagram
            if self.contextSwitch == 0 and {currentProcess.processID: completedTime} not in self.processQueue:
                self.processQueue.append({currentProcess.processID: completedTime})
            # context switch > 0, include context switch pause time
            elif self.contextSwitch > 0 and {currentProcess.processID: completedTime} not in self.processQueue:
                self.processQueue.append({"context switch": (str(int(
                    (completedTime - currentProcess.burstTime) - currentProcess.contextSwitch)) + " -> " + str(
                    int(completedTime - currentProcess.burstTime)))})
                self.processQueue.append({currentProcess.processID: completedTime})
            processArray.pop(0)
        return completionTimes

    """
    Calculate turnaround times for each process, returns as list of dictionaries
        TAT = completion time - arrival time
        
    Returns:
        turnAroundTimes - list of dictionaries ({processID: TAT}), represents TAT for each process
    """

    # calculate turn around times, return as list of dictionaries
    #   TAT = completion time - arrival time
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

    # calculate avg wt from list of wait times
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
        lastProcess = list(max(completionTimes, key=lambda x: max(x.values())).values())[
            0]  # time stored in arrival time of process
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
        throughputDec = self.numProcesses / scheduleLength
        throughput = str(self.numProcesses) + "/" + str(scheduleLength) + " (or " + str(throughputDec) + ")"
        return throughput

    """
    Calculate CPU Efficiency
        efficiency = useful time (active) / total (+ context switch pauses) time 
    
    Returns: 
        cpuEfficiency - str, ratio and decimal representation of efficiency
    """

    # calculate cpu efficiency, usefultime/totaltime
    def efficiency(self):
        totalTime = self.scheduleLength()
        contextTime = self.contextSwitch * self.numProcesses
        usefulTime = self.scheduleLength() - contextTime
        efficiency = usefulTime / totalTime
        cpuEfficiency = str(usefulTime) + "/" + str(totalTime) + " (or " + str(efficiency) + ")"
        return cpuEfficiency


fcfs = FCFS(5, [0, 1, 2, 3, 4], [4, 3, 1, 2, 5], 1)
print("processesOrder:", fcfs.completionTimes())
print("turn around times:", fcfs.turnAroundTimes())
print("waiting times:", fcfs.waitingTime())
print("schedule length:", fcfs.scheduleLength())
print("throughput:", fcfs.throughput())
print("average turn around time:", fcfs.avgTAT())
print("average waiting time:", fcfs.avgWT())
print("CPU Efficiency", fcfs.efficiency())
