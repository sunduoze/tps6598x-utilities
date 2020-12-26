#!/bin/env python
# -*- coding: cp1252 -*-
#==========================================================================
# (c) 2015 Texas Instruments
#--------------------------------------------------------------------------
# Project : Example application utilizing TPS65982 Host Interface
# File    : alternate_modes.py
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
        
    print '\n'

    SVIDs_list = [ 0xff01, 0x8086, 0x8087, 0x0451 ]

    dict_of_modes_by_dict_of_svid = {}

    # discover modes for each SVID
    for next_svid in SVIDs_list:
        dict_of_modes_by_dict_of_svid[next_svid] = GCdm(handle, next_svid)
        
    # print discovered modes
    for next_svid in dict_of_modes_by_dict_of_svid:
        print 'SVID = 0x%x' %(next_svid)
        for next_obj_posn in dict_of_modes_by_dict_of_svid[next_svid]:
            print '\tobject position: %s\n\tmode: 0x%x' %(next_obj_posn, dict_of_modes_by_dict_of_svid[next_svid][next_obj_posn])

    print '\n'
    print 'Exiting all SVIDs as initialization'
    
    # exit all modes as initialization
    for next_svid in dict_of_modes_by_dict_of_svid:
        for next_obj_posn in dict_of_modes_by_dict_of_svid[next_svid]:
            AMEx(handle, next_svid, next_obj_posn)

    enable_disable_list = [ 'disabled', 'enabled' ]


    DATA_STATUS_REG.read(handle)
    print '\tIntel Thunderbolt (SVID 0x8086 or 0x8087) State: %s' %enable_disable_list[ DATA_STATUS_REG.fieldByName('TBTConnection').value ]
    print '\tDisplay Port (SVID 0xFF01) State: %s' %enable_disable_list[ DATA_STATUS_REG.fieldByName('DPConnection').value ]

    print '\n'
    for next_svid in dict_of_modes_by_dict_of_svid:
        for next_obj_posn in dict_of_modes_by_dict_of_svid[next_svid]:
            print 'Attempting to enter SVID = 0x%x, mode = 0x%x' %(next_svid, dict_of_modes_by_dict_of_svid[next_svid][next_obj_posn]) 
            AMEn(handle, next_svid, next_obj_posn)
            DATA_STATUS_REG.read(handle)
            print '\tIntel Thunderbolt (SVID 0x8086 or 0x8087) State: %s' %enable_disable_list[ DATA_STATUS_REG.fieldByName('TBTConnection').value ]
            print '\tDisplay Port (SVID 0xFF01) State: %s' %enable_disable_list[ DATA_STATUS_REG.fieldByName('DPConnection').value ]
            print '\n'
            AMEx(handle, next_svid, next_obj_posn)

    # Close the device
    try :
        handle.hw_close()        
    except Exception as e :
        print e.message
        sys.exit()

    sys.exit()
