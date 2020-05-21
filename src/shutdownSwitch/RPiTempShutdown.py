import os
from gpiozero import Button
import RPi.GPIO as GPIO
from ADCDevice import *
import time
import math

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
            value = adc.analogRead(0)
            voltage = value/255.0*3.3
            Rt = 10*voltage/(3.3-voltage)
            tempK = 1/(1/(273.15 + 25) + math.log(Rt/10)/3950.0)
            tempC = tempK - 273.15
            print(f"Temp Celcius = {round(tempC, 2)} and voltage = {round(voltage, 2)}")
            time.sleep(0.5)

def destroy():
    adc.close()
    GPIO.cleanup()

# Set up GPIO interactions
btn = Button(18, hold_time=4)

# Action code for when the button ir pressed
if __name__ == "__main__":
    adc = ADCDevice()
    print("Starting...")
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()
