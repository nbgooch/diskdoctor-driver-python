// use std::thread;
// use std::time::Duration;

pub mod devices;
pub mod utils;
pub mod config;

use crate::devices::accelerometer::Accelerometer;

// const xl_read_rate: u32 = 40;
// const g_read_rate: u32 = 40;
// const m_read_rate: u32 = 40;

fn main() {
    let mut xl = Accelerometer::new_from_address("/dev/i2c-1")?;
}
