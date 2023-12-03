import gradio as gr

import memallocation as ma

import matplotlib.pyplot as plt
import numpy as np


def formatOutput(blocks, processes, determinant):
    freeBlocks = eval(blocks)
    processArr = eval(processes)
    memAllocate = ma.MemoryAllocation(freeBlocks)
    bestAlg, results = memAllocate.bestAlgorithm(freeBlocks, processArr, determinant)
    out = ""
    out += f"The best memory allocation algorithm is: {bestAlg}"
    out += "\n\nAlgorithm Metrics:\n"
    for algorithmName, metrics in results.items():
        out += f"{algorithmName.upper()}: \n\tTotal Available Memory={metrics['totalMem']} KB, \n\tAllocated Memory in Use={metrics['allocatedMem']} KB, \n\tExternal Fragmentation={metrics['externalFragmentation']} KB, \n\tInternal Fragmentation={metrics['internalFragmentation']} KB, \n\tExecution Time = {metrics['executionTime']}\n"
    return out

def furtherAllocationInformation(blocks, processes, algorithm):
    memoryAllocator = ma.MemoryAllocation(eval(blocks))
    processArray = memoryAllocator.arrayToDict(eval(processes))
    outProcesses = "Processes: "  + str(list(processArray.items()))
    outBlocks = "Memory Blocks: " + str(list(memoryAllocator.freeBlocks.items()))
    out = str(outProcesses) + "\n" + str(outBlocks)
    if algorithm == "First Fit":
        memoryAllocator.firstFitAllocation(eval(processes))
    elif algorithm == "Next Fit":
        memoryAllocator.nextFitAllocation(eval(processes))
    elif algorithm == "Best Fit":
        memoryAllocator.bestFitAllocation(eval(processes))
    elif algorithm == "Worst Fit":
        memoryAllocator.worstFitAllocation(eval(processes))
    out2 = memoryAllocator.printResults()

    return str(out) + "\n\n" + str(out2)

"""
create the diagram of the memory blocks and process allocations

Returns:
    image file of diagram 
"""
def createDiagram(blocks, processes, algorithm):
    # run memoryAllocator
    memoryAllocator = ma.MemoryAllocation(eval(blocks))
    if algorithm == "First Fit":
        memoryAllocator.firstFitAllocation(eval(processes))
    elif algorithm == "Next Fit":
        memoryAllocator.nextFitAllocation(eval(processes))
    elif algorithm == "Best Fit":
        memoryAllocator.bestFitAllocation(eval(processes))
    elif algorithm == "Worst Fit":
        memoryAllocator.worstFitAllocation(eval(processes))



    yDim = sum(list(memoryAllocator.freeBlocks.values()))
    fig, ax = plt.subplots(figsize=(10, yDim/30))

    # Initialize the bottom of the bars
    bottom = 0

    blockLabels = []
    blockSizes = []
    memoryAllocator2 = ma.MemoryAllocation(eval(blocks))

    # create labels and sizes
    for blockID, processSize in memoryAllocator.allocations.items():

        blockLabels.append([str(blockID) , str(processSize[0])])
        blockSizes.append(processSize[1])

        if memoryAllocator2.freeBlocks.get(processSize[0]) > processSize[1]:

            blockLabels.append([processSize[0], processSize[0]])
            blockSizes.append(memoryAllocator2.freeBlocks.get(processSize[0])-processSize[1])
    processes = []
    for blockID in list(memoryAllocator.allocations.values()):
        processes.append(blockID[0])
    # add any memory blocks that had no allocations
    for blockID, blockSize in memoryAllocator.freeBlocks.items():
        if  blockID not in processes and blockSize > 0 :
            blockLabels.append([blockID, blockID])
            blockSizes.append(blockSize)
    # Create a single stacked bar graph
    for label, size in zip(blockLabels, blockSizes):
        if label[0] == label[1]:
            # add bars that are just memory block
            bar = ax.bar('Memory Blocks', size, bottom=bottom, edgecolor='black', linewidth=1, label=f'Memory Block {str(label[0])}', color='antiquewhite')
            ax.text(bar[0].get_x() + bar[0].get_width() / 2, bottom + size / 2, f'Memory Block {str(label[0])}\n Size {size} KB',
                    ha='center', va='center', fontsize=10, color='black')
        else:
            # add bars that are process allocated
            bar = ax.bar('Memory Blocks', size, bottom=bottom, edgecolor='black', linewidth=1, label=f'Process {str(label[0])}, Memory Block {str(label[1])}', color='darkseagreen')
            ax.text(bar[0].get_x() + bar[0].get_width() / 2, bottom + size / 2, f'Process {str(label[0])}, Memory Block {str(label[1])}\nSize {size} KB',
                    ha='center', va='center', fontsize=10, color='black')
        bottom += size

    ax.set_yticks([])
    ax.set_ylabel('Memory Block Sizes')
    ax.set_title('Memory Block Allocations')


    ax.legend()
    # Save the plot to a file and return the file name
    filename = "memoryAllocationPlot.png"
    plt.savefig(filename, format="png")
    plt.show()

    # Close the plot
    plt.close()

    return filename

"""
Create GUI from Gradio Library
    https://github.com/gradio-app/gradio
"""
with gr.Blocks() as demo:
    gr.Markdown("Determine the best memory allocation algorithm.")
    with gr.Row():
        gr.Label("First Fit")
        gr.Label("Next Fit")
        gr.Label("Best Fit")
        gr.Label("Worst Fit")

    # input for memory block sizes array
    freeBlocks = gr.Textbox(
        value="[50,150,300,350,600]",  # example from class
        label="List of Memory Block Sizes, formatted as an array, contained within [], seperated by commas",
        interactive=True  # can be changed for other examples
    )

    # input for processes sizes array
    processesArray = gr.Textbox(
        value="[300,25,125,50]",  # example from class
        label="List of process sizes, formatted as an array, contained within [], separated by commas",
        interactive=True  # can be changed for other examples
    )

    # multiple choice for what determinant should be used for best algorithm
    determinants = gr.Radio(["totalMem", "allocatedMem", "internalFragmentation", "externalFragmentation", "executionTime"], label = "Determinant Choices", interactive=True)

    calculate = gr.Button(value="Calculate!")

    # output results
    output = gr.Textbox(label="Output", interactive=False, autoscroll=False)
    calculate.click(formatOutput, inputs=[freeBlocks, processesArray, determinants], outputs=output)

    # collapsable window for showing extra details for specific algorithms
    with gr.Accordion("Open for memory allocations by algorithm!", open=False):
        # multiple choice for algorithm
        algs = gr.Radio(choices=["First Fit", "Next Fit", "Best Fit", "Worst Fit"], label="Algorithm Options", interactive=True)


        with gr.Row():
            algBtn = gr.Button(value="Get alg specific allocations!")
            diagram = gr.Button(value="Make allocation diagram")
        with gr.Row():
            # output results
            textOutput = gr.Textbox(label="Output", interactive=False)
            algBtn.click(furtherAllocationInformation, inputs=[freeBlocks, processesArray, algs], outputs=textOutput)

            diagram.click(createDiagram, inputs=[freeBlocks,processesArray, algs], outputs=gr.Image(type='pil'))
    markdownText = """
    Ella Grady \n
    December 5, 2023 \n
    Clark University - CS 215 
    """
    gr.Markdown(markdownText)
demo.launch()

