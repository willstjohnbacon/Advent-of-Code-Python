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

    new_chamber = chamber.copy()

    for empty_row in range(len(chamber), pile_height + 9):
        new_chamber.append(0b0000000)

    block_num = turn_num % len(blocks)
    block = blocks[block_num]
    block_height = len(block)
    block_bottom = pile_height + 4

    while True:
        jet_direction = jets[jet_num]
        block = moveSideways(block, block_bottom, jet_direction, new_chamber)
        jet_num = (jet_num + 1) % len(jets)

        if checkIfLanded(block, block_bottom, block_height, new_chamber):
            break

        block_bottom -= 1

    for block_row in range(0, block_height):
        new_chamber[block_bottom + block_row] = \
            new_chamber[block_bottom + block_row] | block[block_row]

    pile_height = max(pile_height, block_bottom + block_height - 1)

    # printChamber(new_chamber)
    # print()

    return new_chamber, pile_height, jet_num


def part1():
    file.seek(0)
    jets = file.readline().rstrip()

    chamber = [0b1111111]   #Note that my floor occupies chamber[0]
    pile_height = jet_num = 0

    for turn_num in range(0, 2022):
        chamber, pile_height, jet_num = add_block(turn_num, pile_height, chamber, jets, jet_num)

    return pile_height

def part2():
    file.seek(0)
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
