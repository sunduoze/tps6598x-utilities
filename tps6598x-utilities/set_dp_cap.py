#!/bin/env python
# -*- coding: cp1252 -*-
#==========================================================================
# (c) 2015 Texas Instruments
#--------------------------------------------------------------------------
# Project : Example application utilizing TPS65982 Host Interface
# File    : set_dp_cap.py
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

# DP pin configuration settings
Ashift = 0
Bshift = 1
Cshift = 2
Dshift = 3
Eshift = 4
Fshift = 5

def set_dp_dfp(handle):
    DP_CAPABILITIES_REG.read(handle)

    DP_CAPABILITIES_REG.fieldByName('Enable DP SID').value = EnabledDisabled_list.index('Enabled')
    DP_CAPABILITIES_REG.fieldByName('Enable DP Mode').value = EnabledDisabled_list.index('Enabled')
    DP_CAPABILITIES_REG.fieldByName('DP Port Capability').value = DPCap_list.index('DFP_D Capable Device')
    DP_CAPABILITIES_REG.fieldByName('Supports DP v1.3 signalling').value = TrueFalse_list.index('True')
    DP_CAPABILITIES_REG.fieldByName('Supports USB Gen2 signalling').value = TrueFalse_list.index('True')
    DP_CAPABILITIES_REG.fieldByName('Receptacle Indication').value = Receptacle_list.index('Receptacle')
    DP_CAPABILITIES_REG.fieldByName('USB 2.0 Signalling Not Used').value = TrueFalse_list.index('True')
    DP_CAPABILITIES_REG.fieldByName('DP DFP_D Pin Configuration Support').value = (1 << Cshift) | (1 << Dshift) | (1 << Eshift)
    DP_CAPABILITIES_REG.fieldByName('DP UFP_D Pin Configuration Support').value = 0
    DP_CAPABILITIES_REG.fieldByName('Multifunction Preferred').value = TrueFalse_list.index('True')
    DP_CAPABILITIES_REG.fieldByName('MuxSwap').value = TrueFalse_list.index('True')
#   best to leave message index unchanged
#    DP_CAPABILITIES_REG.fieldByName('messageIndex').value =

    DP_CAPABILITIES_REG.write(handle)

def set_dp_ufp(handle):
    DP_CAPABILITIES_REG.read(handle)

    DP_CAPABILITIES_REG.fieldByName('Enable DP SID').value = EnabledDisabled_list.index('Enabled')
    DP_CAPABILITIES_REG.fieldByName('Enable DP Mode').value = EnabledDisabled_list.index('Enabled')
    DP_CAPABILITIES_REG.fieldByName('DP Port Capability').value = DPCap_list.index('UFP_D Capable Device')
    DP_CAPABILITIES_REG.fieldByName('Supports DP v1.3 signalling').value = TrueFalse_list.index('True')
    DP_CAPABILITIES_REG.fieldByName('Supports USB Gen2 signalling').value = TrueFalse_list.index('True')
    DP_CAPABILITIES_REG.fieldByName('Receptacle Indication').value = Receptacle_list.index('Receptacle')
    DP_CAPABILITIES_REG.fieldByName('USB 2.0 Signalling Not Used').value = TrueFalse_list.index('True')
    DP_CAPABILITIES_REG.fieldByName('DP DFP_D Pin Configuration Support').value = 0
    DP_CAPABILITIES_REG.fieldByName('DP UFP_D Pin Configuration Support').value = (1 << Cshift) | (1 << Dshift) 
    DP_CAPABILITIES_REG.fieldByName('Multifunction Preferred').value = TrueFalse_list.index('True')
    DP_CAPABILITIES_REG.fieldByName('MuxSwap').value = TrueFalse_list.index('True')
#   best to leave message index unchanged
#    DP_CAPABILITIES_REG.fieldByName('messageIndex').value =

    DP_CAPABILITIES_REG.write(handle)


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
        
    print '\nInitial DP capabilities:\n'
    DP_CAPABILITIES_REG.read(handle)
    DP_CAPABILITIES_REG.show()

    input_var = input('Configure as DFP_D or UFP_D? enter 1 (= DFP_D) or 2 (= UFP_D) > ')


    # change configuration
    if input_var == 1:
        set_dp_dfp(handle)
    else:
        set_dp_ufp(handle)
        

    print 'Issuing PD hard reset to renegotiate DP with new settings'
    print HRST(handle)
    
    print '\nFinal DP capabilities:\n'
    DP_CAPABILITIES_REG.read(handle)
    DP_CAPABILITIES_REG.show()


    # Close the device
    handle.hw_close()

    sys.exit()
