import os
from gpiozero import button

def shutdown():
    print('Button pressed- system shutting down...')
    os.system('sudo shutdown -h now')

def print_test():
    print('Button pressed, system shutting down')

# Set up GPIO interactions
btn = button(18)

# Action code for when the button ir pressed
btn.when_pressed = print_test
