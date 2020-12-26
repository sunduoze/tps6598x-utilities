#!/bin/env python
# -*- coding: cp1252 -*-
#==========================================================================
# (c) 2015 Texas Instruments
#--------------------------------------------------------------------------
# Project : TPS65982 Host Interface Register Definitions
# File    : register_definitions.py
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



from register_class import *
from debug_trace import *

DisablePD_list = [ 'Normal USB-PD Behavior' , 'Stop USB-PD Act Legacy Source', 'Stop USB-PD Act Legacy Sink', 'No VBUS Pretend Dead Battery' ]
EnabledDisabled_list = ['Disabled', 'Enabled']
OnOff_list = [ 'off' , 'on' ]
Connect_list = [ 'disconnected' , 'connected' ]

Receptacle_list = ['Plug', 'Receptacle']

HighLow_list = ['low', 'high']

def translate_current(self):
    return (str(10* self.value))

def rev_translate_current(self, value):
    retval = int(value) // 10
    if retval > 0x3FF:
        retval = 0x3FF
    if retval < 0:
        retval = 0
    return (retval)


VID = cRegister({'register name' : 'Vendor ID', 'address' : 0x00, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'Device ID', 'offset' : 0, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
            ] } )

DID = cRegister({'register name' : 'Device ID', 'address' : 0x01, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'Device ID', 'offset' : 0, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
            ] } )

MODE_REG = cRegister({'register name' : 'MODE', 'address' : 0x03, 'permission' : 'RO', 'translate' : le_register_show,
            'fields' : [
               { 'name' : 'Byte_1', 'offset' : 0, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_2', 'offset' : 8, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_3', 'offset' : 16, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_4', 'offset' : 24, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
            ] } )

UID = cRegister({'register name' : 'Unique ID', 'address' : 0x05, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'Device ID', 'offset' : 0, 'length' : 128, 'value' : 0, 'translate' : hexTranslate } ,
            ] } )

CUSTUSE = cRegister({'register name' : 'Customer Use', 'address' : 0x06, 'permission' : 'RO', 'translate' : be_hex_show,
            'fields' : [
               { 'name' : 'Customer Use 1', 'offset' : 0, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Customer Use 2', 'offset' : 32, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
            ] } )


def version_register_show(self):
    print "VERSION          %02x%02x.%02x.%02x\n" %(self.fieldByName('Byte_4').value, self.fieldByName('Byte_3').value,
                                                  self.fieldByName('Byte_2').value, self.fieldByName('Byte_1').value)

VERSION_REG = cRegister({'register name' : 'VERSION', 'address' : 0x0F, 'permission' : 'RO', 'translate' : version_register_show,
            'fields' : [
               { 'name' : 'Byte_1', 'offset' : 0, 'length' : 8, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Byte_2', 'offset' : 8, 'length' : 8, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Byte_3', 'offset' : 16, 'length' : 8, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Byte_4', 'offset' : 24, 'length' : 8, 'value' : 0, 'translate' : hexTranslate } ,
            ]} )             

INT_EVENT1 = cRegister({'register name' : 'Int Event 1', 'address' : 0x14, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'Soft Reset', 'offset' : 0, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Hard Reset', 'offset' : 1, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 2, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Plug Insert or Removal', 'offset' : 3, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Auto Swap Complete', 'offset' : 4, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 5, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Awoken by Host', 'offset' : 6, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'RDO Received from Sink', 'offset' : 7, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'BIST', 'offset' : 8, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Overcurrent', 'offset' : 9, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Attention Received', 'offset' : 10, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'VDM Received', 'offset' : 11, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'New Contract as Consumer', 'offset' : 12, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'New Contract as Provider', 'offset' : 13, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Source Capabilities Message Ready', 'offset' : 14, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Sink Capabilities Message Ready', 'offset' : 15, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 16, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Swap Requested', 'offset' : 17, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'BIST Message Ignored', 'offset' : 18, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Goto Min Received', 'offset' : 19, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'USB Host Present', 'offset' : 20, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'USB Host Present no Longer', 'offset' : 21, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'High Voltage Warning', 'offset' : 22, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'PP Switch Changed', 'offset' : 23, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Power Status Update', 'offset' : 24, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Data Status Update', 'offset' : 25, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Status Update', 'offset' : 26, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'PD Status Update', 'offset' : 27, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'ADC Low Threshold', 'offset' : 28, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'ADC High Threshold', 'offset' : 29, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'CMD1 Complete', 'offset' : 30, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'CMD2 Complete', 'offset' : 31, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Device Incompatible', 'offset' : 32, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Cannot Provide Voltage or Current', 'offset' : 33, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Can Provide Voltage or Current Later', 'offset' : 34, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Power Event Occurred', 'offset' : 35, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Missing Get Capabilities Message', 'offset' : 36, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Transmission Error', 'offset' : 37, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Protocol Error', 'offset' : 38, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Message Data', 'offset' : 39, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 40, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Discharge Failed', 'offset' : 41, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Sink Transition Complete', 'offset' : 42, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 43, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 44, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 45, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Unable to Source', 'offset' : 46, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Power Source Current Limit', 'offset' : 47, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 48, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 49, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 50, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 51, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 52, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 53, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 54, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 55, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'User SVID Mode Entered', 'offset' : 56, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'User SVID Mode Exited', 'offset' : 57, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'User SVID Attention VDM Received', 'offset' : 58, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'User SVID Other VDM Received', 'offset' : 59, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 60, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 61, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 62, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 63, 'length' : 1, 'value' : 0 } ,
            ] } )

INT_EVENT2 = cRegister({'register name' : 'Int Event 2', 'address' : 0x15, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'Soft Reset', 'offset' : 0, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Hard Reset', 'offset' : 1, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 2, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Plug Insert or Removal', 'offset' : 3, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Auto Swap Complete', 'offset' : 4, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 5, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Awoken by Host', 'offset' : 6, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'RDO Received from Sink', 'offset' : 7, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'BIST', 'offset' : 8, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Overcurrent', 'offset' : 9, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Attention Received', 'offset' : 10, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'VDM Received', 'offset' : 11, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'New Contract as Consumer', 'offset' : 12, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'New Contract as Provider', 'offset' : 13, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Source Capabilities Message Ready', 'offset' : 14, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Sink Capabilities Message Ready', 'offset' : 15, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 16, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Swap Requested', 'offset' : 17, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'BIST Message Ignored', 'offset' : 18, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Goto Min Received', 'offset' : 19, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'USB Host Present', 'offset' : 20, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'USB Host Present no Longer', 'offset' : 21, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'High Voltage Warning', 'offset' : 22, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'PP Switch Changed', 'offset' : 23, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Power Status Update', 'offset' : 24, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Data Status Update', 'offset' : 25, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Status Update', 'offset' : 26, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'PD Status Update', 'offset' : 27, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'ADC Low Threshold', 'offset' : 28, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'ADC High Threshold', 'offset' : 29, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'CMD1 Complete', 'offset' : 30, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'CMD2 Complete', 'offset' : 31, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Device Incompatible', 'offset' : 32, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Cannot Provide Voltage or Current', 'offset' : 33, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Can Provide Voltage or Current Later', 'offset' : 34, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Power Event Occurred', 'offset' : 35, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Missing Get Capabilities Message', 'offset' : 36, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Transmission Error', 'offset' : 37, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Protocol Error', 'offset' : 38, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Message Data', 'offset' : 39, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 40, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Discharge Failed', 'offset' : 41, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 42, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Source Power Fault', 'offset' : 43, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 44, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 45, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Unable to Source', 'offset' : 46, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 47, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 48, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 49, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 50, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 51, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 52, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 53, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 54, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 55, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'User SVID Mode Entered', 'offset' : 56, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'User SVID Mode Exited', 'offset' : 57, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'User SVID Attention VDM Received', 'offset' : 58, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'User SVID Other VDM Received', 'offset' : 59, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 60, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 61, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 62, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 63, 'length' : 1, 'value' : 0 } ,
            ] } )


INT_MASK1 = cRegister({'register name' : 'Int Mask 1', 'address' : 0x16, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Soft Reset', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Hard Reset', 'offset' : 1, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Reserved', 'offset' : 2, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Plug Insert or Removal', 'offset' : 3, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Auto Swap Complete', 'offset' : 4, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Reserved', 'offset' : 5, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Awoken by Host', 'offset' : 6, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'RDO Received from Sink', 'offset' : 7, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'BIST', 'offset' : 8, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Overcurrent', 'offset' : 9, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Attention Received', 'offset' : 10, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'VDM Received', 'offset' : 11, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'New Contract as Consumer', 'offset' : 12, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'New Contract as Provider', 'offset' : 13, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Source Capabilities Message Ready', 'offset' : 14, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Sink Capabilities Message Ready', 'offset' : 15, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Reserved', 'offset' : 16, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Swap Requested', 'offset' : 17, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'BIST Message Ignored', 'offset' : 18, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Goto Min Received', 'offset' : 19, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'USB Host Present', 'offset' : 20, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'USB Host Present no Longer', 'offset' : 21, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'High Voltage Warning', 'offset' : 22, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'PP Switch Changed', 'offset' : 23, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Power Status Update', 'offset' : 24, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Data Status Update', 'offset' : 25, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Status Update', 'offset' : 26, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'PD Status Update', 'offset' : 27, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'ADC Low Threshold', 'offset' : 28, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'ADC High Threshold', 'offset' : 29, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'CMD1 Complete', 'offset' : 30, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'CMD2 Complete', 'offset' : 31, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Error: Device Incompatible', 'offset' : 32, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Error: Cannot Provide Voltage or Current', 'offset' : 33, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Error: Can Provide Voltage or Current Later', 'offset' : 34, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Error: Power Event Occurred', 'offset' : 35, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Error: Missing Get Capabilities Message', 'offset' : 36, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Error: Transmission Error', 'offset' : 37, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Error: Protocol Error', 'offset' : 38, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Error: Message Data', 'offset' : 39, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Reserved', 'offset' : 40, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Error: Discharge Failed', 'offset' : 41, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Reserved', 'offset' : 42, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Source Power Fault', 'offset' : 43, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Reserved', 'offset' : 44, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 45, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Unable to Source', 'offset' : 46, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Reserved', 'offset' : 47, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 48, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 49, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 50, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 51, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 52, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 53, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 54, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 55, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'User SVID Mode Entered', 'offset' : 56, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'User SVID Mode Exited', 'offset' : 57, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'User SVID Attention VDM Received', 'offset' : 58, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'User SVID Other VDM Received', 'offset' : 59, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Reserved', 'offset' : 60, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 61, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 62, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 63, 'length' : 1, 'value' : 0 } ,
            ] } )

INT_MASK2 = cRegister({'register name' : 'Int Mask 2', 'address' : 0x17, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Soft Reset', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Hard Reset', 'offset' : 1, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Reserved', 'offset' : 2, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Plug Insert or Removal', 'offset' : 3, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Auto Swap Complete', 'offset' : 4, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Reserved', 'offset' : 5, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Awoken by Host', 'offset' : 6, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'RDO Received from Sink', 'offset' : 7, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'BIST', 'offset' : 8, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Overcurrent', 'offset' : 9, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Attention Received', 'offset' : 10, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'VDM Received', 'offset' : 11, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'New Contract as Consumer', 'offset' : 12, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'New Contract as Provider', 'offset' : 13, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Source Capabilities Message Ready', 'offset' : 14, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Sink Capabilities Message Ready', 'offset' : 15, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Reserved', 'offset' : 16, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Swap Requested', 'offset' : 17, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'BIST Message Ignored', 'offset' : 18, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Goto Min Received', 'offset' : 19, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'USB Host Present', 'offset' : 20, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'USB Host Present no Longer', 'offset' : 21, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'High Voltage Warning', 'offset' : 22, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'PP Switch Changed', 'offset' : 23, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Power Status Update', 'offset' : 24, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Data Status Update', 'offset' : 25, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Status Update', 'offset' : 26, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'PD Status Update', 'offset' : 27, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'ADC Low Threshold', 'offset' : 28, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'ADC High Threshold', 'offset' : 29, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'CMD1 Complete', 'offset' : 30, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'CMD2 Complete', 'offset' : 31, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Error: Device Incompatible', 'offset' : 32, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Error: Cannot Provide Voltage or Current', 'offset' : 33, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Error: Can Provide Voltage or Current Later', 'offset' : 34, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Error: Power Event Occurred', 'offset' : 35, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Error: Missing Get Capabilities Message', 'offset' : 36, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Error: Transmission Error', 'offset' : 37, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Error: Protocol Error', 'offset' : 38, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Error: Message Data', 'offset' : 39, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Reserved', 'offset' : 40, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Error: Discharge Failed', 'offset' : 41, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Reserved', 'offset' : 42, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Source Power Fault', 'offset' : 43, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Reserved', 'offset' : 44, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 45, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Unable to Source', 'offset' : 46, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Reserved', 'offset' : 47, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 48, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 49, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 50, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 51, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 52, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 53, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 54, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 55, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'User SVID Mode Entered', 'offset' : 56, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'User SVID Mode Exited', 'offset' : 57, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'User SVID Attention VDM Received', 'offset' : 58, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'User SVID Other VDM Received', 'offset' : 59, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list  } ,
               { 'name' : 'Reserved', 'offset' : 60, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 61, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 62, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 63, 'length' : 1, 'value' : 0 } ,
            ] } )

intClear_list = ['No action', 'Clear Interrupt' ]

INT_CLEAR1 = cRegister({'register name' : 'Int Clear 1', 'address' : 0x18, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Soft Reset', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Hard Reset', 'offset' : 1, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Reserved', 'offset' : 2, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Plug Insert or Removal', 'offset' : 3, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Auto Swap Complete', 'offset' : 4, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Reserved', 'offset' : 5, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Awoken by Host', 'offset' : 6, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'RDO Received from Sink', 'offset' : 7, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'BIST', 'offset' : 8, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Overcurrent', 'offset' : 9, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Attention Received', 'offset' : 10, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'VDM Received', 'offset' : 11, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'New Contract as Consumer', 'offset' : 12, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'New Contract as Provider', 'offset' : 13, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Source Capabilities Message Ready', 'offset' : 14, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Sink Capabilities Message Ready', 'offset' : 15, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Reserved', 'offset' : 16, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Swap Requested', 'offset' : 17, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'BIST Message Ignored', 'offset' : 18, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Goto Min Received', 'offset' : 19, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'USB Host Present', 'offset' : 20, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'USB Host Present no Longer', 'offset' : 21, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'High Voltage Warning', 'offset' : 22, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'PP Switch Changed', 'offset' : 23, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Power Status Update', 'offset' : 24, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Data Status Update', 'offset' : 25, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Status Update', 'offset' : 26, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'PD Status Update', 'offset' : 27, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'ADC Low Threshold', 'offset' : 28, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'ADC High Threshold', 'offset' : 29, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'CMD1 Complete', 'offset' : 30, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'CMD2 Complete', 'offset' : 31, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Error: Device Incompatible', 'offset' : 32, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Error: Cannot Provide Voltage or Current', 'offset' : 33, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Error: Can Provide Voltage or Current Later', 'offset' : 34, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Error: Power Event Occurred', 'offset' : 35, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Error: Missing Get Capabilities Message', 'offset' : 36, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Error: Transmission Error', 'offset' : 37, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Error: Protocol Error', 'offset' : 38, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Error: Message Data', 'offset' : 39, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Reserved', 'offset' : 40, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Discharge Failed', 'offset' : 41, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Reserved', 'offset' : 42, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Source Power Fault', 'offset' : 43, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Reserved', 'offset' : 44, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 45, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Unable to Source', 'offset' : 46, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Reserved', 'offset' : 47, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 48, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 49, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 50, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 51, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 52, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 53, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 54, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 55, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'User SVID Mode Entered', 'offset' : 56, 'length' : 1, 'value' : 0, 'translate list' : intClear_list  } ,
               { 'name' : 'User SVID Mode Exited', 'offset' : 57, 'length' : 1, 'value' : 0, 'translate list' : intClear_list  } ,
               { 'name' : 'User SVID Attention VDM Received', 'offset' : 58, 'length' : 1, 'value' : 0, 'translate list' : intClear_list  } ,
               { 'name' : 'User SVID Other VDM Received', 'offset' : 59, 'length' : 1, 'value' : 0, 'translate list' : intClear_list  } ,
               { 'name' : 'Reserved', 'offset' : 60, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 61, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 62, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 63, 'length' : 1, 'value' : 0 } ,
            ] } )

INT_CLEAR2 = cRegister({'register name' : 'Int Clear 2', 'address' : 0x19, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Soft Reset', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Hard Reset', 'offset' : 1, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Reserved', 'offset' : 2, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Plug Insert or Removal', 'offset' : 3, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Auto Swap Complete', 'offset' : 4, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Reserved', 'offset' : 5, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Awoken by Host', 'offset' : 6, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'RDO Received from Sink', 'offset' : 7, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'BIST', 'offset' : 8, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Overcurrent', 'offset' : 9, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Attention Received', 'offset' : 10, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'VDM Received', 'offset' : 11, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'New Contract as Consumer', 'offset' : 12, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'New Contract as Provider', 'offset' : 13, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Source Capabilities Message Ready', 'offset' : 14, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Sink Capabilities Message Ready', 'offset' : 15, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Reserved', 'offset' : 16, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Swap Requested', 'offset' : 17, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'BIST Message Ignored', 'offset' : 18, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Goto Min Received', 'offset' : 19, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'USB Host Present', 'offset' : 20, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'USB Host Present no Longer', 'offset' : 21, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'High Voltage Warning', 'offset' : 22, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'PP Switch Changed', 'offset' : 23, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Power Status Update', 'offset' : 24, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Data Status Update', 'offset' : 25, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Status Update', 'offset' : 26, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'PD Status Update', 'offset' : 27, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'ADC Low Threshold', 'offset' : 28, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'ADC High Threshold', 'offset' : 29, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'CMD1 Complete', 'offset' : 30, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'CMD2 Complete', 'offset' : 31, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Error: Device Incompatible', 'offset' : 32, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Error: Cannot Provide Voltage or Current', 'offset' : 33, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Error: Can Provide Voltage or Current Later', 'offset' : 34, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Error: Power Event Occurred', 'offset' : 35, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Error: Missing Get Capabilities Message', 'offset' : 36, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Error: Transmission Error', 'offset' : 37, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Error: Protocol Error', 'offset' : 38, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Error: Message Data', 'offset' : 39, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Reserved', 'offset' : 40, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Discharge Failed', 'offset' : 41, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Reserved', 'offset' : 42, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Source Power Fault', 'offset' : 43, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Reserved', 'offset' : 44, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 45, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Error: Unable to Source', 'offset' : 46, 'length' : 1, 'value' : 0, 'translate list' : intClear_list } ,
               { 'name' : 'Reserved', 'offset' : 47, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 48, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 49, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 50, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 51, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 52, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 53, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 54, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 55, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'User SVID Mode Entered', 'offset' : 56, 'length' : 1, 'value' : 0, 'translate list' : intClear_list  } ,
               { 'name' : 'User SVID Mode Exited', 'offset' : 57, 'length' : 1, 'value' : 0, 'translate list' : intClear_list  } ,
               { 'name' : 'User SVID Attention VDM Received', 'offset' : 58, 'length' : 1, 'value' : 0, 'translate list' : intClear_list  } ,
               { 'name' : 'User SVID Other VDM Received', 'offset' : 59, 'length' : 1, 'value' : 0, 'translate list' : intClear_list  } ,
               { 'name' : 'Reserved', 'offset' : 60, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 61, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 62, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 63, 'length' : 1, 'value' : 0 } ,
            ] } )


TrueFalse_list = ['False', 'True']    
ConnState_list = ['NC', 'Disabled', 'AudioAcc', 'DebugAcc', 'NC_RA', 'Reserved', 'No_Ra', 'Ra']
PlugOrientation_list = ['Upside_Up_CC_on_CC1', 'Upside_Down_CC_on_CC2']
PowerSource_list = ['Unknown', 'VIN_3P3', 'PP_CABLE', 'VBUS']    
SupplyType_list = ['Fixed', 'Battery', 'Variable']
PortRole_list = ['PullDown_Active_or_Port_Disabled', 'PullUp_Active']
DataRole_list = ['UFP_or_Port_Disabled', 'DFP']
PpSwitch_list = ['Disabled', 'Disabled due to Overcurrent', 'Enabled Reverse current from VBUS to Power Path blocked (acting as output)', 'Enabled Reverse current from Power Path to VBUS blocked (acting as input)']
PpCable_list = ['Disabled', 'Disabled due to Overcurrent', 'PP_CABLE enabled on C_CC1', 'PP_CABLE enabled on C_CC2' ]
Vbus_status_list = ['VBUS at VSafe0V (less than 0.8V)', 'VBUS at VSafe5V (4.75-5.5V)', 'VBUS at negotiated voltage', 'VBUS not at negotiated voltage, 5V or 0V']
USBHost_list = ['UsbHost_Not_Providing_Vbus','UsbHost_Ace_Provider_or_ProviderConsumer','UsbHost_Vbus_from_Non_PD_Device','UsbHost_Vbus_from_PD_Device' ]
Legacy_list = ['Not acting as legacy (PD Active)', 'Acting as legacy sink (PD not active)', 'Acting as legacy source (PD not active)', 'Reserved']

STATUS_REG = cRegister({'register name' : 'Status', 'address' : 0x1A, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'PlugPresent', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'ConnState', 'offset' : 1, 'length' : 3, 'value' : 0, 'translate list' : ConnState_list } ,
               { 'name' : 'PlugOrientation', 'offset' : 4, 'length' : 1, 'value' : 0, 'translate list' : PlugOrientation_list } ,
               { 'name' : 'PortRole', 'offset' : 5, 'length' : 1, 'value' : 0, 'translate list' : PortRole_list } ,
               { 'name' : 'DataRole', 'offset' : 6, 'length' : 1, 'value' : 0, 'translate list' : DataRole_list } ,
               { 'name' : 'VconnEnabled', 'offset' : 7, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'PP5V_Switch', 'offset' : 8, 'length' : 2, 'value' : 0, 'translate list' : PpSwitch_list } ,
               { 'name' : 'PPHV_Switch', 'offset' : 10, 'length' : 2, 'value' : 0, 'translate list' : PpSwitch_list } ,
               { 'name' : 'PPHVE_Switch', 'offset' : 12, 'length' : 2, 'value' : 0, 'translate list' : PpSwitch_list } ,
               { 'name' : 'PPCABLE_Switch', 'offset' : 14, 'length' : 2, 'value' : 0, 'translate list' : PpCable_list } ,
               { 'name' : 'OvercurrentCondition', 'offset' : 16, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'HighVoltageCondition', 'offset' : 17, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'PowerSource', 'offset' : 18, 'length' : 2, 'value' : 0, 'translate list' : PowerSource_list } ,
               { 'name' : 'VBUSStatus', 'offset' : 20, 'length' : 2, 'value' : 0, 'translate list' : Vbus_status_list  } ,
               { 'name' : 'UsbHostPresent', 'offset' : 22, 'length' : 2, 'value' : 0, 'translate list' : USBHost_list  } ,
               { 'name' : 'ActingAsLegacy', 'offset' : 24, 'length' : 2, 'value' : 0, 'translate list' : Legacy_list } ,
               { 'name' : 'GoToMinActive', 'offset' : 26, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Bist', 'offset' : 27, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'HighVoltageWarning', 'offset' : 28, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'LowVoltageWarning', 'offset' : 29, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 30, 'length' : 2, 'value' : 0 } ,               
            ] } )             

PortInfo_list = [ 'CONSUMER_CCPD', 'CONSUMER_CCPD_CCIPU', 'CONSUMER_PROVIDER_CCPD', 'CONSUMER_PROVIDER_CCPD_CCIPU', 'PROVIDER_CONSUMER_CCIPU','PROVIDER_CONSUMER_CCIPU_CCPD','PROVIDER_CCIPU','PORT_DISABLED' ]
ReceptacleType_list = [ 'UsbReceptacle_STD_USB2ONLY_TypeC_Receptacle', 'UsbReceptacle_STD_FULL_TypeC_Receptacle', 'UsbReceptacle_TETH_USB2ONLY_TypeC_Plug', 'UsbReceptacle_TETH_FULL_TypeC_Plug','UsbReceptacle_UNKNOWN' ]
TypeCCurrent_list = [ 'CC_IPU_STD', 'CC_IPU_1P5A', 'CC_IPU_3P0A', 'CC_IPU_NONE' ]
VCONNsupported_list = [ 'VconnConfig_NotUsed', 'VconnConfig_RESERVED', 'VconnConfig_DFP_ONLY', 'VconnConfig_DFP_UFP' ]

def OVPTripPoint_translate(self):
    # in mV
    return (3840 + (320 * self.value))

def OVPTripPoint_revTranslate(self, val):
    value = int(val)
    if (value > (3840 + 320 * (2**self.length - 1))):
        return (2**self.length - 1)

    if (value < 3840):
        return 0
    
    return ((value - 3840) / 320 )

OVPUsage_list = [ 'OvpUsageType_OvpTripPoint', 'OvpUsageType_MaxVoltage5Percent', 'OvpUsageType_MaxVoltage10Percent', 'OvpUsageType_MaxVoltage15Percent' ]
SwitchConfig_list = [ 'SwitchConfig_DISABLED', 'SwitchConfig_AS_OUT', 'SwitchConfig_AS_IN', 'SwitchConfig_AS_IN_AFTER_SYSRDY', 'SwitchConfig_AS_OUT_IN', 'SwitchConfig_AS_OUT_IN_AFTER_SYSRDY' ]
USB3rate_list = [ 'SSSignallingSupport_USB2', 'SSSignallingSupport_USB3p1_Gen1', 'SSSignallingSupport_USB3p2_Gen1_Gen2', 'reserved' ]
RSense_list = [ '10 mOhm PP_HVE current sense resisitor', '5 mOhm PP_HVE current sense resisitor' ]
XBarPort_list = ['No connection', 'UART RX/TX', 'LSX P2R/R2P', 'GPIO 0/1' ]
XBarSys_list = ['No connection', 'C SBU', 'C USB T/P', 'Reserved' ]
VOut33ST_list = ['Assert RESETZ if VOUT_3v3 < 1.125 V', 'Assert RESETZ if VOUT_3v3 < 2.25 V','Assert RESETZ if VOUT_3v3 < 2.375 V','Assert RESETZ if VOUT_3v3 < 2.5 V','Assert RESETZ if VOUT_3v3 < 2.625 V','Assert RESETZ if VOUT_3v3 < 2.75 V','Assert RESETZ if VOUT_3v3 < 2.875 V','Assert RESETZ if VOUT_3v3 < 3.0 V' ]
UVPTrip_list = ['5%', '10%', '15%', '20%', '25%', '30%', '40%', '50%' ]

SysPower_list = ['S0', 'Reserved', 'Reserved', 'S3', 'S4', 'S5']

SYS_POWER = cRegister({'register name' : 'System Power Register', 'address' : 0x20, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'System Power State', 'offset' : 0, 'length' : 8, 'value' : 0, 'translate list' : SysPower_list } ,
            ] } )

ILim_Timeout_list = ['10 uS', '20 uS', '80 uS', '160 uS', '640 uS', '1.28 mS', '5.12 mS', '10.24 mS', '40.96 mS', '81.92 mS', \
                     'Reserved (0xA)', 'Reserved (0xB)', 'Reserved (0xC)', 'Reserved (0xD)', 'Reserved (0xE)', 'Reserved (0xF)']


SYS_CONFIG_REG = cRegister({'register name' : 'System Config', 'address' : 0x28, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'PortInfo', 'offset' : 0, 'length' : 3, 'value' : 0 , 'translate list' : PortInfo_list} ,
               { 'name' : 'ReceptacleType', 'offset' : 3, 'length' : 3, 'value' : 0, 'translate list' : ReceptacleType_list } ,
               { 'name' : 'TypeCCurrent', 'offset' : 6, 'length' : 2, 'value' : 0, 'translate list' : TypeCCurrent_list } ,
               { 'name' : 'VCONNsupported', 'offset' : 8, 'length' : 2, 'value' : 0, 'translate list' : VCONNsupported_list } ,
               { 'name' : 'Reserved', 'offset' : 10, 'length' : 4, 'value' : 0 } ,
               { 'name' : 'HighVoltageWarningLevel', 'offset' : 14, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list  } ,
               { 'name' : 'LowVoltageWarningLevel', 'offset' : 15, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'OvpTripPoint (in mV)', 'offset' : 16, 'length' : 6, 'value' : 0, 'translate' : OVPTripPoint_translate, 'reverse translate' : OVPTripPoint_revTranslate } ,
               { 'name' : 'OVPUsage', 'offset' : 22, 'length' : 2, 'value' : 0, 'translate list' : OVPUsage_list } ,
               { 'name' : 'PP_5V0config', 'offset' : 24, 'length' : 2, 'value' : 0, 'translate list' : SwitchConfig_list } ,
               { 'name' : 'PP_HVconfig', 'offset' : 26, 'length' : 2, 'value' : 0, 'translate list' : SwitchConfig_list } ,
               { 'name' : 'PP_HVEconfig', 'offset' : 28, 'length' : 3, 'value' : 0, 'translate list' : SwitchConfig_list } ,
               { 'name' : 'Reserved', 'offset' : 31, 'length' : 1, 'value' : 0 } , # 32bits
               { 'name' : 'BC12enable', 'offset' : 32, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'USBEPenable', 'offset' : 33, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'USBRPenable', 'offset' : 34, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'USB3rate', 'offset' : 35, 'length' : 2, 'value' : 0, 'translate list' : USB3rate_list } ,
               { 'name' : 'Reserved', 'offset' : 37, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'AudioAccessorySupport', 'offset' : 38, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'DebugAccessorySupport', 'offset' : 39, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'PoweredAccessorySupport', 'offset' : 40, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'RSense', 'offset' : 41, 'length' : 1, 'value' : 0, 'translate list' : RSense_list } ,
               { 'name' : 'TrySRCSupport', 'offset' : 42, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'BillboardAllowed', 'offset' : 43, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } , #48 bits
               { 'name' : 'Reserved', 'offset' : 44, 'length' : 2, 'value' : 0 } , #48 bits
               { 'name' : 'PP_EXT Overcurrent Clamp Timeout', 'offset' : 46, 'length' : 4, 'value' : 0, 'translate list' : ILim_Timeout_list } ,
               { 'name' : 'PP_EXT Overcurrent Clamp Enable', 'offset' : 50, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'ResetZTimeoutCount', 'offset' : 51, 'length' : 6, 'value' : 0 } ,
               { 'name' : 'ResetZTimeoutClock', 'offset' : 57, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Vout3V3SupThresh', 'offset' : 59, 'length' : 3, 'value' : 0, 'translate list' : VOut33ST_list } ,
               { 'name' : 'Vout3V3enable', 'offset' : 62, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 63, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'sinkSenseCCDisconnect', 'offset' : 64, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 65, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'setUvpTo4P5V', 'offset' : 66, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'UvpTripPoint5V', 'offset' : 67, 'length' : 3, 'value' : 0, 'translate list' : UVPTrip_list  } ,
               { 'name' : 'UvpTripPointHV', 'offset' : 70, 'length' : 3, 'value' : 0, 'translate list' : UVPTrip_list  } , 
               { 'name' : 'Reserved', 'offset' : 73, 'length' : 6, 'value' : 0 } ,
               { 'name' : 'UART Disabled', 'offset' : 79, 'length' : 1, 'value' : 0,  'translate list' : TrueFalse_list} ,
               { 'name' : 'Serial String Present', 'offset' : 80, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Product String Index', 'offset' : 81, 'length' : 2, 'value' : 0, 'translate' : decTranslate, 'reverse translate' : decRevTranslate } ,
               { 'name' : 'Manufacturer String Index', 'offset' : 83, 'length' : 2, 'value' : 0, 'translate' : decTranslate, 'reverse translate' : decRevTranslate } ,
               { 'name' : 'Billboard URL String Index', 'offset' : 85, 'length' : 3, 'value' : 0, 'translate' : decTranslate, 'reverse translate' : decRevTranslate } ,
               { 'name' : 'TBT Billboard String Index', 'offset' : 88, 'length' : 4, 'value' : 0, 'translate' : decTranslate, 'reverse translate' : decRevTranslate } ,
               { 'name' : 'Reserved', 'offset' : 92, 'length' : 4, 'value' : 0 } ,
               { 'name' : 'DP Billboard String Index', 'offset' : 96, 'length' : 4, 'value' : 0, 'translate' : decTranslate, 'reverse translate' : decRevTranslate } ,
               { 'name' : 'Reserved', 'offset' : 100, 'length' : 4, 'value' : 0 } ,
               { 'name' : 'Custom 1 Billboard String', 'offset' : 104, 'length' : 4, 'value' : 0, 'translate' : decTranslate, 'reverse translate' : decRevTranslate } ,
               { 'name' : 'Custom 2 Billboard String', 'offset' : 108, 'length' : 4, 'value' : 0, 'translate' : decTranslate, 'reverse translate' : decRevTranslate } ,
               { 'name' : 'Custom 3 Billboard String', 'offset' : 112, 'length' : 4, 'value' : 0, 'translate' : decTranslate, 'reverse translate' : decRevTranslate } ,
               { 'name' : 'Custom 4 Billboard String', 'offset' : 116, 'length' : 4, 'value' : 0, 'translate' : decTranslate, 'reverse translate' : decRevTranslate } ,
               { 'name' : 'PP_5V Overcurrent Clamp Timeout', 'offset' : 120, 'length' : 4, 'value' : 0, 'translate list' : ILim_Timeout_list } ,
               { 'name' : 'PP_5V Overcurrent Clamp Enable', 'offset' : 124, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 125, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'PP_HV Overcurrent Clamp Timeout', 'offset' : 128, 'length' : 4, 'value' : 0, 'translate list' : ILim_Timeout_list } ,
               { 'name' : 'PP_HV Overcurrent Clamp Enable', 'offset' : 132, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 133, 'length' : 3, 'value' : 0 } ,
            ] } )


CONTROL_CONFIG_REG = cRegister({'register name' : 'Control Config', 'address' : 0x29, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'DisablePD', 'offset' : 0, 'length' : 2, 'value' : 0, 'translate list' : DisablePD_list } ,
               { 'name' : 'ExternallyPowered', 'offset' : 2, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 3, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'ProcessSwapToSink', 'offset' : 4, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'InitSwapToSink', 'offset' : 5, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'ProcessSwapToSource', 'offset' : 6, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'InitSwapToSource', 'offset' : 7, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'RDOIntrusiveMode', 'offset' : 8, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'PDOIntrusiveMode', 'offset' : 9, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'ProcessVconnSwap', 'offset' : 10, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'InitiateVconnSwap', 'offset' : 11, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'ProcessSwapToUFP', 'offset' : 12, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'InitiateSwapToUFP', 'offset' : 13, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'ProcessSwapToDFP', 'offset' : 14, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'InitiateSwapToDFP', 'offset' : 15, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 16, 'length' : 8, 'value' : 0 } ,               
               { 'name' : 'AutomaticIDRequest', 'offset' : 24, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'AMIntrusiveMode', 'offset' : 25, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 26, 'length' : 5, 'value' : 0 } ,
               { 'name' : 'ForceUSBGen1', 'offset' : 31, 'length' : 1, 'value' : 0, 'translate list' : OnOff_list } ,
               { 'name' : 'I2C Timeout', 'offset' : 32, 'length' : 3, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'AC Adapter Swap Disable', 'offset' : 35, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 36, 'length' : 4, 'value' : 0 } ,
            ] } )

BOOT_FLAGS = cRegister({'register name' : 'Boot Flags', 'address' : 0x2D, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'BootOk', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'ExtPhvSwitch', 'offset' : 1, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'DeadBatteryFlag', 'offset' : 2, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'SpiFlashPresent', 'offset' : 3, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Region0', 'offset' : 4, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Region1', 'offset' : 5, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Region0Invalid', 'offset' : 6, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Region1Invalid', 'offset' : 7, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Region0FlashErr', 'offset' : 8, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Region1FlashErr', 'offset' : 9, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 10, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'UartCRCFail', 'offset' : 11, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Region0CRCFail', 'offset' : 12, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Region1CRCFail', 'offset' : 13, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'CustomerOTPInvalid', 'offset' : 14, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'OneCallI2COtpBits', 'offset' : 15, 'length' : 2, 'value' : 0, 'translate' : hexTranslate, 'reverse translate' : hexRevTranslate } ,
               { 'name' : 'App Cust Version Error', 'offset' : 17, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'App Cust Length Error', 'offset' : 18, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'App Cust CRC Error', 'offset' : 19, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 20, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Debug Ctl 1 state at boot', 'offset' : 22, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'Debug Ctl 2 state at boot', 'offset' : 23, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'DevNumber', 'offset' : 24, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'UartBoot', 'offset' : 27, 'length' : 1, 'value' : 0,  'translate list' : TrueFalse_list } ,
               { 'name' : 'UartOverflowErr', 'offset' : 28, 'length' : 1, 'value' : 0,  'translate list' : TrueFalse_list } ,
               { 'name' : 'IntPhvSwitch', 'offset' : 29, 'length' : 1, 'value' : 0,  'translate list' : TrueFalse_list } ,
               { 'name' : 'UartRetryErr', 'offset' : 30, 'length' : 1, 'value' : 0,  'translate list' : TrueFalse_list } ,
               { 'name' : 'UartTimeoutErr', 'offset' : 31, 'length' : 1, 'value' : 0,  'translate list' : TrueFalse_list } ,
               { 'name' : 'OTPValid', 'offset' : 32, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'SWD Disable', 'offset' : 34, 'length' : 1, 'value' : 0,  'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 35, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Vout3v3Ctl', 'offset' : 36, 'length' : 1, 'value' : 0,  'translate list' : TrueFalse_list } ,
               { 'name' : 'WaitForVin3V3', 'offset' : 37, 'length' : 1, 'value' : 0,  'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 38, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'OneCallI2cOtpBits', 'offset' : 40, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 42, 'length' : 8, 'value' : 0 } ,
               { 'name' : 'Vout3v3Threshold', 'offset' : 50, 'length' : 5, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 55, 'length' : 9, 'value' : 0 } ,
               { 'name' : 'REV_ID_Metal', 'offset' : 64, 'length' : 4, 'value' : 0 } ,
               { 'name' : 'REV_ID_Base', 'offset' : 68, 'length' : 4, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 72, 'length' : 24, 'value' : 0 } ,
            ] } )             

BUILD_ID_REG = cRegister({'register name' : 'Build Identifier', 'address' : 0x2E, 'permission' : 'RO', 'translate' : le_register_show,
            'fields' : [
               { 'name' : 'Byte_1', 'offset' : 0, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_2', 'offset' : 8, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_3', 'offset' : 16, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_4', 'offset' : 24, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_5', 'offset' : 32, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_6', 'offset' : 40, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_7', 'offset' : 48, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_8', 'offset' : 56, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_9', 'offset' : 64, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_10', 'offset' : 72, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_11', 'offset' : 80, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_12', 'offset' : 88, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_13', 'offset' : 96, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_14', 'offset' : 104, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_15', 'offset' : 112, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_16', 'offset' : 120, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_17', 'offset' : 128, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_18', 'offset' : 136, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_19', 'offset' : 144, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_20', 'offset' : 152, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_21', 'offset' : 160, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_22', 'offset' : 168, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_23', 'offset' : 176, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_24', 'offset' : 184, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_25', 'offset' : 192, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_26', 'offset' : 200, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_27', 'offset' : 208, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_28', 'offset' : 216, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_29', 'offset' : 224, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_30', 'offset' : 232, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_31', 'offset' : 240, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_32', 'offset' : 248, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_33', 'offset' : 256, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_34', 'offset' : 264, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_19', 'offset' : 272, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_20', 'offset' : 280, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_21', 'offset' : 288, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_22', 'offset' : 296, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_23', 'offset' : 304, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_24', 'offset' : 312, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_25', 'offset' : 320, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_26', 'offset' : 328, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_27', 'offset' : 336, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_28', 'offset' : 344, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_29', 'offset' : 352, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_30', 'offset' : 360, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_31', 'offset' : 368, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_32', 'offset' : 376, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_33', 'offset' : 384, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
            ] } )

DEVICE_INFO_REG = cRegister({'register name' : 'Device Info', 'address' : 0x2F, 'permission' : 'RO', 'translate' : le_register_show,
            'fields' : [
               { 'name' : 'Byte_1', 'offset' : 0, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_2', 'offset' : 8, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_3', 'offset' : 16, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_4', 'offset' : 24, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_5', 'offset' : 32, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_6', 'offset' : 40, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_7', 'offset' : 48, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_8', 'offset' : 56, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_9', 'offset' : 64, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_10', 'offset' : 72, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_11', 'offset' : 80, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_12', 'offset' : 88, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_13', 'offset' : 96, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_14', 'offset' : 104, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_15', 'offset' : 112, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_16', 'offset' : 120, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_17', 'offset' : 128, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_18', 'offset' : 136, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_19', 'offset' : 144, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_20', 'offset' : 152, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_21', 'offset' : 160, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_22', 'offset' : 168, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_23', 'offset' : 176, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_24', 'offset' : 184, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_25', 'offset' : 192, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_26', 'offset' : 200, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_27', 'offset' : 208, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_28', 'offset' : 216, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_29', 'offset' : 224, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_30', 'offset' : 232, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_31', 'offset' : 240, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_32', 'offset' : 248, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_33', 'offset' : 256, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
               { 'name' : 'Byte_34', 'offset' : 264, 'length' : 8, 'value' : 0, 'translate' : charTranslate } ,
            ] } )

PeakCurrent_list = [ 'PeakCurrentType_100PercentIOC' , 'PeakCurrentType_150_110_PercentIOC' , 'PeakCurrentType_200_125_PercentIOC' , 'PeakCurrentType_200_150_PercentIOC' ]

def translate_MaxCurrent(self):
    mySupply = self.register.fields[self.register.fields.index(self) + 3].value

    if (SupplyType_list[mySupply] == 'Variable' ) or (SupplyType_list[mySupply] == 'Fixed' ):
        return (self.value * 10) 
    if (SupplyType_list[mySupply] == 'Battery' ) :
        return (self.value * 250) 

def unit_MaxCurrent(self):
    mySupply = self.register.fields[self.register.fields.index(self) + 3].value

    if (SupplyType_list[mySupply] == 'Variable' ) or (SupplyType_list[mySupply] == 'Fixed' ):
        return 'mA' 
    if (SupplyType_list[mySupply] == 'Battery' ) :
        return 'mW' 

def translate_ExtendCurrent1(self):
    mySupply = self.register.fields[self.register.fields.index(self) -1].value

    if (SupplyType_list[mySupply] == 'Variable' ) or (SupplyType_list[mySupply] == 'Fixed' ):
        return (self.value * 10) 
    if (SupplyType_list[mySupply] == 'Battery' ) :
        return (self.value * 250) 

def revTranslate_ExtendCurrent1(self, val):
    value = int(val)
    mySupply = self.register.fields[self.register.fields.index(self) -1].value

    if (SupplyType_list[mySupply] == 'Variable' ) or (SupplyType_list[mySupply] == 'Fixed' ):
        retval = (value // 10)
        if retval < 0:
            retval = 0
        if retval > ((2**10) -1):
            retval = ((2**10) -1)
        return retval
    if (SupplyType_list[mySupply] == 'Battery' ) :
        retval = (value // 250)
        if retval < 0:
            retval = 0
        if retval > ((2**10) -1):
            retval = ((2**10) -1)
        return (retval)


def unit_ExtendCurrent1(self):
    mySupply = self.register.fields[self.register.fields.index(self) -1].value

    if (SupplyType_list[mySupply] == 'Variable' ) or (SupplyType_list[mySupply] == 'Fixed' ):
        return 'mA' 
    if (SupplyType_list[mySupply] == 'Battery' ) :
        return 'mW' 

def translate_ExtendCurrent2(self):
    mySupply = self.register.fields[self.register.fields.index(self) -2].value

    if (SupplyType_list[mySupply] == 'Variable' ) or (SupplyType_list[mySupply] == 'Fixed' ):
        return (self.value * 10) 
    if (SupplyType_list[mySupply] == 'Battery' ) :
        return (self.value * 250) 


def revTranslate_ExtendCurrent2(self, val):
    value = int(val)
    mySupply = self.register.fields[self.register.fields.index(self) -2].value

    if (SupplyType_list[mySupply] == 'Variable' ) or (SupplyType_list[mySupply] == 'Fixed' ):
        retval = (value // 10)
        if retval < 0:
            retval = 0
        if retval > ((2**10) -1):
            retval = ((2**10) -1)
        return retval
    if (SupplyType_list[mySupply] == 'Battery' ) :
        retval = (value // 250)
        if retval < 0:
            retval = 0
        if retval > ((2**10) -1):
            retval = ((2**10) -1)
        return (retval)


def unit_ExtendCurrent2(self):
    mySupply = self.register.fields[self.register.fields.index(self) -2].value

    if (SupplyType_list[mySupply] == 'Variable' ) or (SupplyType_list[mySupply] == 'Fixed' ):
        return 'mA' 
    if (SupplyType_list[mySupply] == 'Battery' ) :
        return 'mW' 


def revTranslate_MaxCurrent(self, val):
    value = int(val)
    mySupply = self.register.fields[self.register.fields.index(self) + 3].value

    if (SupplyType_list[mySupply] == 'Variable' ) or (SupplyType_list[mySupply] == 'Fixed' ):
        retval = (value // 10)
        if retval < 0:
            retval = 0
        if retval > ((2**10) -1):
            retval = ((2**10) -1)
        return retval
    if (SupplyType_list[mySupply] == 'Battery' ) :
        retval = (value // 250)
        if retval < 0:
            retval = 0
        if retval > ((2**10) -1):
            retval = ((2**10) -1)
        return (retval)


def translate_MaxVoltage(self):
    mySupply = self.register.fields[self.register.fields.index(self) + 1].value

    if SupplyType_list[mySupply] == 'Variable':
        return (self.value * 50) 
    if SupplyType_list[mySupply] == 'Fixed':
        return self.value & 0x3
    if SupplyType_list[mySupply] == 'Battery':
        return (self.value * 50) 

def unit_MaxVoltage(self):
    mySupply = self.register.fields[self.register.fields.index(self) + 1].value

    if SupplyType_list[mySupply] == 'Variable':
        return 'mV' 
    if SupplyType_list[mySupply] == 'Fixed':
        return PeakCurrent_list[self.value & 0x3]
    if SupplyType_list[mySupply] == 'Battery':
        return 'mV' 


def revTranslate_MaxVoltage(self, val):
    value = int(val)
    mySupply = self.register.fields[self.register.fields.index(self) + 1].value

    if SupplyType_list[mySupply] == 'Variable':
        retval = (value // 50)
        if retval < 0:
            retval = 0
        if retval > ((2**10) -1):
            retval = ((2**10) -1)
        return retval
    if SupplyType_list[mySupply] == 'Fixed':
        return (value & 0x3)
    if SupplyType_list[mySupply] == 'Battery':
        retval = (value // 50)
        if retval < 0:
            retval = 0
        if retval > ((2**10) -1):
            retval = ((2**10) -1)
        return retval

def translate_MinVoltage(self):
    return (self.value * 50)


def unit_MinVoltage(self):
    return 'mV'

def revTranslate_MinVoltage(self, val):
    value = int(val)
    retval = (value // 50)
    if retval < 0:
        retval = 0
    if retval > ((2**10) -1):
        retval = ((2**10) -1)
    return retval

TX_Source_list = [ 'Only if Externally Powered' , 'Always Enabled' ]

PP_Switch_PDOnum1_list = [ 'PP_5V (internal)', 'PP_5V (internal)', 'PP_HV (Internal)' , 'PP_HVE (External)' ]
PP_Switch_PDO_list = [ 'PP_HV (Internal)' , 'PP_HVE (External)' ]

def hide_rx_source_cap(self) :
    # starts at zero
    PDOnum = (self.register.fields.index(self) - 8) // 4

    totalPDO = int(self.register.fieldByName('numPDOs').value)

    if totalPDO == 0 :
        return 1

    if totalPDO == 1 :
        if self.register.fields.index(self) < 12 :
           return 0
        else :
           return 1

    if PDOnum < totalPDO :
        return 0
    else :
        return 1


RX_SOURCE_CAP = cRegister({'register name' : 'Rx Source Cap', 'address' : 0x30, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'numPDOs', 'offset' : 0, 'length' : 3, 'value' : 0, 'translate' : decTranslate, 'reverse translate' : decRevTranslate } ,
               { 'name' : 'reserved', 'offset' : 3, 'length' : 5, 'value' : 0 } ,
               { 'name' : 'PDO1: MaxCurrent or Power', 'offset' : 8, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent, 'hide' : hide_rx_source_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO1: Min Voltage or Power', 'offset' : 18, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage, 'hide' : hide_rx_source_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO1: Peak Current', 'offset' : 28, 'length' : 2, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_rx_source_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'reserved', 'offset' : 30, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'PDO1: Dual Role Data', 'offset' : 33, 'length' : 1, 'value' : 0, 'hide' : hide_rx_source_cap, 'translate list' : TrueFalse_list } ,
               { 'name' : 'PDO1: USB Comm Capable', 'offset' : 34, 'length' : 2, 'value' : 0, 'hide' : hide_rx_source_cap, 'translate list' : TrueFalse_list } ,
               { 'name' : 'PDO1: Externally Powered', 'offset' : 35, 'length' : 1, 'value' : 0, 'hide' : hide_rx_source_cap, 'translate list' : TrueFalse_list } ,
               { 'name' : 'PDO1: USB Suspend Supported', 'offset' : 36, 'length' : 1, 'value' : 0, 'hide' : hide_rx_source_cap, 'translate list' : TrueFalse_list } ,
               { 'name' : 'PDO1: Dual Role Power', 'offset' : 37, 'length' : 1, 'value' : 0, 'hide' : hide_rx_source_cap, 'translate list' : TrueFalse_list } ,
               { 'name' : 'PDO1: Supply Type', 'offset' : 38, 'length' : 2, 'value' : 0,'hide' : hide_rx_source_cap, 'translate list' : SupplyType_list } ,
               { 'name' : 'PDO2: MaxCurrent or Power', 'offset' : 40, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent,'hide' : hide_rx_source_cap,'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO2: Min Voltage or Power', 'offset' : 50, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage, 'hide' : hide_rx_source_cap,'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO2: Max Voltage', 'offset' : 60, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_rx_source_cap,'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO2: Supply Type', 'offset' : 70, 'length' : 2, 'value' : 0, 'hide' : hide_rx_source_cap, 'translate list' : SupplyType_list } ,
               { 'name' : 'PDO3: MaxCurrent or Power', 'offset' : 72, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent,'hide' : hide_rx_source_cap,'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO3: Min Voltage or Power', 'offset' : 82, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage,'hide' : hide_rx_source_cap,'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO3: Max Voltage', 'offset' : 92, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_rx_source_cap,'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO3: Supply Type', 'offset' : 102, 'length' : 2, 'value' : 0, 'hide' : hide_rx_source_cap, 'translate list' : SupplyType_list } ,
               { 'name' : 'PDO4: MaxCurrent or Power', 'offset' : 104, 'length' : 10, 'value' : 0,'unit' : unit_MaxCurrent,'hide' : hide_rx_source_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO4: Min Voltage or Power', 'offset' : 114, 'length' : 10, 'value' : 0,'unit' : unit_MinVoltage,'hide' : hide_rx_source_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO4: Max Voltage', 'offset' : 124, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_rx_source_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO4: Supply Type', 'offset' : 134, 'length' : 2, 'value' : 0, 'hide' : hide_rx_source_cap, 'translate list' : SupplyType_list } ,
               { 'name' : 'PDO5: MaxCurrent or Power', 'offset' : 136, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent,'hide' : hide_rx_source_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO5: Min Voltage or Power', 'offset' : 146, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage,'hide' : hide_rx_source_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO5: Max Voltage', 'offset' : 156, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_rx_source_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO5: Supply Type', 'offset' : 166, 'length' : 2, 'value' : 0, 'hide' : hide_rx_source_cap, 'translate list' : SupplyType_list } ,
               { 'name' : 'PDO6: MaxCurrent or Power', 'offset' : 168, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent,'hide' : hide_rx_source_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO6: Min Voltage or Power', 'offset' : 178, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage,'hide' : hide_rx_source_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO6: Max Voltage', 'offset' : 188, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_rx_source_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO6: Supply Type', 'offset' : 198, 'length' : 2, 'value' : 0, 'hide' : hide_rx_source_cap, 'translate list' : SupplyType_list } ,
               { 'name' : 'PDO7: MaxCurrent or Power', 'offset' : 200, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent, 'hide' : hide_rx_source_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO7: Min Voltage or Power', 'offset' : 210, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage,'hide' : hide_rx_source_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO7: Max Voltage', 'offset' : 220, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_rx_source_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO7: Supply Type', 'offset' : 230, 'length' : 2, 'value' : 0, 'hide' : hide_rx_source_cap, 'translate list' : SupplyType_list } ,
            ] } )

def hide_rx_sink_cap(self) :
    # starts at zero
    PDOnum = (self.register.fields.index(self) - 8) // 4

    totalPDO = int(self.register.fieldByName('numPDOs').value)

    if totalPDO == 0 :
        return 1

    if totalPDO == 1 :
        if self.register.fields.index(self) < 12 :
           return 0
        else :
           return 1

    if PDOnum < totalPDO :
        return 0
    else :
        return 1

RX_SINK_CAP = cRegister({'register name' : 'Rx Sink Cap', 'address' : 0x31, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'numPDOs', 'offset' : 0, 'length' : 3, 'value' : 0 , 'translate' : decTranslate, 'reverse translate' : decRevTranslate} ,
               { 'name' : 'reserved', 'offset' : 3, 'length' : 5, 'value' : 0 } ,
               { 'name' : 'PDO1: MaxCurrent or Power', 'offset' : 8, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent, 'hide' : hide_rx_sink_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO1: Min Voltage or Power', 'offset' : 18, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage, 'hide' : hide_rx_sink_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO1: Peak Current', 'offset' : 28, 'length' : 2, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_rx_sink_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'reserved', 'offset' : 30, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'PDO1: Dual Role Data', 'offset' : 33, 'length' : 1, 'value' : 0, 'hide' : hide_rx_sink_cap, 'translate list' : TrueFalse_list } ,
               { 'name' : 'PDO1: USB Comm Capable', 'offset' : 34, 'length' : 2, 'value' : 0, 'hide' : hide_rx_sink_cap, 'translate list' : TrueFalse_list } ,
               { 'name' : 'PDO1: Externally Powered', 'offset' : 35, 'length' : 1, 'value' : 0, 'hide' : hide_rx_sink_cap, 'translate list' : TrueFalse_list } ,
               { 'name' : 'PDO1: Higher Capability', 'offset' : 36, 'length' : 1, 'value' : 0, 'hide' : hide_rx_sink_cap, 'translate list' : TrueFalse_list } ,
               { 'name' : 'PDO1: Dual Role Power', 'offset' : 37, 'length' : 1, 'value' : 0, 'hide' : hide_rx_sink_cap, 'translate list' : TrueFalse_list } ,
               { 'name' : 'PDO1: Supply Type', 'offset' : 38, 'length' : 2, 'value' : 0, 'hide' : hide_rx_sink_cap,  'translate list' : SupplyType_list } ,
               { 'name' : 'PDO2: MaxCurrent or Power', 'offset' : 40, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent, 'hide' : hide_rx_sink_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO2: Min Voltage or Power', 'offset' : 50, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage, 'hide' : hide_rx_sink_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO2: Max Voltage', 'offset' : 60, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_rx_sink_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO2: Supply Type', 'offset' : 70, 'length' : 2, 'value' : 0,  'hide' : hide_rx_sink_cap, 'translate list' : SupplyType_list } ,
               { 'name' : 'PDO3: MaxCurrent or Power', 'offset' : 72, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent, 'hide' : hide_rx_sink_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO3: Min Voltage or Power', 'offset' : 82, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage, 'hide' : hide_rx_sink_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO3: Max Voltage', 'offset' : 92, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_rx_sink_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO3: Supply Type', 'offset' : 102, 'length' : 2, 'value' : 0,  'hide' : hide_rx_sink_cap, 'translate list' : SupplyType_list } ,
               { 'name' : 'PDO4: MaxCurrent or Power', 'offset' : 104, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent,  'hide' : hide_rx_sink_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO4: Min Voltage or Power', 'offset' : 114, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage, 'hide' : hide_rx_sink_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO4: Max Voltage', 'offset' : 124, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage,'hide' : hide_rx_sink_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO4: Supply Type', 'offset' : 134, 'length' : 2, 'value' : 0, 'hide' : hide_rx_sink_cap,  'translate list' : SupplyType_list } ,
               { 'name' : 'PDO5: MaxCurrent or Power', 'offset' : 136, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent, 'hide' : hide_rx_sink_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO5: Min Voltage or Power', 'offset' : 146, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage, 'hide' : hide_rx_sink_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO5: Max Voltage', 'offset' : 156, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage,'hide' : hide_rx_sink_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO5: Supply Type', 'offset' : 166, 'length' : 2, 'value' : 0, 'hide' : hide_rx_sink_cap,  'translate list' : SupplyType_list } ,
               { 'name' : 'PDO6: MaxCurrent or Power', 'offset' : 168, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent, 'hide' : hide_rx_sink_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO6: Min Voltage or Power', 'offset' : 178, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage, 'hide' : hide_rx_sink_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO6: Max Voltage', 'offset' : 188, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_rx_sink_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO6: Supply Type', 'offset' : 198, 'length' : 2, 'value' : 0, 'hide' : hide_rx_sink_cap,  'translate list' : SupplyType_list } ,
               { 'name' : 'PDO7: MaxCurrent or Power', 'offset' : 200, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent, 'hide' : hide_rx_sink_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO7: Min Voltage or Power', 'offset' : 210, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage, 'hide' : hide_rx_sink_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO7: Max Voltage', 'offset' : 220, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_rx_sink_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO7: Supply Type', 'offset' : 230, 'length' : 2, 'value' : 0, 'hide' : hide_rx_sink_cap,  'translate list' : SupplyType_list } ,
            ] } )

def hide_tx_source_cap(self) :
    # starts at zero
    PDOnum = (self.register.fields.index(self) - 2) // 6

    totalPDO = int(self.register.fieldByName('numPDOs').value)
    if PDOnum < totalPDO :
        return 0
    else :
        return 1

# PDO1 is always enabled regardless of Enable Mask setting
TX_Source_list_pdo1 = [ 'Always Enabled' , 'Always Enabled' ]


TX_SOURCE_CAP = cRegister({'register name' : 'Tx Source Cap', 'address' : 0x32, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'numPDOs', 'offset' : 0, 'length' : 3, 'value' : 0, 'translate' : decTranslate, 'reverse translate' : decRevTranslate } ,
               { 'name' : 'reserved', 'offset' : 3, 'length' : 6, 'value' : 0 } ,
               { 'name' : 'Enable Mask PDO1', 'offset' : 9, 'length' : 1, 'value' : 0, 'hide' : hide_tx_source_cap, 'translate list' : TX_Source_list_pdo1 } ,               
               { 'name' : 'PP Switch for PDO1', 'offset' : 16, 'length' : 2, 'value' : 0, 'hide' : hide_tx_source_cap, 'translate list' : PP_Switch_PDOnum1_list } ,               
               { 'name' : 'PDO1: MaxCurrent or Power', 'offset' : 24, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent, 'hide' : hide_tx_source_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO1: Min Voltage or Power', 'offset' : 34, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage, 'hide' : hide_tx_source_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO1: Max Voltage', 'offset' : 44, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_tx_source_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO1: Supply Type', 'offset' : 54, 'length' : 2, 'value' : 0,  'hide' : hide_tx_source_cap, 'translate list' : SupplyType_list } ,
               { 'name' : 'Enable Mask PDO2', 'offset' : 10, 'length' : 1, 'value' : 0, 'hide' : hide_tx_source_cap, 'translate list' : TX_Source_list  } ,               
               { 'name' : 'PP Switch for PDO2', 'offset' : 18, 'length' : 1, 'value' : 0, 'hide' : hide_tx_source_cap, 'translate list' : PP_Switch_PDO_list  } ,               
               { 'name' : 'PDO2: MaxCurrent or Power', 'offset' : 56, 'length' : 10, 'value' : 0,'unit' : unit_MaxCurrent, 'hide' : hide_tx_source_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent  } ,
               { 'name' : 'PDO2: Min Voltage or Power', 'offset' : 66, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage, 'hide' : hide_tx_source_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO2: Max Voltage', 'offset' : 76, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_tx_source_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO2: Supply Type', 'offset' : 86, 'length' : 2, 'value' : 0, 'hide' : hide_tx_source_cap,  'translate list' : SupplyType_list } ,
               { 'name' : 'Enable Mask PDO3', 'offset' : 11, 'length' : 1, 'value' : 0, 'hide' : hide_tx_source_cap, 'translate list' : TX_Source_list  } ,               
               { 'name' : 'PP Switch for PDO3', 'offset' : 19, 'length' : 1, 'value' : 0, 'hide' : hide_tx_source_cap, 'translate list' : PP_Switch_PDO_list  } ,               
               { 'name' : 'PDO3: MaxCurrent or Power', 'offset' : 88, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent, 'hide' : hide_tx_source_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO3: Min Voltage or Power', 'offset' : 98, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage, 'hide' : hide_tx_source_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO3: Max Voltage', 'offset' : 108, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_tx_source_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO3: Supply Type', 'offset' : 118, 'length' : 2, 'value' : 0,  'hide' : hide_tx_source_cap, 'translate list' : SupplyType_list } ,
               { 'name' : 'Enable Mask PDO4', 'offset' : 12, 'length' : 1, 'value' : 0, 'hide' : hide_tx_source_cap, 'translate list' : TX_Source_list  } ,               
               { 'name' : 'PP Switch for PDO4', 'offset' : 20, 'length' : 1, 'value' : 0, 'hide' : hide_tx_source_cap, 'translate list' : PP_Switch_PDO_list  } ,               
               { 'name' : 'PDO4: MaxCurrent or Power', 'offset' : 120, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent, 'hide' : hide_tx_source_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO4: Min Voltage or Power', 'offset' : 130, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage, 'hide' : hide_tx_source_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO4: Max Voltage', 'offset' : 148, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_tx_source_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO4: Supply Type', 'offset' : 150, 'length' : 2, 'value' : 0, 'hide' : hide_tx_source_cap,  'translate list' : SupplyType_list } ,
               { 'name' : 'Enable Mask PDO5', 'offset' : 13, 'length' : 1, 'value' : 0, 'hide' : hide_tx_source_cap, 'translate list' : TX_Source_list  } ,               
               { 'name' : 'PP Switch for PDO5', 'offset' : 21, 'length' : 1, 'value' : 0, 'hide' : hide_tx_source_cap, 'translate list' : PP_Switch_PDO_list  } ,               
               { 'name' : 'PDO5: MaxCurrent or Power', 'offset' : 152, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent, 'hide' : hide_tx_source_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO5: Min Voltage or Power', 'offset' : 162, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage, 'hide' : hide_tx_source_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO5: Max Voltage', 'offset' : 172, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_tx_source_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO5: Supply Type', 'offset' : 182, 'length' : 2, 'value' : 0, 'hide' : hide_tx_source_cap,  'translate list' : SupplyType_list } ,
               { 'name' : 'Enable Mask PDO6', 'offset' : 14, 'length' : 1, 'value' : 0, 'hide' : hide_tx_source_cap, 'translate list' : TX_Source_list  } ,               
               { 'name' : 'PP Switch for PDO6', 'offset' : 22, 'length' : 1, 'value' : 0, 'hide' : hide_tx_source_cap, 'translate list' : PP_Switch_PDO_list  } ,               
               { 'name' : 'PDO6: MaxCurrent or Power', 'offset' : 184, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent, 'hide' : hide_tx_source_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO6: Min Voltage or Power', 'offset' : 194, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage, 'hide' : hide_tx_source_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO6: Max Voltage', 'offset' : 204, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_tx_source_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO6: Supply Type', 'offset' : 214, 'length' : 2, 'value' : 0, 'hide' : hide_tx_source_cap,  'translate list' : SupplyType_list } ,
               { 'name' : 'Enable Mask PDO7', 'offset' : 15, 'length' : 1, 'value' : 0, 'hide' : hide_tx_source_cap, 'translate list' : TX_Source_list  } ,               
               { 'name' : 'PP Switch for PDO7', 'offset' : 23, 'length' : 1, 'value' : 0, 'hide' : hide_tx_source_cap, 'translate list' : PP_Switch_PDO_list  } ,               
               { 'name' : 'PDO7: MaxCurrent or Power', 'offset' : 216, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent, 'hide' : hide_tx_source_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO7: Min Voltage or Power', 'offset' : 226, 'length' : 10, 'value' : 0, 'unit' : unit_MinVoltage, 'hide' : hide_tx_source_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO7: Max Voltage', 'offset' : 236, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_tx_source_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO7: Supply Type', 'offset' : 246, 'length' : 2, 'value' : 0, 'hide' : hide_tx_source_cap,  'translate list' : SupplyType_list } ,
            ] } )

def hide_tx_sink_cap(self) :
    # starts at zero
    PDOnum = (self.register.fields.index(self) - 2) // 9

    totalPDO = int(self.register.fieldByName('numPDOs').value)
    if PDOnum < totalPDO :
        return 0
    else :
        return 1

TX_SINK_CAP = cRegister({'register name' : 'Tx Sink Cap', 'address' : 0x33, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'numPDOs', 'offset' : 0, 'length' : 3, 'value' : 0 , 'translate' : decTranslate, 'reverse translate' : decRevTranslate} ,
               { 'name' : 'reserved', 'offset' : 3, 'length' : 5, 'value' : 0 } ,
               { 'name' : 'PDO1: Operating Current or Power', 'offset' : 8, 'length' : 10, 'value' : 0,  'unit' : unit_MaxCurrent, 'hide' : hide_tx_sink_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO1: Min Voltage or Power', 'offset' : 18, 'length' : 10, 'value' : 0,   'unit' : unit_MinVoltage, 'hide' : hide_tx_sink_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO1: Max Voltage', 'offset' : 28, 'length' : 10, 'value' : 0,  'unit' : unit_MaxVoltage, 'hide' : hide_tx_sink_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO1: Supply Type', 'offset' : 38, 'length' : 2, 'value' : 0,  'hide' : hide_tx_sink_cap, 'translate list' : SupplyType_list } ,
               { 'name' : 'PDO1: MaxCurrent or Power', 'offset' : 232, 'length' : 10, 'value' : 0,  'unit' : unit_ExtendCurrent1, 'hide' : hide_tx_sink_cap, 'translate' : translate_ExtendCurrent1, 'reverse translate' : revTranslate_ExtendCurrent1 } ,
               { 'name' : 'PDO1: MinCurrent or Power', 'offset' : 242, 'length' : 10, 'value' : 0,  'unit' : unit_ExtendCurrent2, 'hide' : hide_tx_sink_cap, 'translate' : translate_ExtendCurrent2, 'reverse translate' : revTranslate_ExtendCurrent2 } ,
               { 'name' : 'Reserved', 'offset' : 252, 'length' : 10, 'value' : 0 } ,
               { 'name' : 'PDO1: Ask For Max', 'offset' : 262, 'length' : 1, 'value' : 0, 'hide' : hide_tx_sink_cap, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 263, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'PDO2: Operating Current or Power', 'offset' : 40, 'length' : 10, 'value' : 0,  'unit' : unit_MaxCurrent, 'hide' : hide_tx_sink_cap,  'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO2: Min Voltage or Power', 'offset' : 50, 'length' : 10, 'value' : 0,  'unit' : unit_MinVoltage, 'hide' : hide_tx_sink_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO2: Max Voltage', 'offset' : 60, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_tx_sink_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO2: Supply Type', 'offset' : 70, 'length' : 2, 'value' : 0, 'hide' : hide_tx_sink_cap, 'translate list' : SupplyType_list } ,
               { 'name' : 'PDO2: MaxCurrent or Power', 'offset' : 264, 'length' : 10, 'value' : 0,   'unit' : unit_ExtendCurrent1, 'hide' : hide_tx_sink_cap, 'translate' : translate_ExtendCurrent1, 'reverse translate' : revTranslate_ExtendCurrent1  } ,
               { 'name' : 'PDO2: MinCurrent or Power', 'offset' : 274, 'length' : 10, 'value' : 0,  'unit' : unit_ExtendCurrent2, 'hide' : hide_tx_sink_cap, 'translate' : translate_ExtendCurrent2, 'reverse translate' : revTranslate_ExtendCurrent2 } ,
               { 'name' : 'Reserved', 'offset' : 284, 'length' : 10, 'value' : 0 } ,
               { 'name' : 'PDO2: Ask For Max', 'offset' : 294, 'length' : 1, 'value' : 0, 'hide' : hide_tx_sink_cap, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 295, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'PDO3: Operating Current or Power', 'offset' : 72, 'length' : 10, 'value' : 0,  'unit' : unit_MaxCurrent, 'hide' : hide_tx_sink_cap,  'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO3: Min Voltage or Power', 'offset' : 82, 'length' : 10, 'value' : 0,  'unit' : unit_MinVoltage, 'hide' : hide_tx_sink_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO3: Max Voltage', 'offset' : 92, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_tx_sink_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO3: Supply Type', 'offset' : 102, 'length' : 2, 'value' : 0,'hide' : hide_tx_sink_cap,  'translate list' : SupplyType_list } ,
               { 'name' : 'PDO3: MaxCurrent or Power', 'offset' : 296, 'length' : 10, 'value' : 0,   'unit' : unit_ExtendCurrent1, 'hide' : hide_tx_sink_cap, 'translate' : translate_ExtendCurrent1, 'reverse translate' : revTranslate_ExtendCurrent1   } ,
               { 'name' : 'PDO3: MinCurrent or Power', 'offset' : 306, 'length' : 10, 'value' : 0,  'unit' : unit_ExtendCurrent2, 'hide' : hide_tx_sink_cap, 'translate' : translate_ExtendCurrent2, 'reverse translate' : revTranslate_ExtendCurrent2  } ,
               { 'name' : 'Reserved', 'offset' : 316, 'length' : 10, 'value' : 0 } ,
               { 'name' : 'PDO3: Ask For Max', 'offset' : 326, 'length' : 1, 'value' : 0, 'hide' : hide_tx_sink_cap, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 327, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'PDO4: Operating Current or Power', 'offset' : 104, 'length' : 10, 'value' : 0,  'unit' : unit_MaxCurrent, 'hide' : hide_tx_sink_cap,  'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO4: Min Voltage or Power', 'offset' : 114, 'length' : 10, 'value' : 0,  'unit' : unit_MinVoltage, 'hide' : hide_tx_sink_cap, 'translate' : translate_MinVoltage,  'reverse translate' : revTranslate_MinVoltage} ,
               { 'name' : 'PDO4: Max Voltage', 'offset' : 124, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_tx_sink_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO4: Supply Type', 'offset' : 134, 'length' : 2, 'value' : 0,'hide' : hide_tx_sink_cap,  'translate list' : SupplyType_list } ,
               { 'name' : 'PDO4: MaxCurrent or Power', 'offset' : 328, 'length' : 10, 'value' : 0,  'unit' : unit_ExtendCurrent1, 'hide' : hide_tx_sink_cap, 'translate' : translate_ExtendCurrent1, 'reverse translate' : revTranslate_ExtendCurrent1 } ,
               { 'name' : 'PDO4: MinCurrent or Power', 'offset' : 338, 'length' : 10, 'value' : 0,  'unit' : unit_ExtendCurrent2, 'hide' : hide_tx_sink_cap, 'translate' : translate_ExtendCurrent2, 'reverse translate' : revTranslate_ExtendCurrent2 } ,
               { 'name' : 'Reserved', 'offset' : 348, 'length' : 10, 'value' : 0 } ,
               { 'name' : 'PDO4: Ask For Max', 'offset' : 358, 'length' : 1, 'value' : 0, 'hide' : hide_tx_sink_cap, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 359, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'PDO5: Operating Current or Power', 'offset' : 136, 'length' : 10, 'value' : 0,  'unit' : unit_MaxCurrent, 'hide' : hide_tx_sink_cap,  'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO5: Min Voltage or Power', 'offset' : 146, 'length' : 10, 'value' : 0,  'unit' : unit_MinVoltage, 'hide' : hide_tx_sink_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO5: Max Voltage', 'offset' : 156, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_tx_sink_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO5: Supply Type', 'offset' : 166, 'length' : 2, 'value' : 0,'hide' : hide_tx_sink_cap,  'translate list' : SupplyType_list } ,
               { 'name' : 'PDO5: MaxCurrent or Power', 'offset' : 360, 'length' : 10, 'value' : 0, 'unit' : unit_ExtendCurrent1, 'hide' : hide_tx_sink_cap, 'translate' : translate_ExtendCurrent1, 'reverse translate' : revTranslate_ExtendCurrent1 } ,
               { 'name' : 'PDO5: MinCurrent or Power', 'offset' : 370, 'length' : 10, 'value' : 0,  'unit' : unit_ExtendCurrent2, 'hide' : hide_tx_sink_cap, 'translate' : translate_ExtendCurrent2, 'reverse translate' : revTranslate_ExtendCurrent2 } ,
               { 'name' : 'Reserved', 'offset' : 380, 'length' : 10, 'value' : 0 } ,
               { 'name' : 'PDO5: Ask For Max', 'offset' : 390, 'length' : 1, 'value' : 0, 'hide' : hide_tx_sink_cap, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 391, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'PDO6: Operating Current or Power', 'offset' : 168, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent, 'hide' : hide_tx_sink_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO6: Min Voltage or Power', 'offset' : 178, 'length' : 10, 'value' : 0,  'unit' : unit_MinVoltage, 'hide' : hide_tx_sink_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO6: Max Voltage', 'offset' : 188, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_tx_sink_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO6: Supply Type', 'offset' : 198, 'length' : 2, 'value' : 0,'hide' : hide_tx_sink_cap,  'translate list' : SupplyType_list } ,
               { 'name' : 'PDO6: MaxCurrent or Power', 'offset' : 392, 'length' : 10, 'value' : 0,  'unit' : unit_ExtendCurrent1, 'hide' : hide_tx_sink_cap, 'translate' : translate_ExtendCurrent1, 'reverse translate' : revTranslate_ExtendCurrent1 } ,
               { 'name' : 'PDO6: MinCurrent or Power', 'offset' : 402, 'length' : 10, 'value' : 0,  'unit' : unit_ExtendCurrent2, 'hide' : hide_tx_sink_cap, 'translate' : translate_ExtendCurrent2, 'reverse translate' : revTranslate_ExtendCurrent2 } ,
               { 'name' : 'Reserved', 'offset' : 412, 'length' : 10, 'value' : 0 } ,
               { 'name' : 'PDO6: Ask For Max', 'offset' : 422, 'length' : 1, 'value' : 0, 'hide' : hide_tx_sink_cap, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 423, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'PDO7: Operating Current or Power', 'offset' : 200, 'length' : 10, 'value' : 0, 'unit' : unit_MaxCurrent, 'hide' : hide_tx_sink_cap, 'translate' : translate_MaxCurrent, 'reverse translate' : revTranslate_MaxCurrent } ,
               { 'name' : 'PDO7: Min Voltage or Power', 'offset' : 210, 'length' : 10, 'value' : 0,  'unit' : unit_MinVoltage, 'hide' : hide_tx_sink_cap, 'translate' : translate_MinVoltage, 'reverse translate' : revTranslate_MinVoltage } ,
               { 'name' : 'PDO7: Max Voltage', 'offset' : 220, 'length' : 10, 'value' : 0, 'unit' : unit_MaxVoltage, 'hide' : hide_tx_sink_cap, 'translate' : translate_MaxVoltage, 'reverse translate' : revTranslate_MaxVoltage } ,
               { 'name' : 'PDO7: Supply Type', 'offset' : 230, 'length' : 2, 'value' : 0, 'hide' : hide_tx_sink_cap, 'translate list' : SupplyType_list } ,
               { 'name' : 'PDO7: MaxCurrent or Power', 'offset' : 424, 'length' : 10, 'value' : 0, 'unit' : unit_ExtendCurrent1, 'hide' : hide_tx_sink_cap, 'translate' : translate_ExtendCurrent1, 'reverse translate' : revTranslate_ExtendCurrent1  } ,
               { 'name' : 'PDO7: MinCurrent or Power', 'offset' : 434, 'length' : 10, 'value' : 0,  'unit' : unit_ExtendCurrent2, 'hide' : hide_tx_sink_cap, 'translate' : translate_ExtendCurrent2, 'reverse translate' : revTranslate_ExtendCurrent2 } ,
               { 'name' : 'Reserved', 'offset' : 444, 'length' : 10, 'value' : 0 } ,
               { 'name' : 'PDO7: Ask For Max', 'offset' : 454, 'length' : 1, 'value' : 0, 'hide' : hide_tx_sink_cap, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 455, 'length' : 1, 'value' : 0 } ,
            ] } )

def translate_MaxCurrent(self):
    mySupply = self.register.fieldByName('Supply Type').value

    if (SupplyType_list[mySupply] == 'Variable' ) or (SupplyType_list[mySupply] == 'Fixed' ):
        return str(self.value * 10) + ' mA (Max Current)'
    if (SupplyType_list[mySupply] == 'Battery' ) :
        return str(self.value * 250) + ' mW (Max Power)'

def translate_MaxVoltage(self):
    return str(self.value * 50) + ' mV'

def translate_MinVoltage(self):
    mySupply = self.register.fieldByName('Supply Type').value
    if SupplyType_list[mySupply] == 'Variable':
        return str(self.value * 50) + ' mV (Min Voltage)'
    if SupplyType_list[mySupply] == 'Fixed':
        return None
    if SupplyType_list[mySupply] == 'Battery':
        return str(self.value * 250) + ' mW (Min Power)'


SupplyType_list = ['Fixed', 'Battery', 'Variable']

ACTIVE_CONTRACT_PDO = cRegister({'register name' : 'Active PDO', 'address' : 0x34, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'MaxCurrent or Power', 'offset' : 0, 'length' : 10, 'value' : 0, 'translate' : translate_MaxCurrent } ,
               { 'name' : 'Min Voltage or Power', 'offset' : 10, 'length' : 10, 'value' : 0, 'translate' : translate_MaxVoltage } ,
               { 'name' : 'Max Voltage', 'offset' : 20, 'length' : 10, 'value' : 0, 'translate' : translate_MinVoltage } ,
               { 'name' : 'Supply Type', 'offset' : 30, 'length' : 2, 'value' : 0, 'translate list' : SupplyType_list } ,
               { 'name' : 'Peak current', 'offset' : 32, 'length' : 2, 'value' : 0, 'translate list' : PeakCurrent_list } ,
               { 'name' : 'Reserved', 'offset' : 34, 'length' : 4, 'value' : 0 } ,
               { 'name' : 'USBCommCapable', 'offset' : 38, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Externally Powred', 'offset' : 39, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'USBSuspendSupported', 'offset' : 40, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Dual Role', 'offset' : 41, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 42, 'length' : 6, 'value' : 0 } ,
            ] } )

ACTIVE_CONTRACT_RDO = cRegister({'register name' : 'Active RDO', 'address' : 0x35, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'Max/Min Operating Current or Power', 'offset' : 0, 'length' : 10, 'value' : 0, 'translate' : translate_current } ,
               { 'name' : 'Operating Current or Power', 'offset' : 10, 'length' : 10, 'value' : 0, 'translate' : translate_current } ,
               { 'name' : 'Reserved', 'offset' : 20, 'length' : 4, 'value' : 0 } ,
               { 'name' : 'No USB Suspend', 'offset' : 24, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'USB Communications Capable', 'offset' : 25, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Capability Mismatch', 'offset' : 26, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Give Back Flag', 'offset' : 27, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Object Position', 'offset' : 28, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 31, 'length' : 1, 'value' : 0 } ,
            ] } )

SINK_REQUEST_RDO = cRegister({'register name' : 'Sink Request RDO', 'address' : 0x36, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'Max/Min Operating Current or Power', 'offset' : 0, 'length' : 10, 'value' : 0, 'translate' : translate_current } ,
               { 'name' : 'Operating Current or Power', 'offset' : 10, 'length' : 10, 'value' : 0, 'translate' : translate_current } ,
               { 'name' : 'Reserved', 'offset' : 20, 'length' : 4, 'value' : 0 } ,
               { 'name' : 'No USB Suspend', 'offset' : 24, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'USB Communications Capable', 'offset' : 25, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Capability Mismatch', 'offset' : 26, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Give Back Flag', 'offset' : 27, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Object Position', 'offset' : 28, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 31, 'length' : 1, 'value' : 0 } ,
            ] } )


OfferPriority_list = [ 'Choose highest current offer' , 'Choose highest voltage offer' , 'Choose highest power offer', 'reserved']
NoUSBSusp_list = [ 'Allow USB Suspend (0)' , 'Do not allow USB Suspend (1)' ]

def translate_power(self):
    return (str(250*self.value) + ' mW')

def translate_voltage(self):
    return str(self.value * 50) + ' mV'


AUTONEGOTIATE_SINK = cRegister({'register name' : 'Autonegotiate Sink', 'address' : 0x37, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Autonegotiate Enable', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Use Battery PDO', 'offset' : 1, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Use Variable PDO', 'offset' : 2, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'USB Comm Capable', 'offset' : 3, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Offer Priority', 'offset' : 4, 'length' : 2, 'value' : 0, 'translate list' : OfferPriority_list } ,              
               { 'name' : 'NoUSBSusp', 'offset' : 6, 'length' : 1, 'value' : 0, 'translate list' : NoUSBSusp_list } ,
               { 'name' : 'GiveBack', 'offset' : 7, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Operating Power', 'offset' : 8, 'length' : 10, 'value' : 0, 'translate' : translate_power} ,
               { 'name' : 'Max Operating Power', 'offset' : 18, 'length' : 10, 'value' : 0, 'translate' : translate_power} ,
               { 'name' : 'reserved', 'offset' : 28, 'length' : 12, 'value' : 0 } ,
               { 'name' : 'Operating Current', 'offset' : 40, 'length' : 10, 'value' : 0, 'translate' : translate_current} ,
               { 'name' : 'Max Operating Current', 'offset' : 50, 'length' : 10, 'value' : 0, 'translate' : translate_current} ,
               { 'name' : 'reserved', 'offset' : 60, 'length' : 12, 'value' : 0 } ,
               { 'name' : 'Battery PDO: Max Power', 'offset' : 72, 'length' : 10, 'value' : 0, 'translate' : translate_power } ,
               { 'name' : 'Battery PDO: Max Voltage', 'offset' : 82, 'length' : 10, 'value' : 0, 'translate' : translate_voltage } ,
               { 'name' : 'reserved', 'offset' : 92, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Battery PDO: Min Power', 'offset' : 94, 'length' : 10, 'value' : 0, 'translate' : translate_power } ,
               { 'name' : 'Non-Battery PDO: MaxCurrent', 'offset' : 104, 'length' : 10, 'value' : 0, 'translate' : translate_current } ,
               { 'name' : 'Non-Battery PDO: Max Voltage', 'offset' : 114, 'length' : 10, 'value' : 0, 'translate' : translate_voltage } ,
               { 'name' : 'Non-Battery PDO: Peak Current', 'offset' : 124, 'length' : 2, 'value' : 0, 'translate list' : PeakCurrent_list } ,
               { 'name' : 'Non-Battery PDO: Min Voltage', 'offset' : 126, 'length' : 10, 'value' : 0, 'translate' : translate_voltage } ,
            ] } )


svid_Dict = { 0x0451 : 'Texas Instruments', 0xFF01 : 'Display Port', 0x8086 : 'Intel (0x8086)', 0x8087 : 'Intel (0x8087)' }

def svidTranslate(self):
    try:
        return '%s (%s)' %(str(hexTranslate(self)), svid_Dict[self.value])
    except KeyError:
        return '%s (%s)' %(str(hexTranslate(self)), 'unknown')


ALT_MODE_ENTRY = cRegister({'register name' : 'Alternate Mode Entry', 'address' : 0x38, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Highest Priority SVID', 'offset' : 0, 'length' : 16, 'value' : 0 , 'translate' : svidTranslate, 'reverse translate' : hexRevTranslate} ,
               { 'name' : 'Highest Priority mode', 'offset' : 16, 'length' : 8, 'value' : 0, 'translate' : decTranslate, 'reverse translate' : decRevTranslate } ,
               { 'name' : 'Reserved', 'offset' : 24, 'length' : 8, 'value' : 0 } ,
               { 'name' : 'Second Priority SVID', 'offset' : 32, 'length' : 16, 'value' : 0 , 'translate' : svidTranslate, 'reverse translate' : hexRevTranslate} ,
               { 'name' : 'Second Priority mode', 'offset' : 48, 'length' : 8, 'value' : 0, 'translate' : decTranslate, 'reverse translate' : decRevTranslate } ,
               { 'name' : 'Reserved', 'offset' : 56, 'length' : 8, 'value' : 0 } ,
               { 'name' : 'Lowest Priority SVID', 'offset' : 64, 'length' : 16, 'value' : 0 , 'translate' : svidTranslate, 'reverse translate' : hexRevTranslate} ,
               { 'name' : 'Lowest Priority mode', 'offset' : 80, 'length' : 8, 'value' : 0, 'translate' : decTranslate, 'reverse translate' : decRevTranslate } ,
               { 'name' : 'Reserved', 'offset' : 88, 'length' : 8, 'value' : 0 } ,
            ] } )


BC12Status_list = ['SDP', 'Res', 'CCP', 'DDP']
TypeCCurrent_list = ['USB Def', '1.5A', '3A', 'PD contract']
SourceSink_list = ['TPS65982 is Source', 'TPS65982 is sink']


PWR_STATUS = cRegister({'register name' : 'Power Status', 'address' : 0x3F, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'PowerConnection', 'offset' : 0, 'length' : 1, 'value' : 0 , 'translate list' : Connect_list} ,
               { 'name' : 'SourceSink', 'offset' : 1, 'length' : 1, 'value' : 0 , 'translate list' : SourceSink_list} ,
               { 'name' : 'Type-C Current', 'offset' : 2, 'length' : 2, 'value' : 0 , 'translate list' : TypeCCurrent_list} ,
               { 'name' : 'BC12Detection', 'offset' : 4, 'length' : 1, 'value' : 0 , 'translate list' : EnabledDisabled_list} ,
               { 'name' : 'BC12Status', 'offset' : 5, 'length' : 2, 'value' : 0 , 'translate list' : BC12Status_list} ,
               { 'name' : 'reserved', 'offset' : 7, 'length' : 9, 'value' : 0 } ,
            ] } )                             

HardReset_list = [ 
    'HardReset_None', 
    'HardReset_ReceivedFromFarEnd', 
    'HardReset_RequestbyHost', 
    'HardReset_RequiredByPolicyEngine_Invalid_DR_Swap', 
    'HardReset_RequiredByPolicyEngine_DischargeFailed', 
    'HardReset_RequiredByPolicyEngine_NoResponseTimeOut', 
    'HardReset_RequiredByPolicyEngine_SendSoftReset',
    'HardReset_RequiredByPolicyEngine_Sink_SelectCapability',
    'HardReset_RequiredByPolicyEngine_Sink_TransitionSink',
    'HardReset_RequiredByPolicyEngine_Sink_WaitForCapabilities', 
    'HardReset_RequiredByPolicyEngine_SoftReset', 
    'HardReset_RequiredByPolicyEngine_SourceOnTimeout', 
    'HardReset_RequiredByPolicyEngine_Source_CapabilityResponse', 
    'HardReset_RequiredByPolicyEngine_Source_SendCapabilities',
    'HardReset_RequiredByPolicyEngine_SourcingFault', 
    'HardReset_RequiredByPolicyEngine_UnableToSource', 
    'HardReset_Reserved_0x26'
    ]

SoftReset_list = [ 
    'SoftResetType_None', 
    'SoftResetType_FromOtherDevice',
    'SoftResetType_Reserved_0x2',
    'SoftResetType_ExpectedGoodCRC',
    'SoftResetType_InvalidSourceCapMessage',
    'SoftResetType_OutOfRetries',
    'SoftResetType_UnexpectedMessage_Accept',
    'SoftResetType_Reserved_0x7',
    'SoftResetType_UnexpectedMessage_GetSinkCap',
    'SoftResetType_UnexpectedMessage_GetSourceCap',
    'SoftResetType_UnexpectedMessage_GotoMin',
    'SoftResetType_UnexpectedMessage_PS_RDY',
    'SoftResetType_UnexpectedMessage_Ping', 
    'SoftResetType_UnexpectedMessage_Reject', 
    'SoftResetType_UnexpectedMessage_Request',
    'SoftResetType_UnexpectedMessage_SinkCapabilities',
    'SoftResetType_UnexpectedMessage_SourceCapabilities',
    'SoftResetType_UnexpectedMessage_Swap', 
    'SoftResetType_UnexpectedMessage_Wait', 
    'SoftResetType_UnknownMessage_Control', 
    'SoftResetType_UnknownMessage_Data', 
    'SoftResetType_InitializePlug_SOP_Prime', 
    'SoftResetType_InitializePlug_SOP_DPrime',
    ]

CC_Pullup_list = [ 'Not in CC pull-down mode / no CC pull-up detected','USB Default current','1.5A current','3A current' ]

PortType_list = ['Consumer/Provider','Consumer','Provider','Provider/Consumer' ]

Present_Role_list = ['Sink', 'Source']

plugtype_list = [ 'USB type-C fully featured plug', 'USB2.0 Type-C plug' ]

PD_STATUS = cRegister({'register name' : 'PD Status', 'address' : 0x40, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'PlugDetails', 'offset' : 0, 'length' : 2, 'value' : 0, 'translate list' : plugtype_list } ,
               { 'name' : 'CCPullUp', 'offset' : 2, 'length' : 2, 'value' : 0, 'translate list' : CC_Pullup_list } ,
               { 'name' : 'PortType', 'offset' : 4, 'length' : 2, 'value' : 0, 'translate list' : PortType_list } ,
               { 'name' : 'PresentRole', 'offset' : 6, 'length' : 1, 'value' : 0, 'translate list' : Present_Role_list } ,
               { 'name' : 'reserved', 'offset' : 7, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'SoftResetType', 'offset' : 8, 'length' : 5, 'value' : 0, 'translate list' : SoftReset_list } ,
               { 'name' : 'reserved', 'offset' : 13, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'HardResetType', 'offset' : 16, 'length' : 6, 'value' : 0, 'translate list' : HardReset_list } ,
               { 'name' : 'reserved', 'offset' : 22, 'length' : 10, 'value' : 0 } ,
            ] } )                             


def translate_IDO(self):
    numIDO = self.register.fieldByName('Num Valid SOP IDOs').value
    if (self.offset  < (numIDO * 32 + 8)) :
        return str(hexTranslate(self))

def translate_primeIDO(self):
    numIDO = self.register.fieldByName('Num Valid SOP Prime IDOs').value
    if (self.offset  < (numIDO * 32 + 200)) :
        return str(hexTranslate(self))

def translate_genIDO(self):
    numIDO = self.register.fieldByName('NumValidIDOs').value
    if (self.offset  < (numIDO * 32 + 8)) :
        return str(hexTranslate(self))


prodtype_list = [ 'Undefined', 'Hub', 'Peripheral', 'Passive Cable', 'Active Cable', 'Alternate Mode Adapter' ]

def test_svidTranslate(self):
    numIDO = self.register.fieldByName('Num Valid SOP IDOs').value
    if (self.offset  < (numIDO * 32 + 8)) :
        return svidTranslate(self)        

def test_TrueFalse(self):
    numIDO = self.register.fieldByName('Num Valid SOP IDOs').value
    if (self.offset  < (numIDO * 32 + 8)) :
        return TrueFalse_list[self.value]        

def test_prodtype(self):
    numIDO = self.register.fieldByName('Num Valid SOP IDOs').value
    if (self.offset  < (numIDO * 32 + 8)) :
        if self.value < len(prodtype_list):
            return prodtype_list[self.value]
        else:
            return 'reserved (%s)' %(str(self.value))

def test_bcd(self):
    numIDO = self.register.fieldByName('Num Valid SOP IDOs').value
    if (self.offset  < (numIDO * 32 + 8)) :
        return str(hexTranslate(self))

def test_prodid(self):
    numIDO = self.register.fieldByName('Num Valid SOP IDOs').value
    if (self.offset  < (numIDO * 32 + 8)) :
        return str(hexTranslate(self))

def test_certstat(self):
    numIDO = self.register.fieldByName('Num Valid SOP IDOs').value
    if (self.offset  < (numIDO * 32 + 8)) :
        return str(hexTranslate(self))

def test2_svidTranslate(self):
    numIDO = self.register.fieldByName('Num Valid SOP Prime IDOs').value
    if (self.offset  < (numIDO * 32 + 200)) :
        return svidTranslate(self)        

def test2_TrueFalse(self):
    numIDO = self.register.fieldByName('Num Valid SOP Prime IDOs').value
    if (self.offset  < (numIDO * 32 + 200)) :
        return TrueFalse_list[self.value]        

def test2_prodtype(self):
    numIDO = self.register.fieldByName('Num Valid SOP Prime IDOs').value
    if (self.offset  < (numIDO * 32 + 200)) :
        if self.value < len(prodtype_list):
            return prodtype_list[self.value]
        else:
            return 'reserved (%s)' %(str(self.value))

def test2_certstat(self):
    numIDO = self.register.fieldByName('Num Valid SOP Prime IDOs').value
    if (self.offset  < (numIDO * 32 + 200)) :
        return str(hexTranslate(self))

def test2_bcd(self):
    numIDO = self.register.fieldByName('Num Valid SOP Prime IDOs').value
    if (self.offset  < (numIDO * 32 + 200)) :
        return str(hexTranslate(self))

def test2_prodid(self):
    numIDO = self.register.fieldByName('Num Valid SOP Prime IDOs').value
    if (self.offset  < (numIDO * 32 + 200)) :
        return str(hexTranslate(self))



def test3_svidTranslate(self):
    numIDO = self.register.fieldByName('NumValidIDOs').value
    if (self.offset  < (numIDO * 32 + 8)) :
        return svidTranslate(self)        

def test3_TrueFalse(self):
    numIDO = self.register.fieldByName('NumValidIDOs').value
    if (self.offset  < (numIDO * 32 + 8)) :
        return TrueFalse_list[self.value]        

def test3_prodtype(self):
    numIDO = self.register.fieldByName('NumValidIDOs').value
    if (self.offset  < (numIDO * 32 + 8)) :
        if self.value < len(prodtype_list):
            return prodtype_list[self.value]
        else:
            return 'reserved (%s)' %(str(self.value))

def test3_certstat(self):
    numIDO = self.register.fieldByName('NumValidIDOs').value
    if (self.offset  < (numIDO * 32 + 8)) :
        return str(hexTranslate(self))

def test3_bcd(self):
    numIDO = self.register.fieldByName('NumValidIDOs').value
    if (self.offset  < (numIDO * 32 + 8)) :
        return str(hexTranslate(self))

def test3_prodid(self):
    numIDO = self.register.fieldByName('NumValidIDOs').value
    if (self.offset  < (numIDO * 32 + 8)) :
        return str(hexTranslate(self))



USBGenList = ['USB 2.0 Only', 'USB 3.1 Gen 1', 'USB 3.1 Gen 1 and 2']
VBUS_CurrentCap_List = ['1.5 A', '3.0 A', '5 A']
SSDir_List = ['Fixed', 'Configurable']
CableTerm_List = ['Both Ends Passive, VConn Not Required', 'Both Ends Passive, VConn Is Required', 'One End Active, One End Passive, VConn Is Required', 'Both Ends Active, VConn Is Required']
CableLatency_List = ['reserved (0000b)', '< 10nS (~1m)', '10-20nS (~2m)', '20-30nS (~3m)', '30-40nS (~4m)', '40-50nS (~5m)', '50-60nS (~6m)', '60-70nS (~7m)', '1000nS (~100m)', '2000nS (~200m)', '3000nS (~300m)']
PlugReceptacle_List = ['Plug', 'Receptacle']
TypeABC_List = ['Type-A', 'Type-B', 'Type-C']


###  ToDo: Put in Product, Cable and AMA translations for IDOs 3-6

USBSSSigAMAList = ['USB 2.0 Only', 'USB 3.1 Gen 1', 'USB 3.1 Gen 1 and 2', 'USB 2.0 Billboard Only']
VConnPowAMA_List = ['1 W', '1.5 W', '2 W', '3 W', '4 W', '5 W', '6 W']

TX_IDENTITY_REG = cRegister({'register name' : 'Tx Identity', 'address' : 0x47, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Num Valid SOP IDOs', 'offset' : 0, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 3 , 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Num Valid SOP Prime IDOs', 'offset' : 4, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 3 , 'length' : 1, 'value' : 0 } ,
               { 'name' : 'USB Vendor ID', 'offset' : 8, 'length' : 16, 'value' : 0, 'translate' : test_svidTranslate } ,
               { 'name' : 'Reserved', 'offset' : 24, 'length' : 10, 'value' : 0 } ,
               { 'name' : 'Modal Operation', 'offset' : 34, 'length' : 1, 'value' : 0, 'translate' : test_TrueFalse } ,
               { 'name' : 'Product Type', 'offset' : 35, 'length' : 3, 'value' : 0, 'translate' : test_prodtype } ,
               { 'name' : 'Data Capable as USB Device', 'offset' : 38, 'length' : 1, 'value' : 0, 'translate' : test_TrueFalse } ,
               { 'name' : 'Data Capable as USB Host', 'offset' : 39, 'length' : 1, 'value' : 0, 'translate' : test_TrueFalse } ,
               { 'name' : 'Certification Status', 'offset' : 40, 'length' : 20, 'value' : 0, 'translate' : test_certstat  } ,
               { 'name' : 'Reserved', 'offset' : 60, 'length' : 12, 'value' : 0  } ,
               { 'name' : 'BCD Device', 'offset' : 72, 'length' : 16, 'value' : 0, 'translate' : test_bcd } ,
               { 'name' : 'USB Product ID', 'offset' : 88, 'length' : 16, 'value' : 0, 'translate' : test_prodid } ,
               { 'name' : 'USB SS Signalling', 'offset' : 104, 'length' : 3, 'value' : 0, 'translate list' : USBSSSigAMAList } ,
               { 'name' : 'VBus Required', 'offset' : 107, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'VConn Required', 'offset' : 108, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'VConn Power', 'offset' : 109, 'length' : 3, 'value' : 0, 'translate list' : VConnPowAMA_List } ,
               { 'name' : 'SSRx 2 Directionality', 'offset' : 112, 'length' : 1, 'value' : 0, 'translate list' : SSDir_List } ,
               { 'name' : 'SSRx 1 Directionality', 'offset' : 112, 'length' : 1, 'value' : 0, 'translate list' : SSDir_List } ,
               { 'name' : 'SSTx 2 Directionality', 'offset' : 112, 'length' : 1, 'value' : 0, 'translate list' : SSDir_List } ,
               { 'name' : 'SSTx 1 Directionality', 'offset' : 112, 'length' : 1, 'value' : 0, 'translate list' : SSDir_List } ,
               { 'name' : 'AMA Firmware Version', 'offset' : 128, 'length' : 4, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'AMA Hardware Version', 'offset' : 132, 'length' : 4, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'SOP IDO 5', 'offset' : 136, 'length' : 32, 'value' : 0, 'translate' : translate_IDO } ,
               { 'name' : 'SOP IDO 6', 'offset' : 168, 'length' : 32, 'value' : 0, 'translate' : translate_IDO } ,
               { 'name' : 'USB Vendor ID', 'offset' : 200, 'length' : 16, 'value' : 0, 'translate' : test2_svidTranslate } ,
               { 'name' : 'Reserved', 'offset' : 216, 'length' : 10, 'value' : 0 } ,
               { 'name' : 'Modal Operation', 'offset' : 226, 'length' : 1, 'value' : 0, 'translate' : test2_TrueFalse } ,
               { 'name' : 'Product Type', 'offset' : 227, 'length' : 3, 'value' : 0, 'translate' : test2_prodtype } ,
               { 'name' : 'Data Capable as USB Device', 'offset' : 230, 'length' : 1, 'value' : 0, 'translate' : test2_TrueFalse } ,
               { 'name' : 'Data Capable as USB Host', 'offset' : 231, 'length' : 1, 'value' : 0, 'translate' : test2_TrueFalse } ,
               { 'name' : 'Certification Status', 'offset' : 232, 'length' : 20, 'value' : 0, 'translate' : test2_certstat  } ,
               { 'name' : 'Reserved', 'offset' : 252, 'length' : 12, 'value' : 0  } ,
               { 'name' : 'BCD Device', 'offset' : 264, 'length' : 16, 'value' : 0, 'translate' : test2_bcd } ,
               { 'name' : 'USB Product ID', 'offset' : 280, 'length' : 16, 'value' : 0, 'translate' : test2_prodid } ,
               { 'name' : 'USB SS Signalling', 'offset' : 296, 'length' : 3, 'value' : 0, 'translate list' : USBGenList } ,
               { 'name' : 'SOP" Controller Present', 'offset' : 299, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'VBUS Through Cable', 'offset' : 300, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'VBUS Current Capability', 'offset' : 301, 'length' : 2, 'value' : 0, 'translate list' : VBUS_CurrentCap_List } ,
               { 'name' : 'SSRx 2 Directionality', 'offset' : 303, 'length' : 1, 'value' : 0, 'translate list' : SSDir_List } ,
               { 'name' : 'SSRx 1 Directionality', 'offset' : 304, 'length' : 1, 'value' : 0, 'translate list' : SSDir_List } ,
               { 'name' : 'SSTx 2 Directionality', 'offset' : 305, 'length' : 1, 'value' : 0, 'translate list' : SSDir_List } ,
               { 'name' : 'SSTx 1 Directionality', 'offset' : 306, 'length' : 1, 'value' : 0, 'translate list' : SSDir_List } ,
               { 'name' : 'Cable Termination Type', 'offset' : 307, 'length' : 2, 'value' : 0, 'translate list' : CableTerm_List } ,
               { 'name' : 'Cable Latency', 'offset' : 309, 'length' : 4, 'value' : 0, 'translate list' : CableLatency_List } ,
               { 'name' : 'Type-C Plug or Receptacle', 'offset' : 313, 'length' : 1, 'value' : 0, 'translate list' : PlugReceptacle_List } ,
               { 'name' : 'Type-C to Type-A/B/C', 'offset' : 314, 'length' : 2, 'value' : 0, 'translate list' : TypeABC_List } ,
               { 'name' : 'Reserved', 'offset' : 316, 'length' : 4, 'value' : 0 } ,
               { 'name' : 'Cable Firmware Version', 'offset' : 320, 'length' : 4, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Cable Hardware Version', 'offset' : 324, 'length' : 4, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'SOP Prime IDO 5', 'offset' : 328, 'length' : 32, 'value' : 0, 'translate' : translate_primeIDO } ,
               { 'name' : 'SOP Prime IDO 6', 'offset' : 360, 'length' : 32, 'value' : 0, 'translate' : translate_primeIDO } ,
            ] } )                             

Response_list = ['Discover Identity Request Not Sent or Pending', 'Responder ACK Received', 'Responder NAK Received or Timeout', 'Responder Busy Received' ]

RX_IDENTITY_SOP_REG = cRegister({'register name' : 'Rx SOP Identity', 'address' : 0x48, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'NumValidIDOs', 'offset' : 0, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 3, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'Response', 'offset' : 6, 'length' : 2, 'value' : 0, 'translate list' : Response_list } ,
               { 'name' : 'USB Vendor ID', 'offset' : 8, 'length' : 16, 'value' : 0, 'translate' : test3_svidTranslate } ,
               { 'name' : 'Reserved', 'offset' : 24, 'length' : 10, 'value' : 0 } ,
               { 'name' : 'Modal Operation', 'offset' : 34, 'length' : 1, 'value' : 0, 'translate' : test3_TrueFalse } ,
               { 'name' : 'Product Type', 'offset' : 35, 'length' : 3, 'value' : 0, 'translate' : test3_prodtype } ,
               { 'name' : 'Data Capable as USB Device', 'offset' : 38, 'length' : 1, 'value' : 0, 'translate' : test3_TrueFalse } ,
               { 'name' : 'Data Capable as USB Host', 'offset' : 39, 'length' : 1, 'value' : 0, 'translate' : test3_TrueFalse } ,
               { 'name' : 'Certification Status', 'offset' : 40, 'length' : 20, 'value' : 0, 'translate' : test3_certstat  } ,
               { 'name' : 'Reserved', 'offset' : 60, 'length' : 12, 'value' : 0  } ,
               { 'name' : 'BCD Device', 'offset' : 72, 'length' : 16, 'value' : 0, 'translate' : test3_bcd } ,
               { 'name' : 'USB Product ID', 'offset' : 88, 'length' : 16, 'value' : 0, 'translate' : test3_prodid } ,
               { 'name' : 'IDO 4', 'offset' : 104, 'length' : 32, 'value' : 0, 'translate' : translate_genIDO } ,
               { 'name' : 'IDO 5', 'offset' : 136, 'length' : 32, 'value' : 0, 'translate' : translate_genIDO } ,
               { 'name' : 'IDO 6', 'offset' : 168, 'length' : 32, 'value' : 0, 'translate' : translate_genIDO } ,
            ] } )                             


RX_IDENTITY_SOPP_REG = cRegister({'register name' : 'Rx SOP Prime Identity', 'address' : 0x49, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'NumValidIDOs', 'offset' : 0, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 3, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'Response', 'offset' : 6, 'length' : 2, 'value' : 0, 'translate list' : Response_list } ,
               { 'name' : 'USB Vendor ID', 'offset' : 8, 'length' : 16, 'value' : 0, 'translate' : test3_svidTranslate } ,
               { 'name' : 'Reserved', 'offset' : 24, 'length' : 10, 'value' : 0 } ,
               { 'name' : 'Modal Operation', 'offset' : 34, 'length' : 1, 'value' : 0, 'translate' : test3_TrueFalse } ,
               { 'name' : 'Product Type', 'offset' : 35, 'length' : 3, 'value' : 0, 'translate' : test3_prodtype } ,
               { 'name' : 'Data Capable as USB Device', 'offset' : 38, 'length' : 1, 'value' : 0, 'translate' : test3_TrueFalse } ,
               { 'name' : 'Data Capable as USB Host', 'offset' : 39, 'length' : 1, 'value' : 0, 'translate' : test3_TrueFalse } ,
               { 'name' : 'Certification Status', 'offset' : 40, 'length' : 20, 'value' : 0, 'translate' : test3_certstat  } ,
               { 'name' : 'Reserved', 'offset' : 60, 'length' : 12, 'value' : 0  } ,
               { 'name' : 'BCD Device', 'offset' : 72, 'length' : 16, 'value' : 0, 'translate' : test3_bcd } ,
               { 'name' : 'USB Product ID', 'offset' : 88, 'length' : 16, 'value' : 0, 'translate' : test3_prodid } ,
               { 'name' : 'USB SS Signalling', 'offset' : 104, 'length' : 3, 'value' : 0, 'translate list' : USBGenList } ,
               { 'name' : 'SOP" Controller Present', 'offset' : 107, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'VBUS Through Cable', 'offset' : 108, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'VBUS Current Capability', 'offset' : 109, 'length' : 2, 'value' : 0, 'translate list' : VBUS_CurrentCap_List } ,
               { 'name' : 'SSRx 2 Directionality', 'offset' : 111, 'length' : 1, 'value' : 0, 'translate list' : SSDir_List } ,
               { 'name' : 'SSRx 1 Directionality', 'offset' : 112, 'length' : 1, 'value' : 0, 'translate list' : SSDir_List } ,
               { 'name' : 'SSTx 2 Directionality', 'offset' : 113, 'length' : 1, 'value' : 0, 'translate list' : SSDir_List } ,
               { 'name' : 'SSTx 1 Directionality', 'offset' : 114, 'length' : 1, 'value' : 0, 'translate list' : SSDir_List } ,
               { 'name' : 'Cable Termination Type', 'offset' : 115, 'length' : 2, 'value' : 0, 'translate list' : CableTerm_List } ,
               { 'name' : 'Cable Latency', 'offset' : 117, 'length' : 4, 'value' : 0, 'translate list' : CableLatency_List } ,
               { 'name' : 'Type-C Plug or Receptacle', 'offset' : 121, 'length' : 1, 'value' : 0, 'translate list' : PlugReceptacle_List } ,
               { 'name' : 'Type-C to Type-A/B/C', 'offset' : 122, 'length' : 2, 'value' : 0, 'translate list' : TypeABC_List } ,
               { 'name' : 'Reserved', 'offset' : 124, 'length' : 4, 'value' : 0 } ,
               { 'name' : 'Cable Firmware Version', 'offset' : 128, 'length' : 4, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Cable Hardware Version', 'offset' : 132, 'length' : 4, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'IDO 5', 'offset' : 136, 'length' : 32, 'value' : 0, 'translate' : translate_genIDO } ,
               { 'name' : 'IDO 6', 'offset' : 168, 'length' : 32, 'value' : 0, 'translate' : translate_genIDO } ,
            ] } )                             


# TODO IDO list and correct way to display
def translate_VDM(self):
    numIDO = self.register.fieldByName('NumValidIDOs').value
    if ((self.offset - 8) / 32) < numIDO :
        return str(hexTranslate(self))

SOPType_list = ['SOP', 'SOP Prime', 'SOP double prime', 'SOP Debug' ]

def translate_VDM_mask(self):
    numVDO = self.register.fieldByName('Number of VDMs Supported (0-12)').value
    if ((self.offset - 8) / 16) < numVDO :
        return str(hexTranslate(self))


RX_ATTN_REG = cRegister({'register name' : 'Rx Attn VDM', 'address' : 0x4E, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'NumValidIDOs', 'offset' : 0, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'SOP type', 'offset' : 3, 'length' : 2, 'value' : 0, 'translate list' : SOPType_list } ,
               { 'name' : 'Sequence Number', 'offset' : 5, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'VDM 1', 'offset' : 8, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 2', 'offset' : 40, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 3', 'offset' : 72, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 4', 'offset' : 104, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 5', 'offset' : 136, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 6', 'offset' : 168, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 7', 'offset' : 200, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
            ] } )

RX_VDM_REG = cRegister({'register name' : 'Rx non-Attn VDM', 'address' : 0x4F, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'NumValidIDOs', 'offset' : 0, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'SOP type', 'offset' : 3, 'length' : 2, 'value' : 0, 'translate list' : SOPType_list } ,
               { 'name' : 'Sequence Number', 'offset' : 5, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'VDM 1', 'offset' : 8, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 2', 'offset' : 40, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 3', 'offset' : 72, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 4', 'offset' : 104, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 5', 'offset' : 136, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 6', 'offset' : 168, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 7', 'offset' : 200, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
            ] } )                             


USER_VID_STATUS_REG = cRegister({'register name' : 'User VID Status', 'address' : 0x57, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'User SVID Alternate Mode Entered', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Mode 1 Entered', 'offset' : 1, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Mode 2 Entered', 'offset' : 2, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Mode 3 Entered', 'offset' : 3, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Mode 4 Entered', 'offset' : 4, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 5, 'length' : 3, 'value' : 0, 'translate list' : TrueFalse_list } ,
            ] } )                             

RX_USER_SVID_ATTN_VDM_REG = cRegister({'register name' : 'Rx User SVID Attn VDM', 'address' : 0x60, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'NumValidIDOs', 'offset' : 0, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'SOP type', 'offset' : 3, 'length' : 2, 'value' : 0, 'translate list' : SOPType_list } ,
               { 'name' : 'Sequence Number', 'offset' : 5, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'VDM 1', 'offset' : 8, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 2', 'offset' : 40, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 3', 'offset' : 72, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 4', 'offset' : 104, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 5', 'offset' : 136, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 6', 'offset' : 168, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 7', 'offset' : 200, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
            ] } )

RX_USER_SVID_OTHER_VDM_REG = cRegister({'register name' : 'Rx User SVID non-Attn VDM', 'address' : 0x61, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'NumValidIDOs', 'offset' : 0, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'SOP type', 'offset' : 3, 'length' : 2, 'value' : 0, 'translate list' : SOPType_list } ,
               { 'name' : 'Sequence Number', 'offset' : 5, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'VDM 1', 'offset' : 8, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 2', 'offset' : 40, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 3', 'offset' : 72, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 4', 'offset' : 104, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 5', 'offset' : 136, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 6', 'offset' : 168, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
               { 'name' : 'VDM 7', 'offset' : 200, 'length' : 32, 'value' : 0, 'translate' : translate_VDM } ,
            ] } )



TI_VID_STATUS_REG = cRegister({'register name' : 'TI VID Status', 'address' : 0x5B, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'TI SVID Alternate Mode Entered', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'PDIO Mode Entered', 'offset' : 1, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 2, 'length' : 6, 'value' : 0, 'translate list' : TrueFalse_list } ,
            ] } )                             

DATA_CONTROL_REG = cRegister({'register name' : 'Data Control', 'address' : 0x50, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Intel Thunderbolt (TM) Host Connected', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Soft Reset', 'offset' : 1, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Interrupt Acknowledge', 'offset' : 2, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Status Not Acknowledged', 'offset' : 3, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Status Not Acknowledged Reason', 'offset' : 4, 'length' : 4, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 8, 'length' : 24, 'value' : 0 } ,
            ] } )                             


DPCap_list = ['Reserved', 'UFP_D Capable Device', 'DFP_D Capable Device', 'UFP_D and DFP_D Capable Device' ]

DP_CAPABILITIES_REG = cRegister({'register name' : 'Display Port Config', 'address' : 0x51, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Enable DP SID', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Enable DP Mode', 'offset' : 1, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 2, 'length' : 6, 'value' : 0 } ,
               { 'name' : 'DP Port Capability', 'offset' : 8, 'length' : 2, 'value' : 0, 'translate list' : DPCap_list } ,
               { 'name' : 'Supports DP v1.3 signalling', 'offset' : 10, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Supports USB Gen2 signalling', 'offset' : 11, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 12, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Receptacle Indication', 'offset' : 14, 'length' : 1, 'value' : 0, 'translate list' : Receptacle_list } ,
               { 'name' : 'USB 2.0 Signalling Not Used', 'offset' : 15, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list  } ,
               { 'name' : 'DFP_D Pin Configuration A Supported', 'offset' : 16, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'DFP_D Pin Configuration B Supported', 'offset' : 17, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'DFP_D Pin Configuration C Supported', 'offset' : 18, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'DFP_D Pin Configuration D Supported', 'offset' : 19, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'DFP_D Pin Configuration E Supported', 'offset' : 20, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'DFP_D Pin Configuration F Supported', 'offset' : 21, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 22, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'UFP_D Pin Configuration A Supported', 'offset' : 24, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'UFP_D Pin Configuration B Supported', 'offset' : 25, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'UFP_D Pin Configuration C Supported', 'offset' : 26, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'UFP_D Pin Configuration D Supported', 'offset' : 27, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'UFP_D Pin Configuration E Supported', 'offset' : 28, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 29, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'Multifunction Preferred', 'offset' : 32, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'MuxSwap', 'offset' : 33, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 34, 'length' : 6, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 40, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Autoenter DisplayPort Mode', 'offset' : 41, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 42, 'length' : 6, 'value' : 0 } ,
               { 'name' : 'messageIndex', 'offset' : 48, 'length' : 8, 'value' : 0 } ,
            ] } )                             

INTEL_CONFIG_REG = cRegister({'register name' : 'Intel VID Config', 'address' : 0x52, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Enable Intel VID', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Enable Thunderbolt (TM) Mode', 'offset' : 1, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 2, 'length' : 6, 'value' : 0 } ,
               { 'name' : 'Vout_3v3 Required', 'offset' : 8, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Thunderbolt Emarker Override', 'offset' : 9, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'AN Minimum Power Required', 'offset' : 10, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 11, 'length' : 5, 'value' : 0 } ,
               { 'name' : 'Legacy TBT Adapter', 'offset' : 16, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 17, 'length' : 16, 'value' : 0 } ,
               { 'name' : 'Cable Speed', 'offset' : 32, 'length' : 3, 'value' : 0 } ,
               { 'name' : 'Cable Generation', 'offset' : 35, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Cable Type', 'offset' : 37, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Active Cable', 'offset' : 38, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Cable Training Supported', 'offset' : 39, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 40, 'length' : 9, 'value' : 0 } ,
               { 'name' : 'Autoenter Thunderbolt (TM) Mode', 'offset' : 49, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 50, 'length' : 6, 'value' : 0 } ,
               { 'name' : 'Message Index', 'offset' : 56, 'length' : 8, 'value' : 0 } ,
            ] } )

TI_VID_CONFIG_REG = cRegister({'register name' : 'TI VID Config', 'address' : 0x54, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Enable TI VID', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Enable PDIO Mode', 'offset' : 1, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Enable Quickswap Mode', 'offset' : 2, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 3, 'length' : 5, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 8, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Autoenter PDIO Mode', 'offset' : 9, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Autoenter Quickswap Mode', 'offset' : 10, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 11, 'length' : 5, 'value' : 0 } ,
               { 'name' : 'Message Index', 'offset' : 16, 'length' : 8, 'value' : 0 } ,
            ] } )

DUConn_List = ['Neither DFP_D or UFP_D connected', 'DFP_D is connected', 'UFP_D is connected' 'Both DFP_D and UFP_D are connected']
PowerLow_List = ['Adapter is functioning normally or disabled', 'Adapter has detected low power and DP is disabled']
DPDisabledEnabled_List = ['DP functionality is Disabled', 'DP functionality is enabled']
MFPref_List = ['No Multi-function Preference', 'Multi-function preferred']
USBConf_List = ['Maintain current configuration', 'Request switch to USB Configuration']
DPExit_List = ['Maintain current mode', 'Request exit from DisplayPort Mode']
HPDState_List = ['HPD_Low', 'HPD_High']
IRQHPD_List = ['No IRQ_HPD since last status', 'IRQ_HPD']

SelConf_List = ['Set config for USB', 'Set config for UFP_U as DFP_D', 'Set config for UFP_U as UFP_D', 'Reserved (11b)']
DPSignalling_List = ['Signalling Unspecified', 'DP v1.3 signalling', 'Gen 2 signalling']


DP_STATUS_REG = cRegister({'register name' : 'Display Port Status', 'address' : 0x58, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'DP SID Active', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'DP Mode Active', 'offset' : 1, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 2, 'length' : 6, 'value' : 0 } ,
               { 'name' : 'DP Status TX, DFP_D/UFP_D Connected', 'offset' : 8, 'length' : 1, 'value' : 0, 'translate list' : DUConn_List} ,
               { 'name' : 'DP Status TX, Power Low', 'offset' : 9, 'length' : 1, 'value' : 0, 'translate list' : PowerLow_List} ,
               { 'name' : 'DP Status TX, DP Enabled', 'offset' : 10, 'length' : 1, 'value' : 0, 'translate list' : DPDisabledEnabled_List} ,
               { 'name' : 'DP Status TX, Multi-function Preferred', 'offset' : 11, 'length' : 1, 'value' : 0, 'translate list' : MFPref_List} ,
               { 'name' : 'DP Status TX, USB Config Request', 'offset' : 12, 'length' : 1, 'value' : 0, 'translate list' : USBConf_List} ,
               { 'name' : 'DP Status TX, Exit DP Mode Request', 'offset' : 13, 'length' : 1, 'value' : 0, 'translate list' : DPExit_List} ,
               { 'name' : 'DP Status TX, HPD State', 'offset' : 14, 'length' : 1, 'value' : 0, 'translate list' : HPDState_List} ,
               { 'name' : 'DP Status TX, IRQ_HPD', 'offset' : 15, 'length' : 1, 'value' : 0, 'translate list' : IRQHPD_List} ,
               { 'name' : 'Reserved', 'offset' : 16, 'length' : 24, 'value' : 0 } ,
               { 'name' : 'DP Status RX, DFP_D/UFP_D Connected', 'offset' : 40, 'length' : 1, 'value' : 0, 'translate list' : DUConn_List} ,
               { 'name' : 'DP Status RX, Power Low', 'offset' : 41, 'length' : 1, 'value' : 0, 'translate list' : PowerLow_List} ,
               { 'name' : 'DP Status RX, DP Enabled', 'offset' : 42, 'length' : 1, 'value' : 0, 'translate list' : DPDisabledEnabled_List} ,
               { 'name' : 'DP Status RX, Multi-function Preferred', 'offset' : 43, 'length' : 1, 'value' : 0, 'translate list' : MFPref_List} ,
               { 'name' : 'DP Status RX, USB Config Request', 'offset' : 44, 'length' : 1, 'value' : 0, 'translate list' : USBConf_List} ,
               { 'name' : 'DP Status RX, Exit DP Mode Request', 'offset' : 45, 'length' : 1, 'value' : 0, 'translate list' : DPExit_List} ,
               { 'name' : 'DP Status RX, HPD State', 'offset' : 46, 'length' : 1, 'value' : 0, 'translate list' : HPDState_List} ,
               { 'name' : 'DP Status RX, IRQ_HPD', 'offset' : 47, 'length' : 1, 'value' : 0, 'translate list' : IRQHPD_List} ,
               { 'name' : 'Reserved', 'offset' : 48, 'length' : 24, 'value' : 0 } ,
               { 'name' : 'DP Configure, select config', 'offset' : 72, 'length' : 2, 'value' : 0, 'translate list' : SelConf_List} ,
               { 'name' : 'DP Configure, select signalling', 'offset' : 74, 'length' : 4, 'value' : 0, 'translate list' : DPSignalling_List} ,
               { 'name' : 'Reserved', 'offset' : 78, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'DP Configure, UFP_U as DFP_D Pin Conf A', 'offset' : 80, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'DP Configure, UFP_U as DFP_D Pin Conf B', 'offset' : 81, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'DP Configure, UFP_U as DFP_D Pin Conf C', 'offset' : 82, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'DP Configure, UFP_U as DFP_D Pin Conf D', 'offset' : 83, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'DP Configure, UFP_U as DFP_D Pin Conf E', 'offset' : 84, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'DP Configure, UFP_U as DFP_D Pin Conf F', 'offset' : 85, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 86, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'DP Configure, UFP_U as UFP_D Pin Conf A', 'offset' : 88, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'DP Configure, UFP_U as UFP_D Pin Conf B', 'offset' : 89, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'DP Configure, UFP_U as UFP_D Pin Conf C', 'offset' : 90, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'DP Configure, UFP_U as UFP_D Pin Conf D', 'offset' : 91, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'DP Configure, UFP_U as UFP_D Pin Conf E', 'offset' : 92, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 93, 'length' : 11, 'value' : 0 } ,
               { 'name' : 'RX DP Cap, DP Port Capability', 'offset' : 104, 'length' : 2, 'value' : 0, 'translate list' : DPCap_list } ,
               { 'name' : 'RX DP Cap, Supports DP v1.3 signalling', 'offset' : 106, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'RX DP Cap, Supports USB Gen2 signalling', 'offset' : 107, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 108, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'RX DP Cap, Receptacle Indication', 'offset' : 110, 'length' : 1, 'value' : 0, 'translate list' : Receptacle_list } ,
               { 'name' : 'RX DP Cap, USB 2.0 Signalling Not Used', 'offset' : 111, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list  } ,
               { 'name' : 'RX DP Cap, DFP_D Pin Conf A Supported', 'offset' : 112, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'RX DP Cap, DFP_D Pin Conf B Supported', 'offset' : 113, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'RX DP Cap, DFP_D Pin Conf C Supported', 'offset' : 114, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'RX DP Cap, DFP_D Pin Conf D Supported', 'offset' : 115, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'RX DP Cap, DFP_D Pin Conf E Supported', 'offset' : 116, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'RX DP Cap, DFP_D Pin Conf F Supported', 'offset' : 117, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 118, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'RX DP Cap, UFP_D Pin Conf A Supported', 'offset' : 120, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'RX DP Cap, UFP_D Pin Conf B Supported', 'offset' : 121, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'RX DP Cap, UFP_D Pin Conf C Supported', 'offset' : 122, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'RX DP Cap, UFP_D Pin Conf D Supported', 'offset' : 123, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'RX DP Cap, UFP_D Pin Conf E Supported', 'offset' : 124, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 125, 'length' : 11, 'value' : 0 } ,
            ] } )

INTEL_STATUS_REG = cRegister({'register name' : 'Intel VID Status', 'address' : 0x59, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'Intel VID Active', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Thunderbolt (TM) Mode Active', 'offset' : 1, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 2, 'length' : 6, 'value' : 0 } ,
               { 'name' : 'Thunderbolt Configuration Message', 'offset' : 8, 'length' : 32, 'value' : 0, 'translate' : hexTranslate} ,
            ] } )                             

GPIO_CONFIG_REG_1 = cRegister({'register name' : 'GPIO Configuration 1', 'address' : 0x5C, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Output Enable Bitfield', 'offset' : 0, 'length' : 18, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Reserved', 'offset' : 18, 'length' : 14, 'value' : 0 } ,
               { 'name' : 'Interrupt Enable Bitfield', 'offset' : 32, 'length' : 18, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Reserved', 'offset' : 50, 'length' : 14, 'value' : 0 } ,
               { 'name' : 'Initial Value Bitfield', 'offset' : 64, 'length' : 18, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Reserved', 'offset' : 82, 'length' : 14, 'value' : 0 } ,
               { 'name' : 'Open Drain Enable Bitfield', 'offset' : 96, 'length' : 18, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Reserved', 'offset' : 114, 'length' : 14, 'value' : 0 } ,
               { 'name' : 'LDO3P3 (0) or VDDIO (1) Bitfield', 'offset' : 128, 'length' : 18, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Reserved', 'offset' : 146, 'length' : 14, 'value' : 0 } ,
               { 'name' : 'Weak Pulldown Enable Bitfield', 'offset' : 160, 'length' : 18, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Reserved', 'offset' : 178, 'length' : 14, 'value' : 0 } ,
               { 'name' : 'Weak Pullup Enable Bitfield', 'offset' : 192, 'length' : 18, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Reserved', 'offset' : 210, 'length' : 14, 'value' : 0 } ,
               { 'name' : 'GPIO (1) or ADC (1) Pinmux Bitfield', 'offset' : 224, 'length' : 18, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Reserved', 'offset' : 242, 'length' : 14, 'value' : 0 } ,
               { 'name' : 'Plug Event (0) mapped to GPIO number', 'offset' : 256, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 261, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Plug Event (0) Enable', 'offset' : 263, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Cable Orientation Event (1) mapped to GPIO number', 'offset' : 264, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 269, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Cable Orientation Event (1) Enable', 'offset' : 271, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Enable VOUT3V3 1 (2) mapped to GPIO number', 'offset' : 272, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 277, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Enable VOUT3V3 1 (2) Enable', 'offset' : 279, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Enable VOUT3V3 2 (3) mapped to GPIO number', 'offset' : 280, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 285, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Enable VOUT3V3 2 (3)', 'offset' : 287, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Provider (0) Consumer (1) (4) mapped to GPIO number', 'offset' : 288, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 293, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Provider (0) Consumer (1) (4) Enable', 'offset' : 295, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Wake System (5) mapped to GPIO number', 'offset' : 296, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 301, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Wake System (5) Enable', 'offset' : 303, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Fault Condition (6) mapped to GPIO number', 'offset' : 304, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 309, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Fault Condition (6) Enable', 'offset' : 311, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Boosterpack Config 1 (7) mapped to GPIO number', 'offset' : 312, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 317, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Boosterpack Config 1 (7) Enable', 'offset' : 319, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Boosterpack Config 2 (8) mapped to GPIO number', 'offset' : 320, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 325, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Boosterpack Config 2 (8) Enable', 'offset' : 327, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Boosterpack Config 3 (9) mapped to GPIO number', 'offset' : 328, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 333, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Boosterpack Config 3 (9) Enable', 'offset' : 335, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Bypass DP (10) mapped to GPIO number', 'offset' : 336, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 341, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Bypass DP (10) Enable', 'offset' : 343, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Bypass TBT (11) mapped to GPIO number', 'offset' : 344, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 349, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Bypass TBT (11) Enable', 'offset' : 351, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Bypass BM (12) mapped to GPIO number', 'offset' : 352, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 357, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Bypass BM (12) Enable', 'offset' : 359, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Either DP or USB3 (13) mapped to GPIO number', 'offset' : 360, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 365, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Either DP or USB3 (13) Enable', 'offset' : 367, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'DP Mode Selection (14) mapped to GPIO number', 'offset' : 368, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 373, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'DP Mode Selection (14) Enable', 'offset' : 375, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Wake TPS65982 (15) mapped to GPIO number', 'offset' : 376, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 381, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Wake TPS65982 (15) Enable', 'offset' : 383, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Debug Modem (16) mapped to GPIO number', 'offset' : 384, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 389, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Debug Modem (16) Enable', 'offset' : 391, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Debug Squelch (17) mapped to GPIO number', 'offset' : 392, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 397, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Debug Squelch (17) Enable', 'offset' : 399, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Supply P5V (18) mapped to GPIO number', 'offset' : 400, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 405, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Supply P5V (18) Enable', 'offset' : 407, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Supply PHV (19) mapped to GPIO number', 'offset' : 408, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 413, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Supply PHV (19) Enable', 'offset' : 415, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Supply PHV EXT (20) mapped to GPIO number', 'offset' : 416, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 421, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Supply PHV EXT (20) Enable', 'offset' : 423, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Supply PPCable (21) mapped to GPIO number', 'offset' : 424, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 429, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Supply PPCable (21) Enable', 'offset' : 431, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Attached L (22) to GPIO number', 'offset' : 432, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 437, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Attached L (22) Enable', 'offset' : 439, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'VBUS Detect (23) mapped to GPIO number', 'offset' : 440, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 445, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'VBUS Detect (23) Enable', 'offset' : 447, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Force DFU (24) mapped to GPIO number', 'offset' : 448, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 453, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Force DFU (24) Enable', 'offset' : 455, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Audio Mode Evt (25) mapped to GPIO number', 'offset' : 456, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 461, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Audio Mode Evt (25) Enable', 'offset' : 463, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Audio Mode L Evt (26) mapped to GPIO number', 'offset' : 464, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 469, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Audio Mode L Evt (26) Enable', 'offset' : 471, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'P5V Overcurrent (27) mapped to GPIO number', 'offset' : 472, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 477, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'P5V Overcurrent (27) Enable', 'offset' : 479, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Sink (0) Source (1) (28) mapped to GPIO number', 'offset' : 480, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 485, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Sink (0) Source (1) (28) Enable', 'offset' : 487, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'USB3 Evt (29) mapped to GPIO number', 'offset' : 488, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 493, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'USB3 Evt (29) Enable', 'offset' : 495, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'USB2 Evt (30) mapped to GPIO number', 'offset' : 496, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 501, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'USB2 Evt (30) Enable', 'offset' : 503, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'DPx2 Evt (31) mapped to GPIO number', 'offset' : 504, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 509, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'DPx2 Evt (31) Enable', 'offset' : 511, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
            ] } )

GPIO_CONFIG_REG_2 = cRegister({'register name' : 'GPIO Configuration 2', 'address' : 0x5D, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Consumer (0) Provider (1) (32) mapped to GPIO number', 'offset' : 0, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 5, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Consumer (0) Provider (1) (32) Enable', 'offset' : 7, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'AMSEL (33) mapped to GPIO number', 'offset' : 8, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 13, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'AMSEL (33) Enable', 'offset' : 15, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Aux OE (34) mapped to GPIO number', 'offset' : 16, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 21, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Aux OE (34) Enable', 'offset' : 23, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Enable PD HVE (35) mapped to GPIO number', 'offset' : 24, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 29, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Enable PD HVE (35) Enable', 'offset' : 31, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Power Src on PC (36) mapped to GPIO number', 'offset' : 32, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 37, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Power Src on PC (36) Enable', 'offset' : 39, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Current Limit Event (37) mapped to GPIO number', 'offset' : 40, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 45, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Current Limit Event (37) Enable', 'offset' : 47, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Sink Less Than 12V (38) mapped to GPIO number', 'offset' : 48, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 53, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Sink Less Than 12V (38) Enable', 'offset' : 55, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Sink 12V (39) mapped to GPIO number', 'offset' : 56, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 61, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Sink 12V (39) Enable', 'offset' : 63, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Sink Greater Than 12V (40) mapped to GPIO number', 'offset' : 64, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 69, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Sink Greater Than 12V (40) Enable', 'offset' : 71, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'HS Enabled (41) mapped to GPIO number', 'offset' : 72, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 77, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'HS Enabled (41) Enable', 'offset' : 79, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'UFP (0) DFP (1) (42) mapped to GPIO number', 'offset' : 80, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 85, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'UFP (0) DFP (1) (42) Enable', 'offset' : 87, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'HS Not Enabled (43) mapped to GPIO number', 'offset' : 88, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 93, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'HS Not Enabled (43) Enable', 'offset' : 95, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'AC Detect (44) mapped to GPIO number', 'offset' : 96, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 101, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'AC Detect (44) Enable', 'offset' : 103, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Consumer No AC (45) mapped to GPIO number', 'offset' : 104, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 109, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Consumer No AC (45) Enable', 'offset' : 111, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reset Req (46) mapped to GPIO number', 'offset' : 112, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 117, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Reset Req (46) Enable', 'offset' : 119, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'DFU Req L (47) mapped to GPIO number', 'offset' : 120, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 125, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'DFU Req L (47) Enable', 'offset' : 127, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Debug Enable (48) mapped to GPIO number', 'offset' : 128, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 133, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Debug Enable (48) Enable', 'offset' : 135, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'CC1 Connect (49) mapped to GPIO number', 'offset' : 136, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 141, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'CC1 Connect (49) Enable', 'offset' : 143, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Thunderbolt Connect (50) mapped to GPIO number', 'offset' : 144, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 149, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Thunderbolt Connect (50) Enable', 'offset' : 151, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Boosterpack Config 4 (51) mapped to GPIO number', 'offset' : 152, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 157, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Boosterpack Config 4 (51) Enable', 'offset' : 159, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Barrel Jack (52) mapped to GPIO number', 'offset' : 160, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 165, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Barrel Jack (52) Enable', 'offset' : 167, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'PDIO In 0 (53) mapped to GPIO number', 'offset' : 168, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 173, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'PDIO In 0 (53) Enable', 'offset' : 175, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'PDIO In 1 (54) mapped to GPIO number', 'offset' : 176, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 181, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'PDIO In 1 (54) Enable', 'offset' : 183, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'PDIO In 2 (55) mapped to GPIO number', 'offset' : 184, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 189, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'PDIO In 2 (55) Enable', 'offset' : 191, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'PDIO In 3 (56) mapped to GPIO number', 'offset' : 192, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 197, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'PDIO In 3 (56) Enable', 'offset' : 199, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'PDIO Out 0 (57) mapped to GPIO number', 'offset' : 200, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 205, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'PDIO Out 0 (57) Enable', 'offset' : 207, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'PDIO Out 1 (58) mapped to GPIO number', 'offset' : 208, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 213, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'PDIO Out 1 (58) Enable', 'offset' : 215, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'PDIO Out 2 (59) mapped to GPIO number', 'offset' : 216, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 221, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'PDIO Out 2 (59) Enable', 'offset' : 223, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'PDIO Out 3 (60) mapped to GPIO number', 'offset' : 224, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 229, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'PDIO Out 3 (60) Enable', 'offset' : 231, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Source PDO 0 Negotiated (61) mapped to GPIO number', 'offset' : 232, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 237, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Source PDO 0 Negotiated (61) Enable', 'offset' : 239, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Source PDO 1 Negotiated (62) mapped to GPIO number', 'offset' : 240, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 245, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Source PDO 1 Negotiated (62) Enable', 'offset' : 247, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Source PDO 2 Negotiated (63) mapped to GPIO number', 'offset' : 248, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 253, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Source PDO 2 Negotiated (63) Enable', 'offset' : 255, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Source PDO 3 Negotiated (64) mapped to GPIO number', 'offset' : 256, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 261, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Source PDO 3 Negotiated (64) Enable', 'offset' : 263, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Source PDO Truth Table 1 (65) mapped to GPIO number', 'offset' : 264, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 269, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Source PDO Truth Table 1 (65) Enable', 'offset' : 271, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Source PDO Truth Table 2 (66) mapped to GPIO number', 'offset' : 272, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 277, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Source PDO Truth Table 2 (66) Enable', 'offset' : 279, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Source PDO Truth Table 3 (67) mapped to GPIO number', 'offset' : 280, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 285, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Source PDO Truth Table 3 (67) Enable', 'offset' : 287, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'VBUS UVP Quick Detect (68) mapped to GPIO number', 'offset' : 288, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 293, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'VBUS UVP Quick Detect (68) Enable', 'offset' : 295, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Force PDO Swap (69) mapped to GPIO number', 'offset' : 296, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 301, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Force PDO Swap (69) Enable', 'offset' : 303, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'PD Negotiation Complete (70) mapped to GPIO number', 'offset' : 304, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 309, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'PD Negotiation Complete (70) Enable', 'offset' : 311, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Load App Config Set 1 (71) mapped to GPIO number', 'offset' : 312, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 317, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Load App Config Set 1 (71) Enable', 'offset' : 319, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Load App Config Set 2 (72) mapped to GPIO number', 'offset' : 320, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 325, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Load App Config Set 2 (72) Enable', 'offset' : 327, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Load App Config Set 3 (73) mapped to GPIO number', 'offset' : 328, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 333, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Load App Config Set 3 (73) Enable', 'offset' : 335, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Enable USB EP (74) mapped to GPIO number', 'offset' : 336, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 341, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Enable USB EP (74) Enable', 'offset' : 343, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Sink on PP_HV or PP_EXT (75) mapped to GPIO number', 'offset' : 344, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
               { 'name' : 'Reserved', 'offset' : 349, 'length' : 2, 'value' : 0 } ,
               { 'name' : 'Sink on PP_HV or PP_EXT (75) enable', 'offset' : 351, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
#               { 'name' : 'Event 76 mapped to GPIO number', 'offset' : 352, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
#               { 'name' : 'Reserved', 'offset' : 357, 'length' : 2, 'value' : 0 } ,
#               { 'name' : 'Event 76 Enable', 'offset' : 359, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
#               { 'name' : 'Event 77 mapped to GPIO number', 'offset' : 360, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
#               { 'name' : 'Reserved', 'offset' : 365, 'length' : 2, 'value' : 0 } ,
#               { 'name' : 'Event 77 Enable', 'offset' : 367, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
#               { 'name' : 'Event 78 mapped to GPIO number', 'offset' : 368, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
#               { 'name' : 'Reserved', 'offset' : 373, 'length' : 2, 'value' : 0 } ,
#               { 'name' : 'Event 78 Enable', 'offset' : 375, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
#               { 'name' : 'Event 79 mapped to GPIO number', 'offset' : 376, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
#               { 'name' : 'Reserved', 'offset' : 381, 'length' : 2, 'value' : 0 } ,
#               { 'name' : 'Event 79 Enable', 'offset' : 383, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
#               { 'name' : 'Event 80 mapped to GPIO number', 'offset' : 384, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
#               { 'name' : 'Reserved', 'offset' : 389, 'length' : 2, 'value' : 0 } ,
#               { 'name' : 'Event 80 Enable', 'offset' : 391, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
#               { 'name' : 'Event 81 mapped to GPIO number', 'offset' : 392, 'length' : 5, 'value' : 0, 'translate' : decTranslate } ,
#               { 'name' : 'Reserved', 'offset' : 397, 'length' : 2, 'value' : 0 } ,
#               { 'name' : 'Event 81 Enable', 'offset' : 399, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
            ] } )


USER_VID_CONFIG = cRegister({'register name' : 'User VID Config', 'address' : 0x4A, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'User VID Enabled', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 1, 'length' : 7, 'value' : 0 } ,
               { 'name' : 'Billboard Message Index', 'offset' : 8, 'length' : 8, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'User Alternate Mode SVID', 'offset' : 16, 'length' : 16, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'User AM Mode 1 Enabled', 'offset' : 32, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 33, 'length' : 7, 'value' : 0 } ,
               { 'name' : 'User AM Mode 2 Enabled', 'offset' : 40, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 41, 'length' : 7, 'value' : 0 } ,
               { 'name' : 'User AM Mode 3 Enabled', 'offset' : 48, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 49, 'length' : 7, 'value' : 0 } ,
               { 'name' : 'User AM Mode 4 Enabled', 'offset' : 56, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 57, 'length' : 7, 'value' : 0 } ,
               { 'name' : 'Autoenter User AM Mode 1', 'offset' : 64, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 65, 'length' : 7, 'value' : 0 } ,
               { 'name' : 'Autoenter User AM Mode 2', 'offset' : 72, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 73, 'length' : 7, 'value' : 0 } ,
               { 'name' : 'Autoenter User AM Mode 3', 'offset' : 80, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 81, 'length' : 7, 'value' : 0 } ,
               { 'name' : 'Autoenter User AM Mode 4', 'offset' : 88, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 89, 'length' : 7, 'value' : 0 } ,
               { 'name' : 'Autosend VDM User AM Mode 1', 'offset' : 96, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 97, 'length' : 7, 'value' : 0 } ,
               { 'name' : 'Autosend VDM User AM Mode 2', 'offset' : 104, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 105, 'length' : 7, 'value' : 0 } ,
               { 'name' : 'Autosend VDM User AM Mode 3', 'offset' : 112, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 113, 'length' : 7, 'value' : 0 } ,
               { 'name' : 'Autosend VDM User AM Mode 4', 'offset' : 120, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 121, 'length' : 7, 'value' : 0 } ,
               { 'name' : 'Load Appconfig User AM Mode 1', 'offset' : 128, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 129, 'length' : 7, 'value' : 0 } ,
               { 'name' : 'Load Appconfig User AM Mode 2', 'offset' : 136, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 137, 'length' : 7, 'value' : 0 } ,
               { 'name' : 'Load Appconfig User AM Mode 3', 'offset' : 144, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 145, 'length' : 7, 'value' : 0 } ,
               { 'name' : 'Load Appconfig User AM Mode 4', 'offset' : 152, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 153, 'length' : 7, 'value' : 0 } ,
               { 'name' : 'AM Mode Value for Position 1', 'offset' : 160, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'AM Mode Value for Position 2', 'offset' : 192, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'AM Mode Value for Position 3', 'offset' : 224, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'AM Mode Value for Position 4', 'offset' : 256, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Autosend Data VDO 1', 'offset' : 288, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Autosend Data VDO 2', 'offset' : 320, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Autosend Data VDO 3', 'offset' : 352, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Autosend Data VDO 4', 'offset' : 384, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Autosend Data VDO 5', 'offset' : 416, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Autosend Data VDO 6', 'offset' : 448, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Autosend Vendor Use Data', 'offset' : 480, 'length' : 16, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'Autosend VDO Count', 'offset' : 496, 'length' : 8, 'value' : 0, 'translate' : decTranslate } ,
         ]})

COrient_list = ['Up side up' , 'Up side down' ]
ACable_list = ['Passive cable' , 'Active cable' ]
DpSourceSink_list = ['DP Source connection requested', 'DP Sink connection requested']
USBSpeed_list = ['USB Gen 1 (5 GBps)' ,  'USB Gen 2 (10 GBps)']
TBT_list = ['No Thunderbolt Connection', '10 GBPS Thunderbolt Connection', '20 GBPS Thunderbolt Connection', 'Reserved']
DataRole2_list = ['DFP', 'UFP']
PinAssign_list = ['E/F', 'C/D', 'A/B']
TBTType_list = ['Type-C to Type-C', 'TBT legacy cable', 'Optical Cable' ]

DATA_STATUS_REG = cRegister({'register name' : 'Data Status', 'address' : 0x5F, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'DataConnection', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : Connect_list } ,
               { 'name' : 'ConnectionOrient', 'offset' : 1, 'length' : 3, 'value' : 0, 'translate list' :  COrient_list } ,
               { 'name' : 'ActiveCable', 'offset' : 2, 'length' : 1, 'value' : 0, 'translate list' :  ACable_list } ,
               { 'name' : 'Overcurrent', 'offset' : 3, 'length' : 1, 'value' : 0, 'translate list' :  OnOff_list } ,
               { 'name' : 'USB2Connection', 'offset' : 4, 'length' : 1, 'value' : 0, 'translate list' : Connect_list } ,
               { 'name' : 'USB3Connection', 'offset' : 5, 'length' : 1, 'value' : 0, 'translate list' : Connect_list } ,
               { 'name' : 'USB3Speed', 'offset' : 6, 'length' : 1, 'value' : 0, 'translate list' : USBSpeed_list } ,
               { 'name' : 'Reserved', 'offset' : 7, 'length' : 1, 'value' : 0, 'translate list' : DataRole2_list } ,
               { 'name' : 'DPConnection', 'offset' : 8, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Reserved', 'offset' : 9, 'length' : 1, 'value' : 0, 'translate list' : DpSourceSink_list } ,
               { 'name' : 'DPPinAssignment', 'offset' : 10, 'length' : 2, 'value' : 0, 'translate list' : PinAssign_list } ,
               { 'name' : 'Reserved', 'offset' : 12, 'length' : 4, 'value' : 0  } ,
               { 'name' : 'TBTConnection', 'offset' : 16, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list  } ,
               { 'name' : 'TBT Cable Type', 'offset' : 17, 'length' : 3, 'value' : 0, 'translate list' : TBT_list  } ,
               { 'name' : 'Reserved', 'offset' : 18, 'length' : 5, 'value' : 0 } ,
               { 'name' : 'ForceLSX', 'offset' : 23, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list  } ,
               { 'name' : 'Reserved', 'offset' : 24, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'TBT Gen1 (10 Gbps) support', 'offset' : 25, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'TBT Gen2 (20 Gbps) support', 'offset' : 26, 'length' : 1, 'value' : 0 } ,
               { 'name' : 'Reserved', 'offset' : 27, 'length' : 5, 'value' : 0 } ,
            ] } )


def translate_current_limit_3A(self):
    if self.value == 0:
        return 'Not set'
    else:
        return (str(1000 + int(round(133.3333 * self.value))))

def rev_translate_current_limit_3A(self, value):
    return int((int(value) - 1000) // 133.3333)


def unit_ma(self):
   return 'mA'


def translate_current_limit_5A(self):
    if self.value == 0:
        return 'Not set'
    else:
        return (str(1000 + int(round(266.6667 * self.value))))

def rev_translate_current_limit_5A(self, value):
    return int((int(value) - 1000) // 266.6667)



PP5V_CUR_LIMIT = cRegister({'register name' : 'PP 5V I Limit', 'address' : 0x64, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Current Limit, 5V Internal Power Path', 'offset' : 0, 'length' : 8, 'value' : 0, 'unit' : unit_ma, 'translate' : translate_current_limit_3A , 'reverse translate' : rev_translate_current_limit_3A }
            ] } )

PPHV_CUR_LIMIT = cRegister({'register name' : 'PP HV I Limit', 'address' : 0x65, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Current Limit, High Voltage Internal Power Path', 'offset' : 0, 'length' : 8, 'value' : 0, 'unit' : unit_ma, 'translate' : translate_current_limit_5A, 'reverse translate' : rev_translate_current_limit_5A } ,
            ] } )

PPHVE_CUR_LIMIT = cRegister({'register name' : 'PP HVE I Limit', 'address' : 0x66, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Current Limit, High Voltage External Power Path', 'offset' : 0, 'length' : 8, 'value' : 0, 'unit' : unit_ma, 'translate' : translate_current_limit_5A, 'reverse translate' : rev_translate_current_limit_5A } ,
            ] } )

VCONN_CUR_LIMIT = cRegister({'register name' : 'VConn I Limit', 'address' : 0x67, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Current Limit, VConn', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
            ] } )

pers_clk_list = ['80 uS', '640 uS', '5.12_mS', '40.96 mS']

# TODO: Translate bitfields
PWR_SWITCH = cRegister({'register name' : 'Switch Control', 'address' : 0x68, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'VBUS good deglitch periods', 'offset' : 0, 'length' : 1, 'value' : 0} ,
               { 'name' : 'VBUS good deglitch clock', 'offset' : 1, 'length' : 1, 'value' : 0} ,
               { 'name' : 'VBUS good deglitch enable', 'offset' : 2, 'length' : 1, 'value' : 0} ,
               { 'name' : 'VBUS Over-voltage montior auto recover', 'offset' : 3, 'length' : 1, 'value' : 0} ,
               { 'name' : 'VBUS Over-voltage monitor auto disable', 'offset' : 4, 'length' : 1, 'value' : 0} ,
               { 'name' : 'VBUS OV monitor deglitch period', 'offset' : 5, 'length' : 3, 'value' : 0} ,
               { 'name' : 'VBUS OV monitor deglitch enabled', 'offset' : 8, 'length' : 1, 'value' : 0} ,
               { 'name' : 'VBUS pull-down to ground enabled', 'offset' : 9, 'length' : 1, 'value' : 0} ,
               { 'name' : 'VBUS auto pull-down enabled', 'offset' : 10, 'length' : 1, 'value' : 0} ,
               { 'name' : 'VBUS Over-voltage monitor threshold', 'offset' : 11, 'length' : 6, 'value' : 0} ,
               { 'name' : 'VBUS Over-voltage monitor enabled', 'offset' : 17, 'length' : 1, 'value' : 0} ,
               { 'name' : 'VBUS LDO is forced off', 'offset' : 18, 'length' : 1, 'value' : 0} ,
               { 'name' : 'VBUS Under-voltage monitor', 'offset' : 19, 'length' : 1, 'value' : 0} ,
               { 'name' : 'VBUS Under-voltage monitor auto disable', 'offset' : 20, 'length' : 1, 'value' : 0} ,
               { 'name' : 'VBUS UV monitor deglitch period', 'offset' : 21, 'length' : 3, 'value' : 0} ,
               { 'name' : 'VBUS UV monitor deglitch enabled', 'offset' : 24, 'length' : 1, 'value' : 0} ,
               { 'name' : 'VBUS OV monitor threshold', 'offset' : 25, 'length' : 6, 'value' : 0} ,
               { 'name' : 'VBUS OV monitor enabled', 'offset' : 31, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PPHV_CFG_REG Auto Recover', 'offset' : 32, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PPHV_CFG_REG Auto Disable', 'offset' : 33, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PPHV_CFG_REG Pers Len', 'offset' : 34, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PPHV_CFG_REG Pers Clock', 'offset' : 35, 'length' : 3, 'value' : 0, 'translate list' : pers_clk_list} ,
               { 'name' : 'PPHV_CFG_REG Pers Enable', 'offset' : 38, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PPHV_CFG_REG RCP Enable', 'offset' : 39, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PPHV_CFG_REG RCP loadoff enable', 'offset' : 40, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PPHV_CFG_REG 2x I load set', 'offset' : 41, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PPHV_CFG_REG I Limit', 'offset' : 42, 'length' : 4, 'value' : 0} ,
               { 'name' : 'PPHV_CFG_REG I Limit enable', 'offset' : 46, 'length' : 1, 'value' : 0} ,
               { 'name' : 'reserved', 'offset' : 47, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PPHV_CFG_REG switch enable', 'offset' : 48, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PPHV_CFG_REG RCP Pers length', 'offset' : 49, 'length' : 3, 'value' : 0} ,
               { 'name' : 'PPHV_CFG_REG RCP Pers Enable', 'offset' : 52, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PPHV_CFG_REG RCP Pers Auto PD Disable', 'offset' : 53, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PPHV_CFG_REG RCP Auto PD Disable', 'offset' : 54, 'length' : 1, 'value' : 0} ,
               { 'name' : 'reserved', 'offset' : 55, 'length' : 9, 'value' : 0} ,
               { 'name' : 'PHV_EXT_CFG_REG Auto Recover', 'offset' : 64, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PHV_EXT_CFG_REG Auto Disable', 'offset' : 65, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PHV_EXT_CFG_REG Pers Len', 'offset' : 66, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PHV_EXT_CFG_REG Pers Clock', 'offset' : 67, 'length' : 3, 'value' : 0, 'translate list' : pers_clk_list} ,
               { 'name' : 'PHV_EXT_CFG_REG Pers Enable', 'offset' : 70, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PHV_EXT_CFG_REG Enable', 'offset' : 71, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PHV_EXT_CFG_REG loadoff enable', 'offset' : 72, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PHV_EXT_CFG_REG 2x I load set', 'offset' : 73, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PHV_EXT_CFG_REG I Limit', 'offset' : 77, 'length' : 4, 'value' : 0} ,
               { 'name' : 'PHV_EXT_CFG_REG I Limit enable', 'offset' : 78, 'length' : 1, 'value' : 0} ,
               { 'name' : 'reserved', 'offset' : 79, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PHV_EXT_CFG_REG switch enable', 'offset' : 80, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PHV_EXT_CFG_REG RCP Pers length', 'offset' : 81, 'length' : 3, 'value' : 0} ,
               { 'name' : 'PHV_EXT_CFG_REG RCP Pers Enable', 'offset' : 84, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PHV_EXT_CFG_REG RCP Pers Auto PD Disable', 'offset' : 85, 'length' : 1, 'value' : 0} ,
               { 'name' : 'PHV_EXT_CFG_REG RCP Auto PD Disable', 'offset' : 86, 'length' : 1, 'value' : 0} ,
               { 'name' : 'reserved', 'offset' : 87, 'length' : 9, 'value' : 0} ,
               { 'name' : 'P5VCFG_REG Auto Recover', 'offset' : 96, 'length' : 1, 'value' : 0} ,
               { 'name' : 'P5VCFG_REG Auto Disable', 'offset' : 97, 'length' : 1, 'value' : 0} ,
               { 'name' : 'P5VCFG_REG Pers Len', 'offset' : 98, 'length' : 1, 'value' : 0} ,
               { 'name' : 'P5VCFG_REG Pers Clock', 'offset' : 99, 'length' : 3, 'value' : 0, 'translate list' : pers_clk_list} ,
               { 'name' : 'P5VCFG_REG Pers Enable', 'offset' : 102, 'length' : 1, 'value' : 0} ,
               { 'name' : 'P5VCFG_REG Enable', 'offset' : 103, 'length' : 1, 'value' : 0} ,
               { 'name' : 'P5VCFG_REG loadoff enable', 'offset' : 104, 'length' : 1, 'value' : 0} ,
               { 'name' : 'P5VCFG_REG 2x I load set', 'offset' : 105, 'length' : 1, 'value' : 0} ,
               { 'name' : 'P5VCFG_REG I Limit', 'offset' : 106, 'length' : 4, 'value' : 0} ,
               { 'name' : 'P5VCFG_REG I Limit enable', 'offset' : 110, 'length' : 1, 'value' : 0} ,
               { 'name' : 'reserved', 'offset' : 111, 'length' : 1, 'value' : 0} ,
               { 'name' : 'P5VCFG_REG switch enable', 'offset' : 112, 'length' : 1, 'value' : 0} ,
               { 'name' : 'P5VCFG_REG RCP Pers length', 'offset' : 113, 'length' : 3, 'value' : 0} ,
               { 'name' : 'P5VCFG_REG RCP Pers Enable', 'offset' : 116, 'length' : 1, 'value' : 0} ,
               { 'name' : 'P5VCFG_REG RCP Pers Auto PD Disable', 'offset' : 117, 'length' : 1, 'value' : 0} ,
               { 'name' : 'P5VCFG_REG RCP Auto PD Disable', 'offset' : 118, 'length' : 1, 'value' : 0} ,
               { 'name' : 'reserved', 'offset' : 119, 'length' : 9, 'value' : 0} ,
               { 'name' : 'CCPCABLE_CFG_REG', 'offset' : 128, 'length' : 32, 'value' : 0} ,
            ] } )

PinForPD_list = ['Not Connected', 'CC_1 used for PD', 'CC_2 used for PD', 'Reserved' ]
CCnState_list = ['Not Connected', 'RA Detected', 'RD Detected', 'STD Advertisement Detected', '1.5A Advertisement Detected', '3.0 Advertisement Detected']


CCn_PINSTATE = cRegister({'register name' : 'CCn State', 'address' : 0x69, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'CCn Pin for PD', 'offset' : 0, 'length' : 2, 'value' : 0, 'translate list' : PinForPD_list } ,
               { 'name' : 'Reserved', 'offset' : 2, 'length' : 6, 'value' : 0} ,
               { 'name' : 'CC1 State', 'offset' : 8, 'length' : 3, 'value' : 0, 'translate list' : CCnState_list} ,
               { 'name' : 'Reserved', 'offset' : 11, 'length' : 5, 'value' : 0} ,
               { 'name' : 'CC2 State', 'offset' : 16, 'length' : 3, 'value' : 0, 'translate list' : CCnState_list} ,
               { 'name' : 'Reserved', 'offset' : 19, 'length' : 5, 'value' : 0} ,
               { 'name' : 'Type-C Port State', 'offset' : 24, 'length' : 8, 'value' : 0, 'translate' : translate_typeC_debug } ,
            ] } )


mux_rfu_list = ['Crossbar Passthrough', 'UART_TX to SBU2, UART RX to SBU1', 'DEBUG3 to SBU2, DEBUG4 to SBU1', 'DEBUG1 to SBU2, DEBUG2 to SBU1', \
                'SWD_CLK to SBU2, SWD_DAT to SBU1', 'AUXP to SBU2, AUXN to SBU1', 'LSX_P2R to SBU2, LSX_R2P to SBU1', \
                'Crossbar Passthrough' ]

muxdir_list = ['Cross bar is flipped', 'Cross bar is straight through']

muxdpdm_list = ['HiZ on output', 'UART_TX to D+, UART_RX to D-', 'DEBUG3 to D+, DEBUG4 to D-', 'DEBUG1 to D+, DEBUG2 to D-', \
                'SWD_DAT to D+, SWD_CLK to D-', 'USB_RP', 'USB_EP', 'Middle Switch Passthrough']

MUX_DEBUG_REG = cRegister({'register name' : 'Mux Status (Debug)', 'address' : 0x6E, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Reserved', 'offset' : 0, 'length' : 14, 'value' : 0} ,
               { 'name' : 'MUX RFU Selection', 'offset' : 14, 'length' : 3, 'value' : 0, 'translate list' :  mux_rfu_list } ,
               { 'name' : 'MUX RFU Direction', 'offset' : 17, 'length' : 1, 'value' : 0, 'translate list' :  muxdir_list } ,
               { 'name' : 'MUX RFU Enable', 'offset' : 18, 'length' : 1, 'value' : 0, 'translate list' :  EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 19, 'length' : 2, 'value' : 0} ,
               { 'name' : 'Mux Bottom D+/D- Map', 'offset' : 21, 'length' : 3, 'value' : 0, 'translate list' :  muxdpdm_list } ,
               { 'name' : 'MUX Bottom D+/D- Enable', 'offset' : 24, 'length' : 1, 'value' : 0, 'translate list' :  EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 25, 'length' : 2, 'value' : 0} ,
               { 'name' : 'Mux Top D+/D- Map', 'offset' : 27, 'length' : 3, 'value' : 0, 'translate list' :  muxdpdm_list } ,
               { 'name' : 'MUX Top D+/D- Enable', 'offset' : 30, 'length' : 1, 'value' : 0, 'translate list' :  EnabledDisabled_list } ,
               { 'name' : 'Reserved', 'offset' : 31, 'length' : 1, 'value' : 0} ,
               ] } )


sleep_list = ['Enter Sleep Mode When Possible', 'Wait for at least 100ms before entering sleep mode', 'Wait for at least 1000ms before entering sleep mode']

SLEEP_CONFIG_REG = cRegister({'register name' : 'Sleep Config', 'address' : 0x70, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Sleep mode enable', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : EnabledDisabled_list } ,
               { 'name' : 'Sleep Wait time', 'offset' : 1, 'length' : 2, 'value' : 0, 'translate list' : sleep_list } ,
               { 'name' : 'SleepAt5V', 'offset' : 3, 'length' : 1, 'value' : 0, 'translate list' : TrueFalse_list} ,
               { 'name' : 'Reserved', 'offset' : 4, 'length' : 4, 'value' : 0} ,
               { 'name' : 'Relax I2C Threshold', 'offset' : 8, 'length' : 8, 'value' : 0, 'translate list' : SysPower_list},
            ] } )

# Note:  You need to use the readback register, not the first register, to determine value
GPIO_STATUS = cRegister({'register name' : 'GPIO Status', 'address' : 0x72, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'GPIO 0', 'offset' : 384, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list} ,
               { 'name' : 'GPIO 1', 'offset' : 385, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'GPIO 2', 'offset' : 386, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'GPIO 3', 'offset' : 387, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'GPIO 4', 'offset' : 388, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'GPIO 5', 'offset' : 389, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'GPIO 6', 'offset' : 390, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'GPIO 7', 'offset' : 391, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'GPIO 8', 'offset' : 392, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'GPIO 9 (RESETZ)', 'offset' : 393, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'GPIO 10 (BUS_PWRZ)', 'offset' : 394, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'GPIO 11 (MRESET)', 'offset' : 395, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'GPIO 12 (DEBUG_4)', 'offset' : 396, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'GPIO 13 (DEBUG_3)', 'offset' : 397, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'GPIO 14 (DEBUG_2)', 'offset' : 398, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'GPIO 15 (DEBUG_1)', 'offset' : 399, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,             
               { 'name' : 'GPIO 16 (DEBUG_CTL_1)', 'offset' : 400, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'GPIO 17 (DEBUG_CTL_2)', 'offset' : 401, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'GPIO 18 (SPI_CSZ)', 'offset' : 402, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'GPIO 19 (SPI_MOSI)', 'offset' : 403, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'GPIO 20 (SPI_MISO)', 'offset' : 404, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'GPIO 21 (SPI_CLK)', 'offset' : 405, 'length' : 1, 'value' : 0, 'translate list' : HighLow_list } ,
               { 'name' : 'Reserved', 'offset' : 406, 'length' : 10, 'value' : 0 } ,
               { 'name' : 'GPIO Set REG', 'offset' : 0, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'GPIO Output Enable REG', 'offset' : 32, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'GPIO_RISE_INT_EN_REG', 'offset' : 64, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'GPIO_FALL_INT_EN_REG', 'offset' : 96, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'GPIO_RISE_EDGE_DET_EN_REG', 'offset' : 128, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'GPIO_FALL_EDGE_DET_EN_REG', 'offset' : 160, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'GPIO_SAMPLE_EN_REG', 'offset' : 192, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'GPIO_LOGIC_LEVEL_CFG_REG', 'offset' : 224, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'GPIO_OD_OE_REG', 'offset' : 256, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'GPIO_PD_EN_REG', 'offset' : 288, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'GPIO_PU_EN_REG', 'offset' : 320, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'GPIO_TO_HI_Z_ADC_REG', 'offset' : 352, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'GPIO_DATA_RDBACK_REG', 'offset' : 384, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'GPIO_RISE_EDGE_DETECTED_REG', 'offset' : 416, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'GPIO_FALL_EDGE_DETECTED_REG', 'offset' : 448, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
               { 'name' : 'GPIO_DUAL_EDGE_DETECTED_REG', 'offset' : 480, 'length' : 32, 'value' : 0, 'translate' : hexTranslate } ,
            ] } )


REGS_LIST = [ VID, DID, UID, MODE_REG, VERSION_REG, DEVICE_INFO_REG, CUSTUSE, BOOT_FLAGS, STATUS_REG, DATA_STATUS_REG, CONTROL_CONFIG_REG, SYS_CONFIG_REG, SYS_POWER, PWR_STATUS, PD_STATUS,
              ACTIVE_CONTRACT_PDO, ACTIVE_CONTRACT_RDO, SINK_REQUEST_RDO, TX_SOURCE_CAP, TX_SINK_CAP,
              RX_SOURCE_CAP, RX_SINK_CAP, AUTONEGOTIATE_SINK, INT_EVENT1, INT_MASK1, INT_EVENT2, INT_MASK2, GPIO_CONFIG_REG_1, GPIO_CONFIG_REG_2, GPIO_STATUS, TX_IDENTITY_REG,
              RX_IDENTITY_SOP_REG, RX_IDENTITY_SOPP_REG, RX_VDM_REG, RX_ATTN_REG, ALT_MODE_ENTRY, DATA_CONTROL_REG, DP_CAPABILITIES_REG, INTEL_CONFIG_REG,
              DP_STATUS_REG, INTEL_STATUS_REG, PWR_SWITCH, CCn_PINSTATE, SLEEP_CONFIG_REG,
              MUX_DEBUG_REG, TI_VID_STATUS_REG, USER_VID_CONFIG, USER_VID_STATUS_REG, RX_USER_SVID_ATTN_VDM_REG, RX_USER_SVID_OTHER_VDM_REG]


# Most firmware builds do not support the extended host interface commands
REGS_LIST_EXTENDED_HI_COMMANDS = [ VID, DID, UID, MODE_REG, VERSION_REG, DEVICE_INFO_REG, CUSTUSE, BOOT_FLAGS, STATUS_REG, DATA_STATUS_REG, CONTROL_CONFIG_REG, SYS_CONFIG_REG, SYS_POWER, PWR_STATUS, PD_STATUS,
              PP5V_CUR_LIMIT, PPHV_CUR_LIMIT, PPHVE_CUR_LIMIT, VCONN_CUR_LIMIT, ACTIVE_CONTRACT_PDO, ACTIVE_CONTRACT_RDO, SINK_REQUEST_RDO, TX_SOURCE_CAP, TX_SINK_CAP,
              RX_SOURCE_CAP, RX_SINK_CAP, AUTONEGOTIATE_SINK, INT_EVENT1, INT_MASK1, INT_EVENT2, INT_MASK2, GPIO_CONFIG_REG_1, GPIO_CONFIG_REG_2, GPIO_STATUS, PWR_SWITCH, TX_IDENTITY_REG,
              RX_IDENTITY_SOP_REG, RX_IDENTITY_SOPP_REG, RX_VDM_REG, RX_ATTN_REG, ALT_MODE_ENTRY, DATA_CONTROL_REG, DP_CAPABILITIES_REG, INTEL_CONFIG_REG,
              DP_STATUS_REG, INTEL_STATUS_REG, PWR_SWITCH, CCn_PINSTATE, SLEEP_CONFIG_REG, FW_STATE_HISTORY, FW_STATE_CONFIG, FW_STATE_FOCUS, FW_STATE, MUX_DEBUG_REG, TI_VID_STATUS_REG,
              USER_VID_CONFIG, USER_VID_STATUS_REG, RX_USER_SVID_ATTN_VDM_REG, RX_USER_SVID_OTHER_VDM_REG]


def registerByName(name):
    global REGS_LIST
    for reg in REGS_LIST:
        if reg.name == name :
            return reg

if __name__ == "__main__":
    print 'This file is a helper file defining register class definitions and is not meant to be used stand alone.'
    print 'It should be imported into a python environment or another script using:'
    print 'from register_definitions import *'
    sys.exit()
