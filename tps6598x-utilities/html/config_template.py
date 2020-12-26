#!/bin/env python
# -*- coding: cp1252 -*-
#==========================================================================
# (c) 2015 Texas Instruments
#--------------------------------------------------------------------------
# Project : Configuration parameters for hardware interface adaptations
# File    : config.py
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

# Generate the FTDI driver warning in the GUI
WARNING = **WRNG**

# Constants for various I2C hardware interfaces
AARDVARK = 0
FTDI = 1
USB_TO_ANY = 3
USB_EP = 4

HW_INT_DICT = { 'Aardvark' : AARDVARK, 'FTDI' : FTDI, 'USB EP' : USB_EP }

# Select hardware interface to use
HW_INTERFACE = **HW_INT**

# TPS65982 I2C address
DEVICE_I2C_ADDR = **IIC_ADDR**

BITRATE_DICT = { '400 Kbps' : 400, '100 Kbps' : 100 }

# I2C data rate (KHz)
BITRATE = **BR**

SPIBITRATE_DICT = { '125 Kbps' : 125, '250 Kbps' : 250, '500 Kbps' : 500, '1 Mbps' : 1000, '2 Mbps' : 2000, '4 Mbps' : 4000, '8 Mbps' : 8000 }

# SPI data rate (KHz)
SPIBITRATE = **SBR**

PORT_DICT = { 'Port 0' : 0, 'Port 1' : 1 }

# For Aardvark: defines which Aardvark dongle is being used
# For FTDI: defines which port of FTDI device to use
PORT = **PRT**

SPI_PORT = **SPIPRT**


#==========================================================================
# IMPORTS
#==========================================================================
import sys


#==========================================================================
# main
#==========================================================================
if __name__ == "__main__":
    print 'This file is a helper file for adapting the scripts to different'
    print 'hardware interfaces. It should be imported into a python'
    print 'environment or another script using:'
    print 'from config import *'
    sys.exit()
