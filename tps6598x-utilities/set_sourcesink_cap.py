#!/bin/env python
# -*- coding: cp1252 -*-
#==========================================================================
# (c) 2015 Texas Instruments
#--------------------------------------------------------------------------
# Project : Example application utilizing TPS65982 Host Interface
# File    : set_sourcesink_cap.py
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
from hi_functions import *

from hw_interface import *

#==========================================================================
# GLOBALS
#==========================================================================

handle = hw_interface(config.DEVICE_I2C_ADDR, config.HW_INTERFACE)        

#==========================================================================
# Set Source Capabilities
#==========================================================================

def set_switches(handle):
    SYS_CONFIG_REG.read(handle)

    # configure switches to match source and sink configs
    SYS_CONFIG_REG.fieldByName('PP_5V0config').value = SwitchConfig_list.index('SwitchConfig_AS_OUT')
    SYS_CONFIG_REG.fieldByName('PP_HVconfig').value = SwitchConfig_list.index('SwitchConfig_AS_OUT')
    SYS_CONFIG_REG.fieldByName('PP_HVEconfig').value = SwitchConfig_list.index('SwitchConfig_AS_IN')

    SYS_CONFIG_REG.write(handle)


def set_source(handle):    
    TX_SOURCE_CAP.read(handle)

    TX_SOURCE_CAP.fieldByName('numPDOs').value = 2

    TX_SOURCE_CAP.fieldByName('Enable Mask PDO1').value = TX_Source_list.index('Always Enabled')
    TX_SOURCE_CAP.fieldByName('Enable Mask PDO2').value = TX_Source_list.index('Always Enabled')

    TX_SOURCE_CAP.fieldByName('PP Switch for PDO1').value = PP_Switch_PDOnum1_list.index('PP_5V (internal)')
    TX_SOURCE_CAP.fieldByName('PP Switch for PDO2').value = PP_Switch_PDO_list.index('PP_HV (Internal)')

    TX_SOURCE_CAP.fieldByName('PDO1: MaxCurrent or Power').value = int(round(( 3.0 ) / 0.01)) 
    TX_SOURCE_CAP.fieldByName('PDO1: Min Voltage or Power').value = int(round(( 5.0 ) / 0.05))
    TX_SOURCE_CAP.fieldByName('PDO1: Max Voltage').value = 0
    TX_SOURCE_CAP.fieldByName('PDO1: Supply Type').value = SupplyType_list.index('Fixed')

    TX_SOURCE_CAP.fieldByName('PDO2: MaxCurrent or Power').value = int(round(( 3.0 ) / 0.01)) 
    TX_SOURCE_CAP.fieldByName('PDO2: Min Voltage or Power').value = int(round(( 12.0 ) / 0.05))
    TX_SOURCE_CAP.fieldByName('PDO2: Max Voltage').value = 0
    TX_SOURCE_CAP.fieldByName('PDO2: Supply Type').value = SupplyType_list.index('Fixed')

    TX_SOURCE_CAP.write(handle)


def set_sink(handle):    
    TX_SINK_CAP.read(handle)

    TX_SINK_CAP.fieldByName('numPDOs').value = 2

    TX_SINK_CAP.fieldByName('PDO1: Operating Current or Power').value = int(round(( 0.9 ) / 0.01)) 
    TX_SINK_CAP.fieldByName('PDO1: MaxCurrent or Power').value = int(round(( 2.0 ) / 0.01)) 
    TX_SINK_CAP.fieldByName('PDO1: MinCurrent or Power').value = int(round(( 0.9 ) / 0.01))
    TX_SINK_CAP.fieldByName('PDO1: Ask For Max').value = 1
    TX_SINK_CAP.fieldByName('PDO1: Min Voltage or Power').value = int(round(( 5.0 ) / 0.05))
    TX_SINK_CAP.fieldByName('PDO1: Max Voltage').value = 0
    TX_SINK_CAP.fieldByName('PDO1: Supply Type').value = SupplyType_list.index('Fixed')

    TX_SINK_CAP.fieldByName('PDO2: MaxCurrent or Power').value = int(round(( 2.0 ) / 0.01)) 
    TX_SINK_CAP.fieldByName('PDO2: Min Voltage or Power').value = int(round(( 12.0 ) / 0.05))
    TX_SINK_CAP.fieldByName('PDO2: Max Voltage').value = int(round(( 20.0 ) / 0.05))
    TX_SINK_CAP.fieldByName('PDO2: Supply Type').value = SupplyType_list.index('Variable')

    TX_SINK_CAP.fieldByName('PDO2: Operating Current or Power').value = int(round(( 0.9 ) / 0.01)) 
    TX_SINK_CAP.fieldByName('PDO2: MinCurrent or Power').value = int(round(( 0.9 ) / 0.01))
    TX_SINK_CAP.fieldByName('PDO2: Ask For Max').value = 1


    TX_SINK_CAP.write(handle)


def set_autoneg(handle):    
    AUTONEGOTIATE_SINK.read(handle)

    AUTONEGOTIATE_SINK.fieldByName('Autonegotiate Enable').value = EnabledDisabled_list.index('Enabled')
    AUTONEGOTIATE_SINK.fieldByName('Use Battery PDO').value = TrueFalse_list.index('False')
    AUTONEGOTIATE_SINK.fieldByName('Use Variable PDO').value = TrueFalse_list.index('True')

    AUTONEGOTIATE_SINK.write(handle)


#==========================================================================
# main
#==========================================================================


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1][:2] == '0x':
            config.DEVICE_I2C_ADDR = int(sys.argv[1],16)
        else:
            config.DEVICE_I2C_ADDR = int(sys.argv[1])
            
    try :
        handle.hw_open(config.HW_INTERFACE, config.PORT, config.SPI_PORT, config.BITRATE, config.SPIBITRATE, config.DEVICE_I2C_ADDR)        
    except Exception as e :
        print e.message
        sys.exit()
        
    print '\nInitial source and sink capabilities:\n'
    TX_SOURCE_CAP.read(handle)
    TX_SOURCE_CAP.show()
    TX_SINK_CAP.read(handle)
    TX_SINK_CAP.show()

    set_source(handle)
    set_sink(handle)
    set_autoneg(handle)
    set_switches(handle)
    
    print '\nFinal source and sink capabilities:\n'
    TX_SOURCE_CAP.read(handle)
    TX_SOURCE_CAP.show()
    TX_SINK_CAP.read(handle)
    TX_SINK_CAP.show()

    print '\nIssuing PD hard reset to negotiate contract with new settings'
    print HRST(handle)

    # Close the device
    handle.hw_close()

    sys.exit()
    
