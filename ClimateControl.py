import time
import board
import busio
import adafruit_mcp9808
import threading
import queue

import PySimpleGUI as sg


i2c_bus = busio.I2C(board.SCL, board.SDA)

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


sensors = [
            adafruit_mcp9808.MCP9808(i2c_bus),
            adafruit_mcp9808.MCP9808(i2c_bus,address=0x19),
            adafruit_mcp9808.MCP9808(i2c_bus,address=0x1A),
            adafruit_mcp9808.MCP9808(i2c_bus,address=0x1C)
            ]

def read_temp():
    temp = []
    for sensor in sensors:
        temp.append(((sensor.temperature * 9) / 5) + 32)
    return temp

def average_temp():

    temp_queue.put(sum(read_temp())/len(read_temp()))
    # return sum(read_temp())/len(read_temp())

def update_temp():
    while True:
        average_temp()
        time.sleep(.25)


def climate_control(current_temp,set_temperature = 75):
    if(current_temp - set_temperature > 2):
        print("Too hot")
    elif(current_temp - set_temperature < -2):
        print("Too cold")
    else:
        print("We good")

temp_update = threading.Thread(target=update_temp,args=(),daemon=True)
temp_update.start()

vent_mode = [sg.Button(size=(5,1),image_filename=upper,key='__upper__'),
                sg.Button(size=(5,1),image_filename=upper_lower,key='__upper_lower__'),
                sg.Button(size=(5,1),image_filename=lower,key='__lower__'),
                sg.Button(size=(5,1),image_filename=defrost_lower,key='__defrost_lower__'),
                sg.Button(size=(5,1),image_filename=defrost,key='__defrost__')]

switches = [sg.Button(image_filename=rear_defrost,size=(15,1),key='__rear_defrost__'), sg.Button(size=(15,1),image_filename=ac,key='__ac__')]

power = [[sg.Button("",image_filename=arrow_up,key='__up__'),sg.Text(power_level,key='power_text'),sg.Button("",image_filename=arrow_down,key='__down__')]]

temperature = [[sg.Text("Temperature: "),sg.Slider(range=(65,80),default_value=75,size=(20,10),orientation='horizontal',key='set_temp')]]


layout = [
            [sg.Text("{:.0f}".format(temp_queue.get()),justification='center',key='temp_text',size=(15,1))],
            vent_mode,
            switches,
            [sg.Column(power),
             sg.Column(temperature)
            ]
         ]

window = sg.Window("Climate Control",layout)



while True:
    temp = temp_queue.get()
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
    window['temp_text'].update("{:.0f}".format(temp))
    window['power_text'].update(power_level)
    climate_control(temp,set_temperature)
