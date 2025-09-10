


compressed_data="0754494D3204000100940004702C010040840D80071530001000000103048002F0007FBD4229E6FF07206002"
correct_uncompressed_data="54494D32040001000000000000000000702C010040000000002C010030001000000103048002F0007FBD4229E6FF07206002"



'''
main:
    Locate TIM2 image(s) in file
        Search for TIM2 header
        Identify when TIM2 image ends
    Extract data from file
    Decompress data
        Create empty output data variable
        Determine whether we are reading a 1-byte or 2-byte instruction
            So far all the 2-byte instructions seem to have their first bit set to 1, lets go with that for now
        If 1-byte:
            
    Output to decompressed files
        Name according to input file and order (ex: A002_001.tm2)
'''