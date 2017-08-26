import zlib

limit = 0
x = 0
compressed_stream = []

byte_str = raw_input("Enter Byte Array \r\n")

byte_data_list = byte_str[0::100]
byte_array = byte_str.split()
# byte_data_list = byte_data_list.split()
print len(byte_array)
print byte_array
# print "byte_data_list"
# print byte_data_list





for cnt in range(0, len(byte_array)):
    if byte_array[cnt] == '7d':
        limit = limit + 1

print "nof of escpae char", limit

for cnt in range(0, (len(byte_array) - limit)):
    byte_array[cnt] = byte_array[cnt + x]

    if byte_array[cnt] == '7d':
        print "special Char @ ", cnt, byte_array[cnt + x], byte_array[cnt + x + 1]
        if byte_array[cnt + x + 1] == '5d':
            byte_array[cnt] = '7d'
        else:
            byte_array[cnt] = '7e'
        x = x + 1
    print cnt, "->", byte_array[cnt]



for cnt in range(0, len(byte_array)):
    compressed_stream += (chr(int(byte_array[cnt], 16)))

compressed_stream_list = ''.join(compressed_stream)

print len(compressed_stream_list)

print ("%s" % compressed_stream_list)

uncompressed_stream_list = zlib.decompress(compressed_stream_list)

print uncompressed_stream_list