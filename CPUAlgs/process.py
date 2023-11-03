
class process:

    # initialize process object
    def __init__(self, processid, arrivaltime, bursttime):
        self.processID = processid
        self.arrivalTime = arrivaltime
        self.burstTime = bursttime

    # initialize process object with contextswitch/tq
    def __init__(self, processid, arrivaltime, bursttime, remainingtime=None, contextswitch = None):
        self.processID = processid
        self.arrivalTime = arrivaltime
        self.burstTime = bursttime
        if remainingtime is not None:
            self.remainingTime = remainingtime
        if contextswitch is not None:
            self.contextSwitch = contextswitch

    # comparison function
    def __lt__(self, other):
        return self.remainingTime < other.remainingTime

    # return process' id
    def getID(self):
        return self.processID

    # return arrival time of process
    def getArrivalTime(self):
        return self.arrivalTime

    # return burst time of process
    def getBurstTime(self):
        return self.burstTime

    # reeturn remaining time of process
    def getRemainingTime(self):
        return self.remainingTime


