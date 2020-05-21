import os
from gpiozero import Button

def shutdown():
    print('system shutting down...')
    os.system('sudo shutdown -h now')

if __name__ == '__main__':
    shutdown()
