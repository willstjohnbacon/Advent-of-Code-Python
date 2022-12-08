file = open("day01/input.txt", "r")

def part1():
    calories_str = 0
    highest_calories = 0

    while calories_str != '':
        current_elf_calories = 0
        while ((calories_str := file.readline()) != '\n'):
            if calories_str == '':
                break
            current_elf_calories += int(calories_str)
        if (current_elf_calories > highest_calories):
            highest_calories = current_elf_calories

    return highest_calories

def part2():
    calories_str = 0
    highest_calories = [0]

    while calories_str != '':
        current_elf_calories = 0
        while ((calories_str := file.readline()) != '\n'):
            if calories_str == '':
                break
            current_elf_calories += int(calories_str)
        if (current_elf_calories > highest_calories[len(highest_calories)-1]):
            highest_calories.append(current_elf_calories)

    listLength = len(highest_calories)
    print("1.",highest_calories[listLength-1])
    print("1.",highest_calories[listLength-2])
    print("1.",highest_calories[listLength-3])

    return ("sum:",highest_calories[listLength-1] + highest_calories[listLength-2] + highest_calories[listLength-3])


print("Part 1: ",part1())
print("Part 2: ",part2())
