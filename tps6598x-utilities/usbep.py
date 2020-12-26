#!/bin/env python
# -*- coding: cp1252 -*-
#==========================================================================
# (c) 2015 Texas Instruments
#--------------------------------------------------------------------------
# Project : Method and parameters for USB_EP intgerface 
# File    : usbep.py
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
BM_REQUEST_TYPE_OUT                 = 0x00
BM_REQUEST_TYPE_IN                  = 0x80

BM_REQUEST_TYPE_STANDARD            = 0x00
BM_REQUEST_TYPE_CLASS               = 0x20
BM_REQUEST_TYPE_VENDOR              = 0x40
BM_REQUEST_TYPE_MASK                = 0x60

BM_REQUEST_TYPE_RECIPIENT_DEVICE    = 0x00
BM_REQUEST_TYPE_RECIPIENT_INTERFACE = 0x01
BM_REQUEST_TYPE_RECIPIENT_ENDPOINT  = 0x02
BM_REQUEST_TYPE_RECIPIENT_OTHER     = 0x03
BM_REQUEST_TYPE_RECIPIENT_MASK      = 0x07

B_REQUEST_GET_STATUS                = 0x00
B_REQUEST_CLEAR_FEATURE             = 0x01
B_REQUEST_SET_FEATURE               = 0x03
B_REQUEST_SET_ADDRESS               = 0x05
B_REQUEST_GET_DESCRIPTOR            = 0x06
B_REQUEST_SET_DESCRIPTOR            = 0x07
B_REQUEST_GET_CONFIGURATION         = 0x08
B_REQUEST_SET_CONFIGURATION         = 0x09
B_REQUEST_GET_INTERFACE             = 0x0A
B_REQUEST_SYNCH_FRAME               = 0x0B

DESCRIPTOR_TYPE_DEVICE              = 0x01
DESCRIPTOR_TYPE_CONFIGURATION       = 0x02
DESCRIPTOR_TYPE_STRING              = 0x03
DESCRIPTOR_TYPE_INTERFACE           = 0x04
DESCRIPTOR_TYPE_ENDPOINT            = 0x05
DESCRIPTOR_TYPE_DEVICE_QUALIFIER    = 0x06
DESCRIPTOR_TYPE_OTHER_SPEED_CONFIG  = 0x07
DESCRIPTOR_TYPE_INTERFACE_POWER     = 0x08
DESCRIPTOR_TYPE_BOS                 = 0x0f
DESCRIPTOR_TYPE_DEVICE_CAPABILITY   = 0x10
DESCRIPTOR_TYPE_HID                 = 0x21
DESCRIPTOR_TYPE_REP                 = 0x22

# Command types in USB messages from PC to device
USB_WRITE_REG = 0xFD
USB_READ_REG = 0xFE

USB_MAX_TX_SIZE = 8

# Set to non-zero value to limit USB EP writes to USB_MAX_TX_SIZE bytes
USB_WRITE_SIZE_LIMITED = 1

# NOTE: the size limited feature must be used until we are able to send
# one setup packet followed by more than one data packet (of 8 bytes)!    

#==========================================================================
# HELPER FUNCTIONS
#==========================================================================

#def array_u08 (n):  return array('B', '\0'*n)


#==========================================================================
# IMPORTS
#==========================================================================

from ctypes import *
import sys
from config import *
from array import array, ArrayType
import usb.core
import usb.util

#==========================================================================
# GLOBAL CODE
#==========================================================================

    
#==========================================================================
# FUNCTIONS
#==========================================================================
def usbep_init():

    myException = Exception()
    # Open and initialize the USB_EP channel specified in config.py
           
    # Is the TI (vendor ID 0x0451) ACE device (product ID 0xACE1) connection to the PC?    
    dev = usb.core.find(idVendor=0x0451, idProduct=0xACE1)

    if dev is None:
        raise ValueError('No TI ACE devices found')
        print 'No TI ACE devices found'

    # Set the active configuration. With no arguments, the first
    # configuration will be the active one
    dev.set_configuration()

    # get an endpoint instance
    cfg = dev.get_active_configuration()
    intf = cfg[(0,0)]


    ep = usb.util.find_descriptor(
        intf,
        # match the first OUT endpoint
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_OUT)

    # Assert when ep is None
    assert ep is None
     
    return (dev)

    
def usbep_close():
    myException = Exception()

    # Close the USB_EP channel
        
    return
    

def usbep_read(handle, addr, length):    
    myException = Exception()
   
    # Read 'length' bytes from address 'addr' on the device
    
    # bmRequestType (1 byte) is BM_REQUEST_TYPE_VENDOR | BM_REQUEST_TYPE_OUT
    # bRequest (1 byte) is used for the command byte
    # wValue (2 bytes) is used for the read address
    # wIndex (2 bytes) is used for TBD 
    # wLength (2 bytes) is used number of bytes to read
    # optional timeout, in msec, is last field
    try:
        data_in = handle.ctrl_transfer((BM_REQUEST_TYPE_VENDOR | BM_REQUEST_TYPE_IN), USB_READ_REG, addr, 0, length, 2000)
    except:
        myException.message =  "Error in USB EP register read (register address: %d)" % addr
        raise myException

    # Return the data read from device
    return (len(data_in), data_in)
    

def usbep_write(handle, addr, data_out):    
    myException = Exception()

    transfer_size_to_do = len(data_out)
    transfer_so_far = 0


    # NOTE: the size limited feature must be used until we are able to send
    # one setup packet followed by more than one data packet (of 8 bytes)!    
    if (USB_WRITE_SIZE_LIMITED == 0):
        # Not limited to USB_MAX_TX_SIZE byte transfers, send all of the data in one call

        # Transfer the data to the device
        try:
            bytes_written = handle.ctrl_transfer((BM_REQUEST_TYPE_VENDOR | BM_REQUEST_TYPE_OUT), USB_WRITE_REG, addr, len(data_out), data_out, 2000)
        except:
            myException.message =  "Error in USB EP register write (register address: %d)" % addr
            raise myException

        return(bytes_written)            

    else:
        # Limited to USB_MAX_TX_SIZE byte transfers, break up data for sending

        transfer_size_to_do = len(data_out)
        transfer_so_far = 0

        # For the first transfer we put the total data length in the index field of the setup packet
        transfer_index_flag = transfer_size_to_do

        # Loop until all data is transfered
        while transfer_size_to_do > 0:
            
            # Calculate how many bytes to send for this transfer
            if (transfer_size_to_do <= USB_MAX_TX_SIZE):
                transfer_size_this_time = transfer_size_to_do
            else:
                transfer_size_this_time = USB_MAX_TX_SIZE

            # Create array to hold data for this transfer
            temp_data = array('B')
            for i in range(transfer_size_this_time):
                temp_data.append(0)

            # Copy a group of data from original buffer to the transfer buffer    
            for i in range(transfer_size_this_time):
                temp_data[i] = data_out[transfer_so_far + i]
                
            transfer_so_far = transfer_so_far + transfer_size_this_time
                
            # Transfer the data to the device
            try:
                bytes_written = handle.ctrl_transfer((BM_REQUEST_TYPE_VENDOR | BM_REQUEST_TYPE_OUT), USB_WRITE_REG, addr, transfer_index_flag, temp_data, 2000)
            except:
                myException.message =  "Error in USB EP register write (register address: %d)" % addr
                raise myException

            # For the rest of the transfer we put 0 in the index field of the setup packet
            transfer_index_flag = 0
            
            # Is there more data to transfer?
            transfer_size_to_do = transfer_size_to_do - transfer_size_this_time

        # Return the number of bytes transfered 
        return (transfer_so_far)

    
#==========================================================================
# main
#==========================================================================
if __name__ == "__main__":
    print 'This file is a helper file for adapting the scripts to the USB'
    print 'endpoint interface. It should be imported into a python'
    print 'environment or another script using:'
    print 'from usbep import *'
    sys.exit()
