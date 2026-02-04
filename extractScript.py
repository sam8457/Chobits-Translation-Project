#!/usr/bin/env python3

from codecs import decode#, encode
import json
from tim2CompTools import *

def isValidMoji(value):

    if value.hex()[2:] == '0a': # case sensitive
        return True, "newline"

    # Values the Chobits devs customized that an auto-translator may struggle with
    customized_ranges = [ 
        "8446","845d", # might need to be extended to 845e
    ]
    
    for r in range(0, len(customized_ranges), 2):

        lo = bytes.fromhex(customized_ranges[r])
        hi = bytes.fromhex(customized_ranges[r+1])

        if value >= lo and value <= hi:
            return True, "customized"

    # Values in the original game that contain normal SJIS text
    standard_ranges = [
        "8140","81F1",
        "824f","82f1",
        "8340","8396",
        "8440","845c",
        "8397","83d6",
        "845e","84bc",
        "889f","88ff",
        "8940","897d",
        "897e","89ff",
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

    for r in range(0, len(standard_ranges), 2):

        lo = bytes.fromhex(standard_ranges[r])
        hi = bytes.fromhex(standard_ranges[r+1])

        if value >= lo and value <= hi:
            return True, "standard"

    return False, ""

def extractScript():

    input_file = open('SLPM_652.55.original', 'rb')
    input_data = input_file.read()
    input_file.close()

    script_json = {
    #    "Example":{
    #        "end_offset":"103353",
    #        "orig":"こにちは、\n私の名前わアレクスです。",
    #        "orig_len":31,
    #        "customized?":False,
    #        "tran":"Hello, \nmy name is Alex.",
    #        "tran_len":23,
    #        "shorten?":False,
    #    },
    }

    #end_code = bytes.fromhex('0014') # for inventory item names
    end_code = bytes.fromhex('2564') # for %d variables
    #end_code = bytes.fromhex('0A00') # for general text boxes
    #end_code = bytes.fromhex('0A0015') # more selective but may not include everything
    #end_code = bytes.fromhex('0A001502')
    first_box_offset = 1061803 - 1
    last_box_offset = 2852664

    end_code_2 = bytes.fromhex('FFFF') # change back to 0000 when done
    first_box_offset_2 = 1993136
    last_box_offset_2 = 1998400

    prev_box = first_box_offset
    num_boxes = 0
    total_chars = 0

    while True:

        this_box = ""
        box_end = input_data.find(end_code, prev_box+1, last_box_offset)

        not_found = -1
        if box_end == not_found:

            if end_code == end_code_2:
                break

            # move to options check location & search there
            prev_box = first_box_offset_2 - 1
            end_code = end_code_2
            last_box_offset = last_box_offset_2
            continue

        box_index = box_end
        customized = False

        while True:

            char_code = input_data[box_index-2:box_index]
            valid, type = isValidMoji(char_code)

            if not valid:
                prev_box = box_end
                break

            elif type == 'newline':
                box_index -= 1
                this_box = "\n" + this_box
                continue
            
            elif type == 'customized':
                this_box = "##" + this_box #uncomment when customized is fixed
                customized = True

            else:
                try:
                    this_box = decode(char_code, "shiftjis") + this_box
                except UnicodeDecodeError:
                    this_box = "##" + this_box
                    customized = True

            box_index -= 2

        if len(this_box) == 0:
            continue

        try:
            script_json[num_boxes] = {
                "end_offset":box_end,
                "orig":this_box,
                "orig_len":box_end - box_index,
                "custom?":customized,
                "tran": None, #"Tokyo... Its the big city,\nhuh? Back home was all grass\nand cows, so it was pretty lax.",
                "tran_len":None,
                "shorten?":None,
            }
        except IndexError:
            print("First char_code of box",num_boxes,":",char_code,"at offset",box_end)

        total_chars += len(this_box)
        num_boxes += 1

        #break

    print('Total chars in orig:', total_chars)

    with open('missed_script2.json','w') as file:
        json.dump(script_json, file, ensure_ascii=False, indent=2)

if __name__ == "__main__":

    extractScript()