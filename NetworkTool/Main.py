import subprocess # To run shell commands
import MusicPlayer # To play music
import threading # To run threads
import whois # Library to run whois
from queue import Queue # To make a queue system for threads for port scanner
import socket # Library used to check if port is open
import time # To start a timer for port scanner
from decimal import Decimal #To round numbers
import itertools #For loading animation
import GUI # Our GUI python file, uses PySimpleGUI
import CPU_Monitor
import IPCalc
import pytest



#####################################################################
#                           Functions
#####################################################################
#Clears the window
def clearWindow():
    GUI.window["_INFO_"].update("")


def disableButtons():
    GUI.window["Ping"].update(disabled=True)
    GUI.window["Trace Route"].update(disabled=True)
    GUI.window["Flush DNS"].update(disabled=True)
    GUI.window["Custom Command"].update(disabled=True)
    GUI.window["IP Config"].update(disabled=True)
    GUI.window["Run Whois"].update(disabled=True)
    GUI.window["Run PortScan"].update(disabled=True)

def enableButtons():
    GUI.window["Ping"].update(disabled=False)
    GUI.window["Trace Route"].update(disabled=False)
    GUI.window["Flush DNS"].update(disabled=False)
    GUI.window["Custom Command"].update(disabled=False)
    GUI.window["IP Config"].update(disabled=False)
    GUI.window["Run Whois"].update(disabled=False)
    GUI.window["Run PortScan"].update(disabled=False)

############# Run CMD ##############
#Uses subprocess, which includes stdout, stderr. Using communicate() allows you to get output and error from the subprocess.Popen
def runcmd(cmd, ipreq): # cmd argument is used to determine which command to run. ipreq is used to determine if input from _IP_ is needed or can be ignored. ipreq has to be 1 or 0
    global done
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
        # Starts the loading animation
        done = False

        # Disables the buttons while command is being run
        disableButtons()

        #Runs the command, and outputs it in readable format
        result = subprocess.Popen(temp, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = result.communicate()
        done = True

        # Enables the buttons again
        enableButtons()
        if out:
            clearWindow()
            print(out.decode("ascii"))

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

#Function to start a trace route. Takes input _IP_ to determine address
def traceFunc():
    if values["_WINDOWS_"]:
        threading.Thread(target=runcmd, args=("tracert", 1), daemon=True).start()
    elif values["_LINUX_"]:
        threading.Thread(target=runcmd, args=("traceroute", 1), daemon=True).start()

#To run a custom command
def customcmd():
    #Checks if input is empty, to avoid error
    if values["_IP_"] != "":
        threading.Thread(target=runcmd, args=(values["_IP_"], 0), daemon=True).start()
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
def shutdownPC():
    if values["_WINDOWS_"]:
        subprocess.Popen('shutdown -p -f')
    elif values["_LINUX_"]:
        subprocess.Popen('shutdown -h now')

#Help with a timer that doesn't freeze the program
#https://stackoverflow.com/a/44666336
#This will create a new thread that runs a timer, and then runs the function, without freezing the program
def fun():
    MusicPlayer.setCountdown()
    threading.Timer(17, shutdownPC).start()

############# Whois ##############
#https://github.com/richardpenman/pywhois
#https://www.pythonforbeginners.com/dns/using-pywhois
#Uses module 'python-whois'
def runWhois():
    global done
    
    # If input is not empty, do stuff
    if values["_whoisInput_"] != "":
        clearWindow()
        disableButtons()
        # Start loading animation
        done = False
        # Runs the Whois
        w = whois.whois(values["_whoisInput_"])
        # Stops loading animation
        done = True
        clearWindow()
        print(w)
        enableButtons()
    else:
        clearWindow()
        print("Please enter a target")
#It may or may not say there is an error and whois is not callable.. Ignore it.

############# Port Scanner ##############
#https://pythonprogramming.net/python-threaded-port-scanner/?completed=/python-port-scanner-sockets/
#Added s.settimeout() to make it faster, instead of using default timeout

#The function that does the actual port scan
def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #Sets timeout for each port scan
    s.settimeout(0.5)
    try:
        # Checks if port is reachable
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
        if _FINISH and q.empty():
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

    # print_lock makes sure that once a thread has started "working" on a task/variable, other threads can not use it
    print_lock = threading.Lock()

    # Create the queue
    q = Queue()

    # how many threads are we going to allow for
    # Checks if target input is empty
    if values["_PORTINPUT_"] != "":
        try:
            # Checks if inputs are lower than or equal to 0
            if int(values["_STARTPORT_"]) <= 0 or int(values["_ENDPORT_"]) <= 0:
                print("Start and end port must be higher than 0")
            else:
                # Checks if endport is higher than startport
                if int(values["_ENDPORT_"]) >= int(values["_STARTPORT_"]) and int(values["_ENDPORT_"]) <= 65535:

                    # Disables buttons while scan is going
                    disableButtons()

                    # Used to determine how many threads to create
                    temp = int(values["_ENDPORT_"]) - int(values["_STARTPORT_"]) + 1

                    # If temp is lower than 800, it should only create the needed amount of threads
                    if temp < 800:
                        for x in range(temp):
                            z = threading.Thread(target=threader, daemon=True)
                            z.start()
                    else:
                        # 800 is almost the max amount of threads possible to run at same time
                        for x in range(800):
                            z = threading.Thread(target=threader, daemon=True)
                            z.start()

                    #Start time
                    start = time.time()

                    # Number of ports to scan
                    for worker in range(int(values["_STARTPORT_"]), int(values["_ENDPORT_"]) +1):
                        q.put(worker)

                    _FINISH = True
                    # wait until the thread terminates.
                    q.join()

                    #End time
                    end = time.time()

                    print("Scan completed in", round(end - start, 2), "seconds\nNumber of ports scanned:", temp)

                    # Remember to set _FINISH to False
                    _FINISH = False
                    
                    # Enables buttons again
                    enableButtons()
                else:
                    print("Can't go higher than 65535,\nand end port must be higher than start port")
        # Returns a printed error if non-int has been input
        except ValueError:
            print("Incorrect input. You either didn't type port numbers, or you wrote a non-Int")
    else:
            print("Please enter a target")

############# Loading Animation ##############
#Very basic. We might find something better
#https://stackoverflow.com/a/22029635

#To start and stop loading animation. True = Not loading, False = Loading
done = True

def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        GUI.window["_INFO_"].update('\rloading ' + c)
        time.sleep(0.1)


#Runs the window in a loop
while True:
    event, values = GUI.window.read()
    if event is None:           # always,  always give a way out!    
        break
    if event == "Play Music":
        if values["_SONG_"] == "FitGirl":
            MusicPlayer.setSong1()
        elif values["_SONG_"] == "Eye Of The Tiger":
            MusicPlayer.setSong2()
        elif values["_SONG_"] == "Push It To The Limit":
            MusicPlayer.setSong3()
        elif values["_SONG_"] == "Eye Of The Tiger":
            MusicPlayer.setSong3()
    elif event == "Stop Music":
        MusicPlayer.stopMusic()
    elif event == "+":
        MusicPlayer.volumeUP()
    elif event == "-":
        MusicPlayer.volumeDOWN()
    elif event == "IP Config": #This will do stuff if button named "IP Config" button is pressed
        ipconfigFunc()
        threading.Timer(0.5, animate).start() #Using a timed thread in order to allow some time for other functions to set 'done' to False
    elif event == "Ping":
        pingFunc()
        threading.Timer(0.5, animate).start()
    elif event == "Trace Route":
        traceFunc()
        threading.Timer(0.5, animate).start()
    elif event == "Custom Command":
        customcmd()
        threading.Timer(0.5, animate).start()
    elif event == "Flush DNS":
        flushDNS()
        threading.Timer(0.5, animate).start()
    elif event == "Run Whois":
        threading.Thread(target=runWhois, daemon=True).start()
        threading.Timer(0.5, animate).start()
    elif event == "Run PortScan":
        threading.Thread(target=startPortScan, daemon=True).start()
    elif event == "Begin":
        #threading.Thread(target=CPU_Monitor.main, daemon=True).start()
        CPU_Monitor.main()
    elif event == "Calculate":
        clearWindow()
        IPCalc.ipAdd = values["_IPCALC_"]
        try:
            IPCalc.cidr = int(values["_CIDR_"])
            IPCalc.ipCalc()
        except ValueError:
            print("**Enter a valid CIDR notation number (Integer 1 - 31)**\n")
