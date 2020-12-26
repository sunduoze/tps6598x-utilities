#!/bin/env python
#==========================================================================
# (c) 2015 TI
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

from hi_functions import *
from intelhex import IntelHex
import struct

from hw_interface import *

#==========================================================================
# CONSTANTS
#==========================================================================
PAGE_SIZE = 64

handle = hw_interface(config.DEVICE_I2C_ADDR, config.HW_INTERFACE)


# header values
Ace_ID_Value            = 0xACE00001



#==========================================================================
# Functions
#==========================================================================


# Function to bit-reverse a byte array in place
# '{:08b}'.format(x)converts a byte to a bit string, 8 bits, leading 0s
# slice operator bitstr[start:end:step] reverses the bit string when step -1
# int(bitstr,2) converts bit string (base 2) back to an integer
# write back to the same array
def bit_rev(data):
    index = 0
    for x in data:
        data[index] = int('{:08b}'.format(x)[::-1], 2)
        index +=1
    return data

# Need to zero-fill 32-bit arrays when writing to flash, which is initialized to 0xFFFFFFFF
def four_byte_array(n):
    retval = byteArray(n)

    for i in range(4-len(retval)):
        retval.append(0)

    return retval

#==========================================================================
# MAIN PROGRAM
#==========================================================================
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print "usage: flash_update_region_1 <tps65982xxx_low_region.bin> [I2C address]"
        sys.exit()

    filename = sys.argv[1]

    if len(sys.argv) > 2:
        if sys.argv[2][:2] == '0x':
            config.DEVICE_I2C_ADDR = int(sys.argv[2],16)
        else:
            config.DEVICE_I2C_ADDR = int(sys.argv[2])

    # Open the device
    try :
        handle.hw_open(config.HW_INTERFACE, config.PORT, config.SPI_PORT, config.BITRATE, config.SPIBITRATE, config.DEVICE_I2C_ADDR)        
    except Exception as e :
        print e.message
        sys.exit()


    # Read region 1 pointer
    rp1 = FLrr(handle, 1)
    print 'Region 1 pointer currently set to address 0x%x' %rp1
    print 'Enter new value (dec or hex with 0x) or press return to keep:'
    rpin = raw_input('> ')
    if rpin != '' :
        if rpin[:2] == '0x':
            rp1 = int(rpin,16)
        else:
            rp1 = int(rpin)

    while (rp1 < 0x2000) :
        print 'Region 1 address must be greater than or equal to 0x2000' 
        print 'Enter new value (dec or hex with 0x):'
        rpin = raw_input('> ')
        if rpin != '' :
            if rpin[:2] == '0x':
                rp1 = int(rpin,16)
            else:
                rp1 = int(rpin)


    # erase region 1
    # Max image size is 64K plus a 4K header = 17 sectors
    FLem(handle, rp1, 17)

    print 'Programming region 1 image at offset 0x%x' %rp1
    FLad(handle, rp1)

    count = 0

    # we use a second instance of file in raw mode to write into flash
    try:
        f=open(filename, 'rb')
    except:
        print "Unable to open file '" + filename + "'"
        sys.exit()

    # unroll first loop iteration 
    # Read from the file
    filedata = f.read(PAGE_SIZE)

    # Write the data to the bus
    data1 = array('B', filedata)
    
    length = len(data1)
    if (length < 4):
        print """Input file is not a valid low-region file"""
        print """A low region files is an application binary (max 64k) with a prepended 4k boot header."""
        sys.exit()        

    if (((data1[3] << 24) | (data1[2] << 16) | (data1[1] << 8) | data1[0]) != Ace_ID_Value) :
        print """Input file is not a valid low-region file"""
        print """A low region files is an application binary (max 64k) with a prepended 4k boot header."""
        sys.exit()        


    #Truncate the array to the exact data size
    if (length < PAGE_SIZE):
        del data1[length:]
                
    FLwd(handle, data1)        

    while 1:
        # Read from the file
        filedata = f.read(PAGE_SIZE)
        length = len(filedata)
        if (length == 0):
            break

        # Write the data to the bus
        data1 = array('B', filedata)

        #Truncate the array to the exact data size
        if (length < PAGE_SIZE):
            del data1[length:]
                    
        FLwd(handle, data1)        
        count += 1
        if count == 64:
            print '4K block written'
            count = 0

    f.close()

    print 'Region 1 write complete'
    
    # Erase region 1 data record
    FLem(handle, 0x1000, 1)

    # write in the region pointers
    rpblock = array('B')

    for i in range(64):
        rpblock.append(0xFF)

    rpoffset = rp1 - 0x2000

    rpblock[0] = 0x00
    rpblock[1] = 0x20
    rpblock[2] = 0x00
    rpblock[3] = 0x00

    FLad(handle, 0x1000)
    FLwd(handle, rpblock)        

    rpblock[0] = 0xFF
    rpblock[1] = 0xFF
    rpblock[2] = 0xFF
    rpblock[3] = 0xFF

    rpblock[60] = rpoffset & 0xFF
    rpblock[61] = (rpoffset >> 8) & 0xFF
    rpblock[62] = (rpoffset >> 16) & 0xFF
    rpblock[63] = (rpoffset >> 24) & 0xFF

    FLad(handle, 0x2000 - 0x40)
    FLwd(handle, rpblock)

    # verify boot sequence using FLrr and FLvy
    rp1 = FLrr(handle, 1)
    failure = FLvy(handle, rp1)

    if failure != 0:
        print 'Verification of region 1 FAILED'
    else:
        print 'Verification of region 1 SUCCEEDED'
          
    # Close the device
    try :
        handle.hw_close()        
    except Exception as e :
        print e.message
        sys.exit()

    sys.exit()
