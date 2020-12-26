#!/bin/env python

#==========================================================================
# IMPORTS
#==========================================================================
import sys
import time

from ftdi import *

#==========================================================================
# CONSTANTS
#==========================================================================
SPI_PAGE_SIZE = 256

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



f_spi_write = ftdi.SPI_Write
f_spi_write.argtypes = [c_uint, POINTER(c_ubyte), c_uint, POINTER(c_uint), c_uint]
f_spi_write.restype = c_uint

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

def fsw_basic(handle, data_out):
    sizeTransferred = c_uint(0)
    transferOptions = c_uint(SPI_TRANSFER_OPTIONS_SIZE_IN_BYTES | SPI_TRANSFER_OPTIONS_CHIPSELECT_ENABLE | SPI_TRANSFER_OPTIONS_CHIPSELECT_DISABLE)

    # Get the address of the data array to transmit
    temp_ptr, _ = data_out.buffer_info()
    data_out_p = cast(temp_ptr, POINTER(c_ubyte))

    return f_spi_write(handle, data_out_p, len(data_out), byref(sizeTransferred), transferOptions)
    

# w25q80 uses 8-bit command followed by 3-byte address
# data out is what you write
# data in is what you read
def ftdi_spi_write(handle, cmd, addr, data_out, data_in):
    data_send = array('B', [ cmd ])

    revArray = byteArray(addr)
    for i in range(3-len(byteArray(addr))):
        revArray.append(0)

    for i in range(3):
        data_send.append(revArray[2-i])

    data_send.extend(data_out)

    data_receive = array('B', [0,0,0,0])
    data_receive.extend(data_in)

    sizeTransferred = c_uint(0)
    transferOptions = c_uint(SPI_TRANSFER_OPTIONS_SIZE_IN_BYTES | SPI_TRANSFER_OPTIONS_CHIPSELECT_ENABLE | SPI_TRANSFER_OPTIONS_CHIPSELECT_DISABLE)

    # Get the address of the data array to transmit
    temp_ptr, _ = data_send.buffer_info()
    data_send_p = cast(temp_ptr, POINTER(c_ubyte))


    return f_spi_write(handle, data_send_p, len(data_send), byref(sizeTransferred), transferOptions)


def ftdi_spi_writeMemory (handle, addr, data_in):
    # Write to the SPI FLASH

    # Send write enable command
    data_out = array('B', [ FLASH_COMMAND_WRITE_ENABLE ])
    fsw_basic(handle, data_out)

    # Assemble write command and address
    data_out = array('B', [ 0 for i in range(SPI_PAGE_SIZE) ])

    # Assemble a page of data
    for i in range(min(SPI_PAGE_SIZE, len(data_in))):
        data_out[i] = data_in[i]

    # Truncate the array to the exact data size
    del data_out[i+1:]

    # Write the transaction
    ftdi_spi_write(handle, FLASH_COMMAND_PAGE_PROGRAM, addr, data_out, data_in)
#    aa_sleep_ms(10)

    # Wait until data page is written
    ftdi_flash_block_busy(handle)

    if(len(data_in) > SPI_PAGE_SIZE):
        print 'SPI Write attempt of block size greater than page size of %d' %SPI_PAGE_SIZE 
        sys.exit()

    if(((addr + len(data_in) - 1) & 0xFFFFFF00) != (addr & 0xFFFFFF00)):
        print 'SPI Write attempt wraps past page boundary. This causes unpredicatble write behavior.'  
        sys.exit()


def ftdi_spi_readMemory (handle, addr, length):
    data_in = array('B', [ 0 for i in range(length + 4) ])
    data_out = array('B', [ 0 for i in range(length + 4) ])

    f_spi_read_write = ftdi.SPI_ReadWrite
    f_spi_read_write.argtypes = [c_uint, POINTER(c_ubyte), POINTER(c_ubyte), c_uint, POINTER(c_uint), c_uint]
    f_spi_read_write.restype = c_uint

    sizeTransferred = c_uint(0)
    transferOptions = c_uint(SPI_TRANSFER_OPTIONS_SIZE_IN_BYTES | SPI_TRANSFER_OPTIONS_CHIPSELECT_ENABLE | SPI_TRANSFER_OPTIONS_CHIPSELECT_DISABLE)

    revArray = byteArray(addr)
    for i in range(3-len(byteArray(addr))):
        revArray.append(0)

    data_out[0] = FLASH_COMMAND_READ_DATA
    data_out[1] = revArray[2]
    data_out[2] = revArray[1]
    data_out[3] = revArray[0]

    # Get the address of the data array to transmit
    temp_ptr, _ = data_in.buffer_info()
    data_in_p = cast(temp_ptr, POINTER(c_ubyte))

    temp_ptr, _ = data_out.buffer_info()
    data_out_p = cast(temp_ptr, POINTER(c_ubyte))

    f_spi_read_write(handle, data_in_p, data_out_p, len(data_in), byref(sizeTransferred), transferOptions)

    if (sizeTransferred.value != length + 4):
        print "error: read %d bytes (expected %d)" % (sizeTransferred.value, length)

    return (sizeTransferred.value - 4, data_in[4:])


def ftdi_flash_block_busy(handle):
    data_in = array('B', [0, 0])
    data_out = array('B', [FLASH_COMMAND_READ_STATUS, 0])

    f_spi_read_write = ftdi.SPI_ReadWrite
    f_spi_read_write.argtypes = [c_uint, POINTER(c_ubyte), POINTER(c_ubyte), c_uint, POINTER(c_uint), c_uint]
    f_spi_read_write.restype = c_uint

    sizeTransferred = c_uint(0)
    transferOptions = c_uint(SPI_TRANSFER_OPTIONS_SIZE_IN_BYTES | SPI_TRANSFER_OPTIONS_CHIPSELECT_ENABLE | SPI_TRANSFER_OPTIONS_CHIPSELECT_DISABLE)

    # Get the address of the data array to transmit
    temp_ptr, _ = data_in.buffer_info()
    data_in_p = cast(temp_ptr, POINTER(c_ubyte))

    temp_ptr, _ = data_out.buffer_info()
    data_out_p = cast(temp_ptr, POINTER(c_ubyte))

    f_spi_read_write(handle, data_in_p, data_out_p, len(data_in), byref(sizeTransferred), transferOptions)

    while(data_in[1] & 0x1):
        f_spi_read_write(handle, data_in_p, data_out_p, len(data_in), byref(sizeTransferred), transferOptions)

    # 0 = success
    return 0
    
def ftdi_flash_sector_erase_spi(handle, addr, numSector):
    address = addr & 0xFFFFF000

    # Erase Sectors
    # no data, so make dummy array of len zero
    dummy = array('B', [])
    for i in range(numSector):
        # have to write enable before each erase command
        fsw_basic(handle, array('B', [FLASH_COMMAND_WRITE_ENABLE]))
        ftdi_spi_write(handle, FLASH_COMMAND_SECTOR_ERASE, address, dummy, dummy)
        address += 0x1000
        ftdi_flash_block_busy(handle)

#==========================================================================
# MAIN PROGRAM
#==========================================================================
if __name__ == "__main__":
    
    print 'This file is a helper file for programming SPI flash'
    print 'It should be imported into a python environment or another script'
    print 'using:'
    print 'from aardvark_spi import *'
    sys.exit()
