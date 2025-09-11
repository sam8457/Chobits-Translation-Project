#!/usr/bin/env python3

def intToBits(byte):
    bit_string = bin(byte)[2:].zfill(8)
    return bit_string

def bitsToInt(bits):
    integer = int(bits, 2)
    return integer

def decompress(compressed_data):
    decompressed_data = b""

    compressed_pointer = 0
    data_size = len(compressed_data)

    while compressed_pointer < data_size:

        first_byte = compressed_data[compressed_pointer]
        first_8_bits = intToBits(first_byte)

        first_bit = first_8_bits[0]

        if first_bit == "0":

            compressed_pointer += 1

            length = first_byte + 1
            literal_chunk = compressed_data[compressed_pointer:compressed_pointer + length]

            decompressed_data += literal_chunk
            
            compressed_pointer += length

        else: # first_bit == "1": 

            second_8_bits = intToBits(compressed_data[compressed_pointer + 1])
            first_16_bits = first_8_bits + second_8_bits

            minimum_bytes_copied = 3 # wouldn't save space to substutute < 3 bytes
            length = bitsToInt(first_16_bits[1:6]) + minimum_bytes_copied
            location = bitsToInt(first_16_bits[6:]) + 1

            for i in range(length):

                uncompressed_pointer = len(decompressed_data) - location

                copied_byte = decompressed_data[uncompressed_pointer:uncompressed_pointer+1]
                decompressed_data += copied_byte

            compressed_pointer += 2

    return(decompressed_data)

if __name__ == "__main__":
    compressed_sample=bytes.fromhex("0754494D3204000100940004702C010040840D80071530001000000103048002F0007FBD4229E6FF07206002")
    correct_decompressed_sample=bytes.fromhex("54494D32040001000000000000000000702C010040000000002C010030001000000103048002F0007FBD4229E6FF07206002")

    decompressed_data = decompress(compressed_sample)

    print(decompressed_data.hex())
    print(correct_decompressed_sample.hex())
    print(decompressed_data == correct_decompressed_sample)


'''
decompressor:
    Create empty output data variable
    Determine whether we are reading a 1-byte or 2-byte instruction
        If first bit is on, its a 2-byte instruction, else its 1-bit
    If 1-byte instruction:
        Add the indicated number of bytes to the output data variable
    If 2-byte instruction:
        Ignore first bit
        Take the next 5 bits--this is the number of bytes to copy from the decompressed stream
        Take the final 10 bits, this is how far back to look from the end of the decompressed stream for the desired bits    
        Copy to the output data variable
            Do it byte-by-byte, since you can actually copy previously copied bits for a single instruction

Todo:
    *Locate TIM2 image(s) in file
        Search for TIM2 header
        Identify when TIM2 image ends
    *Extract data from file
    *Output to decompressed files
        Name according to input file and order (ex: A002_001.tm2)
'''