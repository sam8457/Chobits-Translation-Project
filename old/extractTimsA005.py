#!/usr/bin/env python3

# Todo: extract from multiple files at once
# Todo: write re-inserter for multiple files

import os
import tim2CompTools

# A005 doesn't have empty space between its files, so it had to be extracted differently
# Maybe try this on the other files and see what it does (I'm betting infinite loop)
INPUT_NAME = "A005" 

input_file = open(INPUT_NAME, 'rb')
input_data = input_file.read()
input_file.close()

TIM2_code = bytes.fromhex('54494D32')
stop_code = bytes.fromhex('5c4007')

img_num = 0

img_num = 0

while input_data.find(TIM2_code) != -1:
    
    if img_num > 350: # protects against inf loops, may need to increase
        break

    tim_start = input_data.find(TIM2_code) - 1

    prefix = input_data[:tim_start]
    input_data = input_data[tim_start:]

    prefix_name = INPUT_NAME+'_'+str(img_num)+'.prefix'
    print("Writing to", prefix_name)
    prefix_file = open(prefix_name, 'wb')
    prefix_file.write(prefix)
    prefix_file.close()

    tim_end = input_data.find(stop_code)
    tim_data = input_data[:tim_end]
    input_data = input_data[tim_end:]

    decompressed_tim = tim2CompTools.decompress(tim_data)

    tim_name = INPUT_NAME+'_'+str(img_num)+'.tm2'
    print("Writing to", tim_name)
    tim_file = open(tim_name, 'wb')
    tim_file.write(decompressed_tim)
    tim_file.close()

    img_num += 1

suffix_name = tim_name = INPUT_NAME+'_'+str(img_num)+'.suffix'
print("Writing to", suffix_name)
suffix_file = open(suffix_name, 'wb')
suffix_file.write(input_data)
suffix_file.close()

