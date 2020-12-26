#!/bin/env python
# -*- coding: cp1252 -*-
#==========================================================================
# (c) 2015 Texas Instruments
#--------------------------------------------------------------------------
# Project : Example application utilizing TPS65982 Host Interface
# File    : intrusive_PD_example.py
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

handle = None
spi_handle = None


def poll_interrupt(handle, int_name) :
    print 'Polling interrupt: %s' %int_name
    INT_EVENT1.read(handle)
    count = 0
    while INT_EVENT1.fieldByName(int_name).value != 1 :
        INT_EVENT1.read(handle)
        count = count +1
        if count == 1000 :
            print 'Polling interrupt: %s' %int_name
            count = 0
    clear_interrupt(handle, int_name)

def enable_interrupt(handle, int_name) :
    INT_MASK1.read(handle)
    INT_MASK1.fieldByName(int_name).value = 1
    INT_MASK1.write(handle)

def clear_interrupt(handle, int_name) :
    for field in INT_CLEAR1.fields :
        field.value = 0
    INT_CLEAR1.fieldByName(int_name).value = 1
    INT_CLEAR1.write(handle)
            
def negotiate_Source(handle):
    print('Sending Source Capabilities:')
    TX_SOURCE_CAP.read(handle)
    TX_SOURCE_CAP.show()

    enable_interrupt(handle, 'RDO Received from Sink') 
    clear_interrupt(handle, 'RDO Received from Sink') 

    print 'Issuing SSrC'
    print SSrC(handle)

    poll_interrupt(handle, 'RDO Received from Sink')

    print('Received Sink Request RDO:')
    SINK_REQUEST_RDO.read(handle)
    SINK_REQUEST_RDO.show()

    # This example automatically accepts the RDO
    # Logic could be entered here to evaluate and
    #    conditionally issue RRDO (Reject RDO)
    print 'Issuing Accept RDO'
    print ARDO(handle)

    print 'Issuing SSrC (send source capabilities) to generate new RDO request'
    print SSrC(handle)
        
    print 'Negotiated the following contract:'

    ACTIVE_CONTRACT_PDO.read(handle)
    ACTIVE_CONTRACT_PDO.show()

def buildRDO(maxCurrentorPower, OperatingCurrentOrPower, NoUSBSuspend, USBCommCapable, CapabilityMismatch, GiveBackFlag, ObjectPosition) :
    return (maxCurrentorPower & 0x3FF) | (OperatingCurrentOrPower & 0x3FF) << 10 | (NoUSBSuspend & 0x1) << 24 | (USBCommCapable & 0x1) << 25 | (CapabilityMismatch & 0x1) << 26 | (GiveBackFlag & 0x1) << 27 | (ObjectPosition & 0x7) << 28 

def negotiate_Sink(handle) :
    enable_interrupt(handle, 'Source Capabilities Message Ready') 
    clear_interrupt(handle, 'Source Capabilities Message Ready') 

    print 'Sending Get Source Capabilities request'
    print GSrC(handle)

    poll_interrupt(handle, 'Source Capabilities Message Ready')

    print 'Received source capabilities:'
    time.sleep(1)
    

    RX_SOURCE_CAP.read(handle)
    RX_SOURCE_CAP.show()
    
    # This example always takes the first source capabilities PDO
    # Logic could be inserted here to make a more intelligent choice

    maxCurrentorPower = RX_SOURCE_CAP.fieldByName('PDO1: MaxCurrent or Power').value 
    OperatingCurrentOrPower = RX_SOURCE_CAP.fieldByName('PDO1: MaxCurrent or Power').value
    NoUSBSuspend = 1
    USBCommCapable = 1
    CapabilityMismatch = 0
    GiveBackFlag = 0
    ObjectPosition = 1
    
    sendRDO = buildRDO(maxCurrentorPower, OperatingCurrentOrPower, NoUSBSuspend, USBCommCapable, CapabilityMismatch, GiveBackFlag, ObjectPosition)

    print 'Sending Request Data Object'
    print SRDO(handle, sendRDO)

    print 'Negotiated PDO contract'
    ACTIVE_CONTRACT_PDO.read(handle)
    ACTIVE_CONTRACT_PDO.show()
    ACTIVE_CONTRACT_RDO.read(handle)
    ACTIVE_CONTRACT_RDO.show()
    
#==========================================================================
# global variables
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
            
    # Open the device
    try :
        handle.hw_open(config.HW_INTERFACE, config.PORT, config.SPI_PORT, config.BITRATE, config.SPIBITRATE, config.DEVICE_I2C_ADDR)        
    except Exception as e :
        print e.message
        sys.exit()


    CONTROL_CONFIG_REG.read(handle)
    if CONTROL_CONFIG_REG.fieldByName('RDOIntrusiveMode').value == EnabledDisabled_list.index('Disabled') or CONTROL_CONFIG_REG.fieldByName('PDOIntrusiveMode').value == EnabledDisabled_list.index('Disabled') :
        print 'Either PDOIntrusiveMode, RDOIntrusiveMode or both were not enabled. Enabling and issuing PD hard reset.'
        CONTROL_CONFIG_REG.fieldByName('RDOIntrusiveMode').value = EnabledDisabled_list.index('Enabled')
        CONTROL_CONFIG_REG.fieldByName('PDOIntrusiveMode').value = EnabledDisabled_list.index('Enabled')
        CONTROL_CONFIG_REG.write(handle)
        HRST(handle)

    STATUS_REG.read(handle)
    while STATUS_REG.fieldByName('PlugPresent').value == TrueFalse_list.index('False') :
        STATUS_REG.read(handle)
        raw_input('Plug is not connected. Please plug cable and press enter to procede with script: ')

    PWR_STATUS.read(handle)
    if PWR_STATUS.fieldByName('SourceSink').value == SourceSink_list.index('TPS65982 is Source'):
        negotiate_Source(handle)
        
    if PWR_STATUS.fieldByName('SourceSink').value == SourceSink_list.index('TPS65982 is sink') :
        negotiate_Sink(handle)


    # Close the device
    handle.hw_close()

    sys.exit()
