use i2cdev::core::*;
#[cfg(any(target_os = "linux"))]
use i2cdev::linux::{LinuxI2CDevice, LinuxI2CError};

use std::error::Error as StdError;
use std::fmt;

#[derive(Debug)]
pub enum Error<E: StdError + 'static> {
    Init,
    Read,
    Write,
    Device(E),
}

pub fn init<D: I2CDevice>(
    dev: &mut D,
    who_am_i: u8,
    expected_response: u8,
) -> Result<(), Error<D::Error>> {
    let who_am_i_response = dev.smbus_read_byte_data(who_am_i)?;
    if who_am_i_response == expected_response {
        Ok(())
    } else {
        Err(Error::Init)
    }
}

pub fn read_block<D: I2CDevice>(
    dev: &mut D,
    command: u8,
    size: u8,
) -> Result<Vec<u8>, Error<D::Error>> {
    let block = dev.smbus_read_i2c_block_data(command, size)?;
    if block.len() != size as usize {
        return Err(Error::Read);
    }
    Ok(block)
}

impl<E: StdError + 'static> StdError for Error<E> {
    fn source(&self) -> Option<&(dyn StdError + 'static)> {
        match self {
            Error::Device(ref err) => Some(err),
            _ => None,
        }
    }
}

impl<E: StdError + 'static> fmt::Display for Error<E> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Error::Init => write!(f, "init failed"),
            Error::Read => write!(f, "read failed"),
            Error::Write => write!(f, "write failed"),
            Error::Device(err) => write!(f, "device error: {}", err),
        }
    }
}

impl<E: StdError + 'static> From<E> for Error<E> {
    fn from(err: E) -> Self {
        Error::Device(err)
    }
}