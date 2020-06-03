import time
import sys
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
from PIL import ImageFont

font_path = 'ChiKareGo.ttf'


def changing_var(device):
    size = 40
    nf = ImageFont.truetype(font_path, size)  # new font
    for i in range(100):
        with canvas(device) as draw:
        draw.text((28, 7), 'Changing var.', fill=1)
        if i < 10:
            draw.text((50,22),'0{}'.format(str(i)),font=nf,fill=1)
        else:
            draw.text((50, 22), str(i), font=nf, fill=1)
            time.sleep(0.001)


def primitives(device):
    with canvas(device) as draw:
        # Draw a rectangle.
        draw.rectangle((4, 4, 40, 10), outline=1, fill=0)

        # Draw an ellipse.
        draw.ellipse((4, 20, 18, 34), outline=1, fill=1)

        # Draw a triangle.
        draw.polygon([(10,44),(40,20),(40,44)],outline=1,fill=0)

        # Draw an X.
        draw.line((4, 48, 126, 62), fill=1)
        draw.line((4, 62, 126, 48), fill=1)

        # Write two lines of text.
        draw.text((45, 20), 'AZ-Delivery', fill=1)

        size = 10
        nf = ImageFont.truetype(font_path, size)
        draw.text((45, 4), 'AZ-Delivery', font=nf, fill=1)


try:
    serial = i2c(port=1, address=0x3c)
    device = sh1106(serial, rotate=0, width=128, height=64)
    print('[Press CTRL + C to end the script!]')
    while(True):
        print('Testing printing variable.')
        changing_var(device)
        time.sleep(2)
        print('Testing basic graphics.')
        primitives(device)
        time.sleep(3)
        print('Testing display ON/OFF.')
        for _ in range(5):
            time.sleep(0.5)
            device.hide()
            time.sleep(0.5)
            device.show()
            print('Testing clearing display.\n')
            device.clear()
            time.sleep(2)
except KeyboardInterrupt:
    print('Script end!')
