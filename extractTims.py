#!/usr/bin/env python3

# Todo: extract from multiple files at once
# Todo: write re-inserter for multiple files

import os
import tim2CompTools

# Put the file to be extracted in the same directory this script
# Can use grep ./ -r -e "TIM2" in linux terminal to search for files containing TIM2 images
INPUT_FILE_NAME = "A020" # Example: A001

input_file = open(INPUT_FILE_NAME, 'rb')
input_file_data = input_file.read()
input_file.close()

TIM2_in_hex = '54494D32'
start_code = bytes.fromhex(TIM2_in_hex)
stop_code = bytes.fromhex("0000000000000000")
start_of_tim = input_file_data.find(start_code) - 4

img_num = 0

while input_file_data.find(start_code) != -1:
    
    if img_num > 350: # protects against inf loops, may need to increase
        break

    start_of_tim = input_file_data.find(start_code) - 1 # first 1-byte command is 1 before TIM2
    prefix = input_file_data[:start_of_tim]
    input_file_data = input_file_data[start_of_tim:]

    stop_of_tim = input_file_data.find(stop_code)
    tim_data = input_file_data[:stop_of_tim]
    input_file_data = input_file_data[stop_of_tim:]

    decompressed_tim = tim2CompTools.decompress(tim_data)

    output_file_name = INPUT_FILE_NAME+'_'+str(img_num)+'.tm2'
    output_prefix_file_name = INPUT_FILE_NAME+'_'+str(img_num)+'.prefix'
    img_num += 1

    print("Writing to", output_file_name)
    output_file = open(output_file_name, 'wb')
    output_prefix_file = open(output_prefix_file_name, 'wb')

    output_file.write(decompressed_tim)
    output_prefix_file.write(prefix)

    output_file.close()
    output_prefix_file.close()

suffix_file_name = output_file_name = INPUT_FILE_NAME+'_'+str(img_num)+'.suffix'
suffix_file = open(suffix_file_name, 'wb')
suffix_file.write(input_file_data)
suffix_file.close()

