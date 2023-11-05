import srtf as SRTF
import sjf as SJF
import fcfs as FCFS
import ljf as LJF
import gradio as gr
import rr as RR


import matplotlib.pyplot as plt


processesQueue = ""


"""
format string output containing all necessary calculations

Args: 
    function - str representing alg type
    numProcesses - int, number of processes to use CPU
    arrivalTimesText - str representation of array of arrival times of processes (ordered process 1 - numProcesses)
    burstTimesText - str representation of array of burst times of processes (ordered process 1 - numProcesses)
    contextSwitch_TQ - None or int, representing context switch or time quantum 
    
Returns: 
    outputStr - string to be output to GUI window containing all calculations
    
"""
def formatOutput(function, numProcesses, arrivalTimesText, burstTimesText, contextSwitch_TQ=None):

    arrivalTimes = processArray(arrivalTimesText)
    burstTimes = processArray(burstTimesText)

    # based on function selected at top, create corresponding object
    if function == "SJF":
        func = SJF.SJF(numProcesses, arrivalTimes, burstTimes)
    elif function == "SRTF":
        func = SRTF.SRTF(numProcesses, arrivalTimes, burstTimes)
    elif function == "FCFS":
        func = FCFS.FCFS(numProcesses, arrivalTimes, burstTimes, contextSwitch_TQ)
    elif function == "LJF":
        func = LJF.LJF(numProcesses, arrivalTimes, burstTimes)
    else:  # function == "RR":
        func = RR.RR(numProcesses, arrivalTimes, burstTimes, contextSwitch_TQ)

    # calculate the different pieces
    completionTimes = func.completionTimes()
    turnAroundTimes = func.turnAroundTimes()
    waitingTimes = func.waitingTime()
    scheduleLength = func.scheduleLength()
    throughput = func.throughput()
    avgTAT = func.avgTAT()
    avgWT = func.avgWT()

    processQueue = func.makeQueue()

    outputStr = ""
    outputStr += "Completion Times: [" + ', '.join(str(completionTime) for completionTime in completionTimes) + "]\n"
    global processesQueue
    processesQueue = processQueue
    setGlobal(processesQueue)
    outputStr += "Turn Around Times: [" + ', '.join(str(turnAroundTime) for turnAroundTime in turnAroundTimes) + "\n"
    outputStr += "Waiting Times: [" + ','.join(str(waitingTime) for waitingTime in waitingTimes) + "\n"
    outputStr += "Schedule Length: " + str(scheduleLength) + "\n"
    outputStr += "Throughput: " + str(throughput) + "\n"
    outputStr += "Average TAT: " + str(avgTAT) + "\n"
    outputStr += "Average WT: " + str(avgWT)

    return outputStr


"""
create the diagram of the processes in the CPU

Returns:
    image file of diagram 
"""
def createDiagram():
    data = processesQueue
    processIDs = []
    completionTimes = []
    # create queue of processes
    for currProcess in data:
        if list(currProcess.keys())[0] == "null":

            processIDs.append("Waiting")
            completionTimes.append(int(list(currProcess.values())[0].split(' ')[-1]))
            continue
        if list(currProcess.keys())[0] == "context switch":
            processIDs.append("context switch")
            completionTimes.append(int(list(currProcess.values())[0].split(' ')[-1]))
            continue
        processIDs.append(list(currProcess.keys())[0])
        completionTimes.append(list(currProcess.values())[0])

    fig, ax = plt.subplots(figsize=(20, 5))
    if type(completionTimes[0]) != int:
        completionTimes[0] = completionTimes[0].split(' ')[-1]

    # add first process to diagram
    bars = ax.barh(1, completionTimes[0], height=0.1, label=processIDs[0], align='center', edgecolor='black', linewidth=1, color='#465B6B')

    labelX = sum(completionTimes[:1]) + completionTimes[0] / 2
    ax.text(labelX, 0, str(processIDs[0]), ha='center', va='center', color='white', fontsize=12)

    patchHandles = [bars]
    for id, val in enumerate(processIDs[:-1]):
        if type(completionTimes[id]) != int:
            completionTimes[id] = completionTimes[id].split(' ')[-1]
        prevY = completionTimes[id]
        id += 1

        # add bars
        bars = ax.barh(y=1, width=completionTimes[id]-prevY, height=0.1, left=prevY, label=processIDs[id], align='center', edgecolor = 'black', linewidth=1, color='#465B6B')
        patchHandles.append(bars)

    # label names
    labels=[]
    for i in processIDs:
        if type(i) == int:
            labels.append("P"+str(i))
        else:
            labels.append(i.replace(' ', '\n'))

    # add label names
    for j in range(len(patchHandles)):
        for i, patch in enumerate(patchHandles[j]):
            bl = patch.get_xy()
            x = 0.5 * patch.get_width() + bl[0]
            y = 0.5 * patch.get_height() + bl[1]
            ax.text(x, y, labels[j], ha='center', va='center', fontsize=12, color='white')
            print(labels[j])

    customXTicks = completionTimes
    print(customXTicks)
    ax.set_xticks([0] + customXTicks)
    ax.set_xlabel("Process Completion Times")
    ax.set_yticks([])
    ax.set_title("CPU Scheduling")

    plt.tight_layout()

    # Save the plot to a file and return the file name
    plot_filename = "horizontal_stacked_bar_plot.png"
    plt.savefig(plot_filename, format="png")
    plt.close()

    return plot_filename

""" 
process selected input for alg type from Gradio Radio object, return as str

Args: 
    inputOption - input from gr.Radio object

Returns: 
    str(inputOption) - input formatted as string
"""
def processRadio(inputOption):
    return str(inputOption)


"""
process input data to number objects, return as int

Args:
    inputNumber - input from gr.Number object
    
Returns:
    int(inputNumber) - input formatted as int
"""
def processNumber(inputNumber):
    return int(inputNumber)


""" 
process input data to textbox objects, return as string

Args: 
    inputText - input from gr.Textbox object

Returns:
    str(inputText) - input formatted as string
"""
def processText(inputText):
    return str(inputText)


"""
process array input data to textbox objects, return as an array

Args: 
    inputText - input from gr.Textbox object

Returns:
    array - input formatted as a list object
"""
def processArray(inputText):
    array = eval(inputText)
    return array


"""
set a global variable

Args: 
    queue - global variable 

Returns:
    global variable processQueue to be set to input
"""
def setGlobal(queue):
    global processesQueue
    processesQueue = queue
    return processesQueue


"""
calculate parts, calling formatOutput function

Args:
    algChoices - input from gr.Radio, represents algorithm choice
    numProcesses - input from gr.Number, representing number of processes
    arrivalTimes - input from gr.Textbox, representing array of arrival times (ordered process 1 - numProcesses)
    burstTimes - input from gr.Textbox, representing array of burst times (ordered process 1 - numProcesses)
    contextSwitch_TQ - None or input from gr.Number, representing set context switch or time quantum value
    
Returns:
    out - return of formatOutput(algChoice, numProcessesInput, arrivalTiemsInput, burstTimesInput, contextSwitch_TQ)
"""
def calculateFn(algChoices, numProcesses, arrivalTimes, burstTimes, contextSwitch_TQ = None):

    # make sure input is correct
    if algChoices is not None and numProcesses is not None and arrivalTimes is not None and burstTimes is not None:
        algChoice = str(algChoices)
        numProcessesInput = processNumber(numProcesses)
        arrivalTimesInput = processText(arrivalTimes)
        burstTimesInput = processText(burstTimes)
        # when contextSwitch not included
        if contextSwitch_TQ is None:
            out = formatOutput(algChoice, numProcessesInput, arrivalTimesInput, burstTimesInput)
            print("processesQueue:", processesQueue)
            return out
        # when contextSwitch is included
        else:
            out = formatOutput(algChoice, numProcessesInput, arrivalTimesInput, burstTimesInput, contextSwitch_TQ)
            print("processesQueue:", processesQueue)
            return out
    else:
        return "Invalid input."

"""
Create GUI from Gradio Library
    https://github.com/gradio-app/gradio
"""
with gr.Blocks() as demo:
    gr.Markdown("Select the algorithm of your choosing.")
    # one window for algorithms without context switch/time quantum section
    with gr.Tab("SJF/SRTF/LJF"):
        with gr.Row():
            gr.Label("Shortest Job First")
            gr.Label("Shortest Remaining Time First")
            gr.Label("Longest Job First")

        # outputs: completion times, turnaround times, waiting times, schedule length, throughput,
        #   average turn around times, average waiting times,
        algChoices = gr.Radio(["SJF", "SRTF", "LJF"], label="Algorithms", interactive=True)
        numProcesses = gr.Number(label="Number of Processes", interactive=True)
        arrivalTimes = gr.Textbox(label="Arrival Times (formatted as an array, ordered by process ID 1-numProcesses, contained within [])", interactive=True)
        burstTimes = gr.Textbox(label="Burst Times (formatted as an array, ordered by process ID 1-numProcesses, contained within [])", interactive=True)

        calculate = gr.Button(value="Calculate!")

        outputBtn = gr.Textbox(label="Output", interactive=False)
        calculate.click(calculateFn, inputs = [algChoices, numProcesses, arrivalTimes, burstTimes], outputs=outputBtn)

    # tab for algorithms with context switch/time quantum
    with gr.Tab("FCFS/RR"):

        with gr.Row():
            gr.Label("First Come First Serve")
            gr.Label("Round Robin")

        # outputs: completion times, turnaround times, waiting times, schedule length, throughput,
        #   average turn around times, average waiting times,

        algChoices = gr.Radio(["FCFS", "RR"], label="Algorithms", interactive=True)
        numProcesses = gr.Number(label="Number of Processes", interactive=True)
        arrivalTimes = gr.Textbox(
            label="Arrival Times (formatted as an array, ordered by process ID 1-numProcesses, contained within [])",
            interactive=True)
        burstTimes = gr.Textbox(
            label="Burst Times (formatted as an array, ordered by process ID 1-numProcesses, contained within [])",
            interactive=True)
        contextSwitch_TQ = gr.Number(label = "Context Switch (FCFS) | Time Quantum (RR)", interactive=True)

        calculate = gr.Button(value="Calculate!")

        outputBtn = gr.Textbox(label="Output", interactive=False)
        calculate.click(calculateFn, inputs=[algChoices, numProcesses, arrivalTimes, burstTimes, contextSwitch_TQ], outputs=[outputBtn])
        output = calculateFn(algChoices, numProcesses.value, arrivalTimes, burstTimes, contextSwitch_TQ)

    # create the diagram
    with gr.Accordion("Open for Diagram!"):
        createBtn = gr.Button(value="Create Diagram")

        createBtn.click(createDiagram, inputs=None, outputs=gr.Image(type="pil"))


demo.launch(share=True)




