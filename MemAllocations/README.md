CS 215 - Operating Systems, Fall 2023 @ Clark University Ella Grady

Memory Allocations Assignment Classes for the following algorithms:
  - First Fit
  - Next Fit
  - Best Fit
  - Worst Fit

Each algorithm is found within the memallocation.py file, under the MemoryAllocation class. MemoryAllocation objects are initialized with the input of an array containing the sizes of free memory blocks. From there that array is used to make a dictionary, where each block is assigned a block ID, a letter assigned in alphabetical order. Each algorithm function is structured similarly, all taking an input of an array representing the sizes of given processes. This processes array is made into a dictionary like the freeBlocks dictionary, where they are assigned a letter process ID, in reverse alphabetical order, with a 'P.' at the beginning to denote it is a process. From there the processes and freeBlocks dictionaries are used to compute the memory allocation orders for the algorithm. 

The file memgui.py (and app.py which is the same code) creates a GUI build on the Gradio library (https://github.com/gradio-app/gradio). The GUI takes user input for the list of memory block sizes, and list of processes sizes, though they are both default set to the example used in class (memory blocks = [50,150,300,350,600] and processes = [300,25,125,50]). The GUI also takes user selection for determinant which will determine the best algorithm based on total available memory, allocated memory usage, internal fragmentation, external fragmentation, or execution time. From this input, it will return the best algorithm and the computed metrics for each algorithm. 

In addition to this option, there is also a collapsible section of the window, which will show the  memory allocations by algorithm. Under here, users can select an algorithm, be given the written allocation calculations for it, and generate an image that displays a diagram of the allocations. 

App.py is the same code as memgui.py, written out to allow for the GUI window to be deployed to a stable, permanent link hosted on HuggingFaces Spaces that hosts Gradio applications, rather than requiring the program to be run for the GUI to be deployed in the user's browser manually. The application can be accessed at https://huggingface.co/spaces/ellagrady/MemAllocate 

When run on a local server, it generates a window that looks like this: 
![image](https://github.com/ellagrady/CS215/assets/123561564/cd5a9edc-8808-4bb0-9d92-21ad780761d3)
![image](https://github.com/ellagrady/CS215/assets/123561564/c2ac7f8e-56d3-45f1-8128-58fe4b9c3311)


On HuggingFaces Spaces it looks like this:
![image](https://github.com/ellagrady/CS215/assets/123561564/0a8d31dd-86a3-43fd-9342-8f11630137ac)
