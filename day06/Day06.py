file = open("input.txt", "r")
input = file.readline()

bufferSize = 14

def part1():

    for start in range(0, len(input)-(bufferSize-1)):
        end = start + bufferSize
        charSet = set(input[start:end])
        if len(charSet) ==bufferSize:
            return ('First marker is', end)
        print(charSet)
    return 'Packet does not start'

def part2():
    return


print("Part 1: ",part1())
print("Part 2: ",part2())
