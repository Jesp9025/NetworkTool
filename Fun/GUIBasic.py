import PySimpleGUI as sg    

#Sets the theme
sg.change_look_and_feel('Reddit')
#Creates the layouts for each tab
tab1_layout =  [[sg.T('This is inside tab 1')],
                [sg.Button("This is a button", key="_BUTTON1_")]]
tab2_layout = [[sg.T('This is inside tab 2')]]   
tab3_layout = [[sg.T('This is inside tab 2')]]  
tab4_layout = [[sg.T('This is inside tab 2')]]  
tab5_layout = [[sg.T('This is inside tab 2')]]
tab6_layout = [[sg.T('This is inside tab 2')]]  
tab7_layout = [[sg.T('This is inside tab 2')]]
tab8_layout = [[sg.T('This is inside tab 2')],    
               [sg.In(key='_in_')]]

#This is where all layots/tabs are put together, to be used in window
layout = [[sg.TabGroup([[sg.Tab('Tab 1', tab1_layout, tooltip='tip'), sg.Tab('Tab 2', tab2_layout),
        sg.Tab('Tab 3', tab3_layout), sg.Tab('Tab 4', tab4_layout), sg.Tab('Tab 5', tab5_layout),
        sg.Tab('Tab 6', tab6_layout),sg.Tab('Tab 7', tab7_layout), sg.Tab('Tab 8', tab8_layout)]], tooltip='TIP2')],    
          [sg.Button('Read')]]    
#Creates the window
window = sg.Window('My window with tabs', layout, default_element_size=(12,1))    

#Runs the window in a loop
while True:    
    event, values = window.read()   
    if event is None:           # always,  always give a way out!    
        break
