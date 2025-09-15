# int(value, 16) # convert hex to int
# hex(value) # convert int to hex

import tim2CompTools


def vizualiseFont(font_data, max_len=float("inf")):

    # values range from 0 to 15
    light_values = " .cO8#$Bg0MNWQ%&@"
    # _.c08#
    # commonly only 0 thru 6

    width = 24
    height = 12

    x = 0
    y = 0

    for byte in font_data:

        bits = tim2CompTools.intToBits(byte)

        bits_per_pix = 4
        first_pix = tim2CompTools.bitsToInt(bits[:bits_per_pix])
        second_pix = tim2CompTools.bitsToInt(bits[bits_per_pix:])

        print(light_values[first_pix], end="")
        print(light_values[second_pix], end="")

        x += 2

        if x == width:

            x = 0
            y += 1

            print("|")

            if y % height == 0:
                print("------------------------")

            if y == max_len:
                break


if __name__ == "__main__":

    input_file = open('SLPM_652.55.original', 'rb')
    input_data = input_file.read()
    input_file.close()

    bytes_per_char = 144

    start_addr = int("708B4",16) # extra line above
    #start_addr = int("708C0",16) # extra line below
    end_addr = start_addr + bytes_per_char #* 26
    #end_addr = int("ED600",16)

    prefix = input_data[:start_addr]
    #font_data = input_data[start_addr:end_addr]
    font_data = b'\x55' * bytes_per_char
    suffix = input_data[end_addr:]

    #vizualiseFont(font_data)

    output_data = prefix + font_data + suffix

    output_file = open('SLPM_652.55', 'wb')
    output_file.write(output_data)
    output_file.close()