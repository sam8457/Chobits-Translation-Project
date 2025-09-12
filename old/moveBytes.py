# int(value, 16) # convert hex to int
# hex(value) # convert int to hex

import os
if os.path.exists('SLPM_652.55'):
    os.remove("SLPM_652.55")

input_file = open('SLPM_652.55.original', 'rb')
output_file = open('SLPM_652.55', 'ab')

starting_address = int("1024C0",16)
ending_address = int("196F04",16)

first_chunk = input_file.read(starting_address)
output_file.write(first_chunk)

excerpt_length = ending_address - starting_address
excerpt = input_file.read(excerpt_length)
output_file.write(b'\x00' * excerpt_length)
    
last_chunk = input_file.read()
output_file.write(last_chunk)

output_file.write(b'\x00' * 4)
output_file.write(excerpt)

input_file.close()
output_file.close()