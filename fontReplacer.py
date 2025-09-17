
from pprint import pprint
from tim2CompTools import *



    


def dataToList(font_data_unadj):

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

        bpp = 4 # bits per pixel
        second_pix = bitsToInt(first_8_bits[bpp:]) # consider swapping the side of bpp if text comes out garbled
        first_pix = bitsToInt(second_8_bits[:bpp])

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


def listToData(moji_list):

    # Todo: Fix offset for this one to match the other function

    light_values = " .cO8#$Bg0MNWQ%&@"

    data = b''

    for moji in moji_list:

        for row in moji:

            for c in range(0, len(row),2):

                char_1 = row[c]
                char_2 = row[c+1]

                second_4_bits = intToBits(light_values.find(char_1))[4:]
                first_4_bits = intToBits(light_values.find(char_2))[4:]

                two_pixels = bitsToInt(first_4_bits + second_4_bits)

                data += intToByte(two_pixels)

    return data


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

    base_offset = int("6932F", 16)

    first_byte = moji_code[:2]
    second_byte = moji_code[2:]
    moji_index = int(range_offsets[first_byte], 16) + int(second_byte, 16)

    moji_len = 144

    final_offset = base_offset + moji_index * moji_len

    return final_offset


def stitchMojis(moji_1, moji_2):

    newMoji = []

    moji_height = 12
    for row in range(moji_height):

        new_row = moji_1[row] + moji_2[row]

        newMoji.append(new_row)

    return newMoji
        

if __name__ == "__main__":

    input_file = open('SLPM_652.55.original', 'rb')
    input_data = input_file.read()
    input_file.close()

    offset = codeToOffset("81f1")
    font_data = getMojisData(input_data,offset,1)
    pprint(dataToList(font_data))
    
    A_list = dataToList(font_data)
    A_data = listToData(A_list)

    pprint(dataToList(A_data))

    print("Passess sanity check:", font_data == A_data)

    #from alphabet import alphabet
    #AB = stitchMojis(alphabet[0], alphabet[1])
    #pprint(AB)

    #prefix = input_data[:start_addr]
    #font_data = input_data[start_addr:end_addr]
    #font_data = b'\x55' * bytes_per_char
    #suffix = input_data[end_addr:]

    #vizualiseFont(font_data)

    #output_data = prefix + font_data + suffix

    #output_file = open('SLPM_652.55', 'wb')
    #output_file.write(output_data)
    #output_file.close()