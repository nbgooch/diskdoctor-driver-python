#! /usr/bin/python

import signal
import time
import devices
import socket
import socketio

read = 0.2

if __name__ == "__main__":
  print("Here")
  gps = devices.gps.GPS()
  accel = devices.accelerometer.Accelerometer()
  gyro = devices.gyroscope.Gryoscope()
  magneto = devices.magnetometer.Magnetometer()
  # Create a socket object
  # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Connect the socket to the server
  # sock.connect(('192.168.1.2', 5000))

  # Create a Socket.IO client
  sio = socketio.SimpleClient()

  # Connect to the Socket.IO server
  sio.connect('http://192.168.1.2:5000')

  # Listen for events from the server
  event = sio.receive()
  print(f'received event: "{event[0]}" with arguments {event[1:]}')

  while True:
    sio.emit('gps_read', gps.read_gps())
    data = accel.read_xyz()
    sio.emit('accel_read', accel.read_xyz())
    data = gyro.read_xyz()
    sio.emit('gyro_read', gyro.read_xyz())
    data = magneto.read_xyz()
    sio.emit('magneto_read', magneto.read_xyz())
    time.sleep(read)

#This will capture exit when using Ctrl-Cdoogonmg
signal.signal(signal.SIGINT, handle_ctrl_c)
def handle_ctrl_c(signal, frame):
  sys.exit(130)


def on_event(event):
  print(event)
  pass