#GUI Software for Network Helping-Tool
#Threading help: https://realpython.com/intro-to-python-threading/#what-is-a-thread
import PySimpleGUI as sg
import subprocess
import MusicPlayer
import time
import threading

#Func to run commands and update textbox column
def runcmd(cmd, ipreq):
    if ipreq == 1:
        temp = cmd + " " + values["_IP_"]
    elif ipreq == 0:
        temp = cmd
    chars = "-"
    if any((c in chars) for c in temp):
        window["_INFOM_"].update("Not gonna happen..")
    else:
        try:
            result = subprocess.check_output(temp)
            window["_INFOM_"].update(result)
        except subprocess.CalledProcessError:
            window["_INFOM_"].update("Not valid")
        except FileNotFoundError:
            window["_INFOM_"].update("Not valid")

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
    window["_INFOM_"].update("Pinging..")

#Function to start a trace route
def traceFunc():
    if values["_WINDOWS_"]:
        threading.Thread(target=runcmd, args=("tracert", 1), daemon=True).start()
        window["_INFOM_"].update("Running Tracert..")
        

    elif values["_LINUX_"]:
        threading.Thread(target=runcmd, args=("traceroute", 1), daemon=True).start()
        window["_INFOM_"].update("Running Traceroute..")

#Doesn't work as intended yet... Not all commands work
def customcmd():
    if values["_IP_"] != "":
        threading.Thread(target=runcmd, args=(values["_IP_"], 0), daemon=True).start()
        window["_INFOM_"].update("Running your command. Sit tight..")
    else:
        window["_INFOM_"].update("Please enter a command first..")

#Function to flush DNS
def flushDNS():
    if values["_WINDOWS_"]:
        threading.Thread(target=runcmd, args=("ipconfig /flushdns", 0), daemon=True).start()
    elif values["_LINUX_"]:
        threading.Thread(target=runcmd, args=("service nscd restart", 0), daemon=True).start()
        runcmd("service nscd restart", 0)

#Function to shut down PC
def shutFun():
    if values["_WINDOWS_"]:
        subprocess.Popen('shutdown -p -f')
    elif values["_LINUX_"]:
        subprocess.Popen('shutdown -h now')

#Help with a timer that doesn't freeze the program
#https://stackoverflow.com/a/44666336
def fun():
    MusicPlayer.setSong3()
    threading.Timer(16, shutFun, args=None, kwargs=None).start()

#Changes the theme
sg.change_look_and_feel('Reddit')
 
 #Creates the column. Column is needed to enable scrollbars. Frame does not have this.
col = [[sg.Text("This is where information will be shown", size=(25,35), key="_INFOM_")]]

#Sets the layout for the window
layout = [
    [sg.Text('Network Helping-Tool', size=(
        30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Text('This is a network helping-tool')],
    [sg.Frame(layout=[
        [sg.Radio('Windows', "RADIO1", default=True, key="_WINDOWS_"), #key will make it possible to do events and use value of the button, depending on if its pressed or not(True, False)
         sg.Radio('Linux', "RADIO1", key="_LINUX_")]],
            title='Operating System',
            title_color='black',
            relief=sg.RELIEF_SUNKEN)],
    [sg.Column(col, scrollable=True, size=(250,400))],
    [sg.Button(button_text="IP Config")],
    [sg.Text('Enter IPv4 Address or custom command')],
    [sg.InputText(key="_IP_")],
    [sg.Button(button_text="Ping")],
    [sg.Button(button_text="Trace Route")],
    [sg.Button(button_text="Custom Command")],
    [sg.Button(button_text="Flush DNS")],
    [sg.Frame(layout=[      #MusicPlayer Frame. Uses PyGame to play sounds, control volume etc.
        [sg.Text("Some music to enjoy while troubleshooting"), sg.Button(button_text="Play Music"), sg.Button(button_text="Stop Music")
         ]],
            title='Music Player',
            title_color='black',
            relief=sg.RELIEF_SUNKEN)],
    [sg.Button(button_text="Delete System32"), sg.Text("Seriously.. Don't press this button..!")]]

#"Fun" layout
layoutFun = [[sg.Text('Error: System32 not found', size=(
        20, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Text('You really fucked it up..')]]

#"Fun" window
windowFun = sg.Window("System32 Not found", layoutFun, default_element_size=(40,1), grab_anywhere=False)

#This creates the window
window = sg.Window('Network Helping-Tool', layout,
    default_element_size=(40, 1), grab_anywhere=False)


#This will run the window in a loop
while True:
    event, values = window.read() #event, values is needed in order for buttons etc to do stuff.
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
        windowFun.read()
