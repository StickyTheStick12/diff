from SPN import appSbox
from SPN import appPerm


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


def CreateDiffChar(table: list, states:list=None,  depth=1) -> list:
    """Create figure 5"""
    if depth == 1:
        states = []
        for x, y, prob in table:
            for i in range(1, 5):
                reachedSbox = DestBox(i, y)
                entry = {}
                entry["start"] = [depth, i]
                entry["probability"] = [[x, y, prob]]
                entry["state"] = reachedSbox

                states.append(entry)

        return CreateDiffChar(table, states, depth+1)
    else:




def get_diff_characteristics(diff_chr_table, current_states:list=None, depth=1) -> list:

    # run for NUM_ROUNDS - 1 times
    if depth == NUM_ROUNDS:
        # delete elements that involve more than MAX_BLOCKS_TO_BF final sboxes
        current_states = [elem for elem in current_states if len(elem['state']) <= MAX_BLOCKS_TO_BF]

        # return the differential characteristics that reach to no more than MAX_BLOCKS_TO_BF sboxes
        return current_states

    else:
        # for each set of possible states it will do the following:
        #   for each sbox that we last reached,
        #   it will calculate all possible moves according to the bias table.
        #   then it will calculate all possible the combinations of choices
        # this set of combinations, will be our next 'current_states'
        # lastly, it will call itself recursevely
        next_states = []
        for current_state in current_states:

            curr_pos = current_state['state']

            # calculate all possible moves from 'curr_sbox'
            total_combinations = 1
            start_sboxes = {}
            possible_step_per_sbox = {}
            num_possible_step_per_sbox = {}
            num_start_sboxes = 0
            for curr_sbox in curr_pos:

                inputs  = curr_pos[curr_sbox]
                Y_input = bits_to_num(inputs)

                possible_steps = []

                # only use the biases which input matches the current sbox
                possible_biases = [ elem for elem in diff_chr_table if elem[0] == Y_input ]
                for x, y, bias in possible_biases:

                    sboxes_reached = get_destination(curr_sbox, y)

                    step = {'to': sboxes_reached, 'path': [x, y, bias]}

                    possible_steps.append(step)


                if len(possible_steps) > 0:
                    total_combinations *= len(possible_steps)
                    possible_step_per_sbox[curr_sbox] = possible_steps
                    start_sboxes[num_start_sboxes] = curr_sbox
                    num_possible_step_per_sbox[curr_sbox] = len(possible_steps)
                    num_start_sboxes += 1

            if total_combinations == 0:
                continue

            # combine all the possible choises of each sbox in all possible ways
            # for example, if there are 2 sboxes and each has 4 possible moves
            # then calculate all 16 (4x4) possible combinations.


            possible_steps_combinations = []

            for comb_num in range(total_combinations):
                new_comb = []
                new_comb.append( possible_step_per_sbox[start_sboxes[0]][comb_num % num_possible_step_per_sbox[start_sboxes[0]]] )
                for sbox in start_sboxes:
                    if sbox == 0:
                        continue
                    real_sbox = start_sboxes[sbox]

                    mod = 1
                    for prev_sbox in range(sbox):
                        mod *= num_possible_step_per_sbox[start_sboxes[prev_sbox]]

                    index = (comb_num / mod) % num_possible_step_per_sbox[real_sbox]
                    index = int(index)

                    new_comb.append( possible_step_per_sbox[real_sbox][index] )
                possible_steps_combinations.append(new_comb)


            # now, for each combination, check to which sboxes we reached and what are their inputs
            # this will be the next state
            for possible_step in possible_steps_combinations:

                # save the first sbox and the previous biases
                entry = {}
                entry['start'] = current_state['start']
                entry['probabilities'] = current_state['probabilities'].copy()
                entry['state'] = {}

                # add the new biases
                for elem in possible_step:
                    entry['probabilities'].append( elem['path'] )

                    # add the final sboxes and their inputs
                    for destination in elem['to']:
                        if destination not in entry['state']:
                            entry['state'][destination] = []

                        new_bits = elem['to'][destination]
                        entry['state'][destination] += new_bits


                # calculate the resulting Probability
                biases = entry['probabilities']
                resulting_bias = 1
                for _, _, bias in biases:
                    resulting_bias *= bias
                resulting_bias *= 100
                if resulting_bias >= MIN_PROB:
                    # update the next_states
                    next_states.append( entry )


        return get_diff_characteristics(diff_chr_table, next_states, depth + 1)



def DestBox(sbox, y):
    """calculates which sbox will be reached given an output of a sbox and a diff y"""

    # what this does is that if we have an input difference of example 1. And
    # we want to check in the sbox to the left, aka the leftmost, we will convert 1
    # to 1000000000000 which will give us a one on that particular sbox. When we
    # then want a one on the second we will get 100000000 and third 10000 and the last
    # 0001

    #transform our y so 1 in sbox 1 becomes 1000000000000 and 1 in sbox 4 becomes 1
    offset = (3 - (sbox-1)) * 4

    Y = y << offset

    perm = appPerm(Y)
    reachedSbox = {}

    # we want to find every non zero bit in perm.
    for s in range(1, 5):
        for bit in range(4):
            offsetBit = ((3 - (s - 1)) * 4) + bit

            if perm & (1 << offsetBit) != 0:
                if not sbox in reachedSbox:
                    reachedSbox[sbox] = []

                reachedSbox[sbox].append(4-bit)

    return reachedSbox


def Analyze():
    """"""
    #analyze sbox
    table = GenerateTable()
    table = ReduceTable(table)

    # analize the sbox and create the bias table
    table_sorted = sorted(table, key=lambda elem: fabs(elem[2]), reverse=True)


    #calcualte differential characteristics



    # calculate all possible differential characteristics
    diff_characteristics = get_diff_characteristics(table_sorted)
    print(diff_characteristics)
    # sort the list from the best approximations to the worst
    diff_characteristics_sorted = sort_diff_characteristics(diff_characteristics)
    # return the sorted list of approximations
    return diff_characteristics_sorted
