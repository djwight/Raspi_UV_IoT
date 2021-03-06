import time
import sys
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
from PIL import ImageFont

font_path = 'FreePixel.ttf'


def changing_var(device):
    size = 12
    nf = ImageFont.truetype(font_path, size)
    datef = ImageFont.truetype(font_path, 13)
    for i in range(100):
        with canvas(device) as draw:
            draw.text((2, 10), f"Date", font=datef, fill=1)
            draw.text((2, 30), f"UVA {str(i)}", font=nf, fill=1)
            draw.text((2, 45), f"UVB {str(i)}", font=nf, fill=1)
            draw.text((55, 20), f"Temp {str(i)}", font=nf, fill=1)
            draw.text((55, 35), f"Humidity {str(i)}", font=nf, fill=1)
            draw.text((55, 50), f"Pressure {str(i)}", font=nf, fill=1)
            time.sleep(0.01)


def primitives(device):
    with canvas(device) as draw:
        # Draw an X.
        draw.line((0, 4, 128, 4), fill=1)


try:
    serial = i2c(port=1, address=0x3c)
    device = sh1106(serial, rotate=0, width=128, height=64)
    while True:
        changing_var(device)
        time.sleep(2)
        device.clear()
        time.sleep(2)
except KeyboardInterrupt:
    device.clear()
    print('Script end!')

# device.hide()
# device.show()
