#!/bin/env python
# -*- coding: cp1252 -*-
#==========================================================================
# (c) 2015 Texas Instruments
#--------------------------------------------------------------------------
# Project : Method and parameter definitions for a generic register class
# File    : function_class.py
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

#  The function class is a wrapper for the 4CC functions in
#  hi_functions.py to integrate into the GUI

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
    return self.value

def defaultRevTranslate(self, value): 
    return value

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

def decTranslate_func(self):
    return '%d' %(int(self.value))

def hexTranslate_func(self):
    return '0x' + hex(self.value)[2:]

def hexRevTranslate(self, value):
        if value[:2] == '0x':
            return int(value,16)
        else:
            return int(value)

emptyList = list()

class cInputOutput:
    def __init__(self,  iName, iHide, iValue, iUnit, iTranslateList, iTranslate=defaultTranslate, iRevTranslate=defaultRevTranslate):
        self.name = iName
        self.translate = iTranslate
        self.unit = iUnit
        self.revtranslate = iRevTranslate
        self.translist = iTranslateList
        self.hide = iHide
        self.value = iValue

        if ((iTranslate == defaultTranslate) & (iTranslateList != emptyList)):
            self.translate = listTranslate
            self.revtranslate = listRevTranslate
        else:
            self.translate = iTranslate  # opportunity to translate value into human readable
            self.reversetranslate = iRevTranslate
            
        self.translateList = iTranslateList  # lookup table for field bit settings


class cFunction:
    def __init__(self, iDict):
        self.name = iDict['function name']
        self.execute = iDict['execute']

        if 'associate register' in iDict :
            self.assregister = iDict['associate register']
        
        self.inputs = list()
        for f in list(iDict['inputs']):
            if 'unit' in f:
                myUnit = f['unit']
            else:
                myUnit = defaultUnit

            if 'translate list' in f:
                myTranslateList = f['translate list']
                myTranslate = listTranslate
                myRevTranslate = listRevTranslate
            else:
                myTranslateList = emptyList
                myTranslate = defaultTranslate
                myRevTranslate = defaultRevTranslate

            if 'translate' in f:
                myTranslate = f['translate']
                if 'reverse translate' in f:
                    myRevTranslate = f['reverse translate']
                else:
                    myRevTranslate = defaultRevTranslate

            self.inputs.append(cInputOutput(f['name'], 0, f['value'], myUnit, myTranslateList, myTranslate, myRevTranslate))
                
        self.outputs = list()
        for f in list(iDict['outputs']):
            if 'unit' in f:
                myUnit = f['unit']
            else:
                myUnit = defaultUnit

            if 'translate list' in f:
                myTranslateList = f['translate list']
                myTranslate = listTranslate
                myRevTranslate = listRevTranslate
            else:
                myTranslateList = emptyList
                myTranslate = defaultTranslate
                myRevTranslate = defaultRevTranslate

            if 'translate' in f:
                myTranslate = f['translate']
                if 'reverse translate' in f:
                    myRevTranslate = f['reverse translate']
                else:
                    myRevTranslate = defaultRevTranslate

            self.outputs.append(cInputOutput(f['name'], 1, f['value'], myUnit, myTranslateList, myTranslate, myRevTranslate))
            

#==========================================================================
# FUNCTIONS
#==========================================================================


#==========================================================================
# main
#==========================================================================


if __name__ == "__main__":
    print 'This file is a helper file defining register class definitions and is not meant to be used stand alone.'
    print 'It should be imported into a python environment or another script using:'
    print 'from function_class import *'
    sys.exit()
