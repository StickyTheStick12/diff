offset = (3 - (1 - 1)) * 4

y = 4

Y = y << offset

print(bin(Y))

for sbox in range(1, 5):
    for bit in range(4):
        bits_offset = ((4 - (sbox-1) - 1) * 4) + bit
        # if 'sbox' has a 1 in the position 'bit' then take note of that
        print(Y & (1 << bits_offset) != 0)

