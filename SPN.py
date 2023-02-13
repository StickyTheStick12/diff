import binascii
import os

sbox = {0: 0xE, 1: 0x4, 2: 0xD, 3: 0x1, 4: 0x2, 5: 0xF, 6: 0xB, 7: 0x8, 8: 0x3, 9: 0xA, 0xA: 0x6, 0xB: 0xC,
        0xD: 0x9, 0xE: 0x0, 0xF: 0x7}

sboxInverse = {0xE: 0, 0x4: 1, 0xD: 2, 0x1: 3, 0x2: 4, 0xF: 5, 0xB: 6, 0x8: 7, 0x3: 8, 0xA: 9, 0x6: 0xA, 0xC: 0xB,
               0x5: 0xC, 0x9: 0xD, 0x0: 0xE, 0x7: 0xF}

perm = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]


def keygen(p=False) -> str:
    key = str(binascii.b2a_hex(os.urandom(10)))

    if p:
        for i in range(5):
            print(f"key{i} = {key[i*4:i*4+4]}")

    return key


def appSbox(bits: str, p=False) -> str:
    s = ""

    for i in range(4):
        s += sbox[int(bits[i*4: i*4+4], 16)]

    if p:
        print(s)

    return s


def appPerm(bits: str) -> str:
    newBits = [None] * 16

    for i in range(16):
        newBits[perm[i]] = bits[i]

    return "".join(newBits)


def encrypt(text: str, key: str, verbose=False) -> int:
    if verbose:
        temp = text
        print(f"encrypting this: {int(text, 16)}")
        subKeys = [int(key[i*4:i*4+4], 16) for i in range(5)]

        for round in range(0, 3):
            if verbose:
                print(f"roundnumber {round}", end=" ")

            temp = temp ^ subKeys[round]

            if verbose:
                print(f", {temp}", end=" ")

            temp = int(appSbox(str(temp)), 16)

            if verbose:
                print(f", {temp}", end=" ")

            appPerm(str(temp))

            if verbose:
                print(f", {temp}")

        temp = int(temp, 16) ^ subKeys[-2]

        if verbose:
            print(f"roundnumber 3 {temp}", end=" ")

        temp = appSbox(str(temp))

        if verbose:
            print(f", {temp}")

        temp = int(temp, 16) ^ subKeys[-1]
        print(temp)

        return temp
