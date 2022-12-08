file = open("input.txt", "r")
input = file.readline()

def part1():
    markerLength = 4

    for start in range(0, len(input)-(markerLength - 1)):
        end = start + markerLength
        charSet = set(input[start:end])
        if len(charSet) ==markerLength:
            return ('First marker is', end)
        # print(charSet)
    return 'Packet does not start'

def part2():
    markerLength = 14

    for start in range(0, len(input)-(markerLength - 1)):
        end = start + markerLength
        charSet = set(input[start:end])
        if len(charSet) ==markerLength:
            return ('First marker is', end)
        # print(charSet)
    return 'Packet does not start'


print("Part 1: ", part1())
print("Part 2: ", part2())
