import re

TESTING = True

def part1():
    file.seek(0)
    lines = [line.rstrip() for line in file]
    print ("Input lines:", lines)

    sensor_data = {}

    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')

    for line in lines:
        raw_data = re.match('Sensor at x=(.*?), y=(.*?): closest beacon is at x=(.*?), y=(.*?)$', line)
        sensor = (int(raw_data[1]), int(raw_data[2]))
        beacon = (int(raw_data[3]), int(raw_data[4]))

        print (f"Sensor at {sensor}  Beacon at {beacon}")
        sensor_data.update({sensor:beacon})

        min_x = min(min_x, sensor[0], beacon[0])
        max_x = max(max_x, sensor[0], beacon[0])
        min_y = min(min_y, sensor[1], beacon[1])
        max_y = max(max_y, sensor[1], beacon[1])

    print(sensor_data)
    print(f"Cave bounds: ({min_x}, {min_y}) -> ({max_x}, {max_y})")
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
