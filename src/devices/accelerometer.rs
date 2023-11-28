use std::path::Path;
use i2cdev::core::*;
#[cfg(any(target_os = "linux"))]
use i2cdev::linux::{LinuxI2CDevice, LinuxI2CError};
use crate::config::lsm6dsl as config;
use crate::utils::i2c::{self as util, Error};

pub struct Accelerometer<D: I2CDevice>(D);

impl Accelerometer<LinuxI2CDevice> {
    /// Creates a new accelerometer reader from an address.
    ///
    /// # Arguments
    /// * `addr`: The I2C device address, e.g. `/dev/i2c-1`.
    pub fn new_from_address<P: AsRef<Path>>(addr: P) -> Result<Self, Error<LinuxI2CError>> {
        let dev = LinuxI2CDevice::new(addr, config::LSM6DSL_ADDRESS)?;
        Accelerometer::new(dev)
    }
}

impl<D: I2CDevice> Accelerometer<D> {
    /// Creates a new accelerometer reader from an I2C device.
    ///
    /// # Arguments
    /// * `dev`: The I2C device.
    pub fn new(mut dev: D) -> Result<Self, util::Error<D::Error>> {
        util::init(&mut dev, config::LSM6DSL_WHO_AM_I, 0x6A)?;
        dev.smbus_write_byte_data(config::LSM6DSL_CTRL1_XL, 0b10011011)?; // ODR 3.33 kHz, +/- 4g , BW = 400hz
        dev.smbus_write_byte_data(config::LSM6DSL_CTRL8_XL, 0b11001000)?; // Low pass filter enabled, BW9, composite filter
        dev.smbus_write_byte_data(config::LSM6DSL_CTRL3_C, 0b01000100)?; // Enable Block Data update, increment during multi byte read
        Ok(Self(dev))
    }

    /// Read the raw accelerometer values.
    pub fn read(&mut self) -> Result<(i32, i32, i32), util::Error<D::Error>> {
        let block = util::read_block(&mut self.0, config::LSM6DSL_OUTX_L_XL, 6)?;
        // Combine readings for each axis
        let x = ((block[0] as i16) | (block[1] as i16) << 8) as i32;
        let y = ((block[2] as i16) | (block[3] as i16) << 8) as i32;
        let z = ((block[4] as i16) | (block[5] as i16) << 8) as i32;
        Ok((x, y, z))
    }
}