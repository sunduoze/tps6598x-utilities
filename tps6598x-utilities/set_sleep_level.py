#!/bin/env python
# -*- coding: cp1252 -*-
#==========================================================================
# (c) 2015 Texas Instruments
#--------------------------------------------------------------------------
# Project : Example application utilizing TPS65982 Host Interface
# File    : set_sleep_level.py
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
        else:
            address = int(sys.argv[1])
            
    try :
        handle.hw_open(config.HW_INTERFACE, config.PORT, config.SPI_PORT, config.BITRATE, config.SPIBITRATE, config.DEVICE_I2C_ADDR)        
    except Exception as e :
        print e.message
        sys.exit()
        
    print('Initial Sleep Configuration Register Setting:')
    SYS_POWER.read(handle)
    SYS_POWER.show()
    SYS_POWER.fieldByName('System Power State').value = SysPower_list.index('S5')

    print('Setting Sleep Configuration Register to:')
    SYS_POWER.write(handle)
    SYS_POWER.show()

    print('Initial Sleep Mode settings:')
    SLEEP_CONFIG_REG.read(handle)
    SLEEP_CONFIG_REG.show()

    SLEEP_CONFIG_REG.fieldByName('Sleep mode enable').value = EnabledDisabled_list.index('Enabled')
#    SLEEP_CONFIG_REG.fieldByName('Sleep Wait time').value = sleep_list.index('Wait for at least 1000ms before entering sleep mode')
    SLEEP_CONFIG_REG.fieldByName('Sleep Wait time').value = sleep_list.index('Wait for at least 100ms before entering sleep mode')
#    SLEEP_CONFIG_REG.fieldByName('Sleep Wait time').value = sleep_list.index('Enter Sleep Mode When Possible')
    SLEEP_CONFIG_REG.fieldByName('SleepAt5V').value = TrueFalse_list.index('True')
    SLEEP_CONFIG_REG.fieldByName('Relax I2C Threshold').value = SysPower_list.index('S4')
    
    print('Setting Sleep Mode settings to:')
    SLEEP_CONFIG_REG.write(handle)
    SLEEP_CONFIG_REG.show()


    # Close the device
    handle.hw_close()

    sys.exit()
