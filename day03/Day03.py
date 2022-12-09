def getPriority(item):
    if ord(item) >= ord('a'):
        return ord(item) - ord('a') + 1
    return ord(item) - ord('A') + 27

def part1():
    totalItemPriority = 0

    for line in file.readlines():
        # print("Input Line: ", line)

        compartment1 = list(line[:len(line)//2])
        compartment2 = list(line[len(line)//2:].rstrip())

        # print ("Compartment 1:", compartment1, "Compartment 2:", compartment2)

        for item in compartment1:
            if (item in compartment2):
                print (item, getPriority(item))
                totalItemPriority += getPriority(item)
                break

    return totalItemPriority

def part2():
    file.seek(0)
    totalItemPriority = 0

    rucksacks = file.readlines()

    groupNum = 1
    firstGroupRucksack = 0

    while firstGroupRucksack < len(rucksacks):
        for item in rucksacks[firstGroupRucksack]:
            if (item in rucksacks[firstGroupRucksack + 1]) and (item in rucksacks[firstGroupRucksack + 2]):
                print ("Group", groupNum, "badge is item", item, "priority", getPriority(item))
                totalItemPriority += getPriority(item)
                firstGroupRucksack += 3
                groupNum += 1
                break

    return totalItemPriority


Testing = False
if Testing:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
