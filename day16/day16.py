import re

TESTING = True

def readValves(lines):
    for line in lines:
        raw_data = re.match('Valve (.*?) has flow rate=(.*?); tunnel[s]? lead[s]? to valve[s]? (.*?)$', line)
        valve = raw_data[1]
        flow_rate = raw_data[2]
        connecting_valves = raw_data[3].split()
        print(f"Valve {valve} flows at {flow_rate} and connects to {connecting_valves}")

def part1():
    file.seek(0)
    lines = [line.rstrip() for line in file]
    readValves(lines)
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
