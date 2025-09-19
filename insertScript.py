#!/usr/bin/env python3


from pprint import pprint
import json


def encode(text_unadj, length):

    print(length)
    text = text_unadj.replace( "\n","*")
    print(len(text))
    space_left = length - len(text)
    print(space_left)
    text = text + (" " * space_left)
    print(len(text))
    

    encoding_file = open('doubleShift-RIS.csv','r')
    encoding_data = encoding_file.read()
    encoding_lines = encoding_data.split("\n")

    encoding_dict = {
        "\n":'0A'
    }

    # todo: figure out what to do if fed a newline char in the middle of a two-byte moji
    # alternatively, remember to have all /n characters end on even columns
    # use Migu 2M font to line japanese and roman text up for better editing

    for line in encoding_lines:

        code, moji = line.split(",")
        moji = moji.replace( "、",",") # Commas are coded in japanese to be compatible with .csv file
        encoding_dict[moji] = code[2:] 

    text_data = b''

    i = 0
    while i < len(text):

        char1 = text[i]

        if char1 == '*':
            text_data += bytes.fromhex('0A')
            i += 1
            continue

        try:
            char2 = text[i+1]
        except IndexError:
            char2 = " "
            #break

        moji = char1 + char2

        # Todo: add more descriptive logging for key errors that occur here
        text_data += bytes.fromhex(encoding_dict[moji])

        i += 2

    return text_data


def insertScript():
    
    orig_file = open('SLPM_652.55.fontmodded', 'rb')
    input_data = orig_file.read()
    out_data = input_data
    orig_file.close()

    tran_file = open('tran_script.json','r')
    tran_data = json.loads(tran_file.read())
   
    for box_num, box_data in tran_data.items():

        if len(box_data["tran"]) == 0:
            continue

        #if box_data["custom?"] == True:
        #    continue

        end = box_data["end_offset"]
        length = box_data["orig_len"]
        start = end - length #+ 2 # add one ??????????????????????

        new_box_text = box_data["tran"]
        new_box_data = encode(new_box_text, length)

        prefix = out_data[:start]
        old_box_data = out_data[start:end]
        suffix = out_data[end:]

        print("json:")
        pprint(box_data)

        print("New hex:")
        print(new_box_data.hex())

        print("Old hex:")
        print(old_box_data.hex())
        print()

        out_data = prefix + new_box_data + suffix

    output_file = open('SLPM_652.55', 'wb')
    output_file.write(out_data)
    output_file.close()

    print("Old len: ", len(input_data))
    print("New len: ", len(out_data))

from insertFont import insertFont
insertFont()
#from extractScript import extractScript
#extractScript()
insertScript()
