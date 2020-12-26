#!/bin/env python
# -*- coding: cp1252 -*-
#==========================================================================
# (c) 2015 Texas Instruments
#--------------------------------------------------------------------------
# Project : Example application utilizing TPS65982 Host Interface
# File    : read_registers.py
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
from register_definitions import *
from hi_functions import *

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
            config.DEVICE_I2C_ADDR = address
        else:
            address = int(sys.argv[1])
            config.DEVICE_I2C_ADDR = address

    try :
        handle.hw_open(config.HW_INTERFACE, config.PORT, config.SPI_PORT, config.BITRATE, config.SPIBITRATE, config.DEVICE_I2C_ADDR)        

            
        reg_mask = [ INT_EVENT1, INT_MASK1, INT_EVENT2, INT_MASK2,  PWR_SWITCH, FW_STATE_CONFIG, FW_STATE, FW_STATE_FOCUS ]
        # show contents of each register in human-readable format    
        for reg in REGS_LIST:
            if reg not in reg_mask:
                print ''
                reg.read(handle)
                reg.show()

        # col_width = max(len(channel.name) for channel in ADC.channels) + 3

        # print 'ADC'
        # for channel in ADC.channels :
        #     ADCreturn = ADCs(handle, channel)
        #     print '\t' + channel.name.ljust(col_width,' ') + " = " + ADCreturn

        # Example: manipulate a single field from a specific register
        #    STATUS_REG.fieldByName('PlugPresent').show()


        handle.hw_close()


    except Exception as e :
        print e
        sys.exit()


    sys.exit()
