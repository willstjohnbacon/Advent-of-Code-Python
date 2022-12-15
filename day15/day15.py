import re

TESTING = False

MIN_BEACON_POS = 0

if TESTING:
    MAX_BEACON_POS = 20
else:
    MAX_BEACON_POS = 4000000

def readSensors(lines):
    sensor_data = {}
    beacons = set()

    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')

    for line in lines:
        raw_data = re.match('Sensor at x=(.*?), y=(.*?): closest beacon is at x=(.*?), y=(.*?)$', line)
        sensor = (int(raw_data[1]), int(raw_data[2]))
        beacon = (int(raw_data[3]), int(raw_data[4]))

        print (f"Sensor at {sensor}  Beacon at {beacon}")
        sensor_range = abs(beacon[0] - sensor[0]) + abs(beacon[1] - sensor[1])

        sensor_data.update({sensor:sensor_range})
        beacons.add(beacon)

        min_x = max(MIN_BEACON_POS, min(min_x, sensor[0] - sensor_range, beacon[0]))
        max_x = min(MAX_BEACON_POS, max(max_x, sensor[0] + sensor_range, beacon[0]))
        min_y = max(MIN_BEACON_POS, min(min_y, sensor[1] - sensor_range, beacon[1]))
        max_y = min(MAX_BEACON_POS, max(max_y, sensor[1] + sensor_range, beacon[0]))

    print(f"Sensors: {sensor_data}")
    print(f"Beacons: {beacons}")
    print(f"Search bounds: {(min_x, min_y)} -> {(max_x, max_y)}")

    return sensor_data, beacons, (min_x, max_x), (min_y, max_y)

def isInSensorRange(point, sensor_data):
    if (point[0] > MAX_BEACON_POS) or (point[0] < 0) or (point[1] > MAX_BEACON_POS) or (point[1] < 0):
        return True

    for sensor, sensor_range in sensor_data.items():
        if (abs(point[0] - sensor[0]) + abs(point[1] - sensor[1])) <= sensor_range:
            return True
    return False

def findBeacon(sensor_data, x_bounds, y_bounds):
    for sensor, sensor_range in sensor_data.items():
        search_distance = sensor_range + 1

        # x_min = max(x_bounds[0], sensor[0])
        # x_max = min(x_bounds[1], sensor[0])
        # y_min = max(y_bounds[0], sensor[1])
        # y_max = min(y_bounds[1], sensor[1])

        for i in range(0, search_distance + 1):
            topright_segment_xpos = sensor[0] + i
            topright_segment_ypos = sensor[1] - search_distance + i
            bottomright_segment_xpos = sensor[0] + search_distance - i
            bottomright_segment_ypos = sensor[1] + i
            topleft_segment_xpos = sensor[0] - search_distance + i
            topleft_segment_ypos = sensor[1] - i
            bottomleft_segment_xpos = sensor[0] - i
            bottomleft_segment_ypos = sensor[1] + search_distance - i

            if not isInSensorRange((topright_segment_xpos, topright_segment_ypos), sensor_data):
                return topright_segment_xpos * 4000000 + topright_segment_ypos

            if not isInSensorRange((bottomright_segment_xpos, bottomright_segment_ypos), sensor_data):
                return bottomright_segment_xpos * 4000000 + bottomright_segment_ypos

            if not isInSensorRange((topleft_segment_xpos, topleft_segment_ypos), sensor_data):
                return topleft_segment_xpos * 4000000 + topleft_segment_ypos

            if not isInSensorRange((bottomleft_segment_xpos, bottomleft_segment_ypos), sensor_data):
                return bottomleft_segment_xpos * 4000000 + bottomleft_segment_ypos

    return "Failed to find beacon"

        # print(f"Bounds: {(x_min, y_min)} -> {(x_max, y_max)}")
        #
        # for x in range(x_min, x_max):
        #     for y in range(y_min, y_max):
        #         if not isInSensorRange((x, y), sensor_data):
        #             print(f"Suitable beacon position at {(x, y)}")
        #             return (4000000 * x) + y
        #
                # point_distance1 = abs(x - sensor1[0]) + abs(y - sensor1[1])
                # point_distance2 = abs(x - sensor2[0]) + abs(y - sensor2[1])
                # if (point_distance > sensor_range) and (point_distance <= sensor_range + 2):
                #     print(f"Checking point {(x, y)}")
                #     if not isInSensorRange((x, y), sensor_data):
                #         print(f"Suitable beacon position at {(x, y)}")
                #         return (4000000 * x) + y


def part1():
    global MIN_BEACON_POS
    MIN_BEACON_POS = float('-inf')

    global MAX_BEACON_POS
    MAX_BEACON_POS = float('inf')

    file.seek(0)
    lines = [line.rstrip() for line in file]

    sensor_data, beacons, x_bounds, _ = readSensors(lines)

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
    lines = [line.rstrip() for line in file]

    sensor_data, beacons, x_bounds, y_bounds = readSensors(lines)

    return findBeacon(sensor_data, x_bounds, y_bounds)


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

# print("Part 1: ", part1())
print("Part 2: ", part2())
