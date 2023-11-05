CS 215 - Operating Systems, Fall 2023 @ Clark University
Ella Grady 

CPU Algorithms Assignment
Classes for following algorithms:
  - Shortest Job First
  - Longest Job First
  - Shortest Remaining Time First
  - First Come First Serve
  - Round Robin

The algorithms are all based on the process class, which builds a single process, and from there each algorithm builds a list of processes and calculates completion times, turn around times, waiting times, averages, schedule length, and throughput following their rules of CPU access by the algorithm. 

The file guiwindow.py (and app.py which is the same code) creates a GUI build on the Gradio library (https://github.com/gradio-app/gradio). The GUI has two tabs. The first is for SJF, LJF, and SRTF, and the second is for FCFS and RR. Each tab takes user input on which algorithm to use, number of processes, arrival times, and burst times (both entered in array formatting). The second tab also takes user input for context switch (FCFS) and time quantum (RR). The program will calculate the above-listed outputs, and print out the information. From there a diagram of the processes order using the CPU can be created for each algorithm, similar to those drawn in class.  

App.py is the same code as guiwindow.py, written out to allow for the GUI window to be deployed to a stable, permanent link hosted on HuggingFaces Spaces that hosts Gradio applications, rather than requiring the program to be run for the GUI to be deployed in the user's browser manually. The application can be accessed at https://huggingface.co/spaces/ellagrady/CPUalg 
