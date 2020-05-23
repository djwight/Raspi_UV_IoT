import smbus
import time

address = 0x48
A0 = 0x40
A1 = 0x41
A2 = 0x42
A3 = 0x43

bus = smbus.SMBus(1)
while True:
    bus.write_byte(adress, A0)
    value = bus.read_byte(address)
    vol = value*3.3/255
    print(f"A0:     {round(vol, 2)}")
    time.sleep(1)
