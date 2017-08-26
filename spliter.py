byte_str = raw_input("Enter Byte Array \r\n")

byte_data_list = byte_str[48::]
#start:end:split by x number
byte_data_list = byte_data_list[::2]
print byte_data_list
