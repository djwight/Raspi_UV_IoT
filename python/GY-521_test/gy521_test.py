import time
from mpu6050 import mpu6050


if __name__ == "__main__":
    while True:
        mpu = mpu6050(0x68)
        accel_data = mpu.get_accel_data()
        gyro_data = mpu.get_gyro_data()
        temp_data = mpu.get_temp()
        accel, gyro, temp = mpu.get_all_data()
        print("")
        print("Accel data....", accel_data)
        print("")
        print("gyro data...", gyro_data)
        print(f"temp is {temp_data} oC")
        print("")
        print("all data", accel, gyro, temp)
        time.sleep(2)
