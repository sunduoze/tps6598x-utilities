#!/bin/env python
# -*- coding: cp1252 -*-
#==========================================================================
# (c) 2015 Texas Instruments
#--------------------------------------------------------------------------
# Project : Method and parameters for hardware interface adaptations
# File    : aardvark_rw.py
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
# IMPORTS
#==========================================================================
import sys

from aardvark_py import *


#==========================================================================
# CONSTANTS
#==========================================================================
BUS_TIMEOUT = 150  # ms

#==========================================================================
# GLOBALS
#==========================================================================


#==========================================================================
# FUNCTIONS
#==========================================================================

def init_aardvark(port, bitrate, spibitrate):
    myException = Exception()
    handle = aa_open(port)
    if (handle <= 0):
        myException.message = "Unable to open Aardvark device on port %d\n" % port 
        myException.message += "Error code = %d" % handle
        raise myException
        
    # Ensure that the I2C subsystem is enabled
    aa_configure(handle,  AA_CONFIG_SPI_I2C)
            
    # Enable the I2C bus pullup resistors (2.2k resistors).
    # This command is only effective on v2.0 hardware or greater.
    # The pullup resistors on the v1.02 hardware are enabled by default.
    aa_i2c_pullup(handle, AA_I2C_PULLUP_BOTH)

    # Power the EEPROM using the Aardvark adapter's power supply.
    # This command is only effective on v2.0 hardware or greater.
    # The power pins on the v1.02 hardware are not enabled by default.
    aa_target_power(handle, AA_TARGET_POWER_BOTH)

    # Set the bitrate
    bitrate = aa_i2c_bitrate(handle, bitrate)
    print "I2C Bitrate set to %d kHz" % bitrate

    # Set the bus lock timeout
    bus_timeout = aa_i2c_bus_timeout(handle, BUS_TIMEOUT)
    print "I2C Bus lock timeout set to %d ms" % bus_timeout

    # configure spi 
    aa_spi_configure(handle, 0, 0, AA_SPI_BITORDER_MSB)

    # Set the bitrate to 20 MHz
    bitrate = aa_spi_bitrate(handle, spibitrate)
    print "SPI Bitrate set to %d kHz" % spibitrate

    return handle


#==========================================================================
# main
#==========================================================================


if __name__ == "__main__":
    print "This file contains Aardvark related helper functions and is not"
    print "intended to be run stand alone. To use, import constituent functions"
    print "into a script or python environment using:"
    print "from aardvark_rw import *"
    sys.exit()
        
