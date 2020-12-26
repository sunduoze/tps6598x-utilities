#!/bin/env python
# -*- coding: cp1252 -*-
#==========================================================================
# (c) 2015 Texas Instruments
#--------------------------------------------------------------------------
# Project : Method and parameters for hardware interface adaptations
# File    : hw_interface.py
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
import time
import threading

# Import the version number
from version import *

#==========================================================================
# GLOBALS
#==========================================================================

SPI_PAGE_SIZE = 256

#==========================================================================
# REGISTER CLASS DEFINITIONS
#==========================================================================

#==========================================================================
# FUNCTIONS
#==========================================================================

def hw_sleep_ms(time_msec):
    time.sleep(time_msec / 1000.0)


class hw_interface:
    def __init__(self, device_addr, interface):
        self.DEVICE_I2C_ADDR = device_addr
        self.handle = None
        self.spihandle = None
        self.HW_INTERFACE = interface
        self.activityLock = threading.Lock()
        self.openCloseActive = 0

        self.aardvarkInterfaceOpen = 0
        self.aardvarkInterfaceFailure = 0
        self.aardvarkInterfaceFailureMsg = ""

        self.ftdiInterfaceOpen = 0
        self.ftdiInterfaceFailure = 0
        self.ftdiInterfaceFailureMsg = ""

        self.usbepInterfaceOpen = 0
        self.usbepInterfaceFailure = 0
        self.usbepInterfaceFailureMsg = ""

        self.spiPageSize = SPI_PAGE_SIZE


    # allow redundant open and close calls for robustness in the GUI against
    #     dropped connections. This requires checking if a valid handle exists
    def hw_open(self, interface, port, spiport, bitrate, spibitrate, i2caddr):
        myException = Exception()

        if (self.handle != None) :
            print "Hardware channel is already open. Ignoring redundant open request\n"
            return

        if (self.openCloseActive == 1) :
            print "Hardware channel open or close in process by another thread. Ignoring redundant request\n"
            return


        # lock the thread incase multiple threads attempt to open or close simultaneously
        with self.activityLock :
            # recheck within protected space. Exterior check is to keep requests from queueing
            if (self.handle != None) :
                print "Hardware channel is already open. Ignoring redundant open request\n"
                return

            if (self.openCloseActive == 1) :
                print "Hardware channel open or close in process by another thread. Ignoring redundant request\n"
                return

            self.openCloseActive = 1
            
            
            # Initialize the I2C hardware interface based on settings in config.py
            print '\nTPS65982 Debug Tool Version %s\n' %TI_DEBUG_TOOL_VERSION

            self.HW_INTERFACE = interface
            
            if interface == config.AARDVARK:
                if (self.aardvarkInterfaceOpen == 0) :
                    try :
                        import aardvark_py
                        global aardvark_py
                        import aardvark_rw
                        global aardvark_rw
                        import aardvark_spi
                        global aardvark_spi
#                        globals()[aardvark_py] = __import__('aardvark_py') 
#                        globals()[aardvark_rw] = __import__('aardvark_rw') 
#                        globals()[aardvark_spi] = __import__('aardvark_spi')
                        self.aardvarkInterfaceOpen = 1
                    except Exception as e:
                        self.aardvarkInterfaceOpen = 0
                        self.aardvarkInterfaceFailure = 1
                        self.aardvarkInterfaceFailureMsg = " Aardvark Interface loading Error: %s" % e.message

                if (self.aardvarkInterfaceFailure == 0) :
                    try :        
                        self.handle = aardvark_rw.init_aardvark(port, bitrate, spibitrate)
                        self.spihandle = self.handle
                    except Exception as e:
                        self.openCloseActive = 0
                        self.handle = None
                        self.spihandle = None
                        raise e
                else :
                    self.openCloseActive = 0
                    myException.message = self.aardvarkInterfaceFailureMsg
                    raise myException

                
            elif interface == config.FTDI:
                if (self.ftdiInterfaceOpen == 0) :
                    try :
                        import ftdi
                        global ftdi
                        import ftdi_spi
                        global ftdi_spi
#                        globals()[ftdi] = __import__(ftdi)
#                        globals()[ftdi_spi] = __import__(ftdi_spi)
                        self.ftdiInterfaceOpen = 1
                    except Exception as e:
                        self.ftdiInterfaceOpen = 0
                        self.ftdiInterfaceFailure = 1
                        self.ftdiInterfaceFailureMsg = " FTDI Interface loading Error: %s" % e.message


                if (self.ftdiInterfaceFailure == 0) :
                    try:        
                        (self.handle, self.spihandle) = ftdi.ftdi_init(port, spiport, bitrate, spibitrate)
                    except Exception as e:
                        self.openCloseActive = 0
                        self.handle = None
                        self.spihandle = None
                        raise e
                else :
                    self.openCloseActive = 0
                    myException.message = self.ftdiInterfaceFailureMsg
                    raise myException
                    

            elif interface == config.USB_TO_ANY:
                self.openCloseActive = 0
                myException.message =  'USB_TO_ANY hardware interface hw_interface_init not implemented!' 
                raise myException
                
            elif interface == config.USB_EP:
                if (self.usbepInterfaceOpen == 0) :
                    try :
                        import usbep
                        global usbep
                        self.usbepInterfaceOpen = 1
                    except Exception as e:
                        self.usbepInterfaceOpen = 0
                        self.usbepInterfaceFailure = 1
                        self.usbepInterfaceFailureMsg = " USB_EP Interface loading Error: %s" % e.message

                if (self.usbepInterfaceFailure == 0) :
                    try :        
                        (self.handle) = usbep.usbep_init()
                    except Exception as e:
                        self.handle = None
                        self.spihandle = None
                        self.openCloseActive = 0
                        raise e
                else:
                    self.openCloseActive = 0
                    myException.message = self.usbepInterfaceFailureMsg
                    raise myException

            self.openCloseActive = 0


    def hw_close(self):
        status = 0
        message = "No Error"

        if (self.handle == None) :
            print "Hardware channel is already closed. Ignoring redundant close request\n"
            return

        if (self.openCloseActive == 1) :
            print "Hardware channel open or close in process by another thread. Ignoring redundant close request\n"
 
        # lock the thread incase multiple threads attempt to open, close read or write simultaneously
        with self.activityLock :
            # recheck status within protected space before acting
            # exterior check is to keep multiple redundant requests from queueing
            if (self.handle == None) :
                print "Hardware channel is already closed. Ignoring redundant close request\n"
                return

            if (self.openCloseActive == 1) :
                print "Hardware channel open or close in process by another thread. Ignoring redundant close request\n"

            self.openCloseActive = 1
            
            # Close the I2C hardware interface
            if self.HW_INTERFACE == config.AARDVARK:
                aardvark_py.aa_close(self.handle)
                status = 0
                message = ''
            elif self.HW_INTERFACE == config.FTDI:
                ftdi.ftdi_close(self.handle, self.spihandle)
                status = 0
                message = ''
            elif self.HW_INTERFACE == config.USB_TO_ANY:
                status = -1
                message = 'USB_TO_ANY hardware interface hw_interface_init not implemented\n'
                self.openCloseActive = 0
                return (status, message)
            elif self.HW_INTERFACE == config.USB_EP:
                usbep.usbep_close()
                status = 0
                message = ''
            else:
                status = -1
                message = 'Invalid hardware interface selected in config.py\n'
                self.openCloseActive = 0
                return (status, message)

            self.handle = None
            self.spihandle = None

            self.openCloseActive = 0

        return (status, message)

    def hw_set_i2c_addr(self, addr):
        with self.activityLock :
            self.DEVICE_I2C_ADDR = addr

        

    def hw_i2c_write(self, data_out):
        myException = Exception()

        with self.activityLock :
            if self.handle == None :
                myException.message = "hw_i2c_write failure: attempting to write to null handle\n" 
                raise myException

            # Call the appropriate I2C hardware interface to write data
            # (write with normal start and stop conditions)
            if self.HW_INTERFACE == config.AARDVARK:
                aardvark_py.aa_i2c_write (self.handle, self.DEVICE_I2C_ADDR, aardvark_py.AA_I2C_NO_FLAGS, data_out)
            elif self.HW_INTERFACE == config.FTDI:
                flags = ftdi.I2C_TRANSFER_OPTIONS_START_BIT|ftdi.I2C_TRANSFER_OPTIONS_STOP_BIT|ftdi.I2C_TRANSFER_OPTIONS_NACK_LAST_BYTE
                ftdi.ftdi_i2c_write (self.handle, self.DEVICE_I2C_ADDR, flags, data_out)
            elif self.HW_INTERFACE == config.USB_TO_ANY:
                myException.message = 'USB_TO_ANY hardware interface hw_interface_init not implemented\n'  
                raise myException
            elif self.HW_INTERFACE == config.USB_EP:
                myException.message = 'USB_EP interface hw_interface_init not implemented\n'  
                raise myException
            else:
                myException.message = 'Invalid hardware interface selected in config.py\n'   
                raise myException


    def hw_i2c_write_no_stop(self, data_out):
        myException = Exception()

        with self.activityLock :
            if self.handle == None :
                myException.message = "hw_i2c_write_no_stop failure: attempting to write to null handle\n" 
                raise myException

            # Call the appropriate I2C hardware interface to write data
            # (write with start condition but no stop condition)
            if self.HW_INTERFACE == config.AARDVARK:
                aardvark_py.aa_i2c_write(self.handle, self.DEVICE_I2C_ADDR, aardvark_py.AA_I2C_NO_STOP, data_out)
            elif self.HW_INTERFACE == config.FTDI:
                flags = ftdi.I2C_TRANSFER_OPTIONS_START_BIT
                ftdi.ftdi_i2c_write (self.handle, self.DEVICE_I2C_ADDR, flags, data_out)
            elif self.HW_INTERFACE == config.USB_TO_ANY:
                myException.message = 'USB_TO_ANY hardware interface hw_interface_init not implemented\n'  
                raise myException
            else:
                myException.message = 'Invalid hardware interface selected in config.py\n'   
                raise myException


    def hw_i2c_read(self, length):
        myException = Exception()

        with self.activityLock :
            if self.handle == None :
                myException.message = "hw_i2c_read failure: attempting to read from null handle\n" 
                raise myException

            # Call the appropriate I2C hardware interface to read data
            # (read with normal start and stop conditions)
            if self.HW_INTERFACE == config.AARDVARK:
                (count, data_in) = aardvark_py.aa_i2c_read(self.handle, self.DEVICE_I2C_ADDR, aardvark_py.AA_I2C_NO_FLAGS, length)
                if (count < 0):
                    print "error: %s" % aa_status_string(count)
                return(count, data_in)
            elif self.HW_INTERFACE == config.FTDI:
                flags = ftdi.I2C_TRANSFER_OPTIONS_START_BIT|ftdi.I2C_TRANSFER_OPTIONS_STOP_BIT|ftdi.I2C_TRANSFER_OPTIONS_NACK_LAST_BYTE
                (count, data_in) = ftdi.ftdi_i2c_read(self.handle, self.DEVICE_I2C_ADDR, flags, length)
                return(count, data_in)
            elif self.HW_INTERFACE == config.USB_TO_ANY:
                myException.message = 'USB_TO_ANY hardware interface hw_interface_init not implemented\n'  
                raise myException
            elif self.HW_INTERFACE == config.USB_EP:
                myException.message = 'hw_i2c_read USB_EP hardware interface hw_interface_init not implemented\n'  
                raise myException
            else:
                myException.message = 'Invalid hardware interface selected in config.py\n'   
                raise myException


    def hw_spi_read(self, addr, length):
        myException = Exception()

        with self.activityLock :

            if self.spihandle == None :
                myException.message = "hw_spi_read failure: attempting to read from null handle\n" 
                raise myException

            # Call the appropriate SPI hardware interface to read data
            # (read with normal start and stop conditions)
            if self.HW_INTERFACE == config.AARDVARK:
                (count, data_out) = aardvark_spi.aa_spi_readMemory(self.spihandle, addr, length)
                if (count < 0):
                    print "error: %s" % aa_status_string(count)
                return(count, data_out)
            elif self.HW_INTERFACE == config.FTDI:
                (count, data_out) = ftdi_spi.ftdi_spi_readMemory(self.spihandle, addr, length)
                return(count, data_out)
            elif self.HW_INTERFACE == config.USB_TO_ANY:
                myException.message = 'USB_TO_ANY hardware interface hw_interface_init not implemented\n'  
                raise myException
            else:
                myException.message = 'Invalid hardware interface selected in config.py\n'   
                raise myException

    def hw_spi_write(self, addr, data_in):
        myException = Exception()

        with self.activityLock :

            if self.spihandle == None :
                myException.message = "hw_spi_write failure: attempting to write to null handle\n" 
                raise myException

            # Call the appropriate SPI hardware interface to read data
            # (read with normal start and stop conditions)
            if self.HW_INTERFACE == config.AARDVARK:
                aardvark_spi.aa_spi_writeMemory(self.spihandle, addr, data_in)
                return 0
            elif self.HW_INTERFACE == config.FTDI:
                ftdi_spi.ftdi_spi_writeMemory(self.spihandle, addr, data_in)
                return 0
            elif self.HW_INTERFACE == config.USB_TO_ANY:
                myException.message = 'USB_TO_ANY hardware interface hw_interface_init not implemented\n'  
                raise myException
            else:
                myException.message = 'Invalid hardware interface selected in config.py\n'   
                raise myException


    def hw_spi_flash_erase(self, addr, numSectors):
        myException = Exception()

        with self.activityLock :
            if self.spihandle == None :
                myException.message = "hw_spi_flash_erase failure: attempting to erase to null handle\n" 
                raise myException

            # Call the appropriate SPI hardware interface to read data
            # (read with normal start and stop conditions)
            if self.HW_INTERFACE == config.AARDVARK:
                aardvark_spi.aa_flash_sector_erase_spi(self.spihandle, addr, numSectors)
                return 0
            elif self.HW_INTERFACE == config.FTDI:
                ftdi_spi.ftdi_flash_sector_erase_spi(self.spihandle, addr, numSectors)
                return 0
            elif self.HW_INTERFACE == config.USB_TO_ANY:
                myException.message = 'USB_TO_ANY hardware interface hw_interface_init not implemented\n'  
                raise myException
            elif self.HW_INTERFACE == config.USB_EP:
                myException.message = 'USB_EP hardware interface hw_interface_init not implemented\n'  
                raise myException
            else:
                myException.message = 'Invalid hardware interface selected in config.py\n'   
                raise myException

    def hw_usbep_read(self, addr, length):
        myException = Exception()

        with self.activityLock :


            if self.handle == None :
                myException.message = "hw_usbep_read failure: attempting to read from null handle\n" 
                raise myException

            # Call the appropriate USB end point hardware interface to read a register
            (count, data_in) = usbep.usbep_read(self.handle, addr, length)
            
            return (count, data_in)

    def hw_usbep_write(self, addr, data_out):
        myException = Exception()

        with self.activityLock :

            if self.handle == None :
                myException.message = "hw_usbep_write failure: attempting to read from null handle\n" 
                raise myException

            # Call the appropriate USB end point hardware interface to read a register
            bytes_written = usbep.usbep_write(self.handle, addr, data_out)
            
            return (bytes_written)


#==========================================================================
# main
#==========================================================================
if __name__ == "__main__":
    print 'This file is a helper file for adapting the scripts to different'
    print 'hardware interfaces. It should be imported into a python'
    print 'environment or another script using:'
    print 'from hw_interface import *'
    sys.exit()
