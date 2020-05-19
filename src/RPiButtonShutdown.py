import os
from gpiozero import Button
import time

def shutdown():
    print('Button pressed- system shutting down...')
    os.system('sudo shutdown -h now')

def print_test():
    print('Button pressed, system shutting down')

# Set up GPIO interactions
btn = Button(18, hold_time=4)

# Action code for when the button ir pressed
if __name__ == "__main__":
    while True:
        time.sleep(0.5)
        if btn.is_held:
           shutdown()
           # print_test()
        else:
            print("Running regular script....")
