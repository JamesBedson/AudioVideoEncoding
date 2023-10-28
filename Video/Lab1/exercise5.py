# Ex 5 =======================================================================
'''
Create a method which applies a run-length
encoding from a series of bytes given.
'''

def create_run_length_encoding(data_in_bytes: bytes) -> bytes:
    
    run_length_coding = [] 
    count = 1
    
    for idx in range(1, len(data_in_bytes)):
        if data_in_bytes[idx] == data_in_bytes[idx - 1]:
            count += 1
        else:
            run_length_coding.extend([data_in_bytes[idx - 1], count])
            count = 1

    run_length_coding.extend([count, data_in_bytes[-1]])
    return bytes(run_length_coding)


def create_run_length_zeros_only(data_in_bytes: bytes) -> bytes:
    run_length_coding = [] 
    count = 1
    
    for idx in range(1, len(data_in_bytes)):
        
        if data_in_bytes[idx] == data_in_bytes[idx - 1] and data_in_bytes[idx] == 0:
            count += 1
        else:
            if (data_in_bytes[idx - 1] == 0):
                print("Zero detected")
                run_length_coding.extend([data_in_bytes[idx - 1], count])
            else:
                run_length_coding.extend([data_in_bytes[idx - 1]])
            count = 1

    if (data_in_bytes[-1] == 0):
        run_length_coding.extend([data_in_bytes[-1], count])
    else:
        run_length_coding.extend([data_in_bytes[-1]])
        
    return bytes(run_length_coding)


def ex5():

    byte_sequence       = b'\x01\x01\x01\xFA\xB1\xBA\xBA\xBA\x02\x01\x01'
    byte_sequence_enc   = create_run_length_encoding(byte_sequence)

    byte_sequence_zeros = b'\x01\x01\x01\x00\x00\x00\x00\xAB\xBA\x00'
    zeros_enc           = create_run_length_zeros_only(byte_sequence_zeros)

    print(f"Original Sequence: {byte_sequence}")
    print(f"Encoded Sequence: {byte_sequence_enc}")

    print(f"Original Sequence (zeros): {byte_sequence_zeros}")
    print(f"Encoded Sequence (zeros): {zeros_enc}")