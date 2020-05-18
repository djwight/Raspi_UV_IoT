import os
from gpiozero import button

def shutdown():
    os.system('sudo shutdown -h now')

if __name__ == '__main__':
    shutdown()
