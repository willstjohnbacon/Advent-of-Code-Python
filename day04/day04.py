def isSubset(elf1, elf2):
    # if (elf1[0] == elf2[0]) and (elf1[1] == elf2[1]):
    #     print ("Elf 1 and Elf 2 have same sections:", elf1, elf2)
    #     return False

    if (int(elf1[0]) >= int(elf2[0])) and (int(elf1[1]) <= int(elf2[1])):
        # print ("Elf 1 redundant:", elf1, elf2)
        return True

    if (int(elf2[0]) >= int(elf1[0])) and (int(elf2[1]) <= int(elf1[1])):
        # print ("Elf 2 redundant:", elf1, elf2)
        return True

    return False

def isOverlap(elf1, elf2):
    # if (elf1[0] == elf2[0]) and (elf1[1] == elf2[1]):
    #     print ("Elf 1 and Elf 2 have same sections:", elf1, elf2)
    #     return False

    if (int(elf1[0]) <= int(elf2[0])) and (int(elf1[1]) >= int(elf2[0])):
        return True

    if (int(elf1[0]) <= int(elf2[1])) and (int(elf1[1]) >= int(elf2[1])):
        return True

    if (int(elf2[0]) <= int(elf1[0])) and (int(elf2[1]) >= int(elf1[0])):
        return True

    if (int(elf2[0]) <= int(elf1[1])) and (int(elf2[1]) >= int(elf1[1])):
        return True

    return False

def part1():
    overlap_count = 0

    for line in file.readlines():
        pairs = line.strip().split(',')

        elf1 = pairs[0].split('-')
        elf2 = pairs[1].split('-')

        # print ("Elf1", elf1, "Elf2", elf2)

        if isSubset(elf1, elf2):
            overlap_count += 1
    return overlap_count

def part2():
    file.seek(0)
    overlap_count = 0

    for line in file.readlines():
        pairs = line.strip().split(',')

        elf1 = pairs[0].split('-')
        elf2 = pairs[1].split('-')

        # print ("Elf1", elf1, "Elf2", elf2)

        if isSubset(elf1, elf2) or isOverlap(elf1, elf2):
            overlap_count += 1
    return overlap_count

Testing = False
if Testing:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
