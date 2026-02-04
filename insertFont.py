#!/usr/bin/env python3


from alphabet import alph, two_byte_alph,yen
from pprint import pprint
from tim2CompTools import *
import itertools


def dataToASCII(font_data_unadj):
    """
    Converts data representation of the font that the SLPM
    file uses to a 2D list containing ASCII art of the font. 

    font_data_unadj -> data from the SLPM file containing
    the game's font.
    """

    font_bits = ""

    for byte in font_data_unadj:

        font_bits += intToBits(byte)

    half_byte_offset = 4
    font_bits = font_bits[half_byte_offset:]
    
    font_data = b''

    for b in range(0, len(font_bits),8):

        byte = intToByte(bitsToInt(font_bits[b:b+8]))

        font_data += byte

    font = []
    moji = [""]

    light_values = " .cO8#$Bg0MNWQ%&@"

    width = 24
    height = 12

    x = 0
    y = 0

    for i, first_byte in enumerate(font_data):

        try:
            second_byte = font_data[i + 1]
        except IndexError:
            # Todo: see if this can be removed somehow
            second_byte = 0

        first_8_bits = intToBits(first_byte)
        second_8_bits = intToBits(second_byte)

        # This might seem backwards but I think the Chobits devs implemented it backwards in the original
        bpp = 4 
        second_pix = bitsToInt(first_8_bits[bpp:])
        first_pix = bitsToInt(second_8_bits[:bpp])

        moji[y] += light_values[first_pix]
        moji[y] += light_values[second_pix]

        x += 2

        if x == width:

            x = 0
            y += 1

            if y % height == 0:

                y = 0

                font.append(moji)
                moji = [""]

            else:

                moji.append("")

    return font


def ASCIItoData(moji_list):
    """
    Converts a list containing ASCII art of mojis to 
    the data representation that the SLPM file uses.

    moji_list -> Two dimmensional list, each element in the
    outer list is one moji, each element in the inner lists
    is a string representing one row of pixels.
    """

    light_values = " .cO8#$Bg0MNWQ%&@"

    data = b'' + intToByte(0)

    for moji in moji_list:

        for row in moji:

            for c in range(0, len(row), 2):

                char_1 = row[c]
                try:
                    char_2 = row[c+1]
                except IndexError:
                    print('Probelm occured with the following moji:')
                    pprint(moji)
                    raise

                second_4_bits = intToBits(light_values.find(char_1))[4:]
                first_4_bits = intToBits(light_values.find(char_2))[4:]

                two_pixels = bitsToInt(first_4_bits + second_4_bits)

                data += intToByte(two_pixels)

    return data[:-1]


def getMojisData(input_data, offset, range_len):

    bytes_per_char = 144

    start_addr = offset
    end_addr = start_addr + bytes_per_char * range_len

    font_data = input_data[start_addr:end_addr]
   
    return font_data


def codeToOffset(moji_code, base_offset = int("6932F", 16)):
    # equivalent of kanjiRomAdrOriginal function in source

    range_offsets = {
        "first_byte":"offset",
        "81":"-40",
        "82":"71",
        "83":"123",
        "84":"1ba",
        "88":"237",
        "89":"2f7",
        "8a":"3b7",
        "8b":"477",
        "8c":"537",
        "8d":"5f7",
        "8e":"6b7",
        "8f":"777",
        "90":"837",
        "91":"8f7",
        "92":"9b7",
        "93":"a77",
        "94":"b37",
        "95":"bf7",
        "96":"cb7",
        "97":"d77",
        "98":"e37"
    }

    first_byte = moji_code[:2]
    second_byte = moji_code[2:]
    moji_index = int(range_offsets[first_byte], 16) + int(second_byte, 16)

    moji_len = 144

    final_offset = base_offset + moji_index * moji_len

    return final_offset


def stitchMojis(moji_1, moji_2):
    '''
    Takes two 12x12 ASCII characters and combines them into
    one 24x12 moji.

    moji_1 -> 1D list with each element a 12-length string
    moji_2 -> 1D list with each element a 12-length string
    '''

    newMoji = []

    moji_height = 12
    for row in range(moji_height):

        new_row = moji_1[row] + moji_2[row]

        newMoji.append(new_row)

    return newMoji
        

def printMojisLabelled(start_moji, length):
    '''
    Use to view mojis and their offset from beginning of
    file in in terminal. Can be copied to the alphabet.py
    file for manual editing.

    start_moji -> String containing sjis code of desired moji
    length -> How many mojis in total to display
    '''

    input_file = open('SLPM_652.55.original', 'rb')
    input_data = input_file.read()
    input_file.close()

    offset = codeToOffset(start_moji)
    font_data = getMojisData(input_data,offset,length)
    font_list = dataToASCII(font_data)

    start_offset = int(start_moji,16)

    for i in range(length):

        sjis_val = hex(start_offset + i)

        print(sjis_val, "(for below char)")
        pprint (font_list[i])


def createReservedTableFile():
    '''
    Creates a CSV with the hex values of all reserved character codes.
    The actual characters still have to be manually filled out.
    '''

    # Consider adding 814A and 814B, would need more space
    reserved_ranges = [
        "824f","82f1",
        "8340","8396",
        "8440","845d",
        "897e","897e",
    ]

    reserved_values = []

    for r in range(0, len(reserved_ranges), 2):

        range_cur = int(reserved_ranges[r],16)
        range_end = int(reserved_ranges[r+1],16)

        while not (range_cur > range_end):

            reserved_values.append(hex(range_cur))

            range_cur += 1

    lines = map(lambda n: n + ",\n", reserved_values)

    output_file = open('reserved.csv', 'w')
    output_file.write("".join(lines))
    output_file.close()


def createUnreservedTableFile():
    '''
    Creates a CSV with the hex values of all unreserved
    character codes. Will automatically fill out with pairs
    of values to be overwritten in SLPM file.

    The char_combos just so happen to be *exactly* the same
    length as the number of values within the
    unreserved_ranges list, so no extra empty lines are
    produced in the .csv file.
    '''

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

    lines = []

    # Consider making l and I the same if low on space
    possible_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz、.?!" '
    char_combos = list(itertools.product(possible_chars, repeat=2))

    char_combos_index = 0

    for r in range(0, len(unreserved_ranges), 2):

        range_cur = int(unreserved_ranges[r],16)
        range_end = int(unreserved_ranges[r+1],16)

        while not (range_cur > range_end):

            try:
                first_char, second_char = char_combos[char_combos_index]
                this_char_combo = first_char + second_char
            except IndexError:
                this_char_combo = ""

            line = hex(range_cur) + "," + this_char_combo + "\n"

            lines.append(line)

            range_cur += 1
            char_combos_index += 1

    output_file = open('unreserved.csv', 'w')
    output_file.write("".join(lines))
    output_file.close()


def insertFont():
    '''
    For each value in the doubleShift-RIS.csv table, inserts
    the corresponding character into the SLPM file. The file
    must be created manually from the outputs of the previous
    two functions.

    doubleShift-RIS.csv -> contains moji_code,character pairs 
        If 2 characters follow the comma, it needs to be stitched from the corresponding font data in alphabet variable
        If 1 character follows the comma, leave the original, unless its ¥, then substitute the data in the yen variable
        If zero characters follow the comma, leave the original
    '''
    
    input_file = open('SLPM_652.55.original', 'rb')
    input_data = input_file.read()
    output_data = input_data
    input_file.close()

    encoding_table = open('doubleShift-RIS.csv','r')
    encoding_data = encoding_table.read()
    encoding_lines = encoding_data.split("\n")
    
    for line in encoding_lines:

        char_code, moji = line.split(",")

        start_addr = codeToOffset(char_code[2:])
        char_len = 144
        end_addr = start_addr + char_len

        prefix = output_data[:start_addr]
        original_data = output_data[start_addr:end_addr]
        suffix = output_data[end_addr:]

        match len(moji):

            case 2:
                first_roman = moji[0]
                second_roman = moji[1]

                if first_roman == "#":

                    moji_list = two_byte_alph[first_roman + second_roman]
                    final_data = ASCIItoData([moji_list])
                    #final_data = original_data
                    #orig_offset = codeToOffset(char_code[2:])
                    #orig_data = getMojisData(input_data, orig_offset, 1)
                    #final_data = orig_data
                    pass # work on, may need to have dedicated files for these

                else:

                    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz、.?!" '

                    index_1 = chars.find(first_roman)
                    index_2 = chars.find(second_roman)

                    moji_list = stitchMojis(alph[index_1], alph[index_2])
                    final_data = ASCIItoData([moji_list])

            case 1:
                if moji == "¥":
                    final_data = ASCIItoData(yen)
                else:
                    final_data = original_data

            case _:
                final_data = original_data
            
        output_data = prefix + final_data + suffix

    output_file = open('SLPM_652.55.fontmodded', 'wb')
    output_file.write(output_data)
    output_file.close()

    print("Out len: ", len(output_data))
    print(" In len: ", len(input_data))


if __name__ == "__main__":

    printMojisLabelled("8194", 1)
    #insertFont() # uncomment to modify game script

