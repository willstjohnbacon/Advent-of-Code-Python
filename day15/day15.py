import re

TESTING = False

PART2_TUNINGFREQ_MULTIPLIER = 4000000
PART2_MIN_BEACON_POS = 0

if TESTING:
    PART2_MAX_BEACON_POS = 20
else:
    PART2_MAX_BEACON_POS = 4000000

def readSensors(lines):
    sensor_data = {}
    beacons = set()

    min_x = float('inf')
    max_x = float('-inf')

    for line in lines:
        raw_data = re.match('Sensor at x=(.*?), y=(.*?): closest beacon is at x=(.*?), y=(.*?)$', line)
        sensor = (int(raw_data[1]), int(raw_data[2]))
        beacon = (int(raw_data[3]), int(raw_data[4]))

        # print (f"Sensor at {sensor}  Beacon at {beacon}")
        sensor_range = abs(beacon[0] - sensor[0]) + abs(beacon[1] - sensor[1])

        sensor_data.update({sensor:sensor_range})
        beacons.add(beacon)

        min_x = min(min_x, sensor[0] - sensor_range, beacon[0])
        max_x = max(max_x, sensor[0] + sensor_range, beacon[0])

    print(f"Sensors: {sensor_data}")
    print(f"Beacons: {beacons}")

    return sensor_data, beacons, (min_x, max_x)

def isInSensorRange(point, sensor_data, min_beacon_pos, max_beacon_pos):
    if (point[0] > max_beacon_pos) or (point[0] < min_beacon_pos) or \
            (point[1] > max_beacon_pos) or (point[1] < min_beacon_pos):
        return True

    for sensor, sensor_range in sensor_data.items():
        if (abs(point[0] - sensor[0]) + abs(point[1] - sensor[1])) <= sensor_range:
            return True
    return False

def findBeacon(sensor_data):
    for sensor, sensor_range in sensor_data.items():
        search_distance = sensor_range + 1

        for i in range(0, search_distance + 1):
            topright_segment_xpos = sensor[0] + i
            topright_segment_ypos = sensor[1] - search_distance + i
            bottomright_segment_xpos = sensor[0] + search_distance - i
            bottomright_segment_ypos = sensor[1] + i
            topleft_segment_xpos = sensor[0] - search_distance + i
            topleft_segment_ypos = sensor[1] - i
            bottomleft_segment_xpos = sensor[0] - i
            bottomleft_segment_ypos = sensor[1] + search_distance - i

            if not isInSensorRange((topright_segment_xpos, topright_segment_ypos), sensor_data, PART2_MIN_BEACON_POS, PART2_MAX_BEACON_POS):
                return topright_segment_xpos * PART2_TUNINGFREQ_MULTIPLIER + topright_segment_ypos

            if not isInSensorRange((bottomright_segment_xpos, bottomright_segment_ypos), sensor_data, PART2_MIN_BEACON_POS, PART2_MAX_BEACON_POS):
                return bottomright_segment_xpos * PART2_TUNINGFREQ_MULTIPLIER + bottomright_segment_ypos

            if not isInSensorRange((topleft_segment_xpos, topleft_segment_ypos), sensor_data, PART2_MIN_BEACON_POS, PART2_MAX_BEACON_POS):
                return topleft_segment_xpos * PART2_TUNINGFREQ_MULTIPLIER + topleft_segment_ypos

            if not isInSensorRange((bottomleft_segment_xpos, bottomleft_segment_ypos), sensor_data, PART2_MIN_BEACON_POS, PART2_MAX_BEACON_POS):
                return bottomleft_segment_xpos * PART2_TUNINGFREQ_MULTIPLIER + bottomleft_segment_ypos

    return "Failed to find beacon"

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
        if (not (x, y) in beacons) and isInSensorRange((x, y), sensor_data, float('-inf'), float('inf')):
            non_beacon_positions += 1

    return non_beacon_positions

def part2():
    file.seek(0)
    lines = [line.rstrip() for line in file]

    sensor_data, _, _ = readSensors(lines)

    return findBeacon(sensor_data)


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
