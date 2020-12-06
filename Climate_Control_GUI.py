import PySimpleGUI as sg

defrost = "Pictures/Defrost.png"
lower = "Pictures/Lower.png"
upper = "Pictures/Upper.png"
upper_lower = "Pictures/Upper_and_Lower.png"
arrow_up = "Pictures/arrow_up.png"
arrow_down = "Pictures/arrow_down.png"
ac = "Pictures/C.png"
rear_defrost = "Pictures/Rear_Defrost.png"
defrost_lower = "Pictures/Defrost_Lower.png"

power_level = 0

temp_queue = queue.Queue()

vent_mode = [sg.Button(size=(5,1),image_filename=upper,key='__upper__'),
                sg.Button(size=(5,1),image_filename=upper_lower,key='__upper_lower__'),
                sg.Button(size=(5,1),image_filename=lower,key='__lower__'),
                sg.Button(size=(5,1),image_filename=defrost_lower,key='__defrost_lower__'),
                sg.Button(size=(5,1),image_filename=defrost,key='__defrost__')]

switches = [sg.Button(image_filename=rear_defrost,size=(15,1),key='__rear_defrost__'), sg.Button(size=(15,1),image_filename=ac,key='__ac__')]

power = [[sg.Button("",image_filename=arrow_up,key='__up__'),sg.Text(power_level,key='power_text'),sg.Button("",image_filename=arrow_down,key='__down__')]]

temperature = [[sg.Text("Temperature: "),sg.Slider(range=(65,80),default_value=75,size=(20,10),orientation='horizontal',key='set_temp')]]

layout = [
            [sg.Text(75,justification='center',key='temp_text',size=(15,1))],
            vent_mode,
            switches,
            [sg.Column(power),
             sg.Column(temperature)
            ]
         ]

window = sg.Window("Climate Control",layout)



while True:
    # temp = temp_queue.get()
    event, value = window.Read(timeout=25)
    if event in (None, 'Quit'):
        break
    elif event == '__upper__':
        print("upper")
    elif event == '__upper_lower__':
        print("upper_lower")
    elif event == '__lower__':
        print("lower")
    elif event == '__defrost_lower__':
        print("defrost_lower")
    elif event == '__defrost__':
        print("defrost")
    elif event == '__rear_defrost__':
        print("rear_defrost")
    elif event == '__ac__':
        print("ac")
    elif event == '__up__':
        if power_level + 1 < 5:
            power_level = power_level + 1
        print("up")
    elif event == '__down__':
        if power_level - 1 > -1:
            power_level = power_level - 1
        print("down")
    try:
        set_temperature = value['set_temp']
    except:
        set_temperature = 75
    window['power_text'].update(power_level)
    climate_control(temp,set_temperature)
