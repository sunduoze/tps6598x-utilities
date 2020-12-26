#!/bin/env python
# -*- coding: cp1252 -*-
#==========================================================================
# (c) 2015 Texas Instruments
#--------------------------------------------------------------------------
# Project : Example application utilizing TPS65982 Host Interface
# File    : send_commands.py
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
from array import array, ArrayType
from register_definitions import *
from hi_functions import *

from hw_interface import *



#==========================================================================
# GLOBALS
#==========================================================================

handle = hw_interface(config.DEVICE_I2C_ADDR, config.HW_INTERFACE)        

def buildByteArray(data, numBytes) :
    retval = array('B')

    for i in range(numBytes) :
        retval.append((data & (0xFF << 8*i)) >> 8*i)

    return retval

#==========================================================================
# help command
#==========================================================================

def help_msg():
    print 'The following commands are supported (enter number in brackets)'
    print '[0] Print this help'
    print '[1] Issue a PD hard reset (HRST)'
    print '[2] Issue a PD swap to sink request (SWSk)'
    print '[3] Issue a PD swap to source request (SWSr)'
    print '[4] Issue a PD swap to UFP request (SWDF)'
    print '[5] Issue a PD swap to DFP request (SWUF)'
    print '[6] Turn one or all GPIO off (GPsl)'
    print '[7] Turn one or all GPIO on (GPsh)'
    print '[8] Query modes supported by SVID (GCDm)'
    print '[9] Enter Alternate Mode (AMEn)'
    print '[10] Exit Alternate Mode (AMEx)'
    print '[11] Clear Dead Battery Flag (DBfg)'
    print '[12] Alternate Mode Discovery Start (AMDs)'
    print '[13] Read from arbitrary register'
    print '[14] Write to arbitrary register'
    
    print '[-1] Exit'

    

#==========================================================================
# main
#==========================================================================
enable_disable_list = [ 'disabled', 'enabled' ]


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
       

    # start by printing the help message
    help_msg()

    # read user input

    while 1:
        input_var = input('> ')
        input_int = int(input_var)

        if input_int == 0:
            help_msg()

        if input_int == 1:
            print 'Initial Settings'
            PD_STATUS.read(handle)
            PD_STATUS.fieldByName('HardResetType').show()

            # set gpio as output
            print 'Issuing HRST (PD Hard Reset)'
            print HRST(handle)

            print 'Final Settings'
            PD_STATUS.read(handle)
            PD_STATUS.fieldByName('HardResetType').show()

        if input_int == 2:
            print 'Initial Settings'
            PWR_STATUS.read(handle)
            PWR_STATUS.fieldByName('PowerConnection').show()
            PWR_STATUS.fieldByName('SourceSink').show()

            # set gpio as output
            print 'Issuing SWSk (Swap to Sink)'
            print SWSk(handle)

            print 'Final Settings'
            PWR_STATUS.read(handle)
            PWR_STATUS.fieldByName('PowerConnection').show()
            PWR_STATUS.fieldByName('SourceSink').show()

        if input_int == 3:
            print 'Initial Settings'
            PWR_STATUS.read(handle)
            PWR_STATUS.fieldByName('PowerConnection').show()
            PWR_STATUS.fieldByName('SourceSink').show()

            # set gpio as output
            print 'Issuing SWSr (Swap to Source)'
            print SWSr(handle)

            print 'Final Settings'
            PWR_STATUS.read(handle)
            PWR_STATUS.fieldByName('PowerConnection').show()
            PWR_STATUS.fieldByName('SourceSink').show()

        if input_int == 4:
            print 'Initial Settings'
            STATUS_REG.read(handle)
            STATUS_REG.fieldByName('ConnState').show()
            STATUS_REG.fieldByName('DataRole').show()

            # set gpio as output
            print 'Issuing SWUF (Swap to UFP)'
            print SWUF(handle)

            print 'Final Settings'
            STATUS_REG.read(handle)
            STATUS_REG.fieldByName('ConnState').show()
            STATUS_REG.fieldByName('DataRole').show()


        if input_int == 5:
            print 'Initial Settings'
            STATUS_REG.read(handle)
            STATUS_REG.fieldByName('ConnState').show()
            STATUS_REG.fieldByName('DataRole').show()

            # set gpio as output
            print 'Issuing SWDF (Swap to DFP)'
            print SWDF(handle)

            print 'Final Settings'
            STATUS_REG.read(handle)
            STATUS_REG.fieldByName('ConnState').show()
            STATUS_REG.fieldByName('DataRole').show()

        if input_int == 6:
            input_var = input('Enter GPIO number (-1 for all)> ')
            input_int2 = int(input_var)
            if input_int2 == -1:
                print 'Enabling all GPIO as output and setting all to low'
                for gpio in range(19):
                    GPoe(handle, gpio)
                    print GPsl(handle, gpio)
            else:    
                # set gpio as output
                print 'Enabling gpio %d as output' %input_int2
                print GPoe(handle, input_int2)
                # set gpio low
                print 'Setting gpio %d low' %input_int2
                print GPsl(handle, input_int2)

            print '\nFinal GPIO Status:\n'
            GPIO_STATUS.read(handle)
            GPIO_STATUS.show()

        if input_int == 7:
            input_var = input('Enter GPIO number (-1 for all)> ')
            input_int2 = int(input_var)
            if input_int2 == -1:
                print 'Enabling all GPIO as output and setting all to high'
                for gpio in range(19):
                    GPoe(handle, gpio)
                    print GPsh(handle, gpio)
            else:    
                # set gpio as output
                print 'Enabling gpio %d as output' %input_int2
                print GPoe(handle, input_int2)
                # set gpio low
                print 'Setting gpio %d high' %input_int2
                print GPsh(handle, input_int2)

            print '\nFinal GPIO Status:\n'
            GPIO_STATUS.read(handle)
            GPIO_STATUS.show()

        if input_int == 8:
            input_var = input('Enter SVID (dec or hex w/ 0x) > ')
            input_int2 = input_var
            # Run GCDm
            modes = GCdm(handle, input_int2)

            print '\nModes supported by SVID = 0x%x:\n' %input_int2
            if len(modes) == 0:
                print '<none>'
            for next_obj_posn in modes:                
                print '\t0x%x' %modes[next_obj_posn]

        if input_int == 9:
            input_var = input('Enter SVID (dec or hex w/ 0x) > ')
            input_int2 = input_var
            # Run GCDm
            modes = GCdm(handle, input_int2)

            print '\nModes supported by SVID = 0x%x:\n' %input_int2
            if len(modes) == 0:
                print '<none>'
            for next_obj_posn in modes:                
                print '\tobject position = %d \t0x%x' %(next_obj_posn, modes[next_obj_posn])

            input_mode = input('Enter object position to enter (dec or hex w/ 0x) > ')

            print 'Issuing AMEn'
            print AMEn(handle, input_int2, input_mode)

            DATA_STATUS_REG.read(handle)
            print '\tIntel Thunderbolt (SVID 0x8086) State: %s' %enable_disable_list[ DATA_STATUS_REG.fieldByName('TBTConnection').value ]
            print '\tDisplay Port (SVID 0xFF01) State: %s' %enable_disable_list[ DATA_STATUS_REG.fieldByName('DPConnection').value ]


        if input_int == 10:
            input_var = input('Enter SVID (dec or hex w/ 0x) > ')
            input_int2 = input_var
            # Run GCDm
            modes = GCdm(handle, input_int2)

            print '\nModes supported by SVID = 0x%x:\n' %input_int2
            if len(modes) == 0:
                print '<none>'
            for next_obj_posn in modes:                
                print '\tobject position = %d \t0x%x' %(next_obj_posn, modes[next_obj_posn])

            input_mode = input('Enter object position to exit (dec or hex w/ 0x) > ')

            print 'Issuing AMEx'
            print AMEx(handle, input_int2, input_mode)

            DATA_STATUS_REG.read(handle)
            print '\tIntel Thunderbolt (SVID 0x8086 or 0x8087) State: %s' %enable_disable_list[ DATA_STATUS_REG.fieldByName('TBTConnection').value ]
            print '\tDisplay Port (SVID 0xFF01) State: %s' %enable_disable_list[ DATA_STATUS_REG.fieldByName('DPConnection').value ]

        if input_int == 11:
            print 'Boot flags initial state:'
            BOOT_FLAGS.read(handle)
            BOOT_FLAGS.show()

            print 'Clearing dead battery flag with DBfg\n'
            print DBfg(handle)

            print 'Boot flags final state:'
            BOOT_FLAGS.read(handle)
            BOOT_FLAGS.show()

        if input_int == 12:
            print 'Issuing Alternate Mode Discovery Start\n'
            print AMDs(handle)

        if input_int == 13:
            print 'Read from arbitrary register\n'
            input_address = input('Enter register address (dec or hex w/ 0x) > ')
            input_numbytes = input('Enter number of bytes to read (dec or hex w/ 0x) > ')

            (count, readBytes) = read_reg(handle, int(input_address), int(input_numbytes)+1)

            j = 0
            for i in range((count-1) // 4) :
                value32 = readBytes[4*i] | (readBytes[4*i+1] << 8) | (readBytes[4*i+2] << 16) | (readBytes[4*i+3] << 24)
                print '0x%08x' %value32
                j+=1

            if (count-1) > 4*j :
                value32 = 0x0
                for i in range(count - 1 - 4*j) :
                    value32 |= readBytes[4*j + i] << 8*i
                print '0x%08x' %value32
                    
        if input_int == 14:
            print 'Write to arbitrary register\n'
            input_address = input('Enter register address (dec or hex w/ 0x) > ')
            input_numbytes = input('Enter number of bytes to write (dec or hex w/ 0x) > ')
            input_value = input('Enter value to write to register (dec or hex w/ 0x) > ')

            write_reg(handle, int(input_address), buildByteArray(int(input_value), int(input_numbytes)) )

        if input_int == -1:
            break



    # Close the device
    handle.hw_close()
