import smbus
import time

address = 0x48
A0 = 0x40
A1 = 0x41
A2 = 0x42
A3 = 0x43

bus_1 = smbus.SMBus(1)
bus_2 = smbus
while True:
    bus.write_byte(address, A0)
    therm_value = bus.read_byte(address)
    therm_vol = therm_value*3.3/255
    bus.write_byte(address, A1)
    photo_value = bus.read_byte(address)
    photo_vol = photo_value*3.3/255
    print(f"A0:     {round(therm_vol, 2)}")
    print(f"A1:     {round(photo_vol, 2)}")
    time.sleep(1)
