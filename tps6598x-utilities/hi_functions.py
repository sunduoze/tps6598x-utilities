#!/bin/env python

# requires
# pip install enum

#==========================================================================
# IMPORTS
#==========================================================================
import sys
import struct
import time

from device_rw import *
from register_definitions import *
from function_class import *

HI_TIMEOUT_SEC = 5

def byteArray(n):
    strArray = bin(n)[2:].zfill(8*((len(bin(n)[2:])-1) / 8) + 8)

    ret = array('B')

    for i in range(len(strArray)/8):
        if i != 0:
            ret.append(int(strArray[-i*8-8:-i*8],2))
        else:
            ret.append(int(strArray[-8:],2))

    return ret

def verify_cmd_completed(handle, hi_timeout_sec = None) :
    global HI_TIMEOUT_SEC

    if (hi_timeout_sec == None) :
        hi_timeout_sec = HI_TIMEOUT_SEC
    hw_sleep_ms(1)
    (count, cmd_result) = read_reg_4cc(handle, 0x08)
    assert count == 5
    basetime_s = time.time()
    while cmd_result[0] != CC_ZERO:
        hw_sleep_ms(100)
        (count, cmd_result) = read_reg_4cc(handle, 0x08)
        assert count == 5
        if cmd_result.tostring() == CC_NOT_ZERO:
            return "Cmd STATUS ERROR: %s" %cmd_result.tostring()
        if ((time.time() - basetime_s) > HI_TIMEOUT_SEC) :
            # timeout has been reached
            write_reg_4cc(handle, 0x08, 'ABRT')
            basetime_s = time.time()
            (count, cmd_result) = read_reg_4cc(handle, 0x08)
            while cmd_result[0] != CC_ZERO:
                hw_sleep_ms(100)
                assert count == 5
                if cmd_result.tostring() == CC_NOT_ZERO:
                    return "Cmd TIMEOUT followed by ABRT rejection: %s" %cmd_result.tostring()
                else :
                    if((time.time() - basetime_s) > 5) :
                        return "**********************************\nHost Interface function timeout followed by ABRT timeout\n**********************************\n"
            (count, cmd_result) = read_reg_4cc(handle, 0x08)                        
            return "**********************************\nHost Interface function aborted due to %d second timeout\n**********************************\n" %HI_TIMEOUT_SEC

    return "Success"


task_return_dict = { 0x00000000 : 'SUCCESS_CMD', 0x00000001 : 'ABORT_CMD', 0x00000003 : 'REJECT_CMD' }

def verify_task_status(handle):
    hw_sleep_ms(1)
    (count, data) = read_reg(handle, 0x9, 2)
    assert count == 2
    if data[0] != 0:
        if data[0] in task_return_dict :
            return "     Error -> Task Status: %d (%s)" %(data[0], task_return_dict[data[0]])
        else :
            return "     Error -> Task Status: %d (UNKNOWN)" %(data[0])
    else :
        return "Success"

# read and write aren't 4cc commands, but a good place to implement a raw register read or write
def read(handle, register, length):
    (count, data) = read_reg(handle, register, length+1)

    if count == length + 1 :
        return ("Read successful", data)
    else :
        return ("Read failed. Attempted %d bytes, read %d bytes." %(length+1, count), data)

def execRead(self, handle):
    (msg, data) = read(handle, self.inputs[0].value, self.inputs[1].value)

    value = 0
    for (i,byte) in enumerate(data) :
        value |= byte << (8*i)

    self.outputs[0].value = value
    self.outputs[0].hide = 0

    return msg

objRead = cFunction({'function name' : 'read',
            'inputs' : [
               { 'name' : 'Register Address', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
               { 'name' : 'Register Length', 'value' : 0, 'type' : '32-bit', 'translate' : decTranslate_func, 'reverse translate' : hexRevTranslate} ,
            ],
            'outputs' : [
               { 'name' : 'Register Value', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
            ],
            'execute' : execRead } )



#def write(handle, register, length, data):
# read and write aren't 4cc commands, but a good place to implement a raw register read or write
def write(handle, register, length, value):
    data_out = array('B', [ 0 for i in range(length) ])

    for i in range(length) :
        data_out[i] = (value >> (8*i)) & (0xFF)

    write_reg(handle, register, data_out)

    return ("Write successful")

def execWrite(self, handle):
    msg = write(handle, self.inputs[0].value, self.inputs[1].value, self.inputs[2].value)

    return msg

objWrite = cFunction({'function name' : 'write',
            'inputs' : [
               { 'name' : 'Register Address', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
               { 'name' : 'Register Length', 'value' : 0, 'type' : '32-bit', 'translate' : decTranslate_func, 'reverse translate' : hexRevTranslate} ,
               { 'name' : 'Register Value', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
            ],
            'outputs' : [
            ],
            'execute' : execWrite } )



# Issue warm reboot of device
def ABRT(handle):
    write_reg_4cc(handle, 0x08, 'ABRT')    
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        # Special Case, successful Abort returns ABORT_CMD
        (count, data) = read_reg(handle, 0x9, 2)
        assert count == 2
        if data[0] == 0x3:
            return "Function returned ABORT_CMD (Success)"
        else :
            return "     Error -> Task Status: %d (%s)" %(data[0], task_return_dict[data[0]])
    else :
        return cmdret

def execABRT(self, handle):
    return ABRT(handle)
    
objABRT = cFunction({'function name' : 'ABRT',
            'inputs' : [
            ],
            'outputs' : [
            ],
            'execute' : execABRT } )


# Issue warm reboot of device
def Gaid(handle):
    write_reg_4cc(handle, 0x08, 'Gaid')    
    return verify_cmd_completed(handle)

def execGaid(self, handle):
    return Gaid(handle)
    
objGaid = cFunction({'function name' : 'Gaid',
            'inputs' : [
            ],
            'outputs' : [
            ],
            'execute' : execGaid } )



# Issue warm reboot of device
def GAID(handle):
    write_reg_4cc(handle, 0x08, 'GAID')    
    return verify_cmd_completed(handle)

def execGAID(self, handle):
    return GAID(handle)
    
objGAID = cFunction({'function name' : 'GAID',
            'inputs' : [
            ],
            'outputs' : [
            ],
            'execute' : execGAID } )



# Issue PD Hard Reset
def HRST(handle):
    write_reg_4cc(handle, 0x08, 'HRST')    
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return verify_task_status(handle)
    else :
        return cmdret

def execHRST(self, handle):
    return HRST(handle)
    
objHRST = cFunction({'function name' : 'HRST',
            'inputs' : [
            ],
            'outputs' : [
            ],
            'execute' : execHRST } )


# Issue Cable Reset
def CRST(handle):
    write_reg_4cc(handle, 0x08, 'CRST')    
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return verify_task_status(handle)
    else :
        return cmdret

def execCRST(self, handle):
    return CRST(handle)
    
objCRST = cFunction({'function name' : 'CRST',
            'inputs' : [
            ],
            'outputs' : [
            ],
            'execute' : execCRST } )


# clear dead battery flag
def DBfg(handle):
    write_reg_4cc(handle, 0x08, 'DBfg')
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return verify_task_status(handle)
    else :
        return cmdret
    
def execDBfg(self, handle):
    return DBfg(handle)
    
objDBfg = cFunction({'function name' : 'DBfg',
            'inputs' : [
            ],
            'outputs' : [
            ],
            'execute' : execDBfg } )


# Get Sink Capabilities
# Does not return value, loads RxSnkCapabilities register
def GSkC(handle):
    write_reg_4cc(handle, 0x08, 'GSkC')
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return verify_task_status(handle)
    else :
        return cmdret


def execGSkC(self, handle):
    return GSkC(handle)
    
objGSkC = cFunction({'function name' : 'GSkC',
            'inputs' : [
            ],
            'outputs' : [
            ],
            'execute' : execGSkC,
            'associate register' : RX_SINK_CAP } )


# Get Source Capabilities
# Does not return value, loads RxSrcCapabilities register
def GSrC(handle):
    write_reg_4cc(handle, 0x08, 'GSrC')    
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return verify_task_status(handle)
    else :
        return cmdret

def execGSrC(self, handle):
    return GSrC(handle)
    
objGSrC = cFunction({'function name' : 'GSrC',
            'inputs' : [
            ],
            'outputs' : [
            ],
            'execute' : execGSrC,
            'associate register' : RX_SOURCE_CAP } )


# Send Source Capabilities
# Does not have input value, uses TxSrcCapabilities register
def SSrC(handle):
    write_reg_4cc(handle, 0x08, 'SSrC')    
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return verify_task_status(handle)
    else :
        return cmdret

def execSSrC(self, handle):
    return SSrC(handle)
    
objSSrC = cFunction({'function name' : 'SSrC',
            'inputs' : [
            ],
            'outputs' : [
            ],
            'execute' : execSSrC, 
            'associate register' : TX_SOURCE_CAP } )


# Accept the next RDO Received
# Generally used in conjunction with register 0x36, Sink Request RDO register
def ARDO(handle):
    mesg = ""
    CONTROL_CONFIG_REG.read(handle)
    if CONTROL_CONFIG_REG.fieldByName('RDOIntrusiveMode').value != EnabledDisabled_list.index('Enabled'):
        mesg += '**********************************************************************\n'
        mesg += 'WARNING: RDO Intrusive Mode is currently not set\n'
        mesg += 'Issued ARDO will be ignored\n'
        mesg += '**********************************************************************\n'    
    write_reg_4cc(handle, 0x08, 'ARDO')
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return mesg + verify_task_status(handle)
    else :
        return mesg + cmdret

def execARDO(self, handle):
    return ARDO(handle)
    
objARDO = cFunction({'function name' : 'ARDO',
            'inputs' : [
            ],
            'outputs' : [
            ],
            'execute' : execARDO, 
            'associate register' : SINK_REQUEST_RDO } )



# Reject the next RDO Received
# Generally used in conjunction with register 0x36, Sink Request RDO register
def RRDO(handle):
    mesg = ""
    CONTROL_CONFIG_REG.read(handle)
    if CONTROL_CONFIG_REG.fieldByName('RDOIntrusiveMode').value != EnabledDisabled_list.index('Enabled'):
        mesg += '**********************************************************************\n'
        mesg += 'WARNING: RDO Intrusive Mode is currently not set\n'
        mesg += 'Issued RRDO will be ignored\n'
        mesg += '**********************************************************************\n'
    write_reg_4cc(handle, 0x08, 'RRDO')    
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return mesg + verify_task_status(handle)
    else :
        return mesg + cmdret

def execRRDO(self, handle):
    return RRDO(handle)
    
objRRDO = cFunction({'function name' : 'RRDO',
            'inputs' : [
            ],
            'outputs' : [
            ],
            'execute' : execRRDO, 
            'associate register' : SINK_REQUEST_RDO } )


# build RDO helper function
def buildRDO(maxCurrentorPower, OperatingCurrentOrPower, NoUSBSuspend, USBCommCapable, CapabilityMismatch, GiveBackFlag, ObjectPosition) :
    return (maxCurrentorPower & 0x3FF) | (OperatingCurrentOrPower & 0x3FF) << 10 | (NoUSBSuspend & 0x1) << 24 | (USBCommCapable & 0x1) << 25 | (CapabilityMismatch & 0x1) << 26 | (GiveBackFlag & 0x1) << 27 | (ObjectPosition & 0x7) << 28 

def unit_mA(self) :
    return 'mA'

def trans_3(self):
    return int(self.value & 0x7)

def rev_trans_3(self, value):
    # in case its unicode
    retval = int(value)
    if retval > 0x7:
        retval = 0x7
    if retval < 0 :
        retval = 0
    return retval

# Send RDO
def SRDO(handle, sendRDO):
    mesg = ""
    CONTROL_CONFIG_REG.read(handle)
    if CONTROL_CONFIG_REG.fieldByName('PDOIntrusiveMode').value != EnabledDisabled_list.index('Enabled'):
        mesg += '**********************************************************************\n'
        mesg += 'WARNING: PDO Intrusive Mode is currently not set\n'
        mesg += 'Issued SRDO will be rejected\n'
        mesg += '**********************************************************************\n'

    data_in = byteArray(sendRDO)    
    write_reg(handle, 0x09, data_in)
    
    write_reg_4cc(handle, 0x08, 'SRDO')    
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return mesg + verify_task_status(handle)
    else :
        return mesg + cmdret

def execSRDO(self, handle):
    return SRDO(handle, buildRDO(self.inputs[0].value, self.inputs[1].value, self.inputs[2].value, self.inputs[3].value, self.inputs[4].value, self.inputs[5].value, self.inputs[6].value))
    
objSRDO = cFunction({'function name' : 'SRDO',
            'inputs' : [
               { 'name' : 'Max/Min Operating Current or Power', 'value' : 0, 'unit' : unit_mA, 'type' : '10-bit', 'translate' : translate_current, 'reverse translate' : rev_translate_current} ,
               { 'name' : 'Operating Current or Power', 'value' : 0, 'unit' : unit_mA, 'type' : '10-bit', 'translate' : translate_current, 'reverse translate' : rev_translate_current } ,
               { 'name' : 'No USB Suspend', 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'USB Communications Capable', 'value' : 0, 'translate list' : TrueFalse_list } ,
               { 'name' : 'Capability Mismatch', 'value' : 0, 'translate list' : TrueFalse_list  } ,
               { 'name' : 'Give Back Flag', 'value' : 0, 'translate list' : TrueFalse_list  } ,
               { 'name' : 'Object Position', 'value' : 0 , 'translate' : trans_3, 'reverse translate' : rev_trans_3 } ,
            ],
            'outputs' : [
            ],
            'execute' : execSRDO })



# Issue PR Swap to Power Sink
def SWSk(handle):
    mesg = ""
    BOOT_FLAGS.read(handle)
    if BOOT_FLAGS.fieldByName('DeadBatteryFlag').value == TrueFalse_list.index('True'):
        mesg += '**********************************************************************\n'
        mesg += 'WARNING: Dead Battery Flag is currently set\n'
        mesg += 'Issued SWSk will be ignored until DBfg command is issued\n'
        mesg += '**********************************************************************\n'
    write_reg_4cc(handle, 0x08, 'SWSk')
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return mesg + verify_task_status(handle)
    else :
        return mesg + cmdret

def execSWSk(self, handle):
    return SWSk(handle)
    
objSWSk = cFunction({'function name' : 'SWSk',
            'inputs' : [
            ],
            'outputs' : [
            ],
            'execute' : execSWSk, 
            'associate register' : PWR_STATUS } )



# Issue PR Swap to Power Source
def SWSr(handle):
    mesg = ""
    BOOT_FLAGS.read(handle)
    if BOOT_FLAGS.fieldByName('DeadBatteryFlag').value == TrueFalse_list.index('True'):
        mesg += '**********************************************************************\n'
        mesg += 'WARNING: Dead Battery Flag is currently set\n'
        mesg += 'Issued SWSr will be ignored until DBfg command is issued\n'
        mesg += '**********************************************************************\n'
    write_reg_4cc(handle, 0x08, 'SWSr')
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return mesg + verify_task_status(handle)
    else :
        return mesg + cmdret

def execSWSr(self, handle):
    return SWSr(handle)
    
objSWSr = cFunction({'function name' : 'SWSr',
            'inputs' : [
            ],
            'outputs' : [
            ],
            'execute' : execSWSr, 
            'associate register' : PWR_STATUS } )



# Issue PR Swap to Data DFP
def SWDF(handle):
    mesg = ""
    DP_STATUS_REG.read(handle)
    if DP_STATUS_REG.fieldByName('DP SID Active').value == TrueFalse_list.index('True'):
        mesg += '**********************************************************************\n'
        mesg += 'WARNING: DisplayPort Alternate Mode is Active\n'
        mesg += 'Issued SWDF will cause a PD Hard Reset on the far end\n'
        mesg += '**********************************************************************\n'
    INTEL_STATUS_REG.read(handle)
    if INTEL_STATUS_REG.fieldByName('Intel VID Active').value == TrueFalse_list.index('True'):
        mesg += '**********************************************************************\n'
        mesg += 'WARNING: Intel Thunderbolt Alternate Mode is Active\n'
        mesg += 'Issued SWDF will cause a PD Hard Reset on the far end\n'
        mesg += '**********************************************************************\n'
    CONTROL_CONFIG_REG.read(handle)
    write_reg_4cc(handle, 0x08, 'SWDF')
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return mesg + verify_task_status(handle)
    else :
        return mesg + cmdret

def execSWDF(self, handle):
    return SWDF(handle)
    
objSWDF = cFunction({'function name' : 'SWDF',
            'inputs' : [
            ],
            'outputs' : [
            ],
            'execute' : execSWDF, 
            'associate register' : STATUS_REG } )



# Issue PR Swap to Data UFP
def SWUF(handle):
    mesg = ""
    DP_STATUS_REG.read(handle)
    if DP_STATUS_REG.fieldByName('DP SID Active').value == TrueFalse_list.index('True'):
        mesg += '**********************************************************************\n'
        mesg += 'WARNING: DisplayPort Alternate Mode is Active\n'
        mesg += 'Issued SWUF will cause a PD Hard Reset on the far end\n'
        mesg += '**********************************************************************\n'
    INTEL_STATUS_REG.read(handle)
    if INTEL_STATUS_REG.fieldByName('Intel VID Active').value == TrueFalse_list.index('True'):
        mesg += '**********************************************************************\n'
        mesg += 'WARNING: Intel Thunderbolt Alternate Mode is Active\n'
        mesg += 'Issued SWUF will cause a PD Hard Reset on the far end\n'
        mesg += '**********************************************************************\n'
    CONTROL_CONFIG_REG.read(handle)
    write_reg_4cc(handle, 0x08, 'SWUF')
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return mesg + verify_task_status(handle)
    else :
        return mesg + cmdret

def execSWUF(self, handle):
    return SWDF(handle)
    
objSWUF = cFunction({'function name' : 'SWUF',
            'inputs' : [
            ],
            'outputs' : [
            ],
            'execute' : execSWUF, 
            'associate register' : STATUS_REG } )



# Issue PR VCONN swap
def SWVC(handle):
    mesg = ""
    CONTROL_CONFIG_REG.read(handle)
    write_reg_4cc(handle, 0x08, 'SWVC')
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return mesg + verify_task_status(handle)
    else :
        return mesg + cmdret

def execSWVC(self, handle):
    return SWVC(handle)
    
objSWVC = cFunction({'function name' : 'SWVC',
            'inputs' : [
            ],
            'outputs' : [
            ],
            'execute' : execSWVC } )



# Get Custom Discovered Modes
# takes 16-bit SVID value (LE byte ordering)
# returns a dict that translates object position into mode number
# and a reverse dict that translates mode number into object position
def GCdm(handle, SVID):
    mesg = ""
    STATUS_REG.read(handle)
    if STATUS_REG.fieldByName('DataRole').value == DataRole_list.index('UFP_or_Port_Disabled'):
        mesg += '**********************************************************************\n'
        mesg += 'WARNING: GCdm 4cc command has no effect when Data Role is UFP or there is no connection\n'
        mesg += 'Status Register indicates that Data Role is UFP or there is no connection\n'
        mesg += '**********************************************************************\n'
    data_in = byteArray(SVID)
    write_reg(handle, 0x09, data_in)
    write_reg_4cc(handle, 0x08, 'GCdm')
    
    verify_cmd_completed(handle)

    (count, data_out) = read_reg(handle, 0x09, 31)
    assert count == 31

    out_dict = {}

    for i in range(6):
        index = i*5 + 4
        if data_out[index] != 0:
            mode = (data_out[(i*5)+3] << 24) | (data_out[(i*5)+2] << 16) | (data_out[(i*5)+1] << 8) | data_out[i*5]
            out_dict[data_out[index]] = mode

    return out_dict


def execGCdm(self, handle):
    mesg = ""
    out_dict = GCdm(handle, self.inputs[0].value)

    index = 0
    for entry in out_dict:
        self.outputs[index].value = entry
        self.outputs[index].hide = 0
        index = index + 1
        
    for i in range(6 - index):
        self.outputs[index+i].hide = 1

    STATUS_REG.read(handle)
    if STATUS_REG.fieldByName('DataRole').value == DataRole_list.index('UFP_or_Port_Disabled'):
        mesg += '**********************************************************************\n'
        mesg += 'WARNING: GCdm 4cc command has no effect when Data Role is UFP or there is no connection\n'
        mesg += 'Status Register indicates that Data Role is UFP or there is no connection\n'
        mesg += '**********************************************************************\n'

    return mesg + "Success"
    
objGCdm = cFunction({'function name' : 'GCdm',
            'inputs' : [
               { 'name' : 'SVID', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
            ],
            'outputs' : [
               { 'name' : 'mode 1', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func} ,
               { 'name' : 'mode 2', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func} ,
               { 'name' : 'mode 3', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func} ,
               { 'name' : 'mode 4', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func} ,
               { 'name' : 'mode 5', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func} ,
               { 'name' : 'mode 6', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func} ,
            ],
            'execute' : execGCdm } )

                        
# Alternate Mode Enter
def AMEn(handle, SVID, object_pos):
    mesg = ""
    STATUS_REG.read(handle)
    if STATUS_REG.fieldByName('DataRole').value == DataRole_list.index('UFP_or_Port_Disabled'):
        mesg += '**********************************************************************\n'
        mesg += 'WARNING: AMEn 4cc command has no effect when Data Role is UFP or there is no connection\n'
        mesg += 'Status Register indicates that Data Role is UFP or there is no connection\n'
        mesg += '**********************************************************************\n'
    data_in = byteArray(SVID)
    data_in.append(object_pos)
        
    write_reg(handle, 0x09, data_in)
    write_reg_4cc(handle, 0x08, 'AMEn')

    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return mesg + verify_task_status(handle)
    else :
        return mesg + cmdret

def execAMEn(self, handle):
    return AMEn(handle, self.inputs[0].value, self.inputs[1].value)
    
objAMEn = cFunction({'function name' : 'AMEn',
            'inputs' : [
               { 'name' : 'SVID', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
               { 'name' : 'Object Position', 'value' : 0 , 'translate' : trans_3, 'reverse translate' : rev_trans_3 } ,
            ],
            'outputs' : [
            ],
            'execute' : execAMEn })


# Alternate Mode Exit
def AMEx(handle, SVID, object_pos):
    mesg = ""
    STATUS_REG.read(handle)
    if STATUS_REG.fieldByName('DataRole').value == DataRole_list.index('UFP_or_Port_Disabled'):
        mesg += '**********************************************************************\n'
        mesg += 'WARNING: AMEx 4cc command has no effect when Data Role is UFP or there is no connection\n'
        mesg += 'Status Register indicates that Data Role is UFP or there is no connection\n'
        mesg += '**********************************************************************\n'
    data_in = byteArray(SVID)
    data_in.append(object_pos)
        
    write_reg(handle, 0x09, data_in)
    write_reg_4cc(handle, 0x08, 'AMEx')

    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return mesg + verify_task_status(handle)
    else :
        return mesg + cmdret

def execAMEx(self, handle):
    return AMEx(handle, self.inputs[0].value, self.inputs[1].value)
    
objAMEx = cFunction({'function name' : 'AMEx',
            'inputs' : [
               { 'name' : 'SVID', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
               { 'name' : 'Object Position', 'value' : 0 , 'translate' : trans_3, 'reverse translate' : rev_trans_3 } ,
            ],
            'outputs' : [
            ],
            'execute' : execAMEx })



# Autonegotiate Start
# Alternate Mode Discovery Start
def ANeg(handle):
    write_reg_4cc(handle, 0x08, 'ANeg')
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return verify_task_status(handle)
    else :
        return cmdret

def execANeg(self, handle):
    return ANeg(handle)
    
objANeg = cFunction({'function name' : 'ANeg',
            'inputs' : [
            ],
            'outputs' : [
            ],
            'execute' : execANeg })

# Alternate Mode Discovery Start
def AMDs(handle):
    write_reg_4cc(handle, 0x08, 'AMDs')
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return verify_task_status(handle)
    else :
        return cmdret

def execAMDs(self, handle):
    return AMDs(handle)
    
objAMDs = cFunction({'function name' : 'AMDs',
            'inputs' : [
            ],
            'outputs' : [
            ],
            'execute' : execAMDs })


region_list = ['region 0', 'region 1']

# Flash functions need a much longer timeout
FLASH_HI_TIMEOUT = 30

# Flash read region pointer command
# takes region (0 or 1) and returns 32-bit pointer to region offset in flash
def FLrr(handle, region):
    data_in = array('B','\0')
    
    data_in[0] = region & 0xFF
    
    write_reg(handle, 0x09, data_in)
    write_reg_4cc(handle, 0x08, 'FLrr')

    verify_cmd_completed(handle, FLASH_HI_TIMEOUT)

    (count, data_out) = read_reg(handle, 0x09, 5)

    data_out_32bit = (data_out[3] << 24) | (data_out[2] << 16) | (data_out[1] << 8) | data_out[0]
    return data_out_32bit

def execFLrr(self, handle):
    self.outputs[0].value = FLrr(handle, self.inputs[0].value)
    self.outputs[0].hide = 0

    return "Success"
    
objFLrr = cFunction({'function name' : 'FLrr',
            'inputs' : [
                { 'name' : 'Boot region', 'value' : 0, 'translate list' : region_list } ,
            ],
            'outputs' : [
                { 'name' : 'Region start address', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
            ],
            'execute' : execFLrr })



# Flash erase region pointers command
# takes region (0 or 1) no return
def FLer(handle, region):
    data_in = array('B','\0')
    
    data_in[0] = region & 0xFF
    
    write_reg(handle, 0x09, data_in)
    write_reg_4cc(handle, 0x08, 'FLer')

    cmdret = verify_cmd_completed(handle, FLASH_HI_TIMEOUT)
    if (cmdret == "Success") :
        return verify_task_status(handle)
    else :
        return cmdret

def execFLer(self, handle):
    return FLer(handle, self.inputs[0].value)
    
objFLer = cFunction({'function name' : 'FLer',
            'inputs' : [
                { 'name' : 'Boot region', 'value' : 0, 'translate list' : region_list } ,
            ],
            'outputs' : [
            ],
            'execute' : execFLer })


def rev_translate_4k(self, value):
    if value[:2] == '0x':
        retval = int(value,16)
    else:
        retval = int(value)
    return retval & 0xFFFFF000

# Flash erase memory command
# takes start address, 32-bit offset in flash and num_sectors, number of
#       4kB sectors to erase starting at start address
def FLem(handle, start_address, num_sectors):
    data_in = byteArray(start_address)
    for i in range(5-len(data_in)):
        data_in.append(0)
    data_in[4] = num_sectors
    
    write_reg(handle, 0x09, data_in)
    write_reg_4cc(handle, 0x08, 'FLem')

    cmdret = verify_cmd_completed(handle, FLASH_HI_TIMEOUT)
    if (cmdret == "Success") :
        return verify_task_status(handle)
    else :
        return cmdret

def execFLem(self, handle):
    return FLem(handle, self.inputs[0].value, self.inputs[1].value)
    
objFLem = cFunction({'function name' : 'FLem',
            'inputs' : [
                { 'name' : 'Offset', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : rev_translate_4k} ,
                { 'name' : 'Number of 4K Blocks', 'value' : 0 } ,
            ],
            'outputs' : [
            ],
            'execute' : execFLem })


# Flash program memory start address
def FLad(handle, address):
    data_in = byteArray(address)
    for i in range(5-len(data_in)):
        data_in.append(0)

    write_reg(handle, 0x09, data_in)
    write_reg_4cc(handle, 0x08, 'FLad')
    
    cmdret = verify_cmd_completed(handle, FLASH_HI_TIMEOUT)
    if (cmdret == "Success") :
        return verify_task_status(handle)
    else :
        return cmdret

def execFLad(self, handle):
    return FLad(handle, self.inputs[0].value)
    
objFLad = cFunction({'function name' : 'FLad',
            'inputs' : [
                { 'name' : 'Offset', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
            ],
            'outputs' : [
            ],
            'execute' : execFLad })


# Flash data write command (raw, no crc)
# Takes 16 4-byte chunks of image data from a binary file
def FLwd(handle, image_data):
    assert len(image_data) <= 64

    write_reg(handle, 0x09, image_data)
    write_reg_4cc(handle, 0x08, 'FLwd')
    
    cmdret = verify_cmd_completed(handle, FLASH_HI_TIMEOUT)
    if (cmdret == "Success") :
        return verify_task_status(handle)
    else :
        return cmdret


def four_byte_array(value) :
    retval =  byteArray(value)[:4]

    for i in range(4 - len(retval)) :
        retval.extend([0,])

    return retval

def execFLwd(self, handle):
    image_data = four_byte_array(inputs[0].value)
    image_data.extend(four_byte_array(inputs[1].value))
    image_data.extend(four_byte_array(inputs[2].value))
    image_data.extend(four_byte_array(inputs[3].value))
    image_data.extend(four_byte_array(inputs[4].value))
    image_data.extend(four_byte_array(inputs[5].value))
    image_data.extend(four_byte_array(inputs[6].value))
    image_data.extend(four_byte_array(inputs[7].value))
    image_data.extend(four_byte_array(inputs[8].value))
    image_data.extend(four_byte_array(inputs[9].value))
    image_data.extend(four_byte_array(inputs[10].value))
    image_data.extend(four_byte_array(inputs[11].value))
    image_data.extend(four_byte_array(inputs[12].value))
    image_data.extend(four_byte_array(inputs[13].value))
    image_data.extend(four_byte_array(inputs[14].value))
    image_data.extend(four_byte_array(inputs[15].value))
    return FLwd(handle, image_data)
    
objFLwd = cFunction({'function name' : 'FLwd',
            'inputs' : [
                { 'name' : '32-bit word (offset 0 B)', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : '32-bit word (offset 4 B)', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : '32-bit word (offset 8 B)', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : '32-bit word (offset 12 B)', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : '32-bit word (offset 16 B)', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : '32-bit word (offset 20 B)', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : '32-bit word (offset 24 B)', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : '32-bit word (offset 28 B)', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : '32-bit word (offset 32 B)', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : '32-bit word (offset 36 B)', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : '32-bit word (offset 40 B)', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : '32-bit word (offset 44 B)', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : '32-bit word (offset 48 B)', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : '32-bit word (offset 52 B)', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : '32-bit word (offset 56 B)', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : '32-bit word (offset 60 B)', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
            ],
            'outputs' : [
            ],
            'execute' : execFLwd })


successFailure_list = ['success', 'failure']

# Flash writing done command
# Takes 16 4-byte chunks of image data from a binary file
# returns 0 on success, 1 on failure
def FLvy(handle, address):
    data_in = byteArray(address)
    write_reg_4cc(handle, 0x08, 'FLvy')
    
    verify_cmd_completed(handle, FLASH_HI_TIMEOUT)

    (count, data_out) = read_reg(handle, 0x09, 5)
    assert count == 5

    # return of FLvy placed in lower 8 bit
    data_out_8bit = data_out[0]
    return data_out_8bit

def execFLvy(self, handle):
    self.outputs[0].value = FLvy(handle, self.inputs[0].value)
    self.outputs[0].hide = 0

    return "Success"
    
objFLvy = cFunction({'function name' : 'FLvy',
            'inputs' : [
                { 'name' : 'Offset', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
            ],
            'outputs' : [
                { 'name' : 'Success', 'value' : 0, 'translate list' : successFailure_list } ,
            ],
            'execute' : execFLvy })

gpio_num_list = [ 'GPIO 0', 'GPIO 1', 'GPIO 2', 'GPIO 3', 'GPIO 4', 'GPIO 5', 'GPIO 6', 'GPIO 7', 'GPIO 8',
                  'GPIO 9 (RESETZ)', 'GPIO 10 (BUS_PWRZ)', 'GPIO 11 (MRESET)', 'GPIO 12 (DEBUG_4)',
                  'GPIO 13 (DEBUG_3)', 'GPIO 14 (DEBUG_2)', 'GPIO 15 (DEBUG_1)', 'GPIO 16 (DEBUG_CTL_1)',
                  'GPIO 17 (DEBUG_CTL_2)', 'GPIO 18 (SPI_CSZ)', 'GPIO 19 (SPI_MOSI)', 'GPIO 20 (SPI_MISO)',
                  'GPIO 21 (SPI_CLK)' ]


# GPIO Input Enable
# Takes 1 byte indicating GPIO number
def GPie(handle, gpio_num):
    data_in = byteArray(gpio_num)
    write_reg(handle, 0x09, data_in)
    write_reg_4cc(handle, 0x08, 'GPie')
    
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return verify_task_status(handle)
    else :
        return cmdret

def execGPie(self, handle):
    return GPie(handle, self.inputs[0].value)
    
objGPie = cFunction({'function name' : 'GPie',
            'inputs' : [
                { 'name' : 'GPIO Number', 'value' : 0, 'translate list' : gpio_num_list} ,
            ],
            'outputs' : [
            ],
            'execute' : execGPie,
            'associate register' : GPIO_STATUS } )
                    


# GPIO Output Enable
# Takes 1 byte indicating GPIO number
def GPoe(handle, gpio_num):
    data_in = byteArray(gpio_num)
    write_reg(handle, 0x09, data_in)
    write_reg_4cc(handle, 0x08, 'GPoe')
    
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return verify_task_status(handle)
    else :
        return cmdret


def execGPoe(self, handle):
    return GPoe(handle, self.inputs[0].value)
    
objGPoe = cFunction({'function name' : 'GPoe',
            'inputs' : [
                { 'name' : 'GPIO Number', 'value' : 0, 'translate list' : gpio_num_list} ,
            ],
            'outputs' : [
            ],
            'execute' : execGPoe,
            'associate register' : GPIO_STATUS } )


    
# GPIO set high command
# Takes 1 byte indicating GPIO number
def GPsh(handle, gpio_num):
    data_in = byteArray(gpio_num)
    write_reg(handle, 0x09, data_in)
    write_reg_4cc(handle, 0x08, 'GPsh')
    
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return verify_task_status(handle)
    else :
        return cmdret

def execGPsh(self, handle):
    return GPsh(handle, self.inputs[0].value)
    
objGPsh = cFunction({'function name' : 'GPsh',
            'inputs' : [
                { 'name' : 'GPIO Number', 'value' : 0, 'translate list' : gpio_num_list} ,
            ],
            'outputs' : [
            ],
            'execute' : execGPsh,
            'associate register' : GPIO_STATUS } )



# GPIO set low command
# Takes 1 byte indicating GPIO number
def GPsl(handle, gpio_num):
    data_in = byteArray(gpio_num)
    write_reg(handle, 0x09, data_in)
    write_reg_4cc(handle, 0x08, 'GPsl')
    
    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return verify_task_status(handle)
    else :
        return cmdret

def execGPsl(self, handle):
    return GPsl(handle, self.inputs[0].value)
    
objGPsl = cFunction({'function name' : 'GPsl',
            'inputs' : [
                { 'name' : 'GPIO Number', 'value' : 0, 'translate list' : gpio_num_list} ,
            ],
            'outputs' : [
            ],
            'execute' : execGPsl,
            'associate register' : GPIO_STATUS } )
                     


class cADCchannel:
    def __init__(self, iChannel, iName, iDivider, iTranslate):
        self.channel = iChannel
        self.name = iName
        self.divider = iDivider
        self.translate = iTranslate

class cADC :
    def __init__(self, iChannelListOfDict):
        self.channels = list()
        for channelDict in iChannelListOfDict :
            self.channels.append(cADCchannel(channelDict['channel'], channelDict['name'], channelDict['divider'], channelDict['translate']))

    def channelByNumber(self, number):
        for (i,channel) in enumerate(self.channels) :
            if i == number :
                return channel

    def channelByName(self, name):
        for channel in self.channels :
            if channel.name == name :
                return channel


def translateVoltage(self, value) :
    return '%f Volts' %(value * self.divider * 1.2 / 1024 )

def translateCurrent(self, value) :
    return '%f Amps' %(value * self.divider * 1.2 / 1024 )

def translateTemp(self, value) :
#    return '%f Deg C' %(((value * 1.2 / 1024) - 0.784) * 322.58 )
    return 'Raw value = %f V' %(value * 1.2/ 1024)

# Note: ADC_CHAN_I_PP_EXT assumes 10 mOhm resistor. 
ADC = cADC ( [ { 'channel' : 0x0, 'name' :'THERMAL_SENSE', 'divider' : 1 , 'translate' : translateTemp },
               { 'channel' : 0x1, 'name' :'VBUS', 'divider' : 25, 'translate' : translateVoltage },
               { 'channel' : 0x2, 'name' :'SENSEP', 'divider' : 25, 'translate' : translateVoltage },
               { 'channel' : 0x3, 'name' :'I_PP_EXT', 'divider' :  5, 'translate' : translateCurrent},
               { 'channel' : 0x4, 'name' :'PP_HV', 'divider' : 25, 'translate' : translateVoltage },
               { 'channel' : 0x5, 'name' :'I_PP_HV', 'divider' : 3 , 'translate' : translateCurrent},
               { 'channel' : 0x6, 'name' :'PP_5V0', 'divider' : 5, 'translate' : translateVoltage },
               { 'channel' : 0x7, 'name' :'I_PP_5V0', 'divider' : 3 , 'translate' : translateCurrent},
               { 'channel' : 0x8, 'name' :'CC1_BY5', 'divider' : 5, 'translate' : translateVoltage },
               { 'channel' : 0x9, 'name' :'I_CC', 'divider' :  0.7 , 'translate' : translateCurrent},
               { 'channel' : 0xA, 'name' :'CC2_BY5', 'divider' : 5, 'translate' : translateVoltage },
               { 'channel' : 0xB, 'name' :'GPIO_5_RAW', 'divider' : 1, 'translate' : translateVoltage },
               { 'channel' : 0xC, 'name' :'CC1_BY2', 'divider' : 2, 'translate' : translateVoltage },
               { 'channel' : 0xD, 'name' :'CC2_BY2', 'divider' : 2, 'translate' : translateVoltage },
               { 'channel' : 0xE, 'name' :'PP_CABLE', 'divider' : 5, 'translate' : translateVoltage },
               { 'channel' : 0xF, 'name' :'IN_3P3V', 'divider' : 3, 'translate' : translateVoltage },
               { 'channel' : 0x10, 'name' :'OUT_3P3V', 'divider' : 3,'translate' : translateVoltage },
               { 'channel' : 0x11, 'name' :'BRICKID_RFU', 'divider' : 3, 'translate' : translateVoltage },
               { 'channel' : 0x12, 'name' :'V1P8_A', 'divider' : 2, 'translate' : translateVoltage },
               { 'channel' : 0x13, 'name' :'V1P8_D', 'divider' : 2, 'translate' : translateVoltage },
               { 'channel' : 0x14, 'name' :'V3P3', 'divider' : 3, 'translate' : translateVoltage },
               { 'channel' : 0x15, 'name' :'I2CADDR', 'divider' : 3, 'translate' : translateVoltage },
               { 'channel' : 0x16, 'name' :'GPIO_0', 'divider' : 3, 'translate' : translateVoltage },
               { 'channel' : 0x17, 'name' :'GPIO_1', 'divider' : 3, 'translate' : translateVoltage },
               { 'channel' : 0x18, 'name' :'GPIO_2', 'divider' : 3, 'translate' : translateVoltage },
               { 'channel' : 0x19, 'name' :'GPIO_3', 'divider' : 3, 'translate' : translateVoltage },
               { 'channel' : 0x1A, 'name' :'GPIO_4', 'divider' : 3, 'translate' : translateVoltage },
               { 'channel' : 0x1B, 'name' :'GPIO_5', 'divider' : 3, 'translate' : translateVoltage },
               { 'channel' : 0x1C, 'name' :'GPIO_6', 'divider' : 3, 'translate' : translateVoltage },
               { 'channel' : 0x1D, 'name' :'GPIO_7', 'divider' : 3, 'translate' : translateVoltage },
               { 'channel' : 0x1E, 'name' :'GPIO_8', 'divider' : 3, 'translate' : translateVoltage },
               { 'channel' : 0x1F, 'name' :'GPIO_10 (BUSPOWER_Z)', 'divider' : 3, 'translate' : translateVoltage },
            ] )

channelList = []
for record in ADC.channels :
    channelList.append(record.name)


ADC_MON_MODE_SINGLE_CHANNEL_SINGLE = ( 0x00000002 << 5 )

def ADCs(handle, channel) :
    data1 = array('B', '\0\0\0\0')
    data1[0] = channel.channel & 0x1F  

    write_reg(handle, 0x09, data1)
    write_reg_4cc(handle, 0x08, 'ADCs')

    verify_cmd_completed(handle)

    (count, data2) = read_reg(handle, 0x09, 4)
    readvalue = ((data2[2] << 8) | (data2[1])) & 0x3FF

    if readvalue == 0x3FF :
        print '*** Warning *** Saturation on channel : %d, %s' %(channel.channel, channel.name)

    if channel.channel == 0x3 :
        SYS_CONFIG_REG.read(handle)
        if SYS_CONFIG_REG.fieldByName('RSense') == RSense_list.index('5 mOhm PP_HVE current sense resisitor') :
            readvalue = readvalue * 2
    
    return channel.translate(channel, readvalue)


def translatePassthrough(self) :
    print self.value
    return self.value

def execADCs(self, handle):
    self.outputs[0].value = ADCs(handle, ADC.channelByNumber(self.inputs[0].value) )
    self.outputs[0].hide = 0

    return "Success"

objADCs = cFunction({'function name' : 'ADCs',
            'inputs' : [
                { 'name' : 'Channel', 'value' : 0, 'translate list' : channelList} ,
            ],
            'outputs' : [
                { 'name' : 'ADC Read Value', 'value' : '', 'type' : '32-bit', 'translate' : translatePassthrough} ,
            ],
            'execute' : execADCs } )



# PD state dump
def PDSt(handle):
    # read position indicator for circular buffer
    write_reg(handle, 0x09, byteArray(1))
    write_reg_4cc(handle, 0x08, 'PDSt')
    verify_cmd_completed(handle)
    (count, ret1) = read_reg(handle, 0x09, 2)

    position = ret1[0]
    
    write_reg(handle, 0x09, byteArray(2))
    write_reg_4cc(handle, 0x08, 'PDSt')
    verify_cmd_completed(handle)
    (count, array1) = read_reg(handle, 0x09, 65)

    write_reg(handle, 0x09, byteArray(3))
    write_reg_4cc(handle, 0x08, 'PDSt')
    verify_cmd_completed(handle)
    (count, array2) = read_reg(handle, 0x09, 65)

    write_reg(handle, 0x09, byteArray(4))
    write_reg_4cc(handle, 0x08, 'PDSt')
    verify_cmd_completed(handle)
    (count, array3) = read_reg(handle, 0x09, 65)

    write_reg(handle, 0x09, byteArray(5))
    write_reg_4cc(handle, 0x08, 'PDSt')
    verify_cmd_completed(handle)
    (count, array4) = read_reg(handle, 0x09, 65)

    retarray = array1
    for element in array2:
        retarray.append(element)
    for element in array3:
        retarray.append(element)
    for element in array4:
        retarray.append(element)

    return (position, retarray)


# VDMs
# Send arbitrary VDM
def VDMs(handle, packed_data):
    write_reg(handle, 0x09, packed_data)
    write_reg_4cc(handle, 0x08, 'VDMs')

    cmdret = verify_cmd_completed(handle)
    if (cmdret == "Success") :
        return verify_task_status(handle)
    else :
        return cmdret

def execVDMs(self, handle):
    packed_data = byteArray(self.inputs[0].value & 0x7)
    packed_data[0] |= (self.inputs[1].value & 0x3) << 4

    firstObject = 0
    firstObject |= (self.inputs[2].value & 0xFFFF) << 16
    firstObject |= (self.inputs[3].value & 0x1) << 15
    firstObject |= (self.inputs[4].value & 0x7FFF)

    packed_data.extend(four_byte_array(firstObject))

    for i in range((self.inputs[0].value & 0x7)-1) :
        packed_data.extend(four_byte_array(self.inputs[5+i].value))

    return VDMs(handle, packed_data)

sop_type_list = ['SOP', 'SOP Prime', 'SOP Double-Prime']
structured_type_list = ['Unstructured VDM', 'Structured VDM']

objVDMs = cFunction({'function name' : 'VDMs',
            'inputs' : [
                { 'name' : 'Number of 32-bit Vendor-defined Objects', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : 'SOP Type', 'value' : 0, 'type' : '32-bit', 'translate list' : sop_type_list} ,
                { 'name' : 'SVID', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : 'Structured/Unstructured', 'value' : 0, 'type' : '32-bit', 'translate list' : structured_type_list} ,
                { 'name' : 'VDO #1 (Partial, 15-bits)', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : 'VDO #2', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : 'VDO #3', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : 'VDO #4', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : 'VDO #5', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : 'VDO #6', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
                { 'name' : 'VDO #7', 'value' : 0, 'type' : '32-bit', 'translate' : hexTranslate_func, 'reverse translate' : hexRevTranslate} ,
            ],
            'outputs' : [
            ],
            'execute' : execVDMs })



#==========================================================================
# List
#==========================================================================


FUNC_LIST = [ objRead, objWrite,
              objABRT, objGaid, objGAID, objHRST, objCRST, objDBfg,
              objGSkC, objGSrC, objSSrC, objARDO, objRRDO, objSRDO,
              objSWSk,
              objSWSr, objSWDF, objSWUF, objSWVC, objGCdm, objAMEn,
              objAMEx, objANeg, objAMDs, objFLrr, objFLer, objFLem,
              objFLad, objFLwd, objFLvy, objGPie, objGPoe, objGPsh,
              objGPsl, objADCs, objVDMs]

def functionByName(name):
    global FUNC_LIST
    for func in FUNC_LIST:
        if func.name == name :
            return func
    
#==========================================================================
# main
#==========================================================================


if __name__ == "__main__":
    print "This file contains helper functions for the high level host interface functions."
    print "To use, import constituent functions into a script or python environment using:"
    print "from hi_functions import *"

    sys.exit()


