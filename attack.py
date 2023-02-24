from SPN import InverseSbox
from SPN import ApplySbox
from SPN import AppPermutation

def GenerateTable() -> list:
    """Create a table like Table 7"""
    # we will have a table of 16 input difference to 16 output difference
    table = [[0]*16]*16

    for xOne in range(0, 16):
        yOne = ApplySbox(xOne)

        for dx in range(1, 16):
            xTwo = xOne ^ dx
            yTwo = ApplySbox(xTwo)

            dy = yOne ^ yTwo
            table[dx][dy] += 1

    return table


def DestinationSbox(sbox, y) -> dict:
    """calculates which sbox will be reached given an output of a sbox and a diff y"""

    # what this does is that if we have an input difference of example 1. And
    # we want to check in the sbox to the left, aka the leftmost, we will convert 1
    # to 1000000000000 which will give us a one on that particular sbox. When we
    # then want a one on the second we will get 100000000 and third 10000 and the last
    # 0001

    # transform our y so 1 in sbox 1 becomes 1000000000000 and 1 in sbox 4 becomes 1
    offset = (3 - (sbox - 1)) * 4

    Y = y << offset

    # as we stated in the text. Addubg a roundkey wont impact the differntial.

    perm = AppPermutation(Y)
    reachedSbox = {}

    # we want to find every non zero bit in perm.
    for s in range(1, 5):
        for bit in range(4):
            offsetBit = ((3 - (s - 1)) * 4) + bit

            if perm & (1 << offsetBit) != 0:
                if not sbox in reachedSbox:
                    reachedSbox[sbox] = []

                reachedSbox[sbox].append(4 - bit)

    return reachedSbox


def AnalyzeSbox():
    """Generate the characteristics for the crypto"""
    table = GenerateTable()


def GetHits(cPairs: list, characteristic: dict) -> list:
    """Generate all possible keys and check if they satisfy the characteristic"""

    hits = [0] * pow(16, 2) # we have 16 values for part 1 and 16 values for part 2 of the key

    for key in range(pow(16, 2)):
        for cOne, cTwo in cPairs:
            if GetDiff(cOne, cTwo, key, characteristic) == 0:
                hits[key] += 1

    return hits


def GetDiff(cipherOne: int, cipherTwo: int, key: int, characteristic: dict) -> int:
    """implementation of 4.4"""
    diffTotal = 0
    i = 1

    for block in characteristic:
        # get the corresponding block of the cipher
        cipherO = cipherOne >> ((4 - block) * 4)
        cipherO = cipherO & ((1 << 4) - 1)

        cipherT = cipherTwo >> ((4 - block) * 4)
        cipherT = cipherT & ((1 << 4) - 1)

        # split the key
        k = (key & (0x0f << (4 * i))) >> (4 * i)

        # remove the key
        vOne = cipherO ^ k
        vTwo = cipherT ^ k

        uOne = InverseSbox(vOne)
        uTwo = InverseSbox(vTwo)

        diffTotal += uOne ^ uTwo ^ 5 # 5 is the expected bits aka 1001

        i -= 1

    return diffTotal
