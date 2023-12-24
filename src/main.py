#! /usr/bin/python

import signal
import time
import devices

read = 0.2

def handle_ctrl_c(signal, frame):
  sys.exit(130)
#This will capture exit when using Ctrl-C
signal.signal(signal.SIGINT, handle_ctrl_c)

if __name__ == "__main__":
  print("Here")
  gps = devices.gps.GPS()
  accel = devices.accelerometer.Accelerometer()
  gyro = devices.gyroscope.Gryoscope()
  magneto = devices.magnetometer.Magnetometer()
  while True:
    gps.read_gps()
    time.sleep(read)

