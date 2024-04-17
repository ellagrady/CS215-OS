import process

from collections import deque

"""
Class RR
Usage for Round Robin CPU algorithm

Attributes:
    numProcesses - int, number of processes
    arrivalTimes - list, listing arrival times of each process ordered process 1 -> numProcesses
    burstTimes - list, listing burst times of each process ordered process 1 -> numProcesses
    timeQuantum - int, time quantum value

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
class RR:
    """
    initialize RR object

    Args:
        numProcesses - int, number of processes
        arrivalTimes - list, listing arrival times of each process ordered process 1 -> numProcesses
        burstTimes - list, listing burst times of each process ordered process 1 -> numProcesses
        timeQuantum - int, represents set time quantum value for processes
    """
    def __init__(self, numProcesses, arrivalTimes, burstTimes, timeQuantum):
        self.numProcesses = numProcesses
        self.arrivalTimes = arrivalTimes  # array of arrival times ordered by process id least to greatest, len = numProcesses
        self.burstTimes = burstTimes  # array of burst times ordered by process id least to greatest, len = numProcesses
        self.timeQuantum = timeQuantum
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
    create the processes, return array of processes, sorted by arrival time least to greatest

    Returns: 
        processArray - list of process objects
    """
    def createProcesses(self):
        processArray = []
        for i in range(self.numProcesses):
            processID = i + 1
            currentProcess = process.process(processID, self.arrivalTimes[i], self.burstTimes[i], self.burstTimes[i])
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
        # create processes array
        processArray = self.createProcesses()
        for x in processArray:
            print(x.processID)

        completionTimes = []
        self.processQueue = []  # Track order of processes for diagram creation

        readyQueue = []  # queue of processes ready for execution
        currentTime = processArray[0].arrivalTime
        unfinishedProcesses = list(processArray)  # Keep track of processes that are not  completed

        #
        while sum(process.remainingTime for process in processArray) > 0 and len(unfinishedProcesses) > 0:
            if len(readyQueue) == 0 and len(unfinishedProcesses) > 0:
                # add first process to ready queue
                readyQueue.append(unfinishedProcesses[0])
                currentTime = readyQueue[0].arrivalTime

            processToExecute = readyQueue[0]

            if processToExecute.remainingTime <= self.timeQuantum:
                # if burst time less than or equal to time quantum, execute until finished
                remainingTime = processToExecute.remainingTime
                processToExecute.remainingTime -= remainingTime
                currentTime += remainingTime

                # Record the completion time of the process
                self.processQueue.append({
                    processToExecute.processID: int(currentTime)})
            else:
                # Execute for the time quantum
                processToExecute.remainingTime -= self.timeQuantum
                currentTime += self.timeQuantum

                # Record the completion time of the process
                self.processQueue.append({
                    processToExecute.processID:int(currentTime)})

            arrivingProcess = []
            for p in processArray:
                # Find processes that arrive during the current execution
                if p.arrivalTime <= currentTime and p != processToExecute and p not in readyQueue and p in unfinishedProcesses:
                    arrivingProcess.append(p)

            readyQueue.extend(arrivingProcess)
            readyQueue.append(readyQueue.pop(0))  # Move the executed process to the end of the queue

            if processToExecute.remainingTime == 0:
                # Remove completed process from the unfinished processes and ready queue
                unfinishedProcesses.remove(processToExecute)
                readyQueue.remove(processToExecute)

                # Record completion time of the process
                completionTimes.append({
                    processToExecute.processID: int(currentTime),
                })

        # Sort completion times based on process ID
        completionTimes = sorted(completionTimes, key=lambda x: list(x.keys())[0])

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

        avg = (sumTAT/self.numProcesses)
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

        avg = (sum/self.numProcesses)
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
        throughputDec = self.numProcesses/scheduleLength
        throughput = str(self.numProcesses) + "/" + str(scheduleLength) + " (or " + str(throughputDec) + ")"
        return throughput

rr = RR(6, [0,1,2,3,4,6], [4,5,2,1,6,3], 2)
# print(rr.createProcesses())
print("completion times:", rr.completionTimes())
print("turn around times:", rr.turnAroundTimes())
print("waiting times:", rr.waitingTime())
print("schedule length:", rr.scheduleLength())
print("throughput:", rr.throughput())
print("average turn around time:", rr.avgTAT())
print("average waiting time:", rr.avgWT())
