import time
from mpu6050 import mpu6050


if __name__ == "__main__":
    mpu = mpu6050(0x68)
    accel_data = sensor.get_accel_data()
    print(accel_data)
    time.sleep(1)
