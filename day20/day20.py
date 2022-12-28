TESTING = False

def readInput(multiplication_factor = 1):
    file.seek(0)
    nums = [int(line.rstrip()) * multiplication_factor for line in file]
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

def mixInOrder(nums, mixed_nums):
    list_length = len(nums)

    for original_pos, num in enumerate(nums):
        fully_qualified_num = (num, original_pos)

        current_pos = mixed_nums.index(fully_qualified_num)

        mixed_nums.pop(current_pos)

        new_pos = (current_pos + num) % (list_length - 1)

        mixed_nums.insert(new_pos, fully_qualified_num)

    return mixed_nums

def calcGroveCoords(num_list):
    list_length = len(num_list)

    zero_index = num_list.index((0, True))
    index_1k = (zero_index + 1000) % list_length
    index_2k = (zero_index + 2000) % list_length
    index_3k = (zero_index + 3000) % list_length

    print(f"Coords: {num_list[index_1k][0]} + {num_list[index_2k][0]} + {num_list[index_3k][0]}")
    return num_list[index_1k][0] + num_list[index_2k][0] + num_list[index_3k][0]

def calcGroveCoordsPart2(nums, mixed_nums):
    list_length = len(nums)
    zero_original_pos = nums.index(0)

    zero_index = mixed_nums.index((0, zero_original_pos))
    index_1k = (zero_index + 1000) % list_length
    index_2k = (zero_index + 2000) % list_length
    index_3k = (zero_index + 3000) % list_length

    print(f"Coords: {mixed_nums[index_1k][0]} + {mixed_nums[index_2k][0]} + {mixed_nums[index_3k][0]}")
    return mixed_nums[index_1k][0] + mixed_nums[index_2k][0] + mixed_nums[index_3k][0]

def part1():
    nums = mix(readInput())
    print(nums)
    return calcGroveCoords(nums)

def part2():
    nums = readInput(811589153)

    mixed_nums = []

    for original_pos, num in enumerate(nums):
        mixed_nums.append((num, original_pos))

    for mix_num in range(0, 10):
        mixed_nums = mixInOrder(nums, mixed_nums)

    print(mixed_nums)

    return calcGroveCoordsPart2(nums, mixed_nums)


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
