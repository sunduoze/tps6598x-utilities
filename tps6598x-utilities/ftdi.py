#!/bin/env python
# -*- coding: cp1252 -*-
#==========================================================================
# (c) 2015 Texas Instruments
#--------------------------------------------------------------------------
# Project : Method and parameters for FTDI hardware 
# File    : ftdi.py
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#==========================================================================


#==========================================================================
# CONSTANTS
#==========================================================================

# FTDI Clock Rates
I2C_CLOCK_STANDARD_MODE =    100000,  # 100kb/sec
I2C_CLOCK_FAST_MODE =        400000,  # 400kb/sec
I2C_CLOCK_FAST_MODE_PLUS =  1000000,  # 1000kb/sec
I2C_CLOCK_HIGH_SPEED_MODE = 3400000   # 3.4Mb/sec

# Options to I2C_DeviceWrite & I2C_DeviceRead 

# Generate start condition before transmitting 
I2C_TRANSFER_OPTIONS_START_BIT = 0x00000001

# Generate stop condition before transmitting 
I2C_TRANSFER_OPTIONS_STOP_BIT = 0x00000002

# Continue transmitting data in bulk without caring about Ack or nAck from device if this bit is
# not set. If this bit is set then stop transitting the data in the buffer when the device nAcks
I2C_TRANSFER_OPTIONS_BREAK_ON_NACK = 0x00000004

# libMPSSE-I2C generates an ACKs for every byte read. Some I2C slaves require the I2C
# master to generate a nACK for the last data byte read. Setting this bit enables working 
# with such I2C slaves 
I2C_TRANSFER_OPTIONS_NACK_LAST_BYTE = 0x00000008

# No address phase, no USB interframe delays 
I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BYTES = 0x00000010
I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BITS = 0x00000020
I2C_TRANSFER_OPTIONS_FAST_TRANSFER = 0x00000030

# If I2C_TRANSFER_OPTION_FAST_TRANSFER is set, then setting this bit would mean that the
# address field should be ignored. The address is either a part of the data or this is a 
# special I2C frame that doesn't require an address
I2C_TRANSFER_OPTIONS_NO_ADDRESS = 0x00000040

I2C_CMD_GETDEVICEID_RD = 0xF9
I2C_CMD_GETDEVICEID_WR = 0xF8

I2C_GIVE_ACK = 1
I2C_GIVE_NACK = 0

# 3-phase clocking is enabled by default. Setting this bit in ConfigOptions will disable it 
I2C_DISABLE_3PHASE_CLOCKING = 0x0001

# The I2C master should actually drive the SDA line only when the output is LOW. It should be
#tristate the SDA line when the output should be high. This tristating the SDA line during output
#HIGH is supported only in FT232H chip. This feature is called DriveOnlyZero feature and is
#enabled when the following bit is set in the options parameter in function I2C_Init 
I2C_ENABLE_DRIVE_ONLY_ZERO = 0x0002

# Status codes returned from FTDI calls
FT_OK = 0 
FT_INVALID_HANDLE = 1 
FT_DEVICE_NOT_FOUND = 2
FT_DEVICE_NOT_OPENED = 3 
FT_IO_ERROR = 4 
FT_INSUFFICIENT_RESOURCES = 5 
FT_INVALID_PARAMETER = 6 
FT_INVALID_BAUD_RATE = 7 
FT_DEVICE_NOT_OPENED_FOR_ERASE = 8
FT_DEVICE_NOT_OPENED_FOR_WRITE = 9 
FT_FAILED_TO_WRITE_DEVICE = 10 
FT_EEPROM_READ_FAILED = 11
FT_EEPROM_WRITE_FAILED = 12
FT_EEPROM_ERASE_FAILED = 13
FT_EEPROM_NOT_PRESENT = 14
FT_EEPROM_NOT_PROGRAMMED = 15
FT_INVALID_ARGS = 16
FT_NOT_SUPPORTED = 17
FT_OTHER_ERROR = 18
FT_DEVICE_LIST_NOT_READY = 19

errorDict = { 0 : 'FT_OK',
              1 : 'FT_INVALID_HANDLE',
              2 : 'FT_DEVICE_NOT_FOUND',
              3 : 'FT_DEVICE_NOT_OPENED',
              4 : 'FT_IO_ERROR',
              5 : 'FT_INSUFFICIENT_RESOURCES',
              6 : 'FT_INVALID_PARAMETER',
              7 : 'FT_INVALID_BAUD_RATE',
              8 : 'FT_DEVICE_NOT_OPENED_FOR_ERASE',
              9 : 'FT_DEVICE_NOT_OPENED_FOR_WRITE',
              10 : 'FT_FAILED_TO_WRITE_DEVICE',
              11 : 'FT_EEPROM_READ_FAILED',
              12 : 'FT_EEPROM_WRITE_FAILED',
              13 : 'FT_EEPROM_ERASE_FAILED',
              14 : 'FT_EEPROM_NOT_PRESENT',
              15 : 'FT_EEPROM_NOT_PROGRAMMED',
              16 : 'FT_INVALID_ARGS',
              17 : 'FT_NOT_SUPPORTED',
              18 : 'FT_OTHER_ERROR',
              19 : 'FT_DEVICE_LIST_NOT_READY' }

# FTDI SPI definitions
SPI_CONFIG_OPTION_MODE_MASK = 0x00000003
SPI_CONFIG_OPTION_MODE0 = 0x00000000
SPI_CONFIG_OPTION_MODE1 = 0x00000001
SPI_CONFIG_OPTION_MODE2 = 0x00000002
SPI_CONFIG_OPTION_MODE3 = 0x00000003

SPI_CONFIG_OPTION_CS_MASK = 0x0000001C
SPI_CONFIG_OPTION_CS_DBUS3 = 0x00000000
SPI_CONFIG_OPTION_CS_DBUS4 = 0x00000004
SPI_CONFIG_OPTION_CS_DBUS5 = 0x00000008
SPI_CONFIG_OPTION_CS_DBUS6 = 0x0000000C
SPI_CONFIG_OPTION_CS_DBUS7 = 0x00000010

SPI_CONFIG_OPTION_CS_ACTIVELOW = 0x00000020

SPI_TRANSFER_OPTIONS_SIZE_IN_BYTES = 0x00000000
SPI_TRANSFER_OPTIONS_SIZE_IN_BITS = 0x00000001
SPI_TRANSFER_OPTIONS_CHIPSELECT_ENABLE = 0x00000002
SPI_TRANSFER_OPTIONS_CHIPSELECT_DISABLE = 0x00000004

#==========================================================================
# HELPER FUNCTIONS
#==========================================================================

def array_u08 (n):  
    print array('B', '\0'*n)
    return array('B', '\0'*n)


#==========================================================================
# IMPORTS
#==========================================================================

from ctypes import *
import sys
from config import *
from array import array, ArrayType


#==========================================================================
# GLOBAL CODE
#==========================================================================

# Load the libMPSSE from FTDI to use its functions to access FTDI chip
ftdi = cdll.LoadLibrary("libMPSSE.dll")
    
#==========================================================================
# FUNCTIONS
#==========================================================================

# TODO: Implement SPI functions for FTDI
  
def ftdi_init(channel_to_open, spi_channel_to_open, bitrate, spibitrate):
    myException = Exception()
    # Open and initialize the FTDI I2C channel specified in config.py
        
    # Define structure used by I2C_InitChannel
    class CHANNEL_CONFIG(Structure):
        _fields_ = [
            ("ClockRate", c_uint),
            ("LatencyTimer", c_ubyte),
            ("Options", c_uint)]

    channels = c_uint(0)
    ftdi_handle = c_uint(0)
    ftdi_spi_handle = c_uint(0)
 
    # Is the FTDI connected to the PC?
    status = ftdi.I2C_GetNumChannels(byref(channels))

    if status != 0 :
        myException.message = "*** ERROR in FTDI call (I2C_GetNumChannels), status: %r\n" % status 
        raise myException

    # 0 Channels when no FTDI is detected
    if channels.value <= 0:
        myException.message = "No FTDI I2C channels (I2C_GetNumChannels) detected, exiting....\n"
        raise myException
        
    
    # Open the FTDI channel specified in config.py
    status = ftdi.I2C_OpenChannel(channel_to_open, byref(ftdi_handle))
    if status != 0 :
        myException.message = "*** ERROR in FTDI call (I2C_OpenChannel), status: %r" % status
        raise myException


    # Initialize the I2C channel with the parameters specified in config.py
    if ((bitrate != 100) & (bitrate != 400) & (bitrate != 1000) & (bitrate != 3400)): 
        myException.message = "Invalid I2C clock rate,", bitrate, ", specified, exiting..."
        raise myException

    channelConf = CHANNEL_CONFIG(bitrate*1000, 2, 0)
    i2c_channel_init = ftdi.I2C_InitChannel
    i2c_channel_init.argtypes = [c_uint, POINTER(CHANNEL_CONFIG)]
    i2c_channel_init.restype = c_uint
    
    status = i2c_channel_init(ftdi_handle.value, byref(channelConf))
    print("status.value", status)
    if status != 0 :
        myException.message = "*** ERROR in FTDI call (I2C_InitChannel), status: %r" % status
        raise myException


    print "I2C Bitrate set to", bitrate, "kHz"


    # Open the FTDI SPI channel specified in config.py
    status = ftdi.SPI_OpenChannel(spi_channel_to_open, byref(ftdi_spi_handle))
    if status != 0 :
        myException.message = "*** ERROR in FTDI call (SPI_OpenChannel), status: %r" % status
        raise myException


    # Define structure used by I2C_InitChannel
    class SPI_CHANNEL_CONFIG(Structure):
        _fields_ = [
            ("ClockRate", c_uint),
            ("LatencyTimer", c_ubyte),
            ("configOptions", c_uint),
            ("Pin", c_uint),
            ("reserved", c_ushort)]


    spiChannelConf = SPI_CHANNEL_CONFIG(spibitrate*1000, 2, SPI_CONFIG_OPTION_MODE0 | SPI_CONFIG_OPTION_CS_DBUS3 | SPI_CONFIG_OPTION_CS_ACTIVELOW, 0, 0)

    spi_channel_init = ftdi.SPI_InitChannel
    spi_channel_init.argtypes = [c_uint, POINTER(SPI_CHANNEL_CONFIG)]
    spi_channel_init.restype = c_uint

    status = spi_channel_init(ftdi_spi_handle.value, byref(spiChannelConf))
    if status != 0 :
        myException.message = "*** ERROR in FTDI call (SPI_InitChannel), status: %r" % status
        raise myException


    print "SPI Bitrate set to", spibitrate, "kHz"
        
    return (ftdi_handle.value, ftdi_spi_handle.value)

    
def ftdi_close(handle, spihandle):
    myException = Exception()
    # Close the FTDI I2C channel
        
    status = ftdi.I2C_CloseChannel(handle)
    if status != 0 :
        # if there is an error on the first close, perform the second but
        # report the error on the first
        ftdi.SPI_CloseChannel(spihandle)
    else :
        status = ftdi.SPI_CloseChannel(spihandle)
    
    return (status, errorDict[status] )
 
 
def ftdi_i2c_write(handle, slave_addr, flags, data_out):
    myException = Exception()
    # Write data to the I2C slave device
    bytes_transferred = c_uint(0)
    
    # Validate the data
    (data_out, num_bytes) = isinstance(data_out, ArrayType) and (data_out, len(data_out)) or (data_out[0], min(len(data_out[0]), int(data_out[1])))
    if data_out.typecode != 'B' :
        myException.message = "*** ERROR in ftdi_i2c_write, 'data_out' type must be array('B')"
        raise myException

        
    # Send the data

    # Get the address of the data array to transmit
    temp_ptr, _ = data_out.buffer_info()
    data_out_p = cast(temp_ptr, POINTER(c_ubyte))

    # Transmit the data
    status = ftdi.I2C_DeviceWrite(handle, slave_addr, num_bytes, data_out_p, byref(bytes_transferred), flags);
    if status != 0 :
        myException.message = "*** ERROR in FTDI call (I2C_DeviceWrite), status: %r" % status
        raise myException

    
    return


def ftdi_i2c_read(handle, slave_addr, flags, data_in):
    myException = Exception()
    # Read data from the I2C slave device

    bytes_transferred = c_uint(0)
    
    # Validate the data
    __data_in = isinstance(data_in, int)
    if __data_in:
        (data_in, num_bytes) = (array_u08(data_in), data_in)
    else:
        (data_in, num_bytes) = isinstance(data_in, ArrayType) and (data_in, len(data_in)) or (data_in[0], min(len(data_in[0]), int(data_in[1])))
        #if data_in.typecode != 'B':
        if data_in.typecode != 'B' :
            myException.message = "*** ERROR in ftdi_i2c_read, 'data_in' type must be array('B')"
            raise myException
        
    # Get the data

    # Get the address of the data array to transmit
    temp_ptr, _ = data_in.buffer_info()
    data_in_p = cast(temp_ptr, POINTER(c_ubyte))
    
    # Read the data
    status = ftdi.I2C_DeviceRead(handle, slave_addr, num_bytes, data_in_p, byref(bytes_transferred), flags);
    if status != 0 :
        myException.message = "*** ERROR in FTDI call (I2C_DeviceWrite), status: %r" % status
        raise myException


    # data_in post-processing
    return (bytes_transferred.value, data_in)
    
 
#==========================================================================
# main
#==========================================================================
if __name__ == "__main__":
    print 'This file is a helper file for adapting the scripts to the FTDI'
    print 'hardware interface. It should be imported into a python'
    print 'environment or another script using:'
    print 'from ftdi import *'
    sys.exit()
