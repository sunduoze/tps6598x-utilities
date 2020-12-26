#!/bin/env python
# -*- coding: cp1252 -*-
#==========================================================================
# (c) 2015 Texas Instruments
#--------------------------------------------------------------------------
# Project : Example application utilizing TPS65982 Host Interface
# File    : pd_trace.py
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

from register_definitions import *

from hw_interface import *


#==========================================================================
# GLOBALS
#==========================================================================

handle = hw_interface(config.DEVICE_I2C_ADDR, config.HW_INTERFACE)        

#==========================================================================
# main
#==========================================================================


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1][:2] == '0x':
            address = int(sys.argv[1],16)
        else:
            address = int(sys.argv[1])

    try :
        handle.hw_open(config.HW_INTERFACE, config.PORT, config.SPI_PORT, config.BITRATE, config.SPIBITRATE, config.DEVICE_I2C_ADDR)        
    except Exception as e :
        print e.message
        sys.exit()

    FW_STATE_CONFIG.read(handle)

#    FW_STATE_CONFIG.fieldByName('Module for Focus Trace Capture (register 0x7D)').value = modules_list.index('PD Module')
    FW_STATE_CONFIG.fieldByName('Module for Focus Trace Capture (register 0x7D)').value = modules_list.index('PD Module')

    FW_STATE_CONFIG.write(handle)

    # initialize buffer
    for entry in FW_STATE_FOCUS.fields:
        entry.value = 0xFF

    FW_STATE_FOCUS.write(handle)

    print 'PD module configured and initialized.'
    raw_input('Press enter to capture and display PD trace.')
    # os.system('pause')

    FW_STATE_FOCUS.read(handle)
    
    FW_STATE_FOCUS.show()




    # Close the device
    handle.hw_close()

    sys.exit()
