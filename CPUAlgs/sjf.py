import process


# shortest job first algorithm
class SJF:

    # initialize shortest job first object w/ number of processes, list of arrival times, and list of burst times
    def __init__(self, numProcesses, arrivalTimes, burstTimes):
        self.numProcesses = numProcesses
        self.arrivalTimes = arrivalTimes  # array of arrival times ordered by process id least to greatest, len = numProcesses
        self.burstTimes = burstTimes  # array of burst times ordered by process id least to greatest, len = numProcesses
        self.processQueue = []

    # method to get list of process ids from 1-numProcesses
    def getProcessIDs(self):
        idArray = []
        for i in range(self.numProcesses):
            idArray.append(i + 1)
        return idArray

    # create the Process objects for each process in the SJF object
    def createProcesses(self):
        processArray = []
        for i in range(self.numProcesses):
            processID = i + 1
            currentProcess = process.process(processID, self.arrivalTimes[i], self.burstTimes[i])
            processArray.append(currentProcess)
        processArray.sort(key=lambda x: x.arrivalTime)
        return processArray

    # calculate time it takes to complete each process following SJF logic, returns list of dictionaries
    def completionTimes(self):
        processArray = self.createProcesses()
        for i in processArray:
            print(i.processID, i.arrivalTime, i.burstTime)

        completionTimes = []
        # handle process with processId 1
        processOne = processArray[0]
        completedTime = processOne.arrivalTime + processOne.burstTime
        completedProcess = {processOne.processID: completedTime}
        completionTimes.append(completedProcess)
        if processOne.arrivalTime > 0 and {"null": ("0 -> " + str(processOne.arrivalTime))} not in self.processQueue:
            self.processQueue.append({"null": ("0 -> " + str(processOne.arrivalTime))})
        if completedProcess not in self.processQueue:
            self.processQueue.append(completedProcess)
        processArray.remove(processOne)
        # find the shortest processes in processArray and systematically calculate then remove
        while len(processArray) > 0:
            shortestBurst = min(processArray, key=lambda x: x.burstTime)
            completedTime += shortestBurst.burstTime
            completedProcess = {shortestBurst.processID: completedTime}
            completionTimes.append(completedProcess)
            if completedProcess not in self.processQueue:
                self.processQueue.append(completedProcess)
            processArray.remove(shortestBurst)
        return completionTimes

    # return processQueue for use in making diagram
    def makeQueue(self):
        return self.processQueue

    # calculate the turn around times for each process, returns list of dictionaries
    #   turnaround time = completion time - arrival time
    def turnAroundTimes(self):
        processArray = self.createProcesses()
        completionTimes = self.completionTimes()
        turnAroundTimes = []
        # for each process in the processArray and its corresponding calculated completion time
        #   calculate turn around time = completion time - arrival time
        for i in processArray:
            for j in completionTimes:
                #print(list(j.keys())[0])
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

    # calculate the waiting times for each process, returns list of dictionaries
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

sjf = SJF(5, [1, 2, 3, 4, 5], [7, 5, 1, 2, 8])
print("process queue:", sjf.makeQueue())
print("completion times:", sjf.completionTimes())
print("process queue:", sjf.makeQueue())
print("turn around times:", sjf.turnAroundTimes())
print("waiting times:", sjf.waitingTime())
print("schedule length:", sjf.scheduleLength())
print("throughput:", sjf.throughput())
print("average turn around time:", sjf.avgTAT())
print("average waiting time:", sjf.avgWT())
