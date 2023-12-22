
import time
from smbus2 import SMBus
import sys
import config.gps as config

class GPS():
  def __init__(self):
    self.address = config.GPS_ADDRESS
    self.bus = SMBus(1)
    print('Initialized gps')

  def read_xyz(self):
    bytes = self.bus.read_i2c_block_data(self.address, config.LSM6DSL_OUTX_L_G, 6)
    x = (bytes[0] | bytes[1]) << 8
    y = (bytes[2] | bytes[3]) << 8
    z = (bytes[4] | bytes[5]) << 8
    print(f'Read accelerometer x: {x}, y: {y}, z: {z}')
    return (x, y, z)

  def parseResponse(gpsLine):
    if(gpsLine.count(36) == 1):                           # Check #1, make sure '$' doesnt appear twice
      if len(gpsLine) < 84:                               # Check #2, 83 is maximun NMEA sentenace length.
          CharError = 0;
          for c in gpsLine:                               # Check #3, Make sure that only readiable ASCII charaters and Carriage Return are seen.
              if (c < 32 or c > 122) and  c != 13:
                  CharError+=1
          if (CharError == 0):#    Only proceed if there are no errors.
              gpsChars = ''.join(chr(c) for c in gpsLine)
              if (gpsChars.find('txbuf') == -1):          # Check #4, skip txbuff allocation error
                  gpsStr, chkSum = gpsChars.split('*',2)  # Check #5 only split twice to avoid unpack error
                  gpsComponents = gpsStr.split(',')
                  chkVal = 0
                  for ch in gpsStr[1:]: # Remove the $ and do a manual checksum on the rest of the NMEA sentence
                      chkVal ^= ord(ch)
                  if (chkVal == int(chkSum, 16)): # Compare the calculated checksum with the one in the NMEA sentence
                      print(gpsChars)

def readGPS():
    c = None
    response = []
    try:
        while True: # Newline, or bad char.
            c = BUS.read_byte(address)
            if c == 255:
                return False
            elif c == 10:
                break
            else:
                response.append(c)
        parseResponse(response)
    except IOError:
        connectBus()
    except Exception as e:
        print(e)
connectBus()
while True:
    readGPS()
    time.sleep(gpsReadInterval)
