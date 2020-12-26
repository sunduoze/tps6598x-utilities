#!/bin/env python
#==========================================================================
# (c) 2004  Total Phase, Inc.
#--------------------------------------------------------------------------
# Project : Aardvark Sample Code
# File    : aaspi_eeprom.py
#--------------------------------------------------------------------------
# Perform simple read and write operations to an SPI EEPROM device.
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
import time

import config
from hw_interface import *
from hi_functions import *

handle = hw_interface(config.DEVICE_I2C_ADDR, config.HW_INTERFACE)

#==========================================================================
# CONSTANTS
#==========================================================================


#==========================================================================
# FUNCTIONS
#==========================================================================

#==========================================================================
# MAIN PROGRAM
#==========================================================================
if __name__ == "__main__":
    

    try :
        handle.hw_open(config.HW_INTERFACE, config.PORT, config.SPI_PORT, config.BITRATE, config.SPIBITRATE, config.DEVICE_I2C_ADDR)        
    except Exception as e :
        print e.message
        sys.exit()

    filename = sys.argv[1]

    try:
        f=open(filename, 'rb')
    except:
        print "Unable to open file '" + filename + "'"
        assert 1

    # erase 1M flash
    # 1M / 4K = 255
    for i in range(255) :
        handle.hw_spi_flash_erase(i * 0x1000, 1)
    
    print 'Programming image' 
    addr = 0x0
    
    # start programming at 0 offset
    count = 0
    while 1:
        filedata = array('B', [])
        # Read from the file
        for data in f.read(SPI_PAGE_SIZE):
            filedata.append(ord(data))

        length = len(filedata)
        if (length == 0):
            break

        #Truncate the array to the exact data size
        if (length < SPI_PAGE_SIZE):
            del filedata[length:]

        # Write the data to the bus
        handle.hw_spi_write(addr, filedata)

        addr += length

        count += 1
        if count == 256:
            print '64K block written'
            count = 0

    f.close()
    
    print 'Verifying'
    f=open(filename, 'rb')

    # start verifying at 0 offset
    count = 0
    addr = 0
    while 1:
        filedata = array('B', [])
        # Read from the file
        for data in f.read(SPI_PAGE_SIZE):
            filedata.append(ord(data))

        length = len(filedata)
        if (length == 0):
            break

        #Truncate the array to the exact data size
        if (length < SPI_PAGE_SIZE):
            del filedata[length:]

        # Write the data to the bus
        (count,readcomp) = handle.hw_spi_read(addr, len(filedata))

        compval = True
        for i in range (len(filedata)):
            if (filedata[i] != readcomp[i]):
                compval = False
                print 'Unmatched at addr 0x%x position %d, file value 0x%x, read value 0x%x' %(addr, i, filedata[i], readcomp[i])

        addr += length

    if compval == True :
        print 'Verification succeeded'

    # Close the device
    try :
        handle.hw_close()        
    except Exception as e :
        print e.message
        sys.exit()

    sys.exit()
