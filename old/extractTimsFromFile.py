#!/usr/bin/env python3

from os import path as p

import os
import re
import tim2CompTools

working_dir = os.path.dirname(__file__)
input_dir = "original_game_files" # altered game files
output_dir = "extracted_tims" # altered tims

if not os.path.isdir(input_dir):
    os.makedirs(input_dir) 

if not os.path.isdir(output_dir):
    os.makedirs(output_dir) 

for original_name in os.listdir("original_game_files"):
    
    print("Processing ", original_name)

    original_file = open(p.join(input_dir,original_name), 'rb')
    original_file_data = original_file.read()

    tim2_locations = original_file_data.find('TIM2'.encode())
    #tim2_locations = re.findall('TIM2'.encode())

    print(tim2_locations)

'''
    exit()

    tim2_file_name = original_name + ".tm2"
    prefix_file_name = original_name + ".prefix"

    if os.path.exists(tim2_file_name):
        os.remove(tim2_file_name)

    if os.path.exists(tim2_file_name):
        os.remove(prefix_file_name)

    tim2_file = open(tim2_file_name, 'wb')
    prefix_file = open(prefix_file_name, 'wb')
'''

exit()

input_file_head = open("A002", 'rb')
input_file_body = open("A002.tm2", 'rb')

#output_file_name = INPUT_FILE_NAME+'.tm2'
output_file_name = INPUT_FILE_NAME + "_Altered"
if os.path.exists(output_file_name):
    os.remove(output_file_name)
output_file = open(output_file_name, 'ab')

prefix = input_file_head.read(3) # if the starting bit is off even by 1, it will produce incoherent output
uncompressed_data = input_file_body.read()

compressed_data = tim2CompTools.compressBadly(uncompressed_data)

output_data = b''
output_data += prefix
output_data += compressed_data
output_file.write(output_data)

input_file_head.close()
input_file_body.close()
output_file.close()

'''
Todo:
    *Locate TIM2 image(s) in file
        Search for TIM2 header
        Identify when TIM2 image ends
    *Extract data from file
    *Output to decompressed files
        Name according to input file and order (ex: A002_001.tm2)
    *Write recompressor and reinserter
    *Write better compressor
'''