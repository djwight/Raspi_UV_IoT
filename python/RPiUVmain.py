
import os
from gpiozero import Button
import RPi.GPIO as GPIO
from ADCDevice import *
import time
import math
from DFRobot_VEML6075 import DFRobot_VEML6075


def shutdown():
    print('Button pressed- system shutting down...')
    os.system('sudo shutdown -h now')


def print_test():
    print('Button pressed, system shutting down')


def setup():
    global adc
    if(adc.detectI2C(0x48)):
        adc = PCF8591()
    else:
        print("No ADC found")


def loop():
    while True:
        if btn.is_held:
            destroy()
            shutdown()
            # print_test()
            # break
        else:
            # Temperature measurement
            value = adc.analogRead(0)
            voltage = value/255.0*3.3
            Rt = 10*voltage/(3.3-voltage)
            tempK = 1/(1/(273.15 + 25) + math.log(Rt/10)/3950.0)
            tempC = tempK - 273.15

            # Light measurement
           # l_value = adc.analogRead(2)
           # l_voltage = l_value/255.0*3.3

            # UV measurements
            uva = UV_VEML6075.getUva()
            uvb = UV_VEML6075.getUvb()
            uvi = UV_VEML6075.getUvi(uva, uvb)

            # Printing script
            print("\n============== Results ==============")
            print(f"Temp Celcius:   {round(tempC, 2)}")
           # print(f"Light value:    {round(l_value, 4)}")
           # print(f"Light voltage:    {round(l_voltage, 2)}")
            print(f"UVA:   {round(uva, 2)}")
            print(f"UVB:   {round(uvb, 2)}")
            print(f"UV Index:   {round(uvi, 2)}mw/cm^2")
            print("============ Results end ============\n")
            time.sleep(0.5)


def destroy():
    adc.close()
    GPIO.cleanup()


# Set up GPIO interactions
btn = Button(18, hold_time=4)

# Action code for when the button ir pressed
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
