import process

# first come first serve algorithm
class FCFS:

    def __init__(self, numProcesses, arrivalTimes, burstTimes, contextswitch):
        self.numProcesses = numProcesses
        self.arrivalTimes = arrivalTimes  # array of arrival times ordered by process id least to greatest, len = numProcesses
        self.burstTimes = burstTimes  # array of burst times ordered by process id least to greatest, len = numProcesses
        self.contextSwitch = contextswitch
        self.processQueue = []

    def getProcessIDs(self):
        idArray = []
        for i in range(self.numProcesses):
            idArray.append(i + 1)
        return idArray

    def createProcesses(self):
        processArray = []
        for i in range(self.numProcesses):
            id = i + 1
            currentProcess = process.process(id, self.arrivalTimes[i], self.burstTimes[i], None, self.contextSwitch)
            processArray.append(currentProcess)
        processArray.sort(key=lambda x: x.arrivalTime)
        return processArray

    def makeQueue(self):
        return self.processQueue


    def completionTimes(self):
        processArray = self.createProcesses()
        completionTimes = []
        processOne = processArray[0]
        completedTime = int(processArray[0].contextSwitch + processArray[0].arrivalTime+processArray[0].burstTime)
        completed = {processArray[0].processID: completedTime}
        if processOne.arrivalTime > 0 and {"null": ("0 -> " + str(processOne.arrivalTime))} not in self.processQueue:
            self.processQueue.append({"null": ("0 -> " + str(processOne.arrivalTime))})

            if completed not in self.processQueue:
                if self.contextSwitch == 0:
                    self.processQueue.append(completed)
                else:
                    self.processQueue.append({"context switch" : str(processOne.arrivalTime) + " -> " + str(int(processOne.arrivalTime+self.contextSwitch))})
                    self.processQueue.append(completed)
        elif processOne.arrivalTime == 0 and completed not in self.processQueue:
            if self.contextSwitch == 0:
                self.processQueue.append(completed)
            else:
                self.processQueue.append({"context switch": ("0 -> " + str(int(self.contextSwitch)))})
                self.processQueue.append(completed)
        completionTimes.append(completed)
        processArray.remove(processArray[0])

        while len(processArray) > 0:
            currentProcess = processArray[0]
            completedTime += int(currentProcess.contextSwitch + currentProcess.burstTime)
            completed = {currentProcess.processID: completedTime}
            completionTimes.append(completed)
            if self.contextSwitch == 0 and {currentProcess.processID: completedTime} not in self.processQueue:
                self.processQueue.append({currentProcess.processID:completedTime})
            elif self.contextSwitch > 0 and {currentProcess.processID: completedTime} not in self.processQueue:
                self.processQueue.append({"context switch": (str(int((completedTime - currentProcess.burstTime)-currentProcess.contextSwitch)) + " -> " + str(int(completedTime - currentProcess.burstTime)))})
                self.processQueue.append({currentProcess.processID: completedTime})
            processArray.pop(0)
        return completionTimes

    # def completionTimes(self):
    #     processesOrder = self.srtf()
    #     processArray = self.createProcesses()
    #     completionTimes = []
    #     for currentProcess in processArray:
    #         eachProcess = []
    #         for partProcess in processesOrder:
    #             if list(partProcess.keys())[0] == currentProcess.processID:
    #                 partProcess[currentProcess.processID] = (partProcess.get(currentProcess.processID) + 1)
    #                 eachProcess.append(partProcess)
    #         completionTimes.append(eachProcess[-1])
    #     return completionTimes

    def turnAroundTimes(self):
        processArray = self.createProcesses()
        completionTimes = self.completionTimes()
        turnAroundTimes = []
        for i in processArray:
            for j in completionTimes:
                # print(list(j.keys())[0])
                if i.processID == list(j.keys())[0]:
                    completionTime = j.get(i.processID)
                    arrivalTime = i.arrivalTime
                    turnaround = int(completionTime) - int(arrivalTime)
                    turnaroundProcess = {i.processID: turnaround}
                    turnAroundTimes.append(turnaroundProcess)
        return turnAroundTimes

    def avgTAT(self):
        turnAroundTimes = self.turnAroundTimes()
        turnAroundTimesArray = []
        sumTAT = 0
        for currentProcess in turnAroundTimes:
            # turnAroundTimesArray.append(list(currentProcess.values())[0])
            sumTAT += list(currentProcess.values())[0]

        avg = (sumTAT / self.numProcesses)
        return avg

    def waitingTime(self):
        processArray = self.createProcesses()
        turnAroundTimes = self.turnAroundTimes()
        waitingTimes = []
        for i in processArray:
            for j in turnAroundTimes:
                # print(list(j.keys())[0])
                if i.processID == list(j.keys())[0]:
                    turnaroundTime = j.get(i.processID)
                    burstTime = i.burstTime
                    waiting = turnaroundTime - burstTime
                    waitingProcess = {i.processID: waiting}
                    waitingTimes.append(waitingProcess)
        return waitingTimes

    def avgWT(self):
        waitingTimes = self.waitingTime()
        turnAroundTimesArray = []
        sumWT = 0
        for currentProcess in waitingTimes:
            # turnAroundTimesArray.append(list(currentProcess.values())[0])
            sumWT += list(currentProcess.values())[0]

        avg = (sumWT / self.numProcesses)
        return avg

    def scheduleLength(self):
        processArray = self.createProcesses()
        completionTimes = self.completionTimes()
        firstProcess = processArray[0].arrivalTime
        lastProcess = list(max(completionTimes, key=lambda x: max(x.values())).values())[0]  # time stored in arrival time of process
        scheduleLength = lastProcess - firstProcess
        return scheduleLength

    def throughput(self):
        scheduleLength = self.scheduleLength()
        throughputDec = self.numProcesses/scheduleLength
        throughput = str(self.numProcesses) + "/" + str(scheduleLength) + " (or " + str(throughputDec) + ")"
        return throughput

    def efficiency(self):
        totalTime = self.scheduleLength()
        contextTime = self.contextSwitch * self.numProcesses
        usefulTime = self.scheduleLength() - contextTime
        efficiency = usefulTime/totalTime
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