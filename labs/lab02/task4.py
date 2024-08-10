#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import machine
import time

from pololu import IMU

# Constants for sensors
SENSITIVITY_baro = 4096 # (LSB/hPa)
SENSITIVITY_accel = 0.061 # (mg/LSB)
SENSITIVITY_gyro = 4.375 # (mdps/LSB)
SENSITIVITY_mag = 2281  # (LSB/gauss)


# Variable for the multi-sensor object
m_sense = None


def init():
    global m_sense
    i2c = machine.I2C(0,
                  scl=machine.Pin(5),
                  sda=machine.Pin(4))
    m_sense = IMU(i2c)
    m_sense.barometer_init(IMU.BAROMETER_FREQ_1HZ)
    time.sleep(1)
    m_sense.accelerometer_init(IMU.ACCELEROMETER_FREQ_13HZ, IMU.ACCELEROMETER_SCALE_2G )
    time.sleep(1)
    m_sense.gyroscope_init(IMU.GYROSCOPE_FREQ_13HZ, IMU.GYROSCOPE_SCALE_125DPS)
    time.sleep(1)
    m_sense.magnetometer_init(IMU.MAGNETOMETER_FREQ_1_25HZ, IMU.MAGNETOMETER_SCALE_12GAUSS)
    time.sleep(1)


def main():
    init()
    
    while True:
        baro_raw = m_sense.barometer_raw_data()
        baro = baro_raw / SENSITIVITY_baro
        print(f"B: {baro:.2f}")
        time.sleep(1)
        
        accel_raw = m_sense.accelerometer_raw_data()
        accel_x = accel_raw["x"] * SENSITIVITY_accel/1000
        accel_y = accel_raw["y"] * SENSITIVITY_accel/1000
        accel_z = accel_raw["z"] * SENSITIVITY_accel/1000
        print(f"A: {accel_x:.2f} g-units, {accel_y:.2f} g-units, {accel_z:.2f} g-units")

        
        mag_raw = m_sense.magnetometer_raw_data()
        mag_x = mag_raw["x"] / SENSITIVITY_mag
        mag_y = mag_raw["y"] / SENSITIVITY_mag
        mag_z = mag_raw["z"] / SENSITIVITY_mag
        print(f"M: {mag_x:.2f} gauss, {mag_y:.2f} gauss, {mag_z:.2f} gauss")
        
    
        gyro_raw = m_sense.gyroscope_raw_data()
        gyro_x = gyro_raw["x"] * SENSITIVITY_gyro/1000
        gyro_y = gyro_raw["y"] * SENSITIVITY_gyro/1000
        gyro_z = gyro_raw["z"] * SENSITIVITY_gyro/1000
        print(f"G: {gyro_x:.2f} dps, {gyro_y:.2f} dps, {gyro_z:.2f} dps")
        
        temp_raw = m_sense.lps25h_raw_temp()
        temp_new = 42.5 + (temp_raw / 480)
        print(f"T: {temp_new:.2f} C")


if __name__ == "__main__":
    main()
