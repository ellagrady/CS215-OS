
class process:

    def __init__(self, processid, arrivaltime, bursttime):
        self.processID = processid
        self.arrivalTime = arrivaltime
        self.burstTime = bursttime

    def __init__(self, processid, arrivaltime, bursttime, remainingtime=None, contextswitch = None):
        self.processID = processid
        self.arrivalTime = arrivaltime
        self.burstTime = bursttime
        if remainingtime is not None:
            self.remainingTime = remainingtime
        if contextswitch is not None:
            self.contextSwitch = contextswitch

    def __lt__(self, other):
        return self.remainingTime < other.remainingTime

    def getID(self):
        return self.processID

    def getArrivalTime(self):
        return self.arrivalTime

    def getBurstTime(self):
        return self.burstTime

    def getRemainingTime(self):
        return self.remainingTime


