#GUI Software for Network Helping-Tool
#Threading help: https://realpython.com/intro-to-python-threading/#what-is-a-thread
#Threading makes it possible to do multiple tasks at once. For example run a ping command, and still be able to do other stuff in the program at the same.

import PySimpleGUI as sg
import subprocess
import MusicPlayer
import threading

#################################################################################################
#Below is all functions for the program
#################################################################################################

def clearWindow():
    window["_INFO_"].update("")
#Func to run commands and update text
def runcmd(cmd, ipreq):
    clearWindow()
    if ipreq == 1:
        temp = cmd + " " + values["_IP_"]
    elif ipreq == 0:
        temp = cmd
    chars = "-"
    if any((c in chars) for c in temp):
        print("Not gonna happen..")
    else:
            print("Hold on..")
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
#https://stackoverflow.com/questions/5188792/how-to-check-a-string-for-specific-characters
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
    threading.Timer(16, shutFun, args=None, kwargs=None).start()

#################################################################################################
#Below is PySimpleGUI code
#################################################################################################

#Changes the theme
sg.change_look_and_feel('Reddit')

#sg.Output takes the output from stdout and stderr from subprocess, and puts it in a textbox
col0 = sg.Output(size=(52, 1), key="_INFO_")

col1 = sg.Column([
    [sg.Button(button_text="Delete System32"), sg.Text("Seriously.. Don't press this button!")]])

col2 = sg.Frame(layout=[      #MusicPlayer Frame. Uses PyGame to play sounds, control volume etc.
        [sg.Text("Some music to enjoy while troubleshooting"), sg.Button(button_text="Play Music"), sg.Button(button_text="Stop Music")]],
            title='Music Player',
            title_color='black',
            relief=sg.RELIEF_SUNKEN)
#Sets the layout for the window
col3 = sg.Column([
    [sg.Text('Network Helping-Tool', size=(
        30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Text('Made by Jesp9025', size=(15,1))],
    [sg.Text('This is a network helping-tool')],
    [sg.Frame(layout=[
        [sg.Radio('Windows', "RADIO1", default=True, key="_WINDOWS_"), #key will make it possible to do events and use value of the button, depending on if its pressed or not(True, False)
         sg.Radio('Linux', "RADIO1", key="_LINUX_")]],
            title='Operating System',
            title_color='black',
            relief=sg.RELIEF_SUNKEN)],
    [sg.Button(button_text="IP Config")],
    [sg.Text('Enter IPv4 Address or custom command')],
    [sg.InputText(key="_IP_")],
    [sg.Button(button_text="Ping")],
    [sg.Button(button_text="Trace Route")],
    [sg.Button(button_text="Custom Command")],
    [sg.Button(button_text="Flush DNS")]])

#Attempt to make the window smaller, to support 720p monitor
layout = [[col3, col0], [col2], [col1]]
#This creates the window
window = sg.Window('Network Helping-Tool', layout,
    default_element_size=(40, 1), grab_anywhere=False, auto_size_text=True)

#This will run the window in a loop
while True:
    event, values = window.read()
     #event, values is needed in order for buttons etc to do stuff.
    if event == 'EXIT'  or event is None: #Shuts down the program when "exit-cross" is clicked on  
        break
    if event == "IP Config": #This will do stuff if button named "IP Config" button is pressed
        ipconfigFunc()
    elif event == "Ping":
        pingFunc()
    elif event == "Trace Route":
        traceFunc()
    elif event == "Custom Command":
        customcmd()
    elif event == "Flush DNS":
        flushDNS()
    elif event == "Play Music":
        MusicPlayer.setSong()
    elif event == "Stop Music":
        MusicPlayer.stopMusic()
    elif event == "Delete System32":
        fun()
