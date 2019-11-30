import PySimpleGUI as sg # To make a GUI
import subprocess # To run shell commands
import MusicPlayer # To play music
import threading # To run threads
import whois # The name explains it
from queue import Queue # To make a queue system for threads for port scanner
import socket # Library used to check if port is open
import time # To start a timer for port scanner
from decimal import Decimal #To round numbers


#######################
#Functions
#######################
#Clears the window
def clearWindow():
    window["_INFO_"].update("")
    
#Func to run commands and update text
#Uses subprocess, which includes stdout, stderr. Using communicate() allows you to get output and error from the subprocess.Popen
def runcmd(cmd, ipreq):
    clearWindow()
    if ipreq == 1:
        temp = cmd + " " + values["_IP_"]
    elif ipreq == 0:
        temp = cmd
    chars = "-"
    #Checks if the input contains '-'
    #https://stackoverflow.com/questions/5188792/how-to-check-a-string-for-specific-characters
    if any((c in chars) for c in temp):
        print("Not gonna happen..")
    else:
        print("Hold on..")
        #Runs the command, and outputs it in readable format
        result = subprocess.Popen(temp, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = result.communicate()
        if out:
            clearWindow()
            print(out.decode("utf-8"))
        if err:
            clearWindow()
            print("Unknown command")
            
        

#Function to show ipconfig for Windows and Linux
def ipconfigFunc():
    if values["_WINDOWS_"]:
        threading.Thread(target=runcmd, args=("ipconfig", 0), daemon=True).start()
    elif values["_LINUX_"]:
        threading.Thread(target=runcmd, args=("ifconfig", 0), daemon=True).start()

#Function to start a ping. Takes input _IP_ to determine address
def pingFunc():
    threading.Thread(target=runcmd, args=("ping", 1), daemon=True).start()

#Function to start a trace route
def traceFunc():
    if values["_WINDOWS_"]:
        threading.Thread(target=runcmd, args=("tracert", 1), daemon=True).start()
    elif values["_LINUX_"]:
        threading.Thread(target=runcmd, args=("traceroute", 1), daemon=True).start()

#To run a custom command
def customcmd():
    #Checks if input is empty, to avoid error
    if values["_IP_"] != "":
        runcmd(values["_IP_"], 0)
    else:
        clearWindow()
        print("Please enter a command first")

#Function to flush DNS
def flushDNS():
    if values["_WINDOWS_"]:
        threading.Thread(target=runcmd, args=("ipconfig /flushdns", 0), daemon=True).start()
    elif values["_LINUX_"]:
        threading.Thread(target=runcmd, args=("service nscd restart", 0), daemon=True).start()

#Function to shut down PC
def shutFun():
    if values["_WINDOWS_"]:
        subprocess.Popen('shutdown -p -f')
    elif values["_LINUX_"]:
        subprocess.Popen('shutdown -h now')

#Help with a timer that doesn't freeze the program
#https://stackoverflow.com/a/44666336
#This will create a new thread that runs a timer, and then runs the function, without freezing the program
def fun():
    MusicPlayer.setSong3()
    threading.Timer(17, shutFun, args=None, kwargs=None).start()

#https://github.com/richardpenman/pywhois
#https://www.pythonforbeginners.com/dns/using-pywhois
def runWhois():
    clearWindow()
    print("Hold on..")
    w = whois.whois(values["_whoisInput_"])
    clearWindow()
    print(w)
#It may or may not say there is an error and whois is not callable.. Ignore it.

############# Port Scanner #############
#https://pythonprogramming.net/python-threaded-port-scanner/?completed=/python-port-scanner-sockets/
#Added s.settimeout() to make it faster, instead of using default timeout

#The function that does the actual port scan
def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        
        con = s.connect((values["_PORTINPUT_"], port))
        with print_lock:
            print('port', port)
        con.close()
    except:
        pass
_FINISH = False
# The threader thread pulls a worker from the queue and processes it
def threader():
    global _FINISH
    while True:
        if _FINISH:
            break
        # gets a worker from the queue
        worker = q.get()

        # Run the example job with the available worker in queue (thread)
        portscan(worker)

        # completed with the job
        q.task_done()

def startPortScan():
    clearWindow()
    global q
    global print_lock
    global _FINISH
    print_lock = threading.Lock()
    # Create the queue
    q = Queue()

    # how many threads are we going to allow for
    if values["_PORTINPUT_"] != "":
        for x in range(800):
            z = threading.Thread(target=threader, daemon=True)
            z.start()

        #Start time
        start = time.time()

        # Number of ports to scan
        #Problem right now is that if you choose more ports than there are threads, it will hang.
        #But it will actually scan all the ports you tell it to, but you can't run the port scan again.
        for worker in range(1, 801):
            q.put(worker)

        _FINISH = True
        # wait until the thread terminates.
        q.join()

        #End time
        end = time.time()
        print("Scan completed. Time elapsed:", round(end - start, 2), "seconds")
        # Remember to set _FINISH to False
        _FINISH = False
    else:
            print("Please enter a target")

#######################
#GUI Code
#######################
#Sets the theme
sg.change_look_and_feel('Reddit')

#Creates the layouts for each tab
#MusicPlayer Frame. Uses PyGame to play sounds, control volume etc.
tab1_layout =  [[sg.Text("")],
                [sg.Text("Some music to enjoy while troubleshooting")], 
                [sg.Button(button_text="Play Music"),
                    sg.Button(button_text="Stop Music")],
                    [sg.Button(button_text="+", size=(1,1)), 
                    sg.Button(button_text="-", size=(1,1))]]

tab2_layout = [[sg.Frame(layout=[
    [sg.Radio('Windows', "RADIO1", default=True, key="_WINDOWS_"), #key will make it possible to do events and use value of the button, depending on if its pressed or not(True, False)
        sg.Radio('Linux', "RADIO1", key="_LINUX_")]],
            title='Operating System',
            title_color='black',
            relief=sg.RELIEF_SUNKEN)],
    [sg.Button(button_text="IP Config")],
    [sg.Text('Enter IP Address or custom command')],
    [sg.InputText(key="_IP_", size=(20,1))],
    [sg.Button(button_text="Ping")],
    [sg.Button(button_text="Trace Route")],
    [sg.Button(button_text="Flush DNS")],
    [sg.Text("")],
    [sg.Button("Custom Command")]]

tab3_layout = [[sg.T('Who is this?')],
                [sg.InputText(key="_whoisInput_")],
                [sg.Button("Run Whois")]]

tab4_layout = [[sg.Text("Target:"), sg.Input(key="_PORTINPUT_")],
    [sg.Button("Run PortScan")],
    [sg.Text("Select end port: NOT FUNCTIONAL YET! Change port range in code."), sg.Slider(range=(1, 65535), default_value=(1), size=(20,10), orientation='horizontal', key="_STARTPORT_")],
    [sg.Text("Select start port: NOT FUNCTIONAL YET! Change port range in code."), sg.Slider(range=(1, 65535), default_value=(443), size=(20,10), orientation='horizontal', key="_ENDPORT_")]]

tab5_layout = [[sg.T('This is inside tab 5')]]

tab6_layout = [[sg.T('This is inside tab 6')]]

tab7_layout = [[sg.T('This is inside tab 7')]]

tab8_layout = [[sg.T('This is inside tab 8')],
               [sg.In(key='_in_')]]

#This is where all layots/tabs are put together, to be used in window
layout = [[sg.TabGroup([[sg.Tab('Music Player', tab1_layout), sg.Tab('Basics', tab2_layout),
        sg.Tab('Whois', tab3_layout), sg.Tab('Port Scanner', tab4_layout), sg.Tab('Tab 5', tab5_layout),
        sg.Tab('Tab 6', tab6_layout),sg.Tab('Tab 7', tab7_layout), sg.Tab('Tab 8', tab8_layout)]]), sg.Output(size=(46, 18), key="_INFO_")]]
#Creates the window
window = sg.Window('Network Tool', layout, default_element_size=(12,1))    

#Runs the window in a loop
while True:    
    event, values = window.read()   
    if event is None:           # always,  always give a way out!    
        break
    if event == "Play Music":
        MusicPlayer.setSong()
    elif event == "Stop Music":
        MusicPlayer.stopMusic()
    elif event == "+":
        MusicPlayer.volumeUP()
    elif event == "-":
        MusicPlayer.volumeDOWN()
    elif event == "IP Config": #This will do stuff if button named "IP Config" button is pressed
        ipconfigFunc()
    elif event == "Ping":
        pingFunc()
    elif event == "Trace Route":
        traceFunc()
    elif event == "Custom Command":
        customcmd()
    elif event == "Flush DNS":
        flushDNS()
    elif event =="Run Whois":
        threading.Thread(target=runWhois, daemon=True).start()
    elif event =="Run PortScan":
        threading.Thread(target=startPortScan, daemon=True).start()
        #startPortScan()
