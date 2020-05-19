import os
from gpiozero import Button

def shutdown():
    print('Button pressed- system shutting down...')
    os.system('sudo shutdown -h now')

def print_test():
    print('Button pressed, system shutting down')

# Set up GPIO interactions
btn = Button(18)

# Action code for when the button ir pressed
while True:
    if btn.is_pressed:
        print_test()
    else:
        print("Button not pressed")
btn.when_pressed = print_test
