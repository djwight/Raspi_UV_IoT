import sys
import pyRPiRTC
import time
from datetime import datetime

my_format = '%d/%m/%Y %H:%M:%S'
rtc = pyRPiRTC.DS1302(clk_pin=11, data_pin=13, ce_pin=15)


def set_date_time(time, f=my_format):
    global rtc
    dt = datetime.strptime(time, f)
    rtc.write_datetime(dt)


print('Press CTRL + C to end the script!')
try:
    set_date_time(datetime.now().strftime(my_format)) # uncomment this to set date/time
    while True:
        cdt = rtc.read_datetime()
        print(cdt.timestamp())
        print(time.time())
        print('Current date: {}'.format(cdt.strftime('%d/%m/%Y')))
        print('Current time: {}\n'.format(cdt.strftime('%H:%M:%S')))
        time.sleep(1)

except ValueError:
    sys.exit('error with RTC chip, check wiring')

except KeyboardInterrupt:
    print('\nScript end!')

finally:
    rtc.close()  # clean close
