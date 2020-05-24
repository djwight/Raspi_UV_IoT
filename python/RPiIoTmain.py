import os
import json
import time
from datetime import datetime
import math
from gpiozero import Button
import RPi.GPIO as GPIO
from ADCDevice import *
from DFRobot_VEML6075 import DFRobot_VEML6075
import smbus


def setup():
    global bus
    bus = smbus.SMBus(1)


def read(chn):  # channel
    A0 = 0x40
    A1 = 0x41
    A2 = 0x42
    A3 = 0x43
    try:
        if chn == 0:
            bus.write_byte(address, A0)
        if chn == 1:
            bus.write_byte(address, A1)
        if chn == 2:
            bus.write_byte(address, A2)
        if chn == 3:
            bus.write_byte(address, A3)
        bus.read_byte(address)  # dummy read to start conversion
    except Exception:
        print('problem with address')
    return bus.read_byte(address)


def loop():
    # Data collection
    min_dict = {}
    temp = []
    light = []
    uva_lst = []
    uvb_lst = []
    uvi_lst = []
    ts = []
    while True:
        if btn.is_held:
            destroy()
            shutdown()
        else:
            # Temperature measurement
            temp_value = read(0)
            temp_voltage = temp_value/255.0*3.3
            Rt = 10*temp_voltage/(3.3-temp_voltage)
            tempK = 1/(1/(273.15 + 25) + math.log(Rt/10)/3950.0)
            tempC = tempK - 273.15

            # Light measurement
            light_value = read(1)

            # UV measurements
            uva = UV_VEML6075.getUva()
            uvb = UV_VEML6075.getUvb()
            uvi = UV_VEML6075.getUvi(uva, uvb)

            # Data collection section
            now = time.time()
            ts.append(now)
            light.append(light_value)
            temp.append(tempC)
            uva_lst.append(uva)
            uvb_lst.append(uvb)
            uvi_lst.append(uvi)

            # Saving the data every one min as json file
            if len(ts) == 10:
                min_dict['time_stamp'] = ts
                min_dict['temp'] = temp
                min_dict['light_levels'] = light
                min_dict['uva'] = uva_lst
                min_dict['uvb'] = uvb_lst
                min_dict['uvi'] = uvi_lst
                file_time = datetime.now()
                fpath = "data/"
                date = file_time.strftime("%Y-%m")
                hour_min = file_time.strftime("%H_%M")
                filename = "IoT_UV_" + date + "__" + hour_min + ".json"
                if not os.path.exists(fpath):
                    os.makedirs(fpath)
                file_wpath = fpath + filename
                with open(file_wpath, 'w') as jf:
                    json.dump(min_dict, jf)
                min_dict = {}
                temp = []
                light = []
                uva_lst = []
                uvb_lst = []
                uvi_lst = []
                ts = []
            time.sleep(6)


def destroy():
    adc.close()
    GPIO.cleanup()


def shutdown():
    print('Button pressed- system shutting down...')
    os.system('sudo shutdown -h now')


# Main script
if __name__ == "__main__":
    print("Starting...")
    btn = Button(18, hold_time=4)
    UV_VEML6075 = DFRobot_VEML6075(1, 0x10)
    while UV_VEML6075.begin() != True:
        print("UV sensor boot failed!")
        time.sleep(2)
    print("UV sensor boot success...")
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()
