#!/usr/bin/env python3

import tim2CompTools

# Put the file to be extracted in the same directory this script
# Can use grep ./ -r -e "TIM2" in linux terminal to search for files containing TIM2 images TMPGEnc
INPUT_NAME = "A007" # Example: A001

input_file = open(INPUT_NAME, 'rb')
input_data = input_file.read()
input_file.close()

TIM2_code = bytes.fromhex('54494D32')
stop_code = bytes.fromhex("0000000000000000")
#stop_code = bytes.fromhex('5c4007') # Needed for file A005

img_num = 0

def writeAnnounce(data, file_num, extension):
    file_name = INPUT_NAME + '_' + str(file_num) + extension
    print("Writing to", file_name)
    file = open(file_name, 'wb')
    file.write(data)
    file.close()
    return

while input_data.find(TIM2_code) != -1:
    
    if img_num > 350: # protects against inf loops, may need to increase
        break

    tim_start = input_data.find(TIM2_code) - 1
    prefix = input_data[:tim_start]
    input_data = input_data[tim_start:]

    writeAnnounce(prefix,img_num,'.prefix')

    tim_end = input_data.find(stop_code)
    tim_data = input_data[:tim_end]
    input_data = input_data[tim_end:]

    decompd_tim = tim2CompTools.decompress(tim_data)

    writeAnnounce(decompd_tim,img_num,'.tm2')

    img_num += 1

writeAnnounce(input_data,img_num,'.suffix')
