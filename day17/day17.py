TESTING = False

def printChamber(chamber):
    for row_num in range(len(chamber) - 1, -1, -1):
        print(f"#{chamber[row_num]:07b}#")

    print("#########")

def moveSideways(block, block_bottom, jet_direction, chamber):
    block_height = len(block)
    moved_block = block.copy()

    if jet_direction == "<":
        for block_row in range(0, block_height):
            if block[block_row] & 0b1000000:
                return block

            moved_block[block_row] <<= 1

            if moved_block[block_row] & chamber[block_bottom + block_row]:
                return block
    else:
        for block_row in range(0, block_height):
            if moved_block[block_row] & 0b0000001:
                return block

            moved_block[block_row] >>= 1

            if moved_block[block_row] & chamber[block_bottom + block_row]:
                return block

    return moved_block

def checkIfLanded(block, block_bottom, block_height, new_chamber):
    for block_row in range(0, block_height):
        if block[block_row] & new_chamber[block_bottom + block_row - 1]:
            return True

    return False

def add_block(turn_num, pile_height, chamber, jets, jet_num):
    blocks = [[0b0011110],
              [0b0001000, 0b0011100, 0b0001000],
              [0b0011100, 0b0000100, 0b0000100],
              [0b0010000, 0b0010000, 0b0010000, 0b0010000],
              [0b0011000, 0b0011000]]

    for empty_row in range(len(chamber), pile_height + 9):
        chamber.append(0b0000000)

    block_num = turn_num % len(blocks)
    block = blocks[block_num]
    block_height = len(block)
    block_bottom = pile_height + 4

    while True:
        jet_direction = jets[jet_num]
        block = moveSideways(block, block_bottom, jet_direction, chamber)
        jet_num = (jet_num + 1) % len(jets)

        if checkIfLanded(block, block_bottom, block_height, chamber):
            break

        block_bottom -= 1

    for block_row in range(0, block_height):
        chamber[block_bottom + block_row] = \
            chamber[block_bottom + block_row] | block[block_row]

    pile_height = max(pile_height, block_bottom + block_height - 1)

    # printChamber(chamber)
    # print()

    return chamber, pile_height, jet_num


def part1():
    file.seek(0)
    jets = file.readline().rstrip()

    chamber = [0b1111111]   #Note that my floor occupies chamber[0]
    pile_height = jet_num = 0

    for turn_num in range(0, 2022):
        chamber, pile_height, jet_num = add_block(turn_num, pile_height, chamber, jets, jet_num)

    return pile_height

def find_cycle(turn_num, pile_height, jet_num, stats):
    block_num = turn_num % 5  #5 block types

    if (block_num, jet_num) in stats:
        previous_pile_heights_and_turns = stats.get((block_num, jet_num))

        previous_pile_heights_and_turns.append((pile_height, turn_num))

        diffs = []

        # We want to be sure, so need to see the same cycle ten times in a row to be convinced
        if len(previous_pile_heights_and_turns) == 10:
            for record_num in range(0, 9):
                this_record = previous_pile_heights_and_turns[record_num]
                next_record = previous_pile_heights_and_turns[record_num + 1]

                diffs.append((next_record[0] - this_record[0],
                              next_record[1] - this_record[1]))

            height_diff = diffs[0][0]
            turn_diff = diffs[0][1]

            for record_num in range(0, 9):
                if not ((diffs[record_num][0] == height_diff) and (diffs[record_num][1] == turn_diff)):
                    break

                # -1 needed as this calculation would otherwise give us the first blank line above the pile
                total_height = pile_height + ((1000000000000 - turn_num) // turn_diff) * height_diff - 1
                leftover = (1000000000000 - turn_num) % turn_diff

                if leftover == 0:
                    print("Part2:")
                    print(f"Cycle found: Block {block_num} occurs at intervals of {height_diff} blocks and {turn_diff} turns from {previous_pile_heights_and_turns[0]} onwards")
                    print(f"Total height should be {total_height} with {leftover} blocks left over")
                    exit(0)
    else:
        stats.update({(block_num, jet_num): [(pile_height, turn_num)]})

def part2():
    file.seek(0)
    jets = file.readline().rstrip()
    num_jets = len(jets)

    chamber = [0b1111111]   #Note that my floor occupies chamber[0]
    pile_height = jet_num = 0

    stats = {}

    for turn_num in range(0, 1000000): #If we don't find a cycle after this many turns, give up!
        chamber, pile_height, jet_num = add_block(turn_num, pile_height, chamber, jets, jet_num)

        find_cycle(turn_num, pile_height, jet_num, stats)

    return "No cycle found"


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
