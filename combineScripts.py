#!/usr/bin/env python3

from codecs import decode#, encode
import json
from tim2CompTools import *

file_list = [
    'tran_script.json',
    #'missed_script.json',
    #'missed_script2.json'
]

counter = 0
new_data = {}

for file_name in file_list:

    in_file = open(file_name,'r')
    data = json.loads(in_file.read())
    in_file.close

    for box_num, box_data in data.items():

        new_data[counter] = box_data

        counter += 1

for item in new_data.items():
    print(item[1]["end_offset"])
    break

counter = 0
sorted_data = sorted(
    new_data.items(),
    key=lambda item: item[1]["end_offset"])

final_data = {} # this step updates the dict key
for k, v in sorted_data:
    final_data[counter] = v
    counter += 1

with open('combined_script.json','w') as file:
    json.dump(final_data, file, ensure_ascii=False, indent=2)
