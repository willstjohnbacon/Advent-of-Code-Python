def add(old, num):
    return old + num

def multiply(old, num):
    return old * num

def square(old, _):
    return old ** 2

# monkey_behaviour = [
#     {'operation': multiply, 'operand': 19, 'divisor': 23, 'true': 2, 'false': 3},
#     {'operation': add, 'operand': 6, 'divisor': 19, 'true': 2, 'false': 0},
#     {'operation': square, 'operand': -1, 'divisor': 13, 'true': 1, 'false': 3},
#     {'operation': add, 'operand': 3, 'divisor': 17, 'true': 0, 'false': 1}
# ]
#
# monkey_items = [
#     [79, 98],
#     [54, 65, 75, 74],
#     [79, 60, 97],
#     [74]
# ]
#
# monkey_inspections = [0, 0, 0, 0]

monkey_behaviour = [
    {'operation': multiply, 'operand': 13, 'divisor': 19, 'true': 2, 'false': 7},
    {'operation': add, 'operand': 2, 'divisor': 3, 'true': 4, 'false': 5},
    {'operation': add, 'operand': 1, 'divisor': 11, 'true': 7, 'false': 3},
    {'operation': add, 'operand': 8, 'divisor': 17, 'true': 6, 'false': 1},
    {'operation': square, 'operand': -1, 'divisor': 5, 'true': 0, 'false': 5},
    {'operation': add, 'operand': 4, 'divisor': 2, 'true': 2, 'false': 0},
    {'operation': multiply, 'operand': 17, 'divisor': 13, 'true': 4, 'false': 1},
    {'operation': add, 'operand': 5, 'divisor': 7, 'true': 3, 'false': 6}
]

monkey_items = [
    [75, 75, 98, 97, 79, 97, 64],
    [50, 99, 80, 84, 65, 95],
    [96, 74, 68, 96, 56, 71, 75, 53],
    [83, 96, 86, 58, 92],
    [99],
    [60, 54, 83],
    [77, 67],
    [95, 65, 58, 76],
]

monkey_inspections = [0, 0, 0, 0, 0, 0, 0, 0]

def part1():
    for round in range(0, 20):
        monkey_num = 0

        for monkey in monkey_behaviour:
            operation = monkey['operation']
            operand = monkey['operand']
            divisor = monkey['divisor']
            ifTrueMonkey = monkey['true']
            ifFalseMonkey = monkey['false']

            for item_num in range(0, len(monkey_items[monkey_num])):
                monkey_inspections[monkey_num] += 1
                item = monkey_items[monkey_num].pop()
                worry_level = operation(item, operand)
                worry_level = worry_level // 3

                if worry_level % divisor == 0:
                    monkey_items[ifTrueMonkey].append(worry_level)
                else:
                    monkey_items[ifFalseMonkey].append(worry_level)

            monkey_num += 1

    monkey_inspections.sort(reverse=True)

    return monkey_inspections[0] * monkey_inspections[1]

def part2():
    common_divisor = 1

    for monkey in monkey_behaviour:
        common_divisor *= monkey['divisor']

    for round in range(0, 10000):
        # print("Round num:", round)
        monkey_num = 0

        for monkey in monkey_behaviour:
            # print("Monkey num:", monkey_num)
            operation = monkey['operation']
            operand = monkey['operand']
            divisor = monkey['divisor']
            ifTrueMonkey = monkey['true']
            ifFalseMonkey = monkey['false']

            for item_num in range(0, len(monkey_items[monkey_num])):
                monkey_inspections[monkey_num] += 1
                item = monkey_items[monkey_num].pop()

                # if monkey_num == 4:
                #     print ("Squaring...")

                worry_level = operation(item, operand)
                worry_level = worry_level % common_divisor

                # if monkey_num == 4:
                #     print (worry_level)

                # if monkey_num == 4:
                #     print ("Dividing...")

                if worry_level % divisor == 0:
                    monkey_items[ifTrueMonkey].append(worry_level)
                else:
                    monkey_items[ifFalseMonkey].append(worry_level)

                # if monkey_num == 4:
                #     print ("Done")

            # print("Monkey", monkey_num, "inspections:", monkey_inspections[monkey_num])
            monkey_num += 1

    monkey_inspections.sort(reverse=True)

    return monkey_inspections[0] * monkey_inspections[1]


Testing = False
if Testing:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

# print("Part 1: ", part1())
print("Part 2: ", part2())
