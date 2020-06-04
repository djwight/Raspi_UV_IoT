import time
import sys
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
from PIL import ImageFont

font_path = 'ChiKareGo.ttf'


def changing_var(device):
    size = 20
    nf = ImageFont.truetype(font_path, size)  # new font
    for i in range(100):
        with canvas(device) as draw:
            draw.text((0, 0), str(i), font=nf, fill=1)
            time.sleep(0.005)


def primitives(device):
    with canvas(device) as draw:
        # Draw an X.
        draw.line((4, 48, 126, 48), fill=1)
        draw.line((4, 62, 126, 62), fill=1)


try:
    serial = i2c(port=1, address=0x3c)
    device = sh1106(serial, rotate=90, width=128, height=64)
    print('[Press CTRL + C to end the script!]')
    while True:
        print('Testing printing variable.')
        changing_var(device)
        time.sleep(2)
        print('Testing basic graphics.')
        primitives(device)
        time.sleep(3)
        print('Testing clearing display.\n')
        device.clear()
        time.sleep(2)
except KeyboardInterrupt:
    print('Script end!')

# device.hide()
# device.show()
