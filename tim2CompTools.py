#!/usr/bin/env python3

def intToBits(integer):
    bit_string = bin(integer)[2:].zfill(8)
    return bit_string


def bitsToInt(bits):
    integer = int(bits, 2)
    return integer


def intToByte(integer):
    byte = integer.to_bytes(1, byteorder='big')
    return byte


def decompress(compressed_data, logging=False):
    '''
    Decompressor psuedocode
        Create empty output data variable
        Determine whether we are reading a 1-byte or 2-byte instruction
            If first bit is on, its a 2-byte instruction, else its 1-bit
        If 1-byte instruction:
            Add the indicated number of bytes to the output data variable
        If 2-byte instruction:
            First bit is instruction size flag
            Take the next 5 bits--this is the number of bytes to copy from the decompressed stream
            Take the final 10 bits, this is how far back to look from the end of the decompressed stream for the desired bits    
            Copy to the output data variable
                Do it byte-by-byte, since you can actually copy previously copied bits for a single instruction
    '''

    decompressed_data = b""

    compressed_pointer = 0
    data_size = len(compressed_data)

    while compressed_pointer < data_size:

        first_byte = compressed_data[compressed_pointer]
        first_8_bits = intToBits(first_byte)

        first_bit = first_8_bits[0]

        if first_bit == "0":

            compressed_pointer += 1

            min_bytes_copied = 1 # must be at least one literal byte to copy
            length = first_byte + min_bytes_copied
            literal_chunk = compressed_data[compressed_pointer:compressed_pointer + length]

            decompressed_data += literal_chunk
            
            compressed_pointer += length

        else: # first_bit == "1": 

            second_8_bits = intToBits(compressed_data[compressed_pointer + 1])

            first_16_bits = first_8_bits + second_8_bits

            min_bytes_copied = 3 # wouldn't save space to substutute < 3 bytes
            length = bitsToInt(first_16_bits[1:6]) + min_bytes_copied
            location = bitsToInt(first_16_bits[6:]) + 1

            for i in range(length):

                uncompressed_pointer = len(decompressed_data) - location

                copied_byte = decompressed_data[uncompressed_pointer:uncompressed_pointer+1]
                decompressed_data += copied_byte

            compressed_pointer += 2

    return(decompressed_data)


def compressBadly(uncompressed_data):
    """
    While I know how the game decompresses files, I don't necessarily know how the
    compressor searches for redundancies to do the compression in the first place.
    The easy answer is just 'don't compress anything and use only 1-byte commands',
    which is what this function does.

    I may work on finding a way to re-compress them later, but for now, this will 
    allow testing to progress.
    """

    biggest_literal = 128 # must be <=128 since length instructions start at 1 and are 5 bits

    compressed_data = b''

    uncompressed_pointer = 0
    data_size = len(uncompressed_data)

    remaining_data_size = data_size - uncompressed_pointer

    while (remaining_data_size > 0):

        if remaining_data_size < biggest_literal:

            min_bytes_copied = 1 # must be at least one literal byte to copy
            one_byte_instruction = intToByte(remaining_data_size - min_bytes_copied)
            compressed_data += one_byte_instruction

            literal_chunk = uncompressed_data[uncompressed_pointer:]
            compressed_data += literal_chunk

            uncompressed_pointer += remaining_data_size

        else:

            min_bytes_copied = 1 # must be at least one literal byte to copy
            one_byte_instruction = intToByte(biggest_literal - min_bytes_copied)
            compressed_data += one_byte_instruction

            literal_chunk = uncompressed_data[uncompressed_pointer:uncompressed_pointer + biggest_literal]
            compressed_data += literal_chunk

            uncompressed_pointer += biggest_literal

        remaining_data_size = data_size - uncompressed_pointer
    
    return compressed_data


if __name__ == "__main__":
    #compressed_sample=bytes.fromhex("0754494D3204000100940004702C010040840D80071530001000000103048002F0007FBD4229E6FF07206002")
    compressed_sample=bytes.fromhex("3254494D32040001000000000000000000702C010040000000002C010030001000000103048002F0007FBD4229E6FF07206002")
    correct_decompressed_sample=bytes.fromhex("54494D32040001000000000000000000702C010040000000002C010030001000000103048002F0007FBD4229E6FF07206002")

    decompressed_data = decompress(compressed_sample)
    recompressed_data = compressBadly(decompressed_data)
    twice_decompressed_data = decompress(recompressed_data)

    print("Correct:",correct_decompressed_sample.hex())
    print(" Actual:",twice_decompressed_data.hex())
    print("Passes sanity check:", correct_decompressed_sample == twice_decompressed_data)
    # todo: debug why this is false, also gets stuck in infinite loops sometimes
