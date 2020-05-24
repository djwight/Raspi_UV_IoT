import smbus
import time

address = 0x48
A0 = 0x40
A1 = 0x41
A2 = 0x42
A3 = 0x43

bus = smbus.SMBus(1)


def read(chn):  # channel
    try:
        if chn == 0:
            bus.write_byte(address, A0)
        if chn == 1:
            bus.write_byte(address, A1)
        if chn == 2:
            bus.write_byte(address, A2)
        if chn == 3:
            bus.write_byte(address, A3)
        bus.read_byte(address)  # dummy read to start conversion
    except Exception:
        print('problem with address')
    return bus.read_byte(address)

while True:
    print('AIN0:    {read(0)}')
    print('AIN0:    {read(1)}')
    print('AIN0:    {read(2)}')
    print('AIN0:    {read(3)}')


"""
    bus.write_byte(address, A0)
    therm_value = bus.read_byte(address)
    therm_vol = therm_value*3.3/255
    bus.write_byte(address, A1)
    photo_value = bus.read_byte(address)
    photo_vol = photo_value*3.3/255
    bus.write_byte(address, A2)
    A2_value = bus.read_byte(address)
    A2_vol = photo_value*3.3/255
    bus.write_byte(address, A3)
    A3_value = bus.read_byte(address)
    A3_vol = photo_value*3.3/255
    print(f"A0:     {round(therm_vol, 2)}")
    print(f"A1:     {round(photo_vol, 2)}")
    print(f"A2:     {round(A2_vol, 2)}")
    print(f"A2:     {round(A2_vol, 2)}")
    time.sleep(1)
"""
