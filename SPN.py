import binascii
import os

sbox = {0: 0xE, 1: 0x4, 2: 0xD, 3: 0x1, 4: 0x2, 5: 0xF, 6: 0xB, 7: 0x8, 8: 0x3, 9: 0xA, 0xA: 0x6, 0xB: 0xC,
        0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7}

sboxInverse = {0xE: 0, 0x4: 1, 0xD: 2, 0x1: 3, 0x2: 4, 0xF: 5, 0xB: 6, 0x8: 7, 0x3: 8, 0xA: 9, 0x6: 0xA, 0xC: 0xB,
               0x5: 0xC, 0x9: 0xD, 0x0: 0xE, 0x7: 0xF}

perm = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]


def Keygen(p=False) -> bytes:
    """Generate a bytes string containing our 5 keys"""
    key = binascii.b2a_hex(os.urandom(10))

    if p:
        for i in range(5):
            print(f"key{i} = {str(key)[2:][i*4:i*4+4]}")
    return key


def ApplySbox(bits: int, p=False) -> int:
    """Convert decimal to hex and apply the sbox part"""
    # Convert int(binary) to groups of 4 and convert to an int
    bitParts = [(bits & (0x000f << i)) >> i for i in range(0, 16, 4)]

    for index, value in enumerate(bitParts):
        bitParts[index] = sbox[value]

    value = 0
    for i in range(0, 16, 4):
        value += (bitParts[i//4] << i)

    if p:
        print(value)

    return value


def InverseSbox(bits: int, p=False) -> int:
    """Convert decimal to hex and inverse the sbox"""
    # Convert int(binary) to groups of 4 and convert to an int
    bitParts = [(bits & (0x000f << i)) >> i for i in range(0, 16, 4)]

    for index, value in enumerate(bitParts):
        bitParts[index] = sboxInverse[value]

    value = 0
    for i in range(0, 16, 4):
        value += (bitParts[i // 4] << i)

    if p:
        print(value)

    return value


def AppPermutation(bits: int) -> int:
    """Given a decimal number apply permutation to it"""
    temp = 0

    for index in range(16):
        # check if the digit on index i is non-zero, applying permutation to zero doesnt do anything
        if bits & (1 << index) != 0:
            temp += 1 << perm[index]

    return temp


def Encrypt(text: int, key: bytes, verbose=False) -> int:
    """Encrypt an int given a key"""
    if verbose:
        print(f"encrypting this: {text}")

    # split the keys to 5 separate keys
    subKeys = [int(key[i*4:i*4+4], 16) for i in range(5)]

    for round in range(0, 3):
        if verbose:
            print(f"round {round}", end="")

        text = text ^ subKeys[round]

        if verbose:
            print(f", {hex(text)}", end="")

        text = ApplySbox(text)

        if verbose:
            print(f", {hex(text)}", end="")

        text = AppPermutation(text)

        if verbose:
            print(f", {hex(text)}")

    text = text ^ subKeys[-2]

    if verbose:
        print(f"round 3 {hex(text)}")

    text = ApplySbox(text)

    if verbose:
        print(f"round 4 {hex(text)}")

    text = text ^ subKeys[-1]
    if verbose:
        print(f"encrypted text: {text}")

    return text
