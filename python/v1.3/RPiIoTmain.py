import os
import json
import time
from datetime import datetime
import threading
import urllib.request
from gpiozero import Button, LED
import RPi.GPIO as GPIO
from DFRobot_VEML6075 import DFRobot_VEML6075
import smbus2
import bme280
import sys
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
import pyRPiRTC
from PIL import ImageFont

font_path = 'FreePixel.ttf'
btn_on_off = 1
my_format = '%d/%m/%Y %H:%M:%S'
rtc = pyRPiRTC.DS1302(clk_pin=11, data_pin=13, ce_pin=15)  # RTC for time


def bme280_setup():
    """Sets up the BME sensor and exports them as global objects."""
    global bus
    bus = smbus2.SMBus(1)
    global address
    address = 0x76
    global calibration_params
    calibration_params = bme280.load_calibration_params(bus, address)


def screen_display(device, screen_time, uva, uvb, tempC, humid, pressure):
    """Takes in the values from the sensors and diaplayed them on the
    oled screen."""
    size = 9
    nf = ImageFont.truetype(font_path, size)
    datef = ImageFont.truetype(font_path, 11)
    with canvas(device) as draw:
        draw.text((1, 10), f"{screen_time}", font=datef, fill=1)
        draw.text((1, 25), f"UVa {str(round(uva, 1))}", font=nf, fill=1)
        draw.text((1, 45), f"UVb {str(round(uvb, 1))}", font=nf, fill=1)
        draw.text((50, 25), f"Temp {str(round(tempC, 1))}oC", font=nf, fill=1)
        draw.text((50, 38), f"Humid {str(int(humid))} %", font=nf, fill=1)
        draw.text((50, 50), f"Pressu {str(int(pressure))}hPa", font=nf, fill=1)


def screen_off():
    """Switches off the OLED screen and sets the switching variable"""
    device.hide()
    global btn_on_off
    num = 0
    btn_on_off = num
    return btn_on_off


def screen_on():
    """Switches on the OLED screen and sets the switching variable"""
    device.show()
    global btn_on_off
    num = 1
    btn_on_off = num
    return btn_on_off


def set_date_time(time, f=my_format):
    """takes in a time and sets the RTC to that time."""
    global rtc
    dt = datetime.strptime(time, f)
    rtc.write_datetime(dt)


def btn_control():
    while True:
        if btn.is_held:
            shutdown(device)
        elif btn_on_off == 1:
            btn.when_pressed = screen_off
        elif btn_on_off == 0:
            btn.when_pressed = screen_on
            # print(f"btn variable is: {btn_on_off}")
        time.sleep(0.5)


def rec_loop():
    """Main loop for the UV IoT recording device. Saves minute json messages
    for the recorded data"""
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
        # Temperature, pressure and humidity measurement
        bme280_data = bme280.sample(bus, address, calibration_params)
        tempC = bme280_data.temperature
        pressure = bme280_data.pressure
        humid = bme280_data.humidity
        # print(f"Temp:   {tempC} oC")
        # print(f"Pressure:   {pressure} hPa")
        # print(f"Humidity:   {humid} % rH")

        # UV measurements
        uva = UV_VEML6075.getUva()
        uvb = UV_VEML6075.getUvb()
        uvi = UV_VEML6075.getUvi(uva, uvb)

        # Data collection section
        date_time = rtc.read_datetime()
        now = date_time.timestamp()
        ts.append(now)
        temp.append(tempC)
        press.append(pressure)
        hum.append(humid)
        uva_lst.append(uva)
        uvb_lst.append(uvb)
        uvi_lst.append(uvi)

        # Display values on oled
        screen_time = date_time.strftime("%d-%m-%Y %T")
        screen_display(device, screen_time, uva, uvb, tempC, humid, pressure)

        # Saving the data every one min as json file
        if len(ts) == 60:
            min_dict['time_stamp'] = ts[::6]
            min_dict['temp'] = temp[::6]
            min_dict['pressure'] = press[::6]
            min_dict['humidity'] = hum[::6]
            min_dict['uva'] = uva_lst[::6]
            min_dict['uvb'] = uvb_lst[::6]
            min_dict['uvi'] = uvi_lst[::6]
            fpath = "data/"
            date = date_time.strftime("%Y-%m-%d")
            hour_min = date_time.strftime("%H_%M")
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
            led.blink(on_time=0.1, off_time=0.05, n=3)
        time.sleep(0.9)


def destroy():
    """Clears up all the GPIO and clears the screen."""
    device.clear()
    led.close()
    btn.close()


def shutdown(device):
    """Issues a shutdown warning on the OLED and shutsdown the device."""
    device.clear()
    device.show()
    print('Button pressed- system shutting down...')
    size = 11
    fformat = ImageFont.truetype(font_path, size)
    with canvas(device) as draw:
        draw.text((2, 20), "Shutting down...", font=fformat, fill=1)
    time.sleep(2)
    device.hide()
    destroy()
    time.sleep(0.5)
    os.system('sudo shutdown -h now')


def connect():
    """Checks if the internet is on or not. Returns bool of status."""
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False


# Main script
if __name__ == "__main__":
    print("Starting IoT device...")
    btn = Button(18, hold_time=4)
    led = LED(23)
    UV_VEML6075 = DFRobot_VEML6075(1, 0x10)
    while UV_VEML6075.begin() is not True:
        print("UV sensor boot failed!")
        time.sleep(2)
    print("UV sensor boot success...")
    serial = i2c(port=1, address=0x3c)
    device = sh1106(serial, rotate=0, width=128, height=64)
    btn_loop = threading.Thread(target=btn_control)
    main_loop = threading.Thread(target=rec_loop)
    if connect() is True:
        set_date_time(datetime.now().strftime(my_format))
    else:
        break
    try:
        bme280_setup()
        for i in (btn_loop, main_loop):
            i.start()
    except KeyboardInterrupt:
        destroy()
