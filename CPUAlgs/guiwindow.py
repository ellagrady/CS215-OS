import pandas

import srtf as SRTF
import sjf as SJF
import process
import fcfs as FCFS
import ljf as LJF
import gradio as gr
import rr as RR


import matplotlib.pyplot as plt
import pandas as pd
import io
from PIL import Image


import ast
from tkintertable import TableCanvas, TableModel

processesQueue = ""

def sjf(numProcesses, arrivalTimes, burstTimes):
    # print("value", arrivalTimes)
    arrivalTimesList = ast.literal_eval(arrivalTimes)
    burstTimesList = ast.literal_eval(burstTimes)
    sjfProcess = SJF.SJF(int(numProcesses), arrivalTimesList, burstTimesList)
    completionTimes = sjfProcess.completionTimes()
    global processesQueue
    processesQueue = sjfProcess.processQueue
    turnAroundTimes = sjfProcess.turnAroundTimes()
    waitingTimes = sjfProcess.waitingTime()
    scheduleLength = sjfProcess.scheduleLength()
    throughput = sjfProcess.throughput()
    avgTAT = sjfProcess.avgTAT()
    avgWT = sjfProcess.avgWT()
    print(', '.join(str(completionTime) for completionTime in completionTimes))

    return [processesQueue, completionTimes, turnAroundTimes, waitingTimes, scheduleLength, throughput, avgTAT, avgWT]


def srtf(numProcesses, arrivalTimes, burstTimes ):
    arrivalTimesList = ast.literal_eval(arrivalTimes)
    burstTimesList = ast.literal_eval(burstTimes)
    srtfProcess = SRTF.SRTF(int(numProcesses), arrivalTimesList, burstTimesList)
    completionTimes = srtfProcess.completionTimes()
    global processesQueue
    processesQueue = srtfProcess.processQueue
    turnAroundTimes = srtfProcess.turnAroundTimes()
    waitingTimes = srtfProcess.waitingTime()
    scheduleLength = srtfProcess.scheduleLength()
    throughput = srtfProcess.throughput()
    avgTAT = srtfProcess.avgTAT()
    avgWT = srtfProcess.avgWT()
    return [processesQueue, completionTimes, turnAroundTimes, waitingTimes, scheduleLength, throughput, avgTAT, avgWT]


def fcfs(numProcesses, arrivalTimes, burstTimes, contextSwitch):
    arrivalTimesList = ast.literal_eval(arrivalTimes)
    burstTimesList = ast.literal_eval(burstTimes)
    fcfsProcess = FCFS.FCFS(int(numProcesses), arrivalTimesList, burstTimesList, int(contextSwitch))
    completionTimes = fcfsProcess.completionTimes()
    global processesQueue
    processesQueue = fcfsProcess.processQueue
    turnAroundTimes = fcfsProcess.turnAroundTimes()
    waitingTimes = fcfsProcess.waitingTime()
    scheduleLength = fcfsProcess.scheduleLength()
    throughput = fcfsProcess.throughput()
    avgTAT = fcfsProcess.avgTAT()
    avgWT = fcfsProcess.avgWT()
    return [processesQueue, completionTimes, turnAroundTimes, waitingTimes, scheduleLength, throughput, avgTAT, avgWT]


def ljf(numProcesses, arrivalTimes, burstTimes):
    arrivalTimesList = ast.literal_eval(arrivalTimes)
    burstTimesList = ast.literal_eval(burstTimes)
    ljfProcess = LJF.LJF(int(numProcesses), arrivalTimesList, burstTimesList)
    completionTimes = ljfProcess.completionTimes()
    global processesQueue
    processesQueue = ljfProcess.processQueue
    turnAroundTimes = ljfProcess.turnAroundTimes()
    waitingTimes = ljfProcess.waitingTime()
    scheduleLength = ljfProcess.scheduleLength()
    throughput = ljfProcess.throughput()
    avgTAT = ljfProcess.avgTAT()
    avgWT = ljfProcess.avgWT()
    return [processesQueue, completionTimes, turnAroundTimes, waitingTimes, scheduleLength, throughput, avgTAT, avgWT]


def rr(numProcesses, arrivalTimes, burstTimes, timeQuantum):
    arrivalTimesList = ast.literal_eval(arrivalTimes)
    burstTimesList = ast.literal_eval(burstTimes)
    rrProcess = RR.RR(int(numProcesses), arrivalTimesList, burstTimesList, timeQuantum)
    completionTimes = rrProcess.completionTimes()
    global processesQueue
    processesQueue = rrProcess.processQueue
    turnAroundTimes = rrProcess.turnAroundTimes()
    waitingTimes = rrProcess.waitingTime()
    scheduleLength = rrProcess.scheduleLength()
    throughput = rrProcess.throughput()
    avgTAT = rrProcess.avgTAT()
    avgWT = rrProcess.avgWT()
    return [processesQueue, completionTimes, turnAroundTimes, waitingTimes, scheduleLength, throughput, avgTAT, avgWT]


def format_output(function, numProcesses, arrivalTimesText, burstTimesText, contextSwitch_TQ=None):

    arrivalTimes = processArray(arrivalTimesText)
    burstTimes = processArray(burstTimesText)

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

    completionTimes = func.completionTimes()

    turnAroundTimes = func.turnAroundTimes()
    waitingTimes = func.waitingTime()
    scheduleLength = func.scheduleLength()
    throughput = func.throughput()
    avgTAT = func.avgTAT()
    avgWT = func.avgWT()

    processQueue = func.makeQueue()

    outputStr = ""
    # outputStr += "Process Order: [" + ', '.join(str(process) for process in processQueue) + "]\n"
    outputStr += "Completion Times: [" + ', '.join(str(completionTime) for completionTime in completionTimes) + "]\n"
    global processesQueue
    #processesQueue = ', '.join(str(process) for process in processQueue)
    processesQueue = processQueue
    setGlobal(processesQueue)
    outputStr += "Turn Around Times: [" + ', '.join(str(turnAroundTime) for turnAroundTime in turnAroundTimes) + "\n"
    outputStr += "Waiting Times: [" + ','.join(str(waitingTime) for waitingTime in waitingTimes) + "\n"
    outputStr += "Schedule Length: " + str(scheduleLength) + "\n"
    outputStr += "Throughput: " + str(throughput) + "\n"
    outputStr += "Average TAT: " + str(avgTAT) + "\n"
    outputStr += "Average WT: " + str(avgWT)

    return outputStr


imageData = io.BytesIO


def createDiagram():
    # Parse user input data into a DataFrame
    data = processesQueue
    processIDs = []
    completionTimes = []
    print(data)
    for currProcess in data:
        print(currProcess)
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
    print(processIDs)
    print(completionTimes)
    if type(completionTimes[0]) != int:
        completionTimes[0] = completionTimes[0].split(' ')[-1]
    bars = ax.barh(1, completionTimes[0], height=0.1, label=processIDs[0], align='center', edgecolor='black', linewidth=1, color='#465B6B')

    labelX = sum(completionTimes[:1]) + completionTimes[0] / 2
    ax.text(labelX, 0, str(processIDs[0]), ha='center', va='center', color='white', fontsize=12)

    # plt.bar(1, completionTimes[0], color = 'r')
    #labels = [processIDs[0]]
    patchHandles = [bars]
    for id, val in enumerate(processIDs[:-1]):
        if type(completionTimes[id]) != int:
            completionTimes[id] = completionTimes[id].split(' ')[-1]
        prevY = completionTimes[id]
        id += 1

        # plt.bar(x=1, height=completionTimes[id], bottom=prevY)
        bars = ax.barh(y=1, width=completionTimes[id]-prevY, height=0.1, left=prevY, label=processIDs[id], align='center', edgecolor = 'black', linewidth=1, color='#465B6B')
        patchHandles.append(bars)
        # Add labels directly to the stacks using the bar_label method
        #if type(val) == int:

    labels=[]
    for i in processIDs:
        if type(i) == int:
            labels.append("P"+str(i))
        else:
            labels.append(i.replace(' ', '\n'))
        # else:
        #     labels.append(str(str(val).replace(' ', '\n')))


    for j in range(len(patchHandles)):
        for i, patch in enumerate(patchHandles[j]):
            bl = patch.get_xy()
            x = 0.5 * patch.get_width() + bl[0]
            y = 0.5 * patch.get_height() + bl[1]
            ax.text(x, y, labels[j], ha='center', va='center', fontsize=12, color='white')

    customXTicks = completionTimes
    ax.set_xticks(customXTicks)
    ax.set_xlabel("Process Completion Times")
    # customYTicks = [0, 1, 2]
    ax.set_yticks([])
    ax.set_title("CPU Scheduling")



    plt.tight_layout()

    #
    # bottom = None
    # for i, completionTime in enumerate(zip(processIDs, completionTimes)):
    #     ax.barh(completionTime, i, left=bottom, label=i)
    #
    # ax.set_xlabel("Completion Times")
    # ax.set_title("Horizontal Stacked Bar Plot")
    # ax.legend()
    #
    # plt.tight_layout()

    # Save the plot to a file and return the file name
    plot_filename = "horizontal_stacked_bar_plot.png"
    plt.savefig(plot_filename, format="png")
    plt.close()

    return plot_filename
    # print("data frame:", processIDs)
    # print(completionTimes)
    # dataf = {
    #     "processID" : processIDs,
    #     "completionTime": completionTimes
    # }
    # df = pd.DataFrame(dataf)
    #
    # # Create a Gantt chart
    # fig, ax = plt.subplots()
    # for i, row in df.iterrows():
    #     ax.broken_barh([(row["completionTime"], row["processID"])], (i, 1), facecolors=("blue",))
    #
    # # Configure the Gantt chart
    # ax.set_xlabel("Time")
    # ax.set_yticks(range(len(df)))
    # ax.set_yticklabels(df["completionTime"])
    # ax.invert_yaxis()
    # plt.title("Gantt Chart")
    #
    # # Save the chart to an in-memory buffer
    # buffer = io.BytesIO()
    # plt.savefig(buffer, format="png")
    # buffer.seek(0)
    # # Return the binary image data for Gradio to display
    # global imageData
    # imageData = buffer.read()
    # return buffer.read()


def processRadio(inputOption):
    return str(inputOption)


def processNumber(inputNumber):

    return int(inputNumber)


def processText(inputText):
    return str(inputText)


def processArray(inputText):
    array = eval(inputText)
    return array





def createGradioImage():
    print("queue:", processesQueue)

    imageBytes = createDiagram(processesQueue)
    global imageData
    pilImage = Image.open(io.BytesIO(imageData))

    return pilImage


def setGlobal(queue):
    global processesQueue
    processesQueue = queue
    return processesQueue




def calculateFn(algChoices, numProcesses, arrivalTimes, burstTimes, contextSwitch_TQ = None):

    if algChoices is not None and numProcesses is not None and arrivalTimes is not None and burstTimes is not None:
        algChoice = str(algChoices)
        numProcessesInput = processNumber(numProcesses)
        arrivalTimesInput = processText(arrivalTimes)
        burstTimesInput = processText(burstTimes)
        if contextSwitch_TQ is None:
            output = format_output(algChoice, numProcessesInput, arrivalTimesInput, burstTimesInput)
            print("processesQueue:", processesQueue)
            global imageData
            #imageData = createDiagram(processesQueue)
            return output
        else:
            output = format_output(algChoice, numProcessesInput, arrivalTimesInput, burstTimesInput, contextSwitch_TQ)
            print("processesQueue:", processesQueue)
            #imageData = createDiagram(processesQueue)
            return output
    else:
        return "Invalid input."


with gr.Blocks() as demo:
    gr.Markdown("Select the algorithm of your choosing.")
    with gr.Tab("SJF/SRTF/LJF"):
        # numProcesses, arrivalTimes, burstTimes
        with gr.Row():
            gr.Label("Shortest Job First")
            gr.Label("Shortest Remaining Time First")
            gr.Label("Longest Job First")
        #algoName = gr.Label(value={"Shortest Job First Algorithm":"", "Shortest Remaining Time First": "", "Longest Job First"})

        # outputs: completion times, turnaround times, waiting times, schedule length, throughput,
        #   average turn around times, average waiting times,
        algChoices = gr.Radio(["SJF", "SRTF", "LJF"], label="Algorithms", interactive=True)
        numProcesses = gr.Number(label="Number of Processes", interactive=True)
        arrivalTimes = gr.Textbox(label="Arrival Times (formatted as an array, ordered by process ID 1-numProcesses, contained within [])", interactive=True)
        burstTimes = gr.Textbox(label="Burst Times (formatted as an array, ordered by process ID 1-numProcesses, contained within [])", interactive=True)

        calculate = gr.Button(value="Calculate!")


        outputBtn = gr.Textbox(label="Output", interactive=False)
        calculate.click(calculateFn, inputs = [algChoices, numProcesses, arrivalTimes, burstTimes], outputs=outputBtn)

    with gr.Tab("FCFS/RR"):
        # numProcesses, arrivalTimes, burstTimes
        with gr.Row():
            gr.Label("First Come First Serve")
            gr.Label("Round Robin")
        #algoName = gr.Label("First Come First Serve\nRound Robin")

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

    with gr.Accordion("Open for Diagram!"):
        createBtn = gr.Button(value="Create Diagram")
        # outputImage = gr.Image()

        createBtn.click(createDiagram, inputs=None, outputs=gr.outputs.Image(type="pil"))
        # imageButton = gr.Button(label="Create Diagram")
        # image =
        # imageButton.click(createGradioImage, inputs=processesQueue, outputs=gr.outputs.Image(type="pil"))

        #iface = gr.Interface(createGradioImage, inputs=None, outputs=gr.outputs.Image(type="pil"), live=True)

    arrivalTimesList = " " #  ast.literal_eval(str(arrivalTimesInput))
    burstTimesList = " " # ast.literal_eval(str(burstTimesInput))

    # srtfButton.click(srtf, inputs=[numProcessesInput, arrivalTimesInput, burstTimesInput], outputs=srtfOutput)
    # print(str(arrivalTimesInput.input))

demo.launch(share=True)


# class GUIWindow:
#
#     def __init__(self):
#
#
# GUIWindow()


