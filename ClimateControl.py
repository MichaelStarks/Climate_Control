import time
import board
import busio
import adafruit_mcp9808

i2c_bus = busio.I2C(board.SCL, board.SDA)

set_temperature = 75 #Temperature in degrees

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
    return sum(read_temp())/len(read_temp())

def climate_control():
    if(average_temp() - set_temperature > 2):
        print("Too hot")
    elif(average_temp() - set_temperature < -2):
        print("Too cold")
    else:
        print("We good")
