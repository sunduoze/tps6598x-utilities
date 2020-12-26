#!/bin/env python
# -*- coding: cp1252 -*-
#==========================================================================
# (c) 2015 Texas Instruments
#--------------------------------------------------------------------------
# Project : Methods and parameters for reading and writing hardware registers
# File    : device_rw.py
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
import config
from array import array, ArrayType

from hw_interface import *

#==========================================================================
# CONSTANTS
#==========================================================================
CC_NOT_ZERO = '!CMD'
CC_ZERO = 0


#==========================================================================
# FUNCTIONS
#==========================================================================
def write_reg(hw_handle, register, data_):
    # dummy read of MODE reg in case device is asleep
    try:
        read_reg_nodummy(hw_handle,0x03,5)
    except Exception as e :
        pass

    # now do the write
    return write_reg_nodummy(hw_handle, register, data_)

def write_reg_nodummy(hw_handle, register, data_):

    #(0x09, u08[] data_out)
    # Write to the ACE I2C addr register

    (data_, length) = isinstance(data_, ArrayType) and (data_, len(data_)) or (data_[0], min(len(data_[0]), int(data_[1])))
    #print "length %d" %length
    if data_.typecode != 'B':
        hw_handle.hw_interface_close()
        raise TypeError("type for 'data_out' must be array('B')")


    if (config.HW_INTERFACE == config.USB_EP):
        # Handle communications for USB end point

        # Writes up to PAGE_SIZE + register and length
        data_out = array('B', [ 0 for i in range(length) ])

        # Build the data portion of the message
        i = 0
        while 1:
            data_out[i] = data_[i] & 0xff
            i = i+1

            if i == (length): break

        bytes_written = hw_handle.hw_usbep_write(register, data_out)
        hw_sleep_ms(5)
 

    else:
        # Writes up to PAGE_SIZE + register and length
        data_out = array('B', [ 0 for i in range(2+length) ])

        # Fill the packet with data
        data_out[0] = register & 0xff
        data_out[1] = length & 0xff
        
        # Assemble a page of data
        i = 2
        while 1:
            data_out[i] = data_[i-2] & 0xff
            i = i+1

            if i == (length+2): break
            
        # Truncate the array to the exact data size
        #del data_out[i:]

        # Write the address and data
        hw_handle.hw_i2c_write(data_out)
        hw_sleep_ms(5)



def write_reg_4cc(hw_handle, register, data_str):
    # i.e. write_reg_4cc(handle, 0x08, 'FLrr')
    data_out = array('B')
    data_out.fromstring(data_str)
    write_reg (hw_handle, register, data_out)


def read_reg(hw_handle, register, length):
    # dummy read of MODE reg in case device is asleep
    try:
        read_reg_nodummy(hw_handle,0x03,5)
    except Exception as e :
        pass

    # now do the real read
    return read_reg_nodummy(hw_handle, register, length)


def read_reg_nodummy(hw_handle, register, length):

    myException = Exception()

    if (hw_handle.HW_INTERFACE == config.USB_EP):
        # Handle communications for USB end point

        (count, data_in) = hw_handle.hw_usbep_read(register, length)
        hw_sleep_ms(10)
 
    else:
    # Handle communications for other hardware interfaces

        # Write the address
        hw_handle.hw_i2c_write_no_stop(array('B', [register & 0xff]))
        hw_sleep_ms(10)

        # hw_i2c_read returns data_in[0] = count, followed by n-1 data bytes
        #   This function adds 1 to length to add the count and then removes the count from the array
        (count, data_in) = hw_handle.hw_i2c_read(length)

    # Validate length of data read and return it to caller
    if (count < 0):
        myException.message =  "Device read error: %d" %count
        raise myException
        return (count, array('B'))
    elif (count == 0):
        myException.message = "error: no bytes read\n"
        myException.message += "device may be unpowered or I2C address may be incorrect\n"
        raise myException
        return (count, array('B'))
    elif (count != length):
        myException.message = "error: read %d bytes (expected %d)" % (count-1, length)
        raise myException
        return (count, data_in)
    else:
        #print "read %d bytes" % count
        del data_in[0]  #remove first element from the array (count)
    return (count,data_in)

def read_reg_4cc(hw_handle, register):
    return read_reg(hw_handle, register, 5)



#==========================================================================
# main
#==========================================================================


if __name__ == "__main__":
    print "This file contains helper functions related to reading and writing"
    print "device registers and is not intended to be run stand alone. To use,"
    print "import constituent functions into a script or python environment using:"
    print "from device_rw import *"
    sys.exit()
        
