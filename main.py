def num_to_bits(num):
    bits = []
    for index in range(4):
        if (1 << index) & num > 0:
            bits.append( 4 - index )
    return bits

print(num_to_bits(123))