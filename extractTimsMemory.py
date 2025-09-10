# int(value, 16) # convert hex to int
# hex(value) # convert int to hex
# Tm2 file documentation: https://openkh.dev/common/tm2.html

import os
if os.path.exists('image.tm2'):
    os.remove("image.tm2")

input_file = open('eeMemory.bin.original', 'rb')
output_file = open('image.tm2', 'ab')

starting_address = int("46F960",16)
ending_address = int("4825A0",16)

excerpt_length = ending_address - starting_address
input_file.seek(starting_address)
print(hex(input_file.tell()))
excerpt = input_file.read(excerpt_length)

output_file.write(excerpt)

input_file.close()
output_file.close()