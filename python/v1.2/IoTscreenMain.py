import os
import json
import time
from datetime import datetime
import math
from gpiozero import Button
import RPi.GPIO as GPIO
from DFRobot_VEML6075 import DFRobot_VEML6075
import smbus2
import bme280
import sys
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
from PIL import ImageFont

font_path = 'FreePixel.ttf'


def bme280_setup():
    global bus
    bus = smbus2.SMBus(1)
    global address
    address = 0x76
    global calibration_params
    calibration_params = bme280.load_calibration_params(bus, address)


def screen_display(device, date_time, uva, uvb, tempC, humid, pressure):
    size = 11
    nf = ImageFont.truetype(font_path, size)
    datef = ImageFont.truetype(font_path, 10)
    with canvas(device) as draw:
        draw.text((1, 10), f"{date_time}", font=datef, fill=1)
        draw.text((1, 30), f"UVa {str(round(uva, 2))}", font=nf, fill=1)
        draw.text((2, 45), f"UVb {str(round(uvb, 2))}", font=nf, fill=1)
        draw.text((52, 20), f"Temp {str(round(tempC, 1))}oC", font=nf, fill=1)
        draw.text((52, 35), f"Humidity {str(int(humid))} % rH", font=nf, fill=1)
        draw.text((52, 50), f"Pressure {str(int(pressure))} hPa", font=nf, fill=1)


def loop():
    # Data collection
    min_dict = {}
    temp = []
    press = []
    hum = []
    uva_lst = []
    uvb_lst = []
    uvi_lst = []
    ts = []
    while True:
        if btn.is_held:
            destroy()
            shutdown()
        else:
            # Temperature, pressure and humidity measurement
            bme280_data = bme280.sample(bus, address, calibration_params)
            tempC = bme280_data.temperature
            pressure = bme280_data.pressure
            humid = bme280_data.humidity
            print(f"Temp:   {tempC} oC")
            print(f"Pressure:   {pressure} hPa")
            print(f"Humidity:   {humid} % rH")

            # UV measurements
            uva = UV_VEML6075.getUva()
            uvb = UV_VEML6075.getUvb()
            uvi = UV_VEML6075.getUvi(uva, uvb)

            # Data collection section
            now = time.time()
            ts.append(now)
            temp.append(tempC)
            press.append(pressure)
            hum.append(humid)
            uva_lst.append(uva)
            uvb_lst.append(uvb)
            uvi_lst.append(uvi)

            # Display values on oled
            screen_time = datetime.now()
            date_time = screen_time.strftime("%d-%m-%Y %T")
            screen_display(device, date_time, uva, uvb, tempC, humid, pressure)

            # Saving the data every one min as json file
            if len(ts) == 10:
                min_dict['time_stamp'] = ts
                min_dict['temp'] = temp
                min_dict['pressure'] = press
                min_dict['humidity'] = hum
                min_dict['uva'] = uva_lst
                min_dict['uvb'] = uvb_lst
                min_dict['uvi'] = uvi_lst
                file_time = datetime.now()
                fpath = "data/"
                date = file_time.strftime("%Y-%m-%d")
                hour_min = file_time.strftime("%H_%M")
                filename = "IoT_UV_" + date + "__" + hour_min + ".json"
                if not os.path.exists(fpath):
                    os.makedirs(fpath)
                file_wpath = fpath + filename
                with open(file_wpath, 'w') as jf:
                    json.dump(min_dict, jf)
                min_dict = {}
                temp = []
                press = []
                hum = []
                uva_lst = []
                uvb_lst = []
                uvi_lst = []
                ts = []
            time.sleep(6)


def destroy():
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
    serial = i2c(port=1, address=0x3c)
    device = sh1106(serial, rotate=0, width=128, height=64)
    try:
        bme280_setup()
        loop()
    except KeyboardInterrupt:
        destroy()
