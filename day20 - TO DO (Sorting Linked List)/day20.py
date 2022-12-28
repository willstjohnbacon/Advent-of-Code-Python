TESTING = False

def readInput():
    file.seek(0)
    nums = [int(line.rstrip()) for line in file]
    return nums

def mix(nums):
    new_nums = []
    for num in nums:
        new_nums.append((num, False)) #Second value indicates whether the number has already been mixed

    list_length = len(new_nums)

    index = 0

    while index < list_length:
        num, already_mixed = new_nums.pop(index)
        new_pos = index

        if not already_mixed:
            new_pos = (index + num) % (list_length - 1)
        else:
            index += 1

        new_nums.insert(new_pos, (num, True))

    return new_nums

def calcGroveCoords(num_list):
    list_length = len(num_list)

    zero_index = num_list.index((0, True))
    index_1k = (zero_index + 1000) % list_length
    index_2k = (zero_index + 2000) % list_length
    index_3k = (zero_index + 3000) % list_length

    print(f"Coords: {num_list[index_1k][0]} + {num_list[index_2k][0]} + {num_list[index_3k][0]}")
    return num_list[index_1k][0] + num_list[index_2k][0] + num_list[index_3k][0]

def part1():
    nums = mix(readInput())
    print(nums)
    return calcGroveCoords(nums)

def part2():
    file.seek(0)
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
