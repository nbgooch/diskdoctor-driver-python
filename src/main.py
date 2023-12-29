#! /usr/bin/python

import signal
import time
import devices
import socket
import socketIOclient

read = 0.2

if __name__ == "__main__":
  print("Here")
  gps = devices.gps.GPS()
  accel = devices.accelerometer.Accelerometer()
  gyro = devices.gyroscope.Gryoscope()
  magneto = devices.magnetometer.Magnetometer()
  # Create a socket object
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Connect the socket to the server
  sock.connect(('localhost', 5000))

  # Create a Socket.IO client
  sio = socketIOclient.SocketIO(sock)

  # Connect to the Socket.IO server
  sio.connect()

  # Listen for events from the server
  sio.on('server', on_event)

  # Send an event to the server

  # Close the socket
  sock.close()
  while True:
    data = gps.read_gps()
    sio.emit('client', data)
    time.sleep(read)

#This will capture exit when using Ctrl-C
signal.signal(signal.SIGINT, handle_ctrl_c)
def handle_ctrl_c(signal, frame):
  sys.exit(130)


def on_event(event):
  print(event)
  pass