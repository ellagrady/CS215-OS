
class process:

    """
    Initializes process object

    Args:
        processid - int of process' id number
        arrivaltime - int, time process arrives at CPU
        bursttime - int, time process will last
    """
    # initialize process object
    def __init__(self, processid, arrivaltime, bursttime):
        self.processID = processid
        self.arrivalTime = arrivaltime
        self.burstTime = bursttime

    """ 
    Initializes process object, with contextwitch/tq value
    
    Args:
        processid - int of process' id number
        arrivaltime - int, time process arrives at CPU
        bursttime - int, time process will last
        remainingtime - int, time remaining for process
        contextswitch - int, set context switch or time quantum value for process
    """
    def __init__(self, processid, arrivaltime, bursttime, remainingtime=None, contextswitch = None):
        self.processID = processid
        self.arrivalTime = arrivaltime
        self.burstTime = bursttime
        if remainingtime is not None:
            self.remainingTime = remainingtime
        if contextswitch is not None:
            self.contextSwitch = contextswitch

    """
    Less than comparison
    
    Args: 
        other - second process
    
    Returns:
        self.remainingTime < other.remainingTime - boolean, True if self.remainingTime is less than, False if greater than
    """
    def __lt__(self, other):
        return self.remainingTime < other.remainingTime

    """
    Return process' id
    
    Returns:
        self.processID - int, process' id number
    """
    def getID(self):
        return self.processID

    """
    Returns process' arrival time
    
    Returns:  
        self.arrivalTime - int, process' arrival time
    """
    def getArrivalTime(self):
        return self.arrivalTime

    """
    Returns process' burst time
    
    Returns:
        self.burstTime - int, process' burst time
    """
    def getBurstTime(self):
        return self.burstTime

    """
    Returns process' remaining time
    
    Returns: 
        self.remainingTime - int, process' remaining time
    """
    def getRemainingTime(self):
        return self.remainingTime


