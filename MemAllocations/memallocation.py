import time
class MemoryAllocation:
    """
    Initialize MemoryAllocation with free memory blocks and an allocation dictionary self.freeBlocks

    Args:
        blocks - list, array of memory block sizes
    """
    def __init__(self, blocks):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.freeBlocks = {alphabet[i]:element for i, element in enumerate(blocks)}
        self.allocations = {}

    """
    Give each process a label 
    
    Args:  
        inputArr - list, array of process sizes
        
    Returns: 
        result - dictionary, each process in inputArr with key = letter label, value = process size
    """
    def arrayToDict(self, inputArr):
        # Map each element of the array to a letter in the alphabet
        reverseAlphabet = 'ZYXWVUTSRQPONMLKJIHGFEDBCA'
        # Create a dictionary combining the alphabet letters and array elements
        result = {reverseAlphabet[i]: element for i, element in enumerate(inputArr)}

        return result

    """
    Implementation of First Fit Algorithm
    
    Args:
        processesArr - list, array of process sizes
    
    Returns:
        executionTime - float, time execution took
    """
    def firstFitAllocation(self, processesArr):
        # create dictionary
        processes = self.arrayToDict(processesArr)
        # time the algorithm execution
        startTime = time.time()
        self.allocations.clear()
        for processID, processSize in processes.items():
            allocated = False
            # starting at first block
            for blockID, blockSize in self.freeBlocks.items():
                # if process will fit in block
                if blockSize >= processSize:
                    self.allocations[processID] = (blockID, processSize)
                    self.freeBlocks[blockID] -= processSize
                    allocated = True
                    break
            # no suitable block found, mark process as not allocated
            if not allocated:
                self.allocations[processID] = None
        endTime = time.time()
        executionTime = endTime - startTime
        return executionTime

    """
    Implementation of Next Fit Algorithm

    Args:
        processesArr - list, array of process sizes

    Returns:
        executionTime - float, time execution took
    """
    def nextFitAllocation(self, processesArr):
        # create dictionary
        processes = self.arrayToDict(processesArr)
        # time the algorithm execution
        startTime = time.time()
        self.allocations.clear()
        # keep track of last block allocated for next starting point
        lastAllocated = None
        for processID, processSize in processes.items():
            allocated = False
            for blockID, blockSize in self.freeBlocks.items():
                # if block is big enough and has come after lastAllocated
                if blockSize >= processSize and (lastAllocated is None or blockID >= lastAllocated):
                    self.allocations[processID] = (blockID, processSize)
                    self.freeBlocks[blockID] -= processSize
                    allocated = True
                    lastAllocated = blockID
                    break
            # no suitable block found, mark process as not allocated
            if not allocated:
                self.allocations[processID] = None
        endTime = time.time()
        executionTime = endTime - startTime
        return executionTime

    """
    Implementation of Best Fit Algorithm

    Args:
        processesArr - list, array of process sizes

    Returns:
        executionTime - float, time execution took
    """
    def bestFitAllocation(self, processesArr):
        # create dictionary
        processes = self.arrayToDict(processesArr)
        # time the algorithm execution
        startTime = time.time()
        self.allocations.clear()

        for processID, processSize in processes.items():
            bestFit = None  # keep track of allocations for comparisons
            for blockID, blockSize in self.freeBlocks.items():
                # if block is large enough
                if blockSize >= processSize:
                    # update bestFit if block is smallest found so far
                    if bestFit is None or blockSize < self.freeBlocks[bestFit]:
                        bestFit = blockID
            # allocate process to best fit block
            if bestFit is not None:
                allocatedSize = min(processSize, self.freeBlocks[bestFit])
                self.allocations[processID] = (bestFit, allocatedSize)
                self.freeBlocks[bestFit] -= allocatedSize
            # no suitable block found, mark process as not allocated
            else:
                self.allocations[processID] = None
        endTime = time.time()
        executionTime = endTime - startTime
        return executionTime

    """
    Implementation of Worst Fit Algorithm

    Args:
        processesArr - list, array of process sizes

    Returns:
        executionTime - float, time execution took
    """
    def worstFitAllocation(self, processesArr):
        # create dictionary
        processes = self.arrayToDict(processesArr)
        # time algorithm execution
        startTime = time.time()
        self.allocations.clear()
        for processID, processSize in processes.items():
            worstFit = None
            for blockID, blockSize in self.freeBlocks.items():
                # if block large enough for process
                if blockSize >= processSize:
                    # update worstFit if block is largest found so far
                    if worstFit is None or blockSize < self.freeBlocks[worstFit]:
                        worstFit = blockID
            # allocate process to worst fit block
            if worstFit is not None:
                allocatedSize = max(processSize, self.freeBlocks[worstFit])
                self.allocations[processID] = (worstFit, allocatedSize)
                self.freeBlocks[worstFit] -= allocatedSize
            # no suitable block found, mark process as not allocated
            else:
                self.allocations[processID] = None
        endTime = time.time()
        executionTime = endTime - startTime
        return executionTime

    """
    Calculates memory-related metrics (total memory, allocated memory, internal and external fragmentation)
    
    Returns:
        totalMem - total available memory for future allocations, sum of all free memory blocks
        allocatedMem - total memory that is currently in use by processes, sum of sizes of all allocated blocks 
        internalFragmentTotal - total memory currently internally fragmented, sum of differences between block sizes and allocation sizes
        externalFragmentTotal - total memory currently externally fragmented, sum of leftover free block sizes
    """
    def metrics(self):
        # total available memory for future allocations, sum of all free mem blocks
        totalMem = sum(self.freeBlocks.values())
        # total memory in use, sum of sizes of allocated blocks
        allocatedMem = sum([allocation[1] for allocation in self.allocations.values() if allocation])
        internalFragmentTotal = 0  # total memory currently internal fragmentation
        for processID, allocation  in self.allocations.items():
            # sum of differences between block sizes and allocation sizes
            if allocation:
                blockID, allocatedSize = allocation
                fragment = self.freeBlocks[blockID] - allocatedSize
                internalFragmentTotal += fragment
        externalFragmentTotal = 0  # total memory currently external fragmentation
        for blockId, blockSize in self.freeBlocks.items():
            # sum of leftover free blocks sizes
            externalFragmentTotal += blockSize
        return totalMem, allocatedMem, internalFragmentTotal, externalFragmentTotal

    """
    Determines best algorithm for given processes and memory blocks, for given determinant
    
    Args:
        freeBlocks - list, array of memory block sizes
        processes - list, array of process sizes
        determinant - str, what algorithms should be judged on
                    could be: [totalMem, allocatedMem, internalFragmentation, externalFragmentation, executionTime]
    
    Returns:
        bestAlg - name of best suited algorithm
        results - dictionary, contains metrics for each algorithm
    """
    def bestAlgorithm(self, freeBlocks, processes, determinant):
        results = {}
        for algName in ["first fit", "next fit", "best fit", "worst fit"]:
            memoryAllocate = MemoryAllocation(freeBlocks.copy()) # create new MemoryAllocation instance for each algorithm
            # execute corresponding memory allocation algorithm and get information for
            executionTime = getattr(memoryAllocate, f"{algName.lower().replace(' f', 'F')}Allocation")(processes.copy())
            # calculate metrics for algorithm's performance
            totalMem, allocatedMem, internalFragmentTotal, externalFragmentTotal = memoryAllocate.metrics()
            # store results in results dictionary
            results[algName] = {"totalMem": totalMem, "allocatedMem": allocatedMem,"internalFragmentation": internalFragmentTotal, "externalFragmentation": externalFragmentTotal, "executionTime": executionTime}

        # determine best algorithm based on given determinant
        bestAlg = min(results, key= lambda x: results[x][determinant])
        return bestAlg, results

    """
    Displays memory layout
    """
    def memoryLayout(self):
        out = "Memory Layout After Allocation:\n"
        # for each block print its id and free memory size
        for blockID, blockSize in self.freeBlocks.items():
            out += f"Block {blockID}: {blockSize} KB free\n"

        return out
    """
    Displays memory layout and allocations
    """
    def printResults(self):
        # display memory layout
        out = self.memoryLayout()

        out += ("\nAllocations:")
        for processID, allocation in self.allocations.items():
            # for each process output its allocation
            if allocation:
                blockID, allocatedSize = allocation
                out += f"\nProcess " + str(processID) + " allocated to Block " + str(blockID) + " (" + str(allocatedSize) + " KB)"
            else:
                out += "\nProcess " + str(processID) + " could not be allocated."
        return out

if __name__ == "__main__":
    freeBlocksExample = [50,150,300,350,600]
    processExample = [300, 25, 125, 50]

    memAllocate = MemoryAllocation(freeBlocksExample)
    bestAlgorithm, results = memAllocate.bestAlgorithm(freeBlocksExample, processExample, 'externalFragmentation')

    print(f"The best memory allocation algorithm is: {bestAlgorithm}")
    print("Algorithm Metrics:")
    for algorithmName, metrics in results.items():
        print(
            f"{algorithmName}: Total Available Memory={metrics['totalMem']} KB, Allocated Memory in Use={metrics['allocatedMem']} KB, External Fragmentation={metrics['externalFragmentation']} KB, Internal Fragmentation={metrics['internalFragmentation']} KB, Execution Time = {metrics['executionTime']}")
# Example usage:
if __name__ == "__main__":
    freeBlocksExample = [50,150,300,350,600]
    processesExample = [300, 24, 125, 50]

    memoryAllocator = MemoryAllocation(freeBlocksExample)

    print("First Fit Algorithm:")
    memoryAllocator.firstFitAllocation(processesExample)
    memoryAllocator.printResults()
    memoryAllocator.memoryLayout()

    print("\nNext Fit Algorithm:")
    memoryAllocator.nextFitAllocation(processesExample)
    memoryAllocator.printResults()
    memoryAllocator.memoryLayout()

    print("\nBest Fit Algorithm:")
    memoryAllocator = MemoryAllocation(freeBlocksExample)  # Reset for Best Fit
    memoryAllocator.bestFitAllocation(processesExample)
    memoryAllocator.printResults()
    memoryAllocator.memoryLayout()

    print("\nWorst Fit Algorithm:")
    memoryAllocator = MemoryAllocation(freeBlocksExample)  # Reset for Worst Fit
    memoryAllocator.worstFitAllocation(processesExample)
    memoryAllocator.printResults()
    memoryAllocator.memoryLayout()
