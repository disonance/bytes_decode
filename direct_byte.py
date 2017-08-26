#!/usr/bin/env python
#byte parser //The above needs to be present for command line execution
from struct import *
import zlib
import gzip
import StringIO
import csv
import os
import collections
import mav17_opcode
# import usb.core
# import usb.util

# dev = usb.core.find(idVendor=0x05c6, idProduct=0x9002)
#
# if dev is None:
#     raise ValueError('Device not found')
#
# # set the active configuration. With no arguments, the first
# # configuration will be the active one
# dev.set_configuration()
#
# # get an endpoint instance
# cfg = dev.get_active_configuration()
# intf = cfg[(0,0)]
#
# ep = usb.util.find_descriptor(
#     intf,
#     # match the first OUT endpoint
#     custom_match = \
#     lambda e: \
#         usb.util.endpoint_direction(e.bEndpointAddress) == \
#         usb.util.ENDPOINT_OUT)
#
# assert ep is not None
#
# print ep
# # write the data
# ep.write('test')
    
compressed_stream = []
uncompressed_data = []

container = []
byte_hex = []
nof_line = 0
payload_data={"start_idx":0,"nof_seg":0,"end_idx":0,"data_action":0}
opcode_sw = {'0800':mav17_opcode.data_push_op,
             '4000000000040000':mav17_opcode.seq_build,
             '4000000000080000':mav17_opcode.seq_exe}

print "SUPER DUPER v0.0"
print "===================================="
print "Name of the Structure file :",f1.name
print "Name of the Data file      :",f2.name
obiwankanobi = raw_input("Hit Any Key to Continue or 1 to run Auto\r\n")

if obiwankanobi == 'c':
    byte_str = raw_input("Enter Byte Array \r\n")


os.system('clear')
byte_array = byte_str.split()

x = 0
limit = 0
if byte_array[0][0:2]=='0x':

    for cnt in range(0,len(byte_array)):
        if byte_array[cnt] == '0x7d':
            limit = limit +1

    print "nof of escpae char" , limit
    
    for cnt in range(0,(len(byte_array)-limit)):
        byte_array[cnt] = byte_array[cnt+x][2:]
         
        if byte_array[cnt] == '7d':
            print "special Char @ " , cnt , byte_array[cnt+x] , byte_array[cnt+x+1]
            if byte_array[cnt+x+1] == '0x5d':                   
                byte_array[cnt] = '7d'
            else:
                byte_array[cnt] = '7e'
            x=x+1
            
        print cnt,"->", byte_array[cnt]
else:

    for cnt in range(0,len(byte_array)):
        if byte_array[cnt] == '7d':
            limit = limit +1

    print "nof of escpae char" , limit
    
    for cnt in range(0,(len(byte_array)-limit)):
        byte_array[cnt] = byte_array[cnt+x]

        if byte_array[cnt] == '7d':
            print "special Char @ " , cnt , byte_array[cnt+x] , byte_array[cnt+x+1]
            if byte_array[cnt+x+1] == '5d':                   
                byte_array[cnt] = '7d'
            else:
                byte_array[cnt] = '7e'
            x=x+1
        print cnt,"->", byte_array[cnt]


        
byte_pos = 0
os.system('clear')
print "Byte Pos","\t\t","Field","\t","Response"
print "==========================================="
if obiwankanobi == '1':
    
 
    response = mav17_opcode.cal_seq_build(byte_array, payload_data)
    nof_seg = payload_data['nof_seg']

    print payload_data['end_idx'] ,'- >', cnt
    print response
    for cnt in range(payload_data['end_idx'],cnt):
        compressed_stream += (chr(int(byte_array[cnt],16)))

    compressed_stream_list = ''.join(compressed_stream)

    print len(compressed_stream_list)

    uncompressed_stream_list = zlib.decompress(compressed_stream_list)

    print len(uncompressed_stream_list)

    print uncompressed_stream_list
    for cnt in range(0,len(uncompressed_stream_list)):
        uncompressed_data.append(hex(ord(uncompressed_stream_list[cnt]))[2:])

    #print byte_array
    for cnt in range(0,len(uncompressed_data)):
        uncompressed_data[cnt] = uncompressed_data[cnt].zfill(2)
    byte_array = uncompressed_data

 
    payload_data['end_idx'] = 0

    seg_number = 0
    
    while seg_number != 8: #nof_seg:  get opcode
        
        opcode_msb = int(swap(byte_array[payload_data['end_idx']:payload_data['end_idx']+2],2),16)
        opcode_size = (opcode_msb & 0xC000)>>14

        print 'Seg Number' , seg_number
        print '-----------------------'
    
        if opcode_size == 0:
            opcode = swap(byte_array[payload_data['end_idx']:payload_data['end_idx']+2],2)
            print ' OPCODE - > ', opcode
            payload_data['end_idx'] = payload_data['end_idx'] + 2
            opcode_sw[opcode](byte_array, payload_data)
        elif opcode_size == 1:
            opcode = swap(byte_array[payload_data['end_idx']:payload_data['end_idx']+8],8)
            print ' OPCODE - > ', opcode
            payload_data['end_idx'] = payload_data['end_idx'] + 8
            opcode_sw[opcode](byte_array, payload_data)

        print '-----------------------'
        seg_number=seg_number+1
 #       nof_seg = seg_number
# others not currently supported






#    data = payload_value(byte_array,1)
#    print data[0],'\t',data[1]
#    data = payload_value(byte_array,1)
#    print data[0],'\t',data[1]
#    data = payload_value(byte_array,2)
#    print data[0],'\t',data[1]
#    data = payload_value(byte_array,2)
#    print data[0],'\t',data[1]


#case for Sweep Opcode
    #nof Seg
        #Seg N - > Op Code
        #Interval
        #Payload

    


    
else: #manual MODE
    
    for cnt in range (0,nof_line):
     
        nof_byte = int(container[cnt][1])
        
        if nof_byte == 1:
            print byte_pos, "\t", container[cnt][0].ljust(30),"\t", int(byte_array[byte_pos],16), "\t\t\t HEX " , byte_array[byte_pos]

        elif nof_byte == 2:
            print byte_pos, "\t", container[cnt][0].ljust(30),"\t", int(swap(byte_array[byte_pos:byte_pos+nof_byte],2),16), "\t\t\t HEX " ,swap(byte_array[byte_pos:byte_pos+nof_byte],2)

        elif nof_byte == 4:
            print byte_pos, "\t", container[cnt][0].ljust(30),"\t", int(swap(byte_array[byte_pos:byte_pos+nof_byte],4),16), "\t\t\t HEX " ,swap(byte_array[byte_pos:byte_pos+nof_byte],4)

        elif nof_byte == 8:
            print byte_pos, "\t", container[cnt][0].ljust(30),"\t", int(swap(byte_array[byte_pos:byte_pos+nof_byte],8),16), "\t HEX " , swap(byte_array[byte_pos:byte_pos+nof_byte],8)

        byte_pos = byte_pos + nof_byte



