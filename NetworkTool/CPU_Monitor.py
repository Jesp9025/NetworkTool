""" Group 3 - CPU Monitor
Jesper Pedersen 
Erki Hanson 
Mantas Vilimavicius 
Julius Pazitka
    
This widget this widget shows the usage of each processor cores or in total. 

Inspiration: https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Design_Pattern_Multiple_Windows2.py
https://stackoverflow.com/questions/276052/how-to-get-current-cpu-and-ram-usage-in-python
https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Desktop_Widget_CPU_Dashboard.py
https://medium.com/the-andela-way/machine-monitoring-tool-using-python-from-scratch-8d10411782fd
"""

import PySimpleGUI as sg # create GUI in Python
import psutil # psutil is a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks and so on 
import os # OS routines for NT or Posix depending on what system we're on (Windows, Linux or MAC OS)


GRAPH_WIDTH = 150  # each graph size in pixels (value for one graph)
GRAPH_HEIGHT = 120 # each graph height
NUM_COLS = 4 # number of graphs in one row
POLL_FREQUENCY = 500  # update interval of graphs in milliseconds

colors = ('#c93515', '#2ec915', '#1592c9', '#ecff00', 
'#ffffff', '#ffa600', '#ff00d4', '#00fff7') # html color codes for each graph

# CPUGraph does the drawing of each graph (one core → one graph)
class CPUGraph(object):
    def __init__(self, graph_elem, text_elem, starting_count, color): 
        self.graph_current_item = 0
        self.graph_elem = graph_elem
        self.text_elem = text_elem
        self.prev_value = starting_count
        self.max_sent = 1
        self.color = color
# self represents the instance of the class. By using the “self” keyword we can access the attributes and methods of the class in python.

    def graphPercentage(self, value):
        self.graph_elem.draw_line(
                (self.graph_current_item, 0),
                (self.graph_current_item, value),
                color=self.color)
        if self.graph_current_item >= GRAPH_WIDTH:
            self.graph_elem.move(-1,0)
        else:
            self.graph_current_item += 1

    def text_display(self, text):
        self.text_elem.update(text)

def main(): # main loop
    # This part of code combine several elements and enable bulk edits 
    def Txt(text, ** kwargs):
        return (sg.Text(text, ** kwargs)) # kwargs allows you to pass keyworded variable length of arguments to a function

    def graphColumn(name, key):
        column = sg.Col([[Txt(name, key = key + '_TXT_'),], 
                    [sg.Graph((GRAPH_WIDTH, GRAPH_HEIGHT), (0, 0), (GRAPH_WIDTH, 100), background_color='black', # parameters of the graph (color, width and so on)
                              key = key + '_GRAPH_')]], pad = (2, 2))
        return column


    num_cores = len (psutil.cpu_percent(percpu=True))  # len function return the number of cores in the CPU

    layout = [[sg.Text('CPU for each core:')],  # layout of the Window
    [sg.Text('Click on Total, for CPU Total Usage Popup')],
    [sg.Button('Total')]]

    # add information (data) on the graphs
    for rows in range(num_cores // NUM_COLS + 1):
        row = []
        for cols in range(min(num_cores - rows * NUM_COLS, NUM_COLS)):
            row.append(graphColumn('CPU '+ str (rows * NUM_COLS + cols), '_CPU_' + str (rows * NUM_COLS + cols))) # shows the processor core number
        layout.append(row)

    window = sg.Window('CPU Usage Monitor', layout, # GUI Window
                       auto_size_buttons=True, # buttons in this Window should be sized to exactly fit the text on this
                       grab_anywhere=True, # you can manipulate with window on the screen
                       default_button_element_size=(12, 1), # tuple[int, int] (width, height) size in characters (wide) and rows (high) for all Button elements in this window
                       return_keyboard_events=True, # key presses on the keyboard will be returned as Events from Read calls
                       use_default_focus=False, # if its true, will use the default focus algorithm to set the focus to the "Correct" element
                       finalize=True) # If True then the Finalize method will be called. Use this rather than chaining .Finalize for cleaner code
   

    # setup graphs & initial values
    graphs = []
    for i in range(num_cores):
        graphs.append(CPUGraph(window['_CPU_'+ str (i) + '_GRAPH_'],
                                window['_CPU_'+ str (i) + '_TXT_'],
                                0, colors[i%8])) # number of colors (one for each, we set 8 because we are test this code on PC with 8 cores, 4 hardware + 4 hyperthreading)

    while True :
        event, values = window.read(timeout = POLL_FREQUENCY) # Read and update window once every Polling Frequency (every 500ms)
        if event in (None, 'Total'):         
            break
        
        stats = psutil.cpu_percent(percpu = True) # read CPU for each core
        psutil.cpu_percent()
        
        for i in range(num_cores): # update each graph
            graphs[i].graphPercentage(stats[i])
            graphs[i].text_display('{} CPU {:2.0f}'.format(i, stats[i]))
            #print("Current CPU usage is "+str(cpu)+"%") #→ for testing
    window.close()

if __name__ == "__main__":

    main()

# ------------------ Popup Total CPU Usage---------------------

layout = [[sg.Text('CPU Usage in Total')],
           [sg.Text('', size=(8,2), justification='center', key='_text_')],
           [sg.Exit()]]

window = sg.Window('CPU Total').Layout(layout)

while True:
    button, values = window._ReadNonBlocking()

    if button == 'Exit' or values is None:
        break

    cpu_percent = psutil.cpu_percent (interval=1)

    window.FindElement('_text_').Update(f'CPU {cpu_percent:02.0f}%') # it shows the total CPU usage in %
    
