import PySimpleGUI as sg
#Sets the theme
sg.change_look_and_feel('Reddit')

#Creates the layouts for each tab
#MusicPlayer tab. Uses PyGame to play sounds, control volume etc.
tab1_layout =  [[sg.Text("")],
                [sg.Text("Some music to enjoy while troubleshooting")], 
                [sg.Button(button_text="Play Music"),
                    sg.Button(button_text="Stop Music")],
                [sg.Button(button_text="+", size=(1,1)), 
                    sg.Button(button_text="-", size=(1,1))],
                [sg.Text("Choose a song:"),
                sg.Combo([
                    "FitGirl",
                    "Eye Of The Tiger",
                    "Push It To The Limit"],
                    default_value="FitGirl", key="_SONG_")]]

#Basic tools tab
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

#Whois tab
tab3_layout = [[sg.Text("Here you can run a whois on a URL")],
                [sg.T('Target:'), sg.InputText(key="_whoisInput_")],
                [sg.Button("Run Whois")]]

#Port scanner tab
tab4_layout = [[sg.Text("Here you can scan a range of ports")],
    [sg.Text("Target:"), sg.Input(key="_PORTINPUT_")],
    [sg.Button("Run PortScan"), sg.Text("Hackthissite.org is legal to scan")],
    [sg.Frame(layout=[
    [sg.Text("Start Port:"), sg.Input(key="_STARTPORT_", size=(10,1))],
    [sg.Text("End Port: "), sg.Input(key="_ENDPORT_", size=(10,1))]],
            title='Scan Size',
            title_color='black',
            relief=sg.RELIEF_SUNKEN)],
    [sg.Text("Scanning 65535 ports takes 40-60 seconds.")]]

#Wifi-Analyzer tab
tab5_layout = [[sg.T('This is inside tab 5 / Wi-Fi Analyzer')]]

#IP Calculator tab
tab6_layout = [[sg.T('Subnet Calculator')],
                [sg.Text("IPv4 Address: "), sg.Input(key="_IPCALC_")],
                [sg.Text("CIDR Notation:"), sg.Input(key="_CIDR_")],
                [sg.Button(button_text="Calculate")]]

#Cisco IOS tab
tab7_layout = [[sg.T('This is inside tab 7 / Cisco IOS')]]

tab8_layout = [[sg.Text('CPU Usage Monitor')],
                [sg.Text("Press Begin to open the monitor")],
                [sg.Button("Begin")]]


#This is where all layots/tabs are put together, to be used in window
layout = [[sg.TabGroup([[sg.Tab('Music Player', tab1_layout), sg.Tab('Basics', tab2_layout),
            sg.Tab('Whois', tab3_layout), sg.Tab('Port Scanner', tab4_layout), sg.Tab('Wi-Fi Analyzer', tab5_layout),
            sg.Tab('IP (VLSM) Calculator', tab6_layout),sg.Tab('Cisco IOS', tab7_layout), sg.Tab('CPU Usage', tab8_layout)]]),
            sg.Output(size=(46, 18), key="_INFO_")]]

#Creates the window
window = sg.Window('Network Tool', layout, default_element_size=(12,1))
