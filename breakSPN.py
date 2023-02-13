from SPN import appSbox


def GenerateTable() -> list:
    """Create a table like Table 7"""
    # we will have a table of 16 input difference to 16 output difference
    table = [[0]*16]*16

    for xOne in range(0, 16):
        yOne = appSbox(str(xOne))

        for dx in range(1, 16):
            xTwo = xOne ^ dx
            yTwo = appSbox(str(xTwo))

            dy = int(yOne, 16) ^ int(yTwo, 16)
            table[dx][dy] += 1

    return table


def ReduceTable(table: list) -> list:
    """Remove every occurrence that is lower than our lowest probability choice"""
    newTable = []

    # what we are doing here are calculating the probability that given an input difference, example 1, what
    # is the probability of a output difference of 3. Which happens 2/16 times aka 1/8. We will remove every
    # probability that is too low

    for dx in range(16):
        for dy in range(16):
            probability = table[dx][dy]/16

            if probability >= 0.1:
                newTable.append([dx, dy, probability])

    return newTable


def DestBox(sbox, y):

    permuted = permutation



    reachedSbox = []



    for sbox in range(1, 5):

        for bit in range(16):





    # pass 'y' through the permutation

    offset = (NUM_SBOXES - (num_sbox-1) - 1) * SBOX_BITS

    Y = y << offset

    # do_pbox is supposed to transpose the state, make sure is well defined!

    permuted = do_pbox(Y)



    sboxes_reached = {}

    # sboxes go from 1 to NUM_SBOXES from left to right

    # bits go from 1 to SBOX_BITS from left to right

    for sbox in range(1, NUM_SBOXES + 1):

        for bit in range(SBOX_BITS):

            bits_offset = ((NUM_SBOXES - (sbox-1) - 1) * SBOX_BITS) + bit

            # if 'sbox' has a 1 in the position 'bit' then take note of that

            if permuted & (1 << bits_offset) != 0:

                if sbox not in sboxes_reached:

                    sboxes_reached[sbox] = []

                sboxes_reached[sbox].append(SBOX_BITS - bit)

    # return which sboxes where reached and in which bit

    return sboxes_reached


