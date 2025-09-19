#!/usr/bin/env python3

import json
from tim2CompTools import *


def isValidSJIS(value):

    if value.hex()[2:] == '0a':
        return True, "newline"

    # review which ones exactly are reserved, this causes nearly every textbox to be marked
    reserved_ranges = [
        "824f","82f1",
        "8340","8396",
        "8440","845d",
        "897e","897e",
    ]
    
    for r in range(0, len(reserved_ranges), 2):

        lo = bytes.fromhex(reserved_ranges[r])
        hi = bytes.fromhex(reserved_ranges[r+1])

        if value >= lo and value <= hi:
            return True, "reserved"

    unreserved_ranges = [
        "8140","81F1",
        "8397","83d6",
        "845e","84bc",
        "889f","88ff",
        "8940","897d",
        "897f","89ff",
        "8a40","8aff",
    	"8b40","8bff",
	    "8c40","8cff",
    	"8d40","8dff",
    	"8e40","8eff",
    	"8f40","8fff",
    	"9040","90ff",
	    "9140","91ff",
	    "9240","92ff",
	    "9340","93ff",
	    "9440","94ff",
        "9540","95ff",
        "9640","96ff",
        "9740","97ff",
        "9840","9872",
    ]

    for r in range(0, len(unreserved_ranges), 2):

        lo = bytes.fromhex(unreserved_ranges[r])
        hi = bytes.fromhex(unreserved_ranges[r+1])

        if value >= lo and value <= hi:
            return True, "unreserved"

    return False, ""


input_file = open('SLPM_652.55.original', 'rb')
input_data = input_file.read()
input_file.close()

script_json = {
#    "Example":{
#        "end_offset":"103353",
#        "orig":"こにちは、\n私の名前わサムです。",
#        "orig_len":31,
#        "reserved?":False,
#        "tran":"Hello, \nmy name is Sam.",
#        "tran_len":23,
#        "shorten?":False,
#    },
}

end_code = bytes.fromhex('0A001502')
last_box = 0
num_boxes = 0

while True:

    box_end = input_data.find(end_code, last_box+1)

    if box_end == -1:
        break

    box_index = box_end
    reserved = False

    while True:

        char_code = input_data[box_index-2:box_index]
        valid, type = isValidSJIS(char_code)

        if not valid:
            last_box = box_end
            break

        if type == 'newline':
            box_index -= 1
            continue
        
        if type == 'reserved':
            reserved = True

        box_index -= 2

    # need to add support for converting input data to SJIS chars, then adding them to this_box (do it in the loop above)
    this_box = input_data[box_index:box_end]

    try:
        script_json[num_boxes] = {
            "end_offset":box_end,
            "orig":this_box[0], # still needs converted to sjis
            "orig_len":len(this_box),
            "reserved?":reserved,
        }
    except IndexError:
        print("First char_code of box",num_boxes,":",char_code,"at offset",box_end)

    num_boxes += 1

with open('script.json','w') as file:
    json.dump(script_json, file, ensure_ascii=False, indent=2)

