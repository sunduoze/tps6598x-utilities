#!/bin/env python
# -*- coding: cp1252 -*-
#==========================================================================
# (c) 2015 Texas Instruments
#--------------------------------------------------------------------------
# Project : Method and parameter definitions for a generic register class
# File    : register_class.py
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

# for simplicity we import the read and write function layer as global functions
#    Be sure to only import one physical layer implementation
from array import *
from device_rw import *

#==========================================================================
# GLOBALS
#==========================================================================


#==========================================================================
# REGISTER CLASS DEFINITIONS
#==========================================================================

def lentomask(length):
    ret = 0x0
    for i in range(length):
        ret |= 1 << i
    return ret

def defaultTranslate(self):
    eOverflow = Exception(-1)
    retval = self.value & lentomask(self.length)
    if retval != self.value :
        eOverflow.message = "Truncated field to report. Stored value = 0x%x. Truncated value = 0x%x\n" %(self.value, retval)
        eOverflow.message += "Register = %s, field = %s\n" %(self.register.name, self.name)
        raise eOverflow        
    return self.value

# value is natively an integer so always convert
# This is important for the GUI where values are submitted as Unicode
def defaultRevTranslate(self, value): 
    eOverflow = Exception(-1)
    if value[:2] == '0x':
        retval = int(value, 16) & lentomask(self.length)
        if int(value, 16) != retval:
            eOverflow.message = "Truncated field to store. Input value = 0x%x. Truncated value = 0x%x\n" %(value, retval)
            eOverflow.message += "Register = %s, field = %s\n" %(self.register.name, self.name)
            raise eOverflow            
        return retval
    else:
        retval = int(value) & lentomask(self.length)
        if int(value) != retval:
            eOverflow.message = "Truncated field to store. Input value = %d. Truncated value = %d\n" %(value, retval)
            eOverflow.message += "Register = %s, field = %s\n" %(self.register.name, self.name)
            raise eOverflow            
        return retval

def defaultUnit(self):
    return ''

def defaultHide(self):
    return 0

def listTranslate(self):
    if self.value < len(self.translateList):
        return self.translateList[self.value]
    else:
        return 'reserved (%d)' %self.value

def listRevTranslate(self, value):
    if value in self.translateList:
        return self.translateList.index(value)
    else:
        return 0

def charTranslate(self):
    return chr(self.value)

def decTranslate(self):
    return '%d' %self.value

def decRevTranslate(self, val):
    value = str(val)
    eOverflow = Exception(-1)
    if value[:2] == '0x':
        retval = int(value, 16) & lentomask(self.length)
        if int(value, 16) != retval:
            eOverflow.message = "Truncated field to store. Input value = 0x%x. Truncated value = 0x%x\n" %(value, retval)
            eOverflow.message += "Register = %s, field = %s\n" %(self.register.name, self.name)
            raise eOverflow            
        return retval
    else:
        retval = int(value) & lentomask(self.length)
        if int(value) != retval:
            eOverflow.message = "Truncated field to store. Input value = %d. Truncated value = %d\n" %(value, retval)
            eOverflow.message += "Register = %s, field = %s\n" %(self.register.name, self.name)
            raise eOverflow            
        return retval

def hexTranslate(self):
    return '0x' + hex(self.value)[2:].zfill(self.length/4)

def hexRevTranslate(self, val):
    value = int(val)
    eOverflow = Exception(-1)
    if value[:2] == '0x':
        retval = int(value, 16) & lentomask(self.length)
        if int(value, 16) != retval:
            eOverflow.message = "Truncated field to store. Input value = 0x%x. Truncated value = 0x%x\n" %(value, retval)
            eOverflow.message += "Register = %s, field = %s\n" %(self.register.name, self.name)
            raise eOverflow            
        return retval
    else:
        retval = int(value) & lentomask(self.length)
        if int(value) != retval:
            eOverflow.message = "Truncated field to store. Input value = %d. Truncated value = %d\n" %(value, retval)
            eOverflow.message += "Register = %s, field = %s\n" %(self.register.name, self.name)
            raise eOverflow            
        return retval

def show_by_field(self):
    print "%s (0x%x)" % (self.name, self.addr)
    field_dict_array = []
    for f in self.fields:
        if (f.hide(f) != 1):
            if f.report() != None:
                field_dict_array.append( f.report())

    col_width = max(len(entry['name']) for entry in field_dict_array) + 3
    col_width2 = max(len('[%d:%d]' %(entry['offset']+entry['length']-1,entry['offset'])) for entry in field_dict_array) + 3

    for entry in field_dict_array:
            print '\t' + ('[%d:%d]' %(entry['offset']+entry['length']-1,entry['offset'])).ljust(col_width2)  + entry['name'].ljust(col_width, ' ') + entry['value'] + ' ' + entry['unit']

def le_register_show(self):
    outstring=''
    for f in self.fields:
        outstring = outstring + chr(f.value & 0xFF)
    print '%s\t%s\n' %(self.name, outstring)

def be_hex_show(self):
    outstring=''
    for f in self.fields:
        outstring = hex(f.value & 0xFF)[2:].zfill(2) + outstring
    outstring='0x' + outstring
    print '%s\t%s\n' %(self.name, outstring)


emptyList = list()

class cField:
    def __init__(self, iName, iOffset, iLength, iValue, iUnit, iHide, iRegister, iTranslate=defaultTranslate, iRevTranslate=defaultRevTranslate, iTranslateList=emptyList):
        self.name = iName
        self.offset = iOffset
        self.length = iLength
        self.value = iValue & lentomask(iLength)
        self.register = iRegister
        self.unit = iUnit
        self.hide = iHide
        if ((iTranslate == defaultTranslate) & (iTranslateList != emptyList)):
            self.translate = listTranslate
            self.reversetranslate = listRevTranslate
        else:
            self.translate = iTranslate  # opportunity to translate value into human readable
            self.reversetranslate = iRevTranslate
        self.translateList = iTranslateList  # lookup table for field bit settings
    def show(self):
        if self.name != 'Reserved' and self.name != 'reserved' and self.translate(self) != None:
            print '\t%s\t\t%s' % (self.name, str(self.translate(self)))
    def report(self):
        if self.name != 'Reserved' and self.name != 'reserved' and self.translate(self) != None:
            return {'name' : self.name, 'value' : str(self.translate(self)), 'offset' : self.offset, 'length' : self.length, 'unit' : self.unit(self)}
        else:
            return None

class cRegister:
    def __init__(self, iDict):
        self.name = iDict['register name']
        self.addr = iDict['address']
        self.RW = iDict['permission']
        if 'translate' in iDict:
            self.translate = iDict['translate']
        else:
            self.translate = show_by_field
        self.fields = list()
        for f in list(iDict['fields']):
            if 'unit' in f:
                myUnit = f['unit']
            else:
                myUnit = defaultUnit

            if 'hide' in f:
                myHide = f['hide']
            else:
                myHide = defaultHide
                
            # make sure its a cField
            if 'translate list' in f:
                self.fields.append(cField(f['name'], f['offset'], f['length'], f['value'], myUnit, myHide, self, listTranslate, listRevTranslate, f['translate list']))
            elif 'translate' in f:
                if 'reverse translate' in f:
                    self.fields.append(cField(f['name'], f['offset'], f['length'], f['value'], myUnit, myHide, self, f['translate'], f['reverse translate']))
                else:
                    self.fields.append(cField(f['name'], f['offset'], f['length'], f['value'], myUnit, myHide, self, f['translate']))
            else:
                self.fields.append(cField(f['name'], f['offset'], f['length'], f['value'], myUnit, myHide, self))

    def length(self):
        mySize=0
        for f in self.fields:
            mySize += f.length
        return (mySize)
    def fieldByName(self, name):
        for f in self.fields:
            if f.name == name:
                return f
            
    def byteArray(self):
        localLength = self.length() // 8
        if (self.length() % 8) != 0:
            localLength += 1
        strArray = ''
        for i in range(8*localLength):
            strArray += '0'
        for f in self.fields:
            if f.offset != 0:
                strArray = strArray[:-f.offset-f.length] + bin(f.value)[2:].zfill(f.length) + strArray[-f.offset:]
            else :
                strArray = strArray[:-f.length] + bin(f.value)[2:].zfill(f.length) 
            
        ret = array('B')

        for i in range(localLength):
            if i != 0:
                ret.append(int(strArray[-i*8-8:-i*8],2))
            else:
                ret.append(int(strArray[-8:],2))

        return ret

    def showByteArray(self):
        byteArray = self.byteArray()

        myString = ''
        for b in byteArray:
            myString = str('0x%x ' %b) + myString

        print '%s' %myString
                          
    def read(self, hw_handle):
        numbytes = self.length() // 8
        (count,readByteArray) = read_reg(hw_handle, self.addr,numbytes+1)
        assert count==numbytes+1
        strArray = ''
        for i in range(len(readByteArray)):
            strArray = bin(readByteArray[i])[2:].zfill(8) + strArray 
        for f in self.fields:
            if f.offset != 0:
                f.value = int(strArray[-f.offset-f.length:-f.offset],2)
            else:
                f.value = int(strArray[-f.length:],2)

    def write(self, hw_handle):
        numbytes = self.length() // 8
        write_reg(hw_handle,self.addr, self.byteArray())

    def show(self):
        self.translate(self)
            

#==========================================================================
# FUNCTIONS
#==========================================================================


#==========================================================================
# main
#==========================================================================


if __name__ == "__main__":
    print 'This file is a helper file defining register class definitions and is not meant to be used stand alone.'
    print 'It should be imported into a python environment or another script using:'
    print 'from register_class import *'
    sys.exit()
