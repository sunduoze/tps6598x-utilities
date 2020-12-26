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

from aardvark_py import *

SPI_PAGE_SIZE = 256

#==========================================================================
# CONSTANTS
#==========================================================================

FLASH_COMMAND_WRITE_ENABLE               = 0x06
FLASH_COMMAND_WRITE_ENABLE_STATUS        = 0x50
FLASH_COMMAND_WRITE_DISABLE              = 0x04
FLASH_COMMAND_READ_STATUS                = 0x05
FLASH_COMMAND_WRITE_STATUS               = 0x01
# READ_DATA requires SPI CLK < 33 MHz
FLASH_COMMAND_READ_DATA                  = 0x03
# FAST_READ supports 50 MHz clock
FLASH_COMMAND_FAST_READ                  = 0x0B    
FLASH_COMMAND_FAST_READ_DUAL_OUTPUT      = 0x3B
FLASH_COMMAND_FAST_READ_DUAL_IO          = 0xBB
FLASH_COMMAND_PAGE_PROGRAM               = 0x02
FLASH_COMMAND_SECTOR_ERASE               = 0x20
FLASH_COMMAND_BLOCK_ERASE_32K            = 0x52
FLASH_COMMAND_BLOCK_ERASE_64K            = 0xD8
FLASH_COMMAND_CHIP_ERASE                 = 0xC7
FLASH_COMMAND_POWER_DOWN                 = 0xB9
FLASH_COMMAND_RELEASE_POWER_DOWN         = 0xAB

#==========================================================================
# FUNCTIONS
#==========================================================================
def byteArray(n):
    strArray = bin(n)[2:].zfill(8*((len(bin(n)[2:])-1) / 8) + 8)

    ret = array('B')

    for i in range(len(strArray)/8):
        if i != 0:
            ret.append(int(strArray[-i*8-8:-i*8],2))
        else:
            ret.append(int(strArray[-8:],2))

    return ret

# w25q80 uses 8-bit command followed by 3-byte address
# data out is what you write
# data in is what you read
def spi_write(handle, cmd, addr, data_out, data_in):
    data_send = array('B', [ cmd ])

    revArray = byteArray(addr)
    for i in range(3-len(byteArray(addr))):
        revArray.append(0)

    for i in range(3):
        data_send.append(revArray[2-i])

    data_send.extend(data_out)

    data_receive = array('B', [0,0,0,0])
    data_receive.extend(data_in)

    return aa_spi_write(handle, data_send, data_receive)


def aa_spi_writeMemory (handle, addr, data_in):
    # Write to the SPI FLASH

    # Send write enable command
    data_out = array('B', [ FLASH_COMMAND_WRITE_ENABLE ])

    # aa_spi_write(handle, array_in, array_out)
    #    arrays may be replaced by an integer specifying length
    aa_spi_write(handle, data_out, array('B',[]))
    aa_sleep_ms(10)

    # Assemble write command and address
    data_out = array('B', [ 0 for i in range(SPI_PAGE_SIZE) ])

    # Assemble a page of data
    for i in range(min(SPI_PAGE_SIZE, len(data_in))):
        data_out[i] = data_in[i]

    # Truncate the array to the exact data size
    del data_out[i+1:]

    # Write the transaction
    spi_write(handle, FLASH_COMMAND_PAGE_PROGRAM, addr, data_out, data_in)
    aa_sleep_ms(10)

    # Wait until data page is written
    flash_block_busy(handle)

    if(len(data_in) > SPI_PAGE_SIZE):
        print 'SPI Write attempt of block size greater than page size of %d' %SPI_PAGE_SIZE 
        sys.exit()

    if(((addr + len(data_in) - 1) & 0xFFFFFF00) != (addr & 0xFFFFFF00)):
        print 'SPI Write attempt wraps past page boundary. This causes unpredicatble write behavior.'  
        sys.exit()


def aa_spi_readMemory (handle, addr, length):
    data_in = array('B', [ 0 for i in range(length) ])
    data_out = array('B', [ 0 for i in range(length) ])

    # Write length empty bytes to drive SPI clk for read
    (count, data_in) = spi_write(handle, FLASH_COMMAND_READ_DATA, addr, data_out, data_in)

    if (count < 0):
        print "error: %s\n" % aa_status_string(count)
        return
    elif (count != length+4):
        print "error: read %d bytes (expected %d)" % (count-4, length)

    return (count-4, data_in[4:])


def flash_block_busy(handle):
    data_out = array('B', [FLASH_COMMAND_READ_STATUS, 0])
    data_in = array('B', [0,0])
    (count, data_in) = aa_spi_write(handle, data_out, data_in)
        
    while(data_in[1] & 0x1):
        (count, data_in) = aa_spi_write(handle, data_out, data_in)

    # 0 = success
    return 0
    
def aa_flash_sector_erase_spi(handle, addr, numSector):
    address = addr & 0xFFFFF000

    # Erase Sectors
    # no data, so make dummy array of len zero
    dummy = array('B', [])
    for i in range(numSector):
        # have to write enable before each erase command
        data_out = array('B', [ FLASH_COMMAND_WRITE_ENABLE ])
        aa_spi_write(handle, data_out, array('B',[]))
        aa_sleep_ms(10)
        spi_write(handle, FLASH_COMMAND_SECTOR_ERASE, address, dummy, dummy)
        address += 0x1000
        flash_block_busy(handle)
        aa_sleep_ms(10)


#==========================================================================
# MAIN PROGRAM
#==========================================================================
if __name__ == "__main__":
    
    print 'This file is a helper file for programming SPI flash'
    print 'It should be imported into a python environment or another script'
    print 'using:'
    print 'from aardvark_spi import *'
    sys.exit()
