from register_class import *
from register_definitions import *

modules_list = [ 'Type-C Module', 'BC 1.2 Module', 'USB EP Module', 'HPD Module',
                 'PD Module', 'INTS Module', 'Sleep Module', 'Other Module' ]


typeC_debug_dict = { 0x0 : 'SRC_STATE_DISABLED', 0x1 : 'SRC_STATE_UNATTACHED_SRC', 0x2 : 'SRC_STATE_AUDIO_ACC',
                     0x3 : 'SRC_STATE_DEBUG_ACC', 0x4 : 'SRC_STATE_ATTACHED_SRC', 0x5 : 'SRC_STATE_ERROR_RECOVERY',
                     0x6 : 'SRC_STATE_ATTACHWAIT', 0x7 : 'SRC_STATE_ATTACHED_SNK', 
                     0x20 : 'SNK_STATE_DISABLED', 0x21 : 'SNK_STATE_UNATTACHED_SNK', 0x22 : 'SNK_STATE_ATTACHED_SNK',
                     0x23 : 'SNK_STATE_ACCESSORY_PRESENT', 0x24 : 'SNK_STATE_UNATTACHED_ACCESSORY',
                     0x25 : 'SNK_STATE_POWERED_ACCESSORY', 0x26 : 'SNK_STATE_UNSUPPORTED_ACCESSORY',
                     0x27 : 'SNK_STATE_AUDIO_ACC', 0x28 : 'SNK_STATE_DEBUG_ACC', 0x29 : 'SNK_STATE_ERROR_RECOVERY',
                     0x2A : 'SNK_STATE_ATTACHWAIT_SNK', 0x2B : 'SNK_STATE_ATTACHWAIT_ACCESSORY',
                     0x2C : 'SNK_STATE_ATTACHED_SRC', 
                     0x40 : 'DRP_STATE_DISABLED', 0x41 : 'DRP_STATE_UNATTACHED_SRC', 0x42 : 'DRP_STATE_UNATTACHED_SNK',
                     0x43 : 'reserved', 0x44 : 'DRP_STATE_ATTACHED_SRC', 0x45 : 'DRP_STATE_TRY_SRC', 0x46 : 'reserved',
                     0x47 : 'DRP_STATE_ATTACHED_SNK', 0x48 : 'reserved', 0x49 : 'DRP_STATE_AUDIO_ACC', 0x4A : 'DRP_STATE_DEBUG_ACC',
                     0x4B : 'DRP_STATE_ERROR_RECOVERY', 0x4C : 'DRP_STATE_ATTACHWAIT_SNK', 0x4D : 'DRP_STATE_ATTACHWAIT_SRC',
                     0x4E : 'DRP_TRY_WAIT_SNK' }


BC12_debug_dict = { 0x0 : 'CHARGER_DETECTION_INIT', 0x1 : 'DATA_CONNECTION_DETECTION', 0x2 : 'BRICK_ID_DETECTION_DP',
                    0x3 : 'BRICK_ID_DETECTION_DN', 0x4 : 'PRIMARY_DETECTION', 0x5 : 'SECONDARY_DETECTION',
                    0x6 : 'CHARGER_DETECTION_COMPLETE', 0x7 : 'BRICK_ID_DETECTION', 0x8 : 'CHARGER_DETECTION_HALTED' }

USB20_debug_dict = { 0x0 : 'USB_EP_RESET', 0x1 : 'USB_EP_ENUM_DONE' }

HPD_dict = { 0x0 :  'reserved' }

# I2C1 has offset of 0x0
# I2C2 has offset of 0x80
# So 'Soft Reset' on I2C2 is a 0x80 (not repeated in dictionary)

INTs_dict = { 0x0 : 'Soft Reset', 0x1 : 'Hard Reset', 0x2 : 'Power Path Event', 0x3 : 'Plug Insert or Removal',
              0x4 : 'PR Swap Complete', 0x5 : 'DR Swap Complete', 0x6 : 'Awoken by Host',
              0x7 : 'RDO Received from Sink', 0x8 : 'BIST', 0x9 : 'Overcurrent', 0xA : 'Attention Received',
              0xB : 'VDM Received', 0xC : 'New Contract as Consumer', 0xD : 'New Contract as Provider',
              0xE : 'Source Capabilities Message Ready', 0xF : 'Sink Capabilities Message Ready',
              0x10 : 'Supervisor Event', 0x11 : 'Swap Requested', 0x12 : 'BIST Message Ignored',
              0x13 : 'Goto Min Received', 0x14 : 'USB Host Present', 0x15 : 'USB Host Present no Longer',
              0x16 : 'High Voltage Warning', 0x17 : 'PP Switch Changed', 0x18 : 'Power Status Update',
              0x19 : 'Data Status Update', 0x1A : 'Status Update', 0x1B : 'PD Status Update',
              0x1C : 'ADC Low Threshold', 0x1D : 'ADC High Threshold', 0x1E : 'CMD1 Complete',
              0x1F : 'CMD2 Complete', 0x20 : 'Error: Device Incompatible',
              0x21 : 'Error: Cannot Provide Voltage or Current',
              0x22 : 'Error: Can Provide Voltage or Current Later', 0x23 : 'Error: Power Event Occurred',
              0x24 : 'Error: Missing Get Capabilities Message', 0x25 : 'Error: Transmission Error',
              0x26 : 'Error: Protocol Error', 0x27 : 'Error: Message Data', 0x28 : 'Reserved',
              0x29 : 'Error: Discharge Failed', 0x2A : 'Sink Transition Complete',
              0x2B : 'Reserved', 0x2C : 'Reserved', 0x2D : 'Reserved', 0x2E : 'Error: Unable to Source',
              0x2F : 'Error: Power Source Current Limit', 0x30 : 'Reserved', 0x31 : 'VDM Entered Mode',
              0x32 : 'VDM Message Sent', 0x33 : 'Discover Modes Complete', 0x34 : 'Exit Modes Complete',
              0x35 : 'Reserved', 0x36 : 'Reserved', 0x37 : 'Reserved', 0x37 : 'WAKE_PLUG',
              0x38 : 'WAKE_UNPLUG', 0x39 : 'WAKE_PD_CONTRACT', 0x3A : 'WAKE_HPD_LOW',
              0x3B : 'WAKE_HPD_HIGH', 0x3C : 'WAKE_HPD_IRQ', 0x3D : 'WAKE_GPIO_0', 0x3E : 'WAKE_GPIO_1',
              0x3F : 'WAKE_GPIO_2', 0x40 : 'WAKE_GPIO_3', 0x41 : 'WAKE_GPIO_4', 0x42 : 'WAKE_GPIO_5',
              0x43 : 'WAKE_GPIO_6', 0x44 : 'WAKE_GPIO_7', 0x45 : 'WAKE_GPIO_8', 0x46 : 'WAKE_GPIO_9'    
              }

other_debug_dict = { 0x0 : 'reserved' }

Power_state_debug_dict = { 0x0 : 'Awake', 0x3 : 'Sleep Arm', 0x4 : 'Lite Sleep Ace', 0x5 : 'Deep Sleep Ace' }

PD_state_debug_dict = { 0x0 : 'PEState_Start', 0x1 : 'PEState_CableTypeDetect', 0x2 : 'PEState_LaunchPolicyEngine', 0x3 : 'PEState_Priority__Start',
                        0x4 : 'PEState_SendSoftReset', 0x5 : 'PEState_SoftReset', 0x6 : 'PEState_HardReset', 0x7 : 'PEState_Priority__Stop',
                        0x8 : 'PEState_SendSoftReset_Accept', 0x9 : 'PEState_SoftReset_Exit', 0xA : 'PEState_Start_WrapUp', 0xB : 'PEState_WrapUpDone',
                        0xC : 'PEState_GiveSourceCap', 0xD : 'PEState_GiveSinkCap', 0xE : 'PEState_GetCap', 0xF : 'PEState_GetCap_Rx',
                        0x10 : 'PEState_GetCap_Timeout', 0x11 : 'PEState_UnUsed_0x11', 0x12 : 'PEState_UnUsed_0x12',
                        0x13 : 'PEState_Source_Startup', 0x14 : 'PEState_Source_Startup_Continue', 0x15 : 'PEState_Source_Discovery',
                        0x16 : 'PEState_Source_SendCapabilities', 0x17 : 'PEState_Source_Ready', 0x18 : 'PEState_Source_CapabilityResponse',
                        0x19 : 'PEState_Source_NegotiateCapability', 0x1A : 'PEState_Source_TransitionSupply_GotoMin',
                        0x1B : 'PEState_Source_TransitionSupply_Accept', 0x1C : 'PEState_Source_TransitionSupply', 0x1D : 'PEState_UnUsed_0x1D',
                        0x1E : 'PEState_Source_TransitionSupply_SetAlarmsNew', 0x1F : 'PEState_Source_TransitionSupply_PS_RDY',                       
                        0x20 : 'PEState_UnUsed_0x20', 0x21 : 'PEState_Sink_Startup', 0x22 : 'PEState_Sink_Discovery',
                        0x23 : 'PEState_RxCapabilitiesOk__Start', 0x24 : 'PEState_Sink_WaitForCapabilities', 0x25 : 'PEState_Sink_WaitForCapabilities_Cont',
                        0x26 : 'PEState_Sink_EvaluateCapability', 0x27 : 'PEState_Sink_SelectCapability', 0x28 : 'PEState_Sink_TransitionSink',
                        0x29 : 'PEState_Sink_TransitionSink_PS_RDY', 0x2A : 'PEState_Sink_Ready', 0x2B : 'PEState_UnUsed_0x2B',
                        0x2C : 'PEState_RxCapabilitiesOk__Stop', 0x2D : 'PEState_Reject_Request', 0x2E : 'PEState_Enable_VCONN',
                        0x2F : 'PEState_Enable_VBUS', 0x30 : 'PEState_UnUsed_0x30', 0x31 : 'PEState_UnUsed_0x31', 0x32 : 'PEState_UnUsed_0x32',
                        0x33 : 'PEState_UnUsed_0x33', 0x34 : 'PEState_PD_Send_Custom_Message', 0x35 : 'PEState_PRS_Evaluate_PR_Swap',
                        0x36 : 'PEState_PRS_Send_PR_Swap', 0x37 : 'PEState_PRS_Accept_PR_Swap', 0x38 : 'PEState_PRS_AssertRp',
                        0x39 : 'PEState_PRS_AssertRd', 0x3A : 'PEState_PRS_TransitionToOff', 0x3B : 'PEState_PRS_TransitionToOff_Sink',
                        0x3C : 'PEState_PRS_TransitionToOff_Source', 0x3D : 'PEState_PRS_SourceOff', 0x3E : 'PEState_PRS_SourceOn',
                        0x3F : 'PEState_PRS_SourceOn_PS_RDY', 0x40 : 'PEState_UnUsed_0x40', 0x41 : 'PEState_UnUsed_0x41',
                        0x42 : 'PEState_UnUsed_0x42', 0x43 : 'PEState_Pretend_DeadBattery', 0x44 : 'PEState_GotoBISTTesterMode', 0x45 : 'PEState_BIST_CarrierMode2',
                        0x46 : 'PEState_BIST_TestData', 0x47 : 'PEState_BIST_End_Continuous_Test', 0x48 : 'reserved',
                        0x49 : 'reserved', 0x4A : 'PEState_VCS_Send_Swap', 0x4B : 'PEState_VCS_Wait_for_VCONN', 0x4C : 'PEState_VCS_Turn_Off_VCONN',
                        0x4D : 'PEState_VCS_Turn_On_VCONN', 0x4E : 'PEState_VCS_Send_PS_Rdy', 0x4F : 'PEState_VCS_Evaluate_Swap',
                        0x50 : 'PEState_VCS_Accept_Swap', 0x51 : 'PEState_UnUsed_0x51', 0x52 : 'PEState_UnUsed_0x52', 0x53 : 'PEState_DRS_Evaluate_DR_Swap',
                        0x54 : 'PEState_DRS_Accept_DR_Swap', 0x55 : 'PEState_DRS_DFP_UFP_Change_to_UFP', 0x56 : 'PEState_DRS_Send_DR_Swap',
                        0x57 : 'PEState_DRS_UFP_DFP_Change_to_DFP', 0x58 : 'PEState_DRS_SoftReset_SOP_DPrime_AfterDRSwap', 0x59 : 'PEState_UnUsed_0x59',
                        0x5A : 'PEState_UnUsed_0x5A', 0x5B : 'PEState_UFP_VDM_Send_NAK', 0x5C : 'PEState_UFP_VDM_Send_Identity', 0x5D : 'PEState_UFP_VDM_Send_SVIDs',
                        0x5E : 'PEState_UFP_VDM_Send_Modes', 0x5F : 'PEState_UFP_VDM_Evaluate_Mode_Entry',                        
                        0x60 : 'PEState_UFP_VDM_Mode_Entry_ACK', 0x61 : 'PEState_UFP_VDM_Mode_Entry_NAK', 0x62 : 'PEState_UFP_VDM_Mode_Exit',
                        0x63 : 'PEState_UFP_VDM_Mode_Exit_ACK', 0x64 : 'PEState_UFP_VDM_Mode_Exit_NAK', 0x65 : 'PEState_UFP_VDM_Attention_Request',
                        0x66 : 'PEState_UFP_VDM_Status_Request', 0x67 : 'PEState_UFP_VDM_Config_Request', 0x68 : 'PEState_UFP_VDM_Config_ACK',
                        0x69 : 'PEState_UFP_VDM_Send_Data', 0x6A : 'PEState_UFP_VDM_Send_Data_ACK', 0x6B : 'PEState_UFP_VDM_RxVWire_Status',
                        0x6C : 'PEState_UFP_VDM_RxVWire_Status_ACK', 0x6D : 'PEState_UnUsed_0x6D', 0x6E : 'PEState_UnUsed_0x6E',
                        0x6F : 'PEState_UnUsed_0x6F',
                        0x70 : 'PEState_UnUsed_0x70', 0x71 : 'PEState_DFP_VDM_BUSY_Response',
                        0x72 : 'PEState_DFP_VDM_Identity_Request', 0x73 : 'PEState_DFP_VDM_Identity_ACKed', 0x74 : 'PEState_DFP_VDM_Identity_NAKed',
                        0x75 : 'PEState_DFP_VDM_SVIDs_Request', 0x76 : 'PEState_DFP_VDM_SVIDs_ACKed', 0x77 : 'PEState_DFP_VDM_SVIDs_NAKed',
                        0x78 : 'PEState_DFP_VDM_Modes_Request', 0x79 : 'PEState_DFP_VDM_Modes_ACKed', 0x7A : 'PEState_DFP_VDM_Modes_NAKed',
                        0x7B : 'PEState_DFP_VDM_Mode_Entry_Request', 0x7C : 'PEState_DFP_VDM_Mode_Entry_ACKed', 0x7D : 'PEState_DFP_VDM_Mode_Entry_NAKed',
                        0x7E : 'PEState_DFP_VDM_Mode_Exit_Request', 0x7F : 'PEState_DFP_VDM_Exit_Mode_ACKed',
                        0x80 : 'PEState_DFP_VDM_Attention_Request',
                        0x81 : 'PEState_DFP_VDM_Config_Request', 0x82 : 'PEState_DFP_VDM_Config_ACK', 0x83 : 'PEState_DFP_VDM_Config_NAKed',
                        0x84 : 'PEState_DFP_VDM_Send_Data', 0x85 : 'PEState_DFP_VDM_Send_Data_ACK', 0x86 : 'PEState_DFP_VDM_Get_Msg',
                        0x87 : 'PEState_DFP_VDM_Get_Msg_RCV', 0x88 : 'PEState_DFP_VDM_Status_Update', 0x89 : 'PEState_DFP_VDM_VWStatus_Send',
                        0x8A : 'PEState_DFP_VDM_VWStatus_BUSY', 0x8B : 'PEState_UnUsed_0x8B', 0x8C : 'PEState_UnUsed_0x8C',
                        0x8D : 'PEState_UnUsed_0x8D', 0x8E : 'PEState_UnUsed_0x8E', 0x8F : 'PEState_UnUsed_0x8F',                        
                        0x90 : 'PEState_UnUsed_0x90', 0x91 : 'PEState_UnUsed_0x91', 0x92 : 'PEState_UnUsed_0x92', 
                        0x93 : 'PEState_UnUsed_0x93', 0x94 : 'PEState_UnUsed_0x94', 0x95 : 'PEState_UnUsed_0x95',
                        0x96 : 'PESTATE_SRC2PLUG_VDM_Identity_Request', 0x97 : 'PESTATE_SRC2PLUG_VDM_Identity_ACKed', 0x98 : 'PESTATE_SRC2PLUG_VDM_Identity_NAKed',
                        0x99 : 'PEState_PLUG_Send_SoftReset_Request', 0x9A : 'PEState_PLUG_Prepare_For_CableReset', 0x9B : 'PEState_PLUG_CableReset',
                        0x9C : 'PEState_PLUG_CableReset_Sent', 0x9D : 'PEState_DFP2PLUG_VDM_Identity_Request', 0x9E : 'PEState_DFP2PLUG_VDM_Identity_ACKed',
                        0x9F : 'PEState_DFP2PLUG_VDM_Identity_NAKed',
                        0xA0 : 'PEState_DFP2PLUG_VDM_SVIDs_Request', 0xA1 : 'PEState_DFP2PLUG_VDM_SVIDs_ACKed',
                        0xA2 : 'PEState_DFP2PLUG_VDM_SVIDs_NAKed', 0xA3 : 'PEState_DFP2PLUG_VDM_Modes_Request', 0xA4 : 'PEState_DFP2PLUG_VDM_Modes_ACKed',
                        0xA5 : 'PEState_DFP2PLUG_VDM_Modes_NAKed', 0xA6 : 'PEState_DFP2PLUG_VDM_Mode_Entry_Request', 0xA7 : 'PEState_DFP2PLUG_VDM_Mode_Entry_ACKed',
                        0xA8 : 'PEState_DFP2PLUG_VDM_Mode_Entry_NAKed', 0xA9 : 'PEState_DFP2PLUG_VDM_Mode_Exit_Request',
                        0xAA : 'PEState_DFP2PLUG_VDM_Mode_Exit_ACKed', 0xAB : 'PEState_DFP2PLUG_VDM_Mode_Exit_NAKed',
                        0xAC : 'PEState_DFP2PLUG_VDM_DP_Config_Request', 0xAD : 'PEState_DFP2PLUG_VDM_DP_Config_ACK',
                        0xAE : 'PEState_DFP2PLUG_VDM_DP_Config_NACK', 0xAF : 'PEState_DFP2PLUG_VDM_RESERVED_0xAF',
                        0xB0 : 'PEState_DFP2PLUG_VDM_RESERVED_0xB0', 0xB1 : 'PEState_DFP2PLUG_VDM_RESERVED_0xB1', 0xB2 : 'PEState_DFP2PLUG_VDM_RESERVED_0xB2',
                        0xB3 : 'PEState_DFP2PLUG_VDM_RESERVED_0xB3', 0xB4 : 'PEState_DFP2PLUG_VDM_RESERVED_0xB4', 0xB5 : 'PEState_DFP2PLUG_VDM_RESERVED_0xB5',
                        0xB6 : 'PEState_DFP2PLUG_VDM_RESERVED_0xB6', 0xB7 : 'PEState_DFP2PLUG_VDM_RESERVED_0xB7', 0xB8 : 'PEState_UnUsed_0xB8',
                        0xB9 : 'PEState_UnUsed_0xB9', 0xBA : 'PEState_UnUsed_0xBA', 0xBB : 'PEState_UnUsed_0xBB',
                        0xBC : 'PEState_UnUsed_0xBC', 0xBD : 'PEState_Legacy', 0xBE : 'PEState_Disabled', 0xBF : 'PEState_ErrorRecovery',
                        0xC0 : 'PRState_SQUELCH_ACTIVE', 0xC1 : 'PRState_SQUELCH_IDLE', 0xC2 : 'PRState_SOP_RECEIVED', 0xC3 : 'PRState_SOP_PRIME_RECEIVED',
                        0xC4 : 'PRState_SOP_DPRIME_RECEIVED', 0xC5 : 'PRState_RX_BUF_RDY', 0xC6 : 'PRState_HARDRESET_RECEIVED',
                        0xC7 : 'PRState_CABLERESET_RECEIVED', 0xC8 : 'PRState_TXDONE', 0xC9 : 'PRState_INVALID_BIT_TIME', 0xCA : 'PRState_SENDING_GOODCRC',
                        0xCB : 'PRState_RECEIVED_GOODCRC', 0xCC : 'PRState_VBUS_MON_HILO', 0xCD : 'PRState_VBUS_OVP',
                        0xCE : 'PEState_DFP_VDM_Reconfigure', 0xCF : 'PEState_Unused_0xCF',
                        0xD0 : 'PE_CBL_Ready',
                        0xD1 : 'PE_CBL_Send_Identity_SOP_P', 0xD2 : 'PE_CBL_Send_SVIDs_SOP_P', 0xD3 : 'PE_CBL_Send_Modes_SOP_P',
                        0xD4 : 'PE_CBL_Evaluate_Mode_Entry_SOP_P', 0xD5 : 'PE_CBL_Mode_Entry_ACK_SOP_P', 0xD6 : 'PE_CBL_Mode_Entry_NAK_SOP_P',
                        0xD7 : 'PE_CBL_Mode_Exit_SOP_P', 0xD8 : 'PE_CBL_Mode_Exit_ACK_SOP_P', 
                        0xFF : '***PEstate_Invalid***'
                        }

state_list_dict = [ typeC_debug_dict, BC12_debug_dict, USB20_debug_dict, HPD_dict, PD_state_debug_dict, INTs_dict, Power_state_debug_dict,
                    other_debug_dict ]

modules_list = [ 'Type-C Module', 'BC 1.2 Module', 'USB EP Module', 'HPD Module',
                 'PD Module', 'INTS Module', 'Sleep Module', 'Other Module' ]


def translate_fw_history(self):
    byte1 = 0xFF & self.value
    byte2 = 0xFF & (self.value >> 8)

    ret_string = ''

    if byte2 == 0xFF:
        ret_string = '0xFF (Circular Buffer Entry Point)'
    else:
        if byte1 == 5:
            if byte2 < 0x80 :
                if byte2 in state_list_dict[byte1] :
                    ret_string = ret_string + 'INTS Module (I2C1) - %s' %state_list_dict[byte1][byte2]
                else :
                    ret_string = ret_string + 'INTS Module (I2C1) - Unknown (0x%x)' %byte2
            else :
                i2c2value = byte2 - 0x80
                if i2c2value in state_list_dict[byte1] :
                    ret_string = ret_string + 'INTS Module (I2C2) - %s' %state_list_dict[byte1][i2c2value]
                else :
                    ret_string = ret_string + 'INTS Module (I2C2) - Unknown (0x%x)' %i2c2value
        else:
            if byte2 in state_list_dict[byte1]:
                ret_string = ret_string + modules_list[ byte1 ] + ' - ' + state_list_dict[byte1][byte2]
            else:
                ret_string = ret_string + modules_list[ byte1 ] + ' - unknown(0x%x)' %byte2
                    
#    For debugging, display the raw value before it was decoded
#    ret_string = '(%d %d)\t' %(byte1,byte2) + ret_string

    return ret_string


def translate_fw_focus(self):
    byte1 = FW_STATE_CONFIG.fieldByName('Module for Focus Trace Capture (register 0x7D)').value
    byte2 = self.value

    ret_string = ''

    if byte2 == 0xFF:
        ret_string = '0xFF (Circular Buffer Entry Point)'
    else:
        if byte1 == 5:
            if byte2 < 0x80 :
                if byte2 in state_list_dict[byte1] :
                    ret_string = ret_string + '(I2C1) ' + state_list_dict[byte1][byte2]
                else :
                    ret_string = ret_string + '(I2C1) Unknown (0x%x)' %byte2
            else :
                i2c2value = byte2 - 0x80
                if i2c2value in state_list_dict[byte1] :
                    ret_string = ret_string + '(I2C2) ' + state_list_dict[byte1][i2c2value]
                else :
                    ret_string = ret_string + '(I2C2) - Unknown (0x%x)' %i2c2value
        else:
            if byte2 in state_list_dict[byte1]:
                ret_string = ret_string + ' ' + state_list_dict[byte1][byte2]
            else:
                ret_string = ret_string + ' - unknown(0x%x)' %byte2

#    For debugging, display the raw value before it was decoded
#    ret_string = '(%d %d)\t' %(byte1,byte2) + ret_string

    return ret_string

def translate_ints(self):
    if self.value < 0x80 :
        if self.value in INTs_dict :
            return 'I2C1 interrupt %d - %s' %(self.value, INTs_dict[self.value])
        else :
            return 'I2C1 interrupt %d - Unknown' %(self.value, INTs_dict[self.value])
    else :
        i2c2val = self.value - 0x80
        if i2c2val in INTs_dict :
            return 'I2C2 interrupt %d - %s' %(self.value, INTs_dict[i2c2val])
        else :
            return 'I2C2 interrupt %d - Unknown' %(self.value, INTs_dict[i2c2val])


FalseTrue_list = ['True (0)', 'False (1)'] 


FW_STATE_CONFIG = cRegister({'register name' : 'Firmware State Config', 'address' : 0x7C, 'permission' : 'RW',
            'fields' : [
               { 'name' : 'Capture Type-C state transitions (Captures if 0)', 'offset' : 0, 'length' : 1, 'value' : 0, 'translate list' : FalseTrue_list } ,
               { 'name' : 'Capture BC 1.2 state transitions (Captures if 0)', 'offset' : 1, 'length' : 1, 'value' : 0, 'translate list' : FalseTrue_list } ,
               { 'name' : 'Capture USB EP state transitions (Captures if 0)', 'offset' : 2, 'length' : 1, 'value' : 0, 'translate list' : FalseTrue_list } ,
               { 'name' : 'Capture HPD state transitions (Captures if 0)', 'offset' : 3, 'length' : 1, 'value' : 0, 'translate list' : FalseTrue_list } ,
               { 'name' : 'Capture PD state transitions (Captures if 0)', 'offset' : 4, 'length' : 1, 'value' : 0, 'translate list' : FalseTrue_list } ,
               { 'name' : 'Capture INTS state transitions (Captures if 0)', 'offset' : 5, 'length' : 1, 'value' : 0, 'translate list' : FalseTrue_list } ,
               { 'name' : 'Capture Sleep state transitions (Captures if 0)', 'offset' : 6, 'length' : 1, 'value' : 0, 'translate list' : FalseTrue_list } ,
               { 'name' : 'Capture Other state transitions (Captures if 0)', 'offset' : 7, 'length' : 1, 'value' : 0, 'translate list' : FalseTrue_list } ,
               { 'name' : 'Module for Focus Trace Capture (register 0x7D)', 'offset' : 8, 'length' : 3, 'value' : 0, 'translate list' : modules_list } ,
               { 'name' : 'reserved', 'offset' : 11, 'length' : 5, 'value' : 0 } ,
            ] } )


FW_STATE_FOCUS = cRegister({'register name' : 'Firmware State Focus', 'address' : 0x7D, 'permission' : 'RO',
            'fields' : [
               { 'name' : '0', 'offset' : 0, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '1', 'offset' : 8, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '2', 'offset' : 16, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '3', 'offset' : 24, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '4', 'offset' : 32, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '5', 'offset' : 40, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '6', 'offset' : 48, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '7', 'offset' : 56, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '8', 'offset' : 64, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '9', 'offset' : 72, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '10', 'offset' : 80, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '11', 'offset' : 88, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '12', 'offset' : 96, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '13', 'offset' : 104, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '14', 'offset' : 112, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '15', 'offset' : 120, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '16', 'offset' : 128, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '17', 'offset' : 136, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '18', 'offset' : 144, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '19', 'offset' : 152, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '20', 'offset' : 160, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '21', 'offset' : 168, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '22', 'offset' : 176, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '23', 'offset' : 184, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '24', 'offset' : 192, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '25', 'offset' : 200, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '26', 'offset' : 208, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '27', 'offset' : 216, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '28', 'offset' : 224, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '29', 'offset' : 232, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '30', 'offset' : 240, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '31', 'offset' : 248, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '32', 'offset' : 256, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '33', 'offset' : 264, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '34', 'offset' : 272, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '35', 'offset' : 280, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '36', 'offset' : 288, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '37', 'offset' : 296, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '38', 'offset' : 304, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '39', 'offset' : 312, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '40', 'offset' : 320, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '41', 'offset' : 328, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '42', 'offset' : 336, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '43', 'offset' : 344, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '44', 'offset' : 352, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '45', 'offset' : 360, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '46', 'offset' : 368, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '47', 'offset' : 376, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '48', 'offset' : 384, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '49', 'offset' : 392, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '50', 'offset' : 400, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '51', 'offset' : 408, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '52', 'offset' : 416, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '53', 'offset' : 424, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '54', 'offset' : 432, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '55', 'offset' : 440, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '56', 'offset' : 448, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '57', 'offset' : 456, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '58', 'offset' : 464, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '59', 'offset' : 472, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '60', 'offset' : 480, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '61', 'offset' : 488, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '62', 'offset' : 496, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
               { 'name' : '63', 'offset' : 504, 'length' : 8, 'value' : 0, 'translate' : translate_fw_focus } ,
            ] } )


def translate_typeC_debug(self):
    if self.value in typeC_debug_dict :
        return typeC_debug_dict[self.value]
    else:
        return 'Unknown (0x%x)' %self.value


def translate_BC12_debug(self):
    if self.value in BC12_debug_dict :
        return BC12_debug_dict[self.value]
    else:
        return 'Unknown (0x%x)' %self.value
    
def translate_USB20_debug(self):
    if self.value in USB20_debug_dict :
        return USB20_debug_dict[self.value]
    else:
        return 'Unknown (0x%x)' %self.value

def translate_HPD_debug(self):
    if self.value in HPD_dict :
        return HPD_dict[self.value]
    else:
        return 'Unknown (0x%x)' %self.value

def translate_PD_state_debug(self):
    if self.value in PD_state_debug_dict :
        return '(0x%x) ' %self.value +  PD_state_debug_dict[self.value]
    else:
        return 'Unknown (0x%x)' %self.value

def translate_Power_state_debug(self):
    if self.value in Power_state_debug_dict :
        return Power_state_debug_dict[self.value]
    else:
        return 'Unknown (0x%x)' %self.value

def translate_other_debug(self):
    if self.value in other_debug_dict :
        return other_debug_dict[self.value]
    else:
        return 'Unknown (0x%x)' %self.value
    

FW_STATE = cRegister({'register name' : 'Current Firmware State', 'address' : 0x7E, 'permission' : 'RO',
            'fields' : [
               { 'name' : 'Type-C current state', 'offset' : 0, 'length' : 8, 'value' : 0, 'translate' : translate_typeC_debug } ,
               { 'name' : 'BC 1.2 current state', 'offset' : 0, 'length' : 8, 'value' : 0, 'translate' : translate_BC12_debug } ,
               { 'name' : 'USB2.0 EP current state', 'offset' : 0, 'length' : 8, 'value' : 0, 'translate' : translate_USB20_debug } ,
               { 'name' : 'HPD current state', 'offset' : 0, 'length' : 8, 'value' : 0, 'translate' : translate_HPD_debug } ,
               { 'name' : 'PD current state', 'offset' : 0, 'length' : 8, 'value' : 0, 'translate' : translate_PD_state_debug } ,
               { 'name' : 'INTs current state', 'offset' : 0, 'length' : 8, 'value' : 0, 'translate' : translate_ints } ,
               { 'name' : 'Sleep current state', 'offset' : 0, 'length' : 8, 'value' : 0, 'translate' : translate_Power_state_debug } ,
               { 'name' : 'Other current state', 'offset' : 0, 'length' : 8, 'value' : 0, 'translate' : translate_other_debug } ,
            ] } )


FW_STATE_HISTORY = cRegister({'register name' : 'Firmware State History', 'address' : 0x7F, 'permission' : 'RO',
            'fields' : [
               { 'name' : '0', 'offset' : 0, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '1', 'offset' : 16, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '2', 'offset' : 32, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '3', 'offset' : 48, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '4', 'offset' : 64, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '5', 'offset' : 80, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '6', 'offset' : 96, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '7', 'offset' : 112, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '8', 'offset' : 128, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '9', 'offset' : 144, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '10', 'offset' : 160, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '11', 'offset' : 176, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '12', 'offset' : 192, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '13', 'offset' : 208, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '14', 'offset' : 224, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '15', 'offset' : 240, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '16', 'offset' : 256, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '17', 'offset' : 272, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '18', 'offset' : 288, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '19', 'offset' : 304, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '20', 'offset' : 320, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '21', 'offset' : 336, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '22', 'offset' : 352, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '23', 'offset' : 368, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '24', 'offset' : 384, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '25', 'offset' : 400, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '26', 'offset' : 416, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '27', 'offset' : 432, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '28', 'offset' : 448, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '29', 'offset' : 464, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '30', 'offset' : 480, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
               { 'name' : '31', 'offset' : 496, 'length' : 16, 'value' : 0, 'translate' : translate_fw_history } ,
            ] } )






