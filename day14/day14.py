TESTING = True

xpoints = []

def printGrid(width, height):
    y = 1
    print('  ', end='')
    for x in range(0, width):
        print(y, end='')
        y = y + 1
        if y == 10:
            y = 0
    print('')

    print(' +', '-' * (width), sep='')
    z = 1
    for i in range(0, height):
        line = str(z) + "|"
        for x in range(width):
            if [x, i] in xpoints:
                line += 'X'
            else:
                line += '.'
        print(line)
        z = z + 1
        if z == 10:
            z = 0

def axisSize(lines):
    highest_point_x = 0
    lowest_point_x = 1000
    highest_point_y = 0
    lowest_point_y = 1000
    for points in lines:
        current_line = points.split(' -> ')
        for point in current_line:
            print(point)
            x = int(point[0:3])
            y = int(point[4:])
            if highest_point_x < x:
                highest_point_x = x
            elif lowest_point_x > x:
                lowest_point_x = x

            if highest_point_y < y:
                highest_point_y = y
            elif lowest_point_y > y:
                lowest_point_y = y

    print(lowest_point_x, highest_point_x)
    print(lowest_point_y, highest_point_y)

def part1():
    file.seek(0)
    lines = [line.rstrip() for line in file]
    # width = 551 - 492
    # height = 177 - 14
    width = 503 - 498
    height = 9 - 4
    for points in lines:
        current_line = points.split(' -> ')
        for point in current_line:
            x = int(point[0:3])
            y = int(point[4:])
            # xpoints.append([551-x, 177-y])
            print(x, y)
            xpoints.append([503-x, 9-y])

    printGrid(width, height)
    return

def part2():
    file.seek(0)
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
