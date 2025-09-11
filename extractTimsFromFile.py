#!/usr/bin/env python3

import os
import tim2CompTools

INPUT_FILE_NAME = "A002"

input_file = open(INPUT_FILE_NAME, 'rb')

output_file_name = INPUT_FILE_NAME+'.tm2'
if os.path.exists(output_file_name):
    os.remove(output_file_name)
output_file = open(output_file_name, 'ab')

prefix = input_file.read(3) # if the starting bit is off even by 1, it will produce incoherent output
print(prefix.hex())
compressed_data = input_file.read()

decompressed_data = tim2CompTools.decompress(compressed_data)

output_file.write(decompressed_data)

input_file.close()
output_file.close()