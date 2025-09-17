# int(value, 16) # convert hex to int
# hex(value) # convert int to hex

import tim2CompTools
from pprint import pprint


def convertToList(font_data):

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
            second_byte = 0

        first_8_bits = tim2CompTools.intToBits(first_byte)
        second_8_bits = tim2CompTools.intToBits(second_byte)

        bpp = 4 # bits per pixel
        first_pix = tim2CompTools.bitsToInt(first_8_bits[:bpp]) # consider swapping the side of bpp if text comes out garbled
        second_pix = tim2CompTools.bitsToInt(second_8_bits[bpp:])

        #print(moji)
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


def getMojisData(input_data, offset, range_len):

    bytes_per_char = 144

    start_addr = offset
    end_addr = start_addr + bytes_per_char * range_len

    font_data = input_data[start_addr:end_addr]
   
    return font_data


def codeToOffset(moji_code):
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

    #base_offset = int("6B72F", 16)
    base_offset = int("6932F", 16)

    first_byte = moji_code[:2]
    second_byte = moji_code[2:]
    moji_index = int(range_offsets[first_byte], 16) + int(second_byte, 16)

    moji_len = 144

    final_offset = base_offset + moji_index * moji_len

    return final_offset


if __name__ == "__main__":

    input_file = open('SLPM_652.55.original', 'rb')
    input_data = input_file.read()
    input_file.close()

    offset = codeToOffset("8281")
    font_data = getMojisData(input_data,offset,26)
    pprint(convertToList(font_data))

    #prefix = input_data[:start_addr]
    #font_data = input_data[start_addr:end_addr]
    #font_data = b'\x55' * bytes_per_char
    #suffix = input_data[end_addr:]

    #vizualiseFont(font_data)

    #output_data = prefix + font_data + suffix

    #output_file = open('SLPM_652.55', 'wb')
    #output_file.write(output_data)
    #output_file.close()