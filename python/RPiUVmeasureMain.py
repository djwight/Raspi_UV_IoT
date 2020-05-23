import os
from gpiozero import Button
import RPi.GPIO as GPIO
from ADCDevice import *
import time
import math
from DFRobot_VEML6075 import DFRobot_VEML6075


def setup():
    global adc
    if(adc.detectI2C(0x48)):
        adc = PCF8591()
    else:
        print("No ADC found")


def loop():
    # Data collection
    min_dict = {}
    temp = []
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
            value = adc.analogRead(0)
            voltage = value/255.0*3.3
            Rt = 10*voltage/(3.3-voltage)
            tempK = 1/(1/(273.15 + 25) + math.log(Rt/10)/3950.0)
            tempC = tempK - 273.15

            # UV measurements
            uva = UV_VEML6075.getUva()
            uvb = UV_VEML6075.getUvb()
            uvi = UV_VEML6075.getUvi(uva, uvb)

            # Data collection section
            now = time.time()
            ts.append(now)
            temp.append(tempC)
            uva_lst.append(uva)
            uvb_lst.append(uvb)
            uvi_lst.append(uvi)

            # Saving the data every one min as json file
            if len(ts) == 10:
                min_dict['time_stamp'] = ts
                min_dict['temp'] = temp
                min_dict['uva'] = uva_lst
                min_dict['uvb'] = uvb_lst
                min_dict['uvi'] = uvi_lst
                file_time = time.now()
                fpath = "data/"
                date = file_time.strftime("%Y-%m")
                hour = file_time.strftime("%H_%M")
                filename = "IoT_UV_" + date + "__" + time + ".json"
                if not os.path.exists(fpath):
                    os.makedirs(fpath)
                with open(filename, 'w') as json:
                    json.dump(min_dict, json)
                min_dict = {}
                temp = []
                uva_lst = []
                uvb_lst = []
                uvi_lst = []
                ts = []
            time.sleep(10)

            # Printing script
            # print("\n============== Results ==============")
            # print(f"Temp Celcius:   {round(tempC, 2)}")
            # print(f"UVA:   {round(uva, 2)}")
            # print(f"UVB:   {round(uvb, 2)}")
            # print(f"UV Index:   {round(uvi, 2)}mw/cm^2")
            # print("============ Results end ============\n")


def destroy():
    adc.close()
    GPIO.cleanup()


def shutdown():
    print('Button pressed- system shutting down...')
    os.system('sudo shutdown -h now')


# Set up GPIO interactions
btn = Button(18, hold_time=4)

# Main script
if __name__ == "__main__":
    print("Starting...")
    adc = ADCDevice()
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
