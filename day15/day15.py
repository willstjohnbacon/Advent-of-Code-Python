import re

TESTING = False

# def printCaveSegment(cave, x_bounds, y_bounds, center, segment):
#     y_min = center[1] - y_bounds[0] - (segment[1] // 2)
#     y_max = center[1] - y_bounds[0] + (segment[1] // 2)
#     x_min = center[0] - x_bounds[0] - (segment[0] // 2)
#     x_max = center[0] - x_bounds[0] + (segment[0] // 2)
#
#     print(f"Showing cave segment ({x_min + x_bounds[0]}, {y_min + y_bounds[0]}) to ({x_max + x_bounds[0]}, {y_max + y_bounds[0]})")
#
#     for y in range(y_min, y_max):
#         for x in range(x_min, x_max):
#             item = cave.get((x, y))
#             print(item if item else ".", end='')
#         print()

def readSensors(lines):
    sensor_data = {}
    beacons = set()

    min_x = float('inf')
    max_x = float('-inf')
    # min_y = float('inf')
    # max_y = float('-inf')

    for line in lines:
        raw_data = re.match('Sensor at x=(.*?), y=(.*?): closest beacon is at x=(.*?), y=(.*?)$', line)
        sensor = (int(raw_data[1]), int(raw_data[2]))
        beacon = (int(raw_data[3]), int(raw_data[4]))

        print (f"Sensor at {sensor}  Beacon at {beacon}")
        sensor_range = abs(beacon[0] - sensor[0]) + abs(beacon[1] - sensor[1])

        sensor_data.update({sensor:sensor_range})
        beacons.add(beacon)

        min_x = min(min_x, sensor[0] - sensor_range, beacon[0])
        max_x = max(max_x, sensor[0] + sensor_range, beacon[0])
        # min_y = min(min_y, sensor[1], beacon[1])
        # max_y = max(max_y, sensor[1], beacon[1])

    print(f"Sensors: {sensor_data}")
    print(f"Beacons: {beacons}")
    # print(f"Cave bounds: ({min_x}, {min_y}) -> ({max_x}, {max_y})")

    return sensor_data, beacons, (min_x, max_x) #, (min_y, max_y)

def isInSensorRange(point, sensor_data):
    for sensor, sensor_range in sensor_data.items():
        if (abs(point[0] - sensor[0]) + abs(point[1] - sensor[1])) <= sensor_range:
            return True
    return False

def part1():
    file.seek(0)
    lines = [line.rstrip() for line in file]

    sensor_data, beacons, x_bounds = readSensors(lines)

    non_beacon_positions = 0

    if TESTING:
        y = 10
    else:
        y = 2000000

    for x in range(x_bounds[0], x_bounds[1] + 1):
        if (x, y) in beacons:
            print(f"Beacon at {(x, y)}")
        if (not (x, y) in beacons) and isInSensorRange((x, y), sensor_data):
            non_beacon_positions += 1

    return non_beacon_positions

def part2():
    file.seek(0)
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
