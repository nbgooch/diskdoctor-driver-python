import config.lis3mdl as config
from smbus2 import SMBus


class Magnetometer:
  def __init__(self):
    self.address = config.LIS3MDL_ADDRESS
    self.bus = SMBus(1)
    self.bus.write_byte_data(self.address, config.LIS3MDL_CTRL_REG1, 0b11011100) # Temp sensor enabled, High performance, ODR 80 Hz, FAST ODR disabled and Selft test disabled.
    self.bus.write_byte_data(self.address, config.LIS3MDL_CTRL_REG2, 0b00100000) # +/- 8 gauss
    self.bus.write_byte_data(self.address, config.LIS3MDL_CTRL_REG3, 0b00000000) # Continuous-conversion mode
    print('Initialized magnetometer')

  def read_xyz(self):
    bytes = self.bus.read_i2c_block_data(self.address, config.LIS3MDL_OUT_X_L, 6)
    x = (bytes[0] | bytes[1]) << 8
    y = (bytes[2] | bytes[3]) << 8
    z = (bytes[4] | bytes[5]) << 8
    print(f'Read magnetometer x: {x}, y: {y}, z: {z}')
    return (x, y, z)