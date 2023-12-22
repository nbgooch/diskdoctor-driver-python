import config.lsm6dsl as config
from smbus2 import SMBus


class Gryoscope:
  def __init__(self):
    self.address = config.LSM6DSL_ADDRESS
    self.bus = SMBus(1)
    self.bus.write_byte_data(self.address, config.LSM6DSL_CTRL2_G, 0b10011100) # ODR 3.3kHz, 200 dps
    print('Initialized gyroscope')

  def read_xyz(self):
    bytes = self.bus.read_i2c_block_data(self.address, config.LSM6DSL_OUTX_L_G, 6)
    x = (bytes[0] | bytes[1]) << 8
    y = (bytes[2] | bytes[3]) << 8
    z = (bytes[4] | bytes[5]) << 8
    print(f'Read gyroscope x: {x}, y: {y}, z: {z}')
    return (x, y, z)