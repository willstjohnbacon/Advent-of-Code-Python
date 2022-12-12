import sys

Testing = False

def getNumericHeight(alphaHeight):
    if alphaHeight == 'S':
        return -1
    if alphaHeight == 'E':
        return 26

    return ord(alphaHeight) - 97

class Point:
    def __init__(self, y, x, height_map):
        self.y = y
        self.x = x
        self.height = getNumericHeight(height_map[y][x])
        self.connecting_points = []
        self.isDeadEnd = False

    def __str__(self):
        return f"Point {self.y}, {self.x}: {len(self.connecting_points)} connections"

    def getHeight(self):
        return self.height

    def getConnectingPoints(self):
        return self.connecting_points

    def determineConnectingPoints(self, point_map):
        for y in range(self.y - 1, self.y + 2):
            if (y >= 0) and (y < len(point_map)):
                for x in range(self.x - 1, self.x + 2):
                    if (x >= 0) and (x < len(point_map[y])):
                        if not ((y == self.y and x == self.x) or
                                (y == self.y - 1 and x == self.x - 1) or
                                (y == self.y - 1 and x == self.x + 1) or
                                (y == self.y + 1 and x == self.x - 1) or
                                (y == self.y + 1 and x == self.x + 1)):
                                    if (self.height - point_map[y][x].getHeight()) <= 1:
                                        self.connecting_points.append(point_map[y][x])

        # self.connecting_points.sort(key=lambda p: p.height, reverse=True)

def endPos(point_map):
    for y in range(0, len(point_map)):
        for point in point_map[y]:
            if point.getHeight() == 26:
                return point

def findRoute(search_stack, min_steps):
    print (f'Min Steps {min_steps}  Stack Size {len(search_stack)}')

    point = search_stack[len(search_stack) - 1]

    if point.getHeight() == -1:
        min_steps = min(min_steps, len(search_stack) - 1)

    connections = point.getConnectingPoints()

    if len(connections) > 0:
        connections.sort(key=lambda p: p.height, reverse=True)

    for connection in connections:
        if not (connection in search_stack):
            search_stack.append(connection)
            min_steps = findRoute(search_stack, min_steps)

    search_stack.pop()
    return min_steps

def part1():
    point_map = []
    search_stack = []

    height_map = [list(line.rstrip()) for line in file]
    print("Height Map: ", height_map)

    for y in range(0, len(height_map)):
        point_map.append([])
        for x in range(0, len(height_map[y])):
            point_map[y].append(Point(y, x, height_map))

    for y in range(0, len(point_map)):
        for x in range(0, len(point_map[y])):
            point_map[y][x].determineConnectingPoints(point_map)

    search_stack.append(endPos(point_map))

    return findRoute(search_stack, 99999999999999999999999999999999999999999999999999)

def part2():
    file.seek(0)
    return

sys.setrecursionlimit(100000)

if Testing:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
