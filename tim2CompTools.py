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


def decompress(compd_data):

    decompd_data = b""

    compd_ptr = 0
    data_size = len(compd_data)

    while compd_ptr < data_size:

        first_byte = compd_data[compd_ptr]
        first_8_bits = intToBits(first_byte)

        first_bit = first_8_bits[0]

        if first_bit == "0":

            compd_ptr += 1

            min_bytes_copied = 1 # must be at least one literal byte to copy
            length = first_byte + min_bytes_copied

            literal_chunk = compd_data[compd_ptr:compd_ptr + length]
            decompd_data += literal_chunk
            
            compd_ptr += length

        else: # first_bit == "1": 

            if len(compd_data) - compd_ptr < 2: # added to protect index out of range error
                # Todo: figure out what to do with this last byte
                # decompd_data += intToByte(compd_data) # causes crashes
                ## May be because the first of the '00 00 00 00...' bits is actually the copy location?
                    # Consider setting second_8_bits to 00 in this event, otherwise do the code below
                break
            second_8_bits = intToBits(compd_data[compd_ptr + 1])
            first_16_bits = first_8_bits + second_8_bits

            min_bytes_copied = 3 # wouldn't save space to substutute < 3 bytes
            length = bitsToInt(first_16_bits[1:6]) + min_bytes_copied
            location = bitsToInt(first_16_bits[6:]) + 1

            for b in range(length): # must be done per-byte to allow copying from the decomp stream

                uncompd_ptr = len(decompd_data) - location

                copied_byte = decompd_data[uncompd_ptr:uncompd_ptr+1]
                decompd_data += copied_byte

            compd_ptr += 2

    return decompd_data


def compressBadly(uncompd_data):
    """
    While I know how the decompression algorithm works, I don't know how the
    compression algorithm works to find redundancies. The easy answer is to
    only use 1-byte instructs to code for literals, which is all this
    function does.

    I may work on finding a way to re-compress them later, but for now, this will 
    allow testing to progress.
    """

    max_literal = 128 # must be <=128 since length instructs start at 00000 = 1 and are 5 bits

    compd_data = b''

    uncompd_ptr = 0
    data_size = len(uncompd_data)

    remaining_data_size = data_size - uncompd_ptr

    while (remaining_data_size > 0):

        if remaining_data_size < max_literal:

            min_bytes_copied = 1
            one_byte_instruct = intToByte(remaining_data_size - min_bytes_copied)
            compd_data += one_byte_instruct

            literal_chunk = uncompd_data[uncompd_ptr:]
            compd_data += literal_chunk

            uncompd_ptr += remaining_data_size

        else:

            min_bytes_copied = 1 # must be at least one literal byte to copy
            one_byte_instruct = intToByte(max_literal - min_bytes_copied)
            compd_data += one_byte_instruct

            literal_chunk = uncompd_data[uncompd_ptr:uncompd_ptr + max_literal]
            compd_data += literal_chunk

            uncompd_ptr += max_literal

        remaining_data_size = data_size - uncompd_ptr
    
    return compd_data


if __name__ == "__main__":
    compd_sample=bytes.fromhex("0754494D3204000100940004702C010040840D80071530001000000103048002F0007FBD4229E6FF07206002")
    #badly_compd_sample=bytes.fromhex("3254494D32040001000000000000000000702C010040000000002C010030001000000103048002F0007FBD4229E6FF07206002")
    correct_decompd_sample=bytes.fromhex("54494D32040001000000000000000000702C010040000000002C010030001000000103048002F0007FBD4229E6FF07206002")

    decompd_data = decompress(compd_sample)
    recompd_data = compressBadly(decompd_data)
    twice_decompd_data = decompress(recompd_data)

    print("Correct:",correct_decompd_sample.hex())
    print(" Actual:",twice_decompd_data.hex())
    print("Passes sanity check:", correct_decompd_sample == twice_decompd_data)
