#!/usr/bin/env python
import collections
PayLoad_type = collections.OrderedDict()


container = []
byte_hex = []
nof_apt = []
nof_line = 0


f1 = open('test.csv',"rU")

for line in f1.readlines():
    container.append(line.split(','))
    nof_line = nof_line + 1

for cnt in range (0,nof_line):
    PayLoad_type[container[cnt][0]]=int(container[cnt][1])

def swap (c,i):
    if i == 2:
        c[0],c[1] = c[1],c[0]
    elif i == 4:
        c[0],c[1],c[2],c[3] =  c[3],c[2],c[1],c[0]
    elif i == 8:
         c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7] = c[1],c[0],c[3],c[2],c[5],c[4],c[7],c[6]
        
    return  ''.join(c)

def extend_query_to_term():

    iput = raw_input("enter key\r\n") 
    while not iput == 'quit':
        iput = raw_input("enter key\r\n") 

        try:
            PayLoad_type[iput]
        except KeyError:
            pass
    return 


def load_mav_op(iput):

    return PayLoad_type[iput]

def print_byte_seq(seq, byte_array, payload_data , return_idx_req):

    start_idx = payload_data['end_idx']
    value_to_return = 0
    for cnt in range(0,len(seq)):
        print start_idx,'\t', seq[cnt].ljust(30),'\t', int(swap(byte_array[start_idx:start_idx + PayLoad_type[seq[cnt]]],PayLoad_type[seq[cnt]]),16), '\t\t  HEX \t', swap(byte_array[start_idx:start_idx + PayLoad_type[seq[cnt]]],PayLoad_type[seq[cnt]])
        #for return_cnt in range(0,len(return_idx_req)): 
        if seq[cnt] == return_idx_req:
            value_to_return = int(swap(byte_array[start_idx:start_idx + PayLoad_type[seq[cnt]]],PayLoad_type[seq[cnt]]),16)
        start_idx = start_idx + PayLoad_type[seq[cnt]]

    payload_data['end_idx'] = start_idx

    return value_to_return

def print_byte_seq_single(seq, byte_array, payload_data):

    start_idx = payload_data['end_idx']
    value_to_return = 0
    print start_idx,'\t', seq.ljust(30),'\t', int(swap(byte_array[start_idx:start_idx + PayLoad_type[seq]],PayLoad_type[seq]),16), '\t\t  HEX \t', swap(byte_array[start_idx:start_idx + PayLoad_type[seq]],PayLoad_type[seq])
    #for return_cnt in range(0,len(return_idx_req)): 
    value_to_return = int(swap(byte_array[start_idx:start_idx + PayLoad_type[seq]],PayLoad_type[seq]),16)
    start_idx = start_idx + PayLoad_type[seq]

    payload_data['end_idx'] = start_idx

    return value_to_return


def get_byte_seq(seq, byte_array, payload_data , seq_list):

    start_idx = payload_data['end_idx']
    print seq_list , len(seq_list)
    value_to_return = 0
    for cnt in range(0,len(seq)):
          for key in seq_list:
            if seq[cnt] == key:
                seq_list[key] = int(swap(byte_array[start_idx:start_idx + PayLoad_type[seq[cnt]]],PayLoad_type[seq[cnt]]),16)
                value_to_return = int(swap(byte_array[start_idx:start_idx + PayLoad_type[seq[cnt]]],PayLoad_type[seq[cnt]]),16)

    start_idx = start_idx + PayLoad_type[seq[cnt]]

    return value_to_return

def cal_seq_build(byte_array, payload_data):

    cmd_seq = [
    'CMD_CODE',
    'SUB_SYS_ID',
    'MODE ID',
    'FTM CMD',
    'REQ LENGTH',
    'RSP LENGTH',
    'START_CAL',
    'RADIO_TD',
    'ENABLE_DB',
    'NOF_SEG',
    'PAYLOAD',
    'RESULT_SIZE']

    ftm_cmd = get_byte_seq(cmd_seq, byte_array, payload_data,'FTM CMD')
    payload_data['nof_seg'] = print_byte_seq(cmd_seq, byte_array, payload_data,'NOF_SEG')        
    end_idx = payload_data['end_idx'] 
    nof_seg = payload_data['nof_seg']

    return end_idx , nof_seg , ftm_cmd


def data_push_op(byte_array, payload_data):

    data_action = 0 
    cmd_seq = [
    'INTERVAL',
    'VERSION',
    'DEBUG_MODE',
    'FLAG',
    'TECH_1',
    'REF_CH',
    'DEV',
    'DATA_ACTION']


    data_action = print_byte_seq(cmd_seq, byte_array, payload_data,'DATA_ACTION')
    data_push[data_action](byte_array,payload_data)

    return 

def fbr_push_action(byte_array, payload_data):

    fbr_seq_type = ['FBR_DATA_TYPE']    

    fbr_seq = [
    'NV_GEN',
    'BAND',
    'SUB_BAND',
    'NOF_RFM_PATHS',
    'NV_CONTAINER',
    'RFM_DEV',
    'SIG_PATH',
    'ANT_PATH',
    'RESERVED',
    'TERM_ADC',
    'NOF_FRBX_MODE',
    'FBRX_MODE',
    'NOF_CHANNEL'
    ]

    fbr_ch = ['CHANNEL']

    fbr_gain_states = ['NOF_FBRX_GAIN_STATE']

    fbr_data = [
    'FBRX_GAIN_STATE',
    'PREDET_IDX',
    'TRUNC_BITS',
    'FBRX_HW_GAIN',
    'FBRX_SW_GAIN',
    'TX_POWER',
    'LSE_ERROR',
    ]

    fbr_seq_type = print_byte_seq(fbr_seq_type, byte_array, payload_data,'FBR_DATA_TYPE') 
    
    if fbr_seq_type == 2:
        nof_channel = print_byte_seq(fbr_seq, byte_array, payload_data,'NOF_CHANNEL')

        for cnt in range (0,nof_channel):
            print_byte_seq(fbr_ch, byte_array, payload_data,'') #channel            
            nof_fbr_gain_states = print_byte_seq(fbr_gain_states, byte_array, payload_data,'NOF_FBRX_GAIN_STATE')

            for fbr_cnt in range (0,nof_fbr_gain_states):
                print_byte_seq(fbr_data, byte_array, payload_data,'')
    else:
        print ' fbr seq not supported'
        
    return

def seq_build(byte_array, payload_data):

    seq_data = [
   'INTERVAL',
    'VERSION',
    'DEBUG_MODE',
    'FLAG',
    'SEQ_TYPE',
    'HANDLE',
    ]

    seq_type_payload = print_byte_seq(seq_data, byte_array, payload_data,'SEQ_TYPE') #channel 
    seq_type_build[seq_type_payload](byte_array, payload_data)
    return


def build_radio_setup(byte_array, payload_data):
    
    payload_data_header = [
        'VER',        
        'TECH_2',
        'TEAR_DN'
        ]

    radio_setup_type_info = [
        'RADIO_SETUP_TYPE'
        ]

    nof_rfm_path_info = [
        'NOF_RFM_PATH'
        ]

    rfm_path_type_info = [
        'BAND',
        'SUB_BAND',
        'RFM_DEV',
        'SIG_PATH',
        'ANT_SW',
        'RES',
        'RFM_PATH_TYPE',
        'BW',
        ]
    
    nof_channel_info = [
        'NOF_CH',
        ]

    channel_info =[
        'CH'
        ]
    
    nv_container_info = [
        'NV_CONTAINER'
        ]

    tx_param = [
        'TX_WAVE',
        'NOF_RB',
        'START_RB',
        ]

    is_teardown = print_byte_seq(payload_data_header, byte_array, payload_data,'TEAR_DN')

    if is_teardown == 1:
        return

    radio_setup_type = print_byte_seq(radio_setup_type_info, byte_array, payload_data,'RADIO_SETUP_TYPE')
    nof_rfm_path = print_byte_seq(nof_rfm_path_info, byte_array, payload_data,'NOF_RFM_PATH')

    if radio_setup_type == 0:
        for rfm_path in range (0, nof_rfm_path):
            print '+++++++'
            rfm_path_type = print_byte_seq(rfm_path_type_info, byte_array, payload_data,'RFM_PATH_TYPE')
            nof_ch = print_byte_seq(nof_channel_info, byte_array, payload_data,'NOF_CH')

            for ch_cnt in range (0, nof_ch):
                print_byte_seq(channel_info, byte_array, payload_data,'')
                print_byte_seq(nv_container_info, byte_array, payload_data,'')

            if rfm_path_type == 0: #tx path
                print_byte_seq(tx_param, byte_array, payload_data,'')
             

    else:
        print "NO SUPPORT - TELL DN TO FIX IT"
        return -1
    
    return


def build_apt_cal(byte_array, payload_data):

    apt_seq_type_info = [
    'APT_SEQ_TYPE'    
    ]

    apt_seq_type_0_nof_pa_state_info = [
    'UPPERBOUND_CHANNEL',
    'NOF_PA',
    ]

    apt_seq_type_0_pa_info = [
    'PA_STATE',
    'BIAS',
    'ICQ',
    ]
    apt_seq_type_0_nof_rgi_info = [
    'NOF_RGI'
    ]

    apt_seq_type_0_rgi_info = [
    'RGI'
    ]

    apt_seq_type_0_exp_power_option_info = [
    'EXP_PWR_OPTION'
    ]

    apt_seq_type_0_exp_power_info = [
    'EXP_PWR'
    ]

    apt_seq_type_0_limit_option_info = [
    'LIMIT_OP'
    ]


    seq_query_list = {
        'UPPERBOUND_CHANNEL':0,
        }
    apt_seq_type = print_byte_seq(apt_seq_type_info, byte_array, payload_data,'APT_SEQ_TYPE')

    if apt_seq_type == 0: # full bias
        #get_byte_seq(apt_seq_type_0_nof_pa_state_info, byte_array, payload_data,seq_query_list)
        nof_pa_state = print_byte_seq(apt_seq_type_0_nof_pa_state_info, byte_array, payload_data,'NOF_PA')

        for nof_pa_state_cnt in range(0,nof_pa_state):
            print_byte_seq(apt_seq_type_0_pa_info, byte_array, payload_data,'NOF_PA')
            nof_rgi = print_byte_seq(apt_seq_type_0_nof_rgi_info, byte_array, payload_data,'NOF_RGI')

            for nof_rgi_cnt in range (0, nof_rgi):
                print_byte_seq(apt_seq_type_0_rgi_info, byte_array, payload_data,'')

            exp_power_option = print_byte_seq(apt_seq_type_0_exp_power_option_info, byte_array, payload_data,'EXP_PWR_OPTION')        
            if exp_power_option == 1:
                for nof_rgi_cnt in range (0, nof_rgi):
                    print_byte_seq(apt_seq_type_0_exp_power_info, byte_array, payload_data,'')
            elif exp_power_option == 0:
                print 'Apt - Expected Gain - no support'
                return -1

            limit_option = print_byte_seq(apt_seq_type_0_limit_option_info, byte_array, payload_data,'LIMIT_OP')
            if limit_option == 1:
                print 'Apt - Limits option En - no support'
                return -1

    elif apt_seq_type == 1: # apt linearizer
            nof_pa = print_byte_seq_single('NOF_PA', byte_array, payload_data)
            for cnt in range(0,nof_pa):
                print_byte_seq_single('PA_STATE', byte_array, payload_data)

            for cnt in range(0,nof_pa):
                nof_apt.append(print_byte_seq_single('PA_STAT_ENTRIES', byte_array, payload_data))

            for cnt in  range (0, nof_pa):
                print "PA STATE PARAM " , cnt
                for apt_cnt in range(0,nof_apt[cnt]):
                    print_byte_seq_single('APT_PWR', byte_array, payload_data)
                for apt_cnt in range(0,nof_apt[cnt]):
                    print_byte_seq_single('APT_BIAS', byte_array, payload_data)
                for apt_icq in range(0,nof_apt[cnt]):
                    print_byte_seq_single('APT_ICQ', byte_array, payload_data)                    
            GAIN_DELTA_OPTION = print_byte_seq_single('PA_STAT_ENTRIES', byte_array, payload_data)

            if GAIN_DELTA_OPTION == 1:
                print 'Gain Delta APT  - no support'

            return -1
    elif apt_seq_type == 2: # freq comp
            print 'Apt Freq Comp Sweep - no support'
            return -1

    return

def build_xpt_cal(byte_array, payload_data):
    print 'xpt no support'
    #param type
    payload_type_id = ['TYPE_ID']

    #Debug Type
    payload_0 = [
    'DEBUG_STOP_STEP',
    'DEBUG_LOG'
    ]

    #RGI DELTA
    payload_1 = [
    'DEBUG_STOP_STEP',
    'DEBUG_LOG',
    'RGI_DELTA_START',
    'RGI_DELTA_STOP',
    'RGI_DELTA_STEP',
    ]

    #Mline Param
    payload_2 = [
    'NUM_IQ_CAP',
    'XPT_MODE',
    'PA_STATE',
    'ICQ',
    ]

    payload_2_para = [
    'RGI',
    'BIAS',
    'EXP_PWR'
    ]

    payload_3 = [
    'MLINE_RES_FLAG',
    'COMP_DB',
    'CURFIT',
    'VD_MAX',
    'NOF_TARGET_MEAS_PWR',
    ]

    payload_3_target = ['TARGET_POWER']

    payload_4 = ['notinuse']
    
    payload_5_nof_ET_V = ['NOF_ET_VMIN']

    nof_params = print_byte_seq_single('NUM_OF_PARAM', byte_array, payload_data)

    for cnt in range(0,nof_params):
        payload_type = print_byte_seq(payload_type_id, byte_array, payload_data,'')
        if payload_type == 0:
            print_byte_seq(payload_0, byte_array, payload_data,'')
        elif payload_type == 1:
            print_byte_seq(payload_1, byte_array, payload_data,'')
        elif payload_type == 2:
            nof_iq_cap = print_byte_seq(payload_2, byte_array, payload_data,'NUM_IQ_CAP')
            for iq_cnt in range(0,nof_iq_cap):
                print_byte_seq(payload_2_para, byte_array, payload_data,'')
        elif payload_type == 3:
            print_byte_seq(payload_2_para, byte_array, payload_data,'')
    
    return
def seq_exe(byte_array, payload_data):

    seq_data = [
   'INTERVAL',
    'VERSION',
    'DEBUG_MODE',
    'FLAG',
    'SEQ_TYPE',
    'HANDLE',
    ]

    seq_type_payload = print_byte_seq(seq_data, byte_array, payload_data,'SEQ_TYPE') #channel 
    seq_type_exe[seq_type_payload](byte_array, payload_data)
    
    return

def exe_radio_setup(byte_array, payload_data):

    radio_setup_exe = [
    'RADIO_SETUP_VER'
    ]

    print_byte_seq(radio_setup_exe, byte_array, payload_data,'')


    return

def exe_apt_setup(byte_array, payload_data):

    radio_setup_exe = [
    'APT_CAL_SEQ_TYPE',
    'APT_CAL_VER'
    ]

    print_byte_seq(radio_setup_exe, byte_array, payload_data,'')


    return

data_push = {2048:fbr_push_action}
seq_type_build ={
                1:build_radio_setup,
                6:build_apt_cal,
                7:build_xpt_cal,
                }

seq_type_exe = {
                1:exe_radio_setup,
                6:exe_apt_setup,
                }

