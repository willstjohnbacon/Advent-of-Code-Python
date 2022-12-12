Testing = False

def getNumericHeight(alphaHeight):
    if alphaHeight == 'S':
        return 0
    if alphaHeight == 'E':
        return 25

    return ord(alphaHeight) - 97

class Point:
    def __init__(self, y, x, height_map):
        self.y = y
        self.x = x
        self.start = (height_map[y][x] == "S")
        self.end = (height_map[y][x] == "E")
        self.height = getNumericHeight(height_map[y][x])
        self.connecting_points = []

    def __str__(self):
        return f"Point {self.y}, {self.x}: {len(self.connecting_points)} connections"

    def isStart(self):
        return self.start

    def isEnd(self):
        return self.end

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

def findRoute(seek_start, search_stack, steps_stack):
    while len(search_stack) > 0:
        # print(f'Steps: {steps_stack}')

        point = search_stack.pop(0)
        steps = steps_stack.pop(0)

        if seek_start and point.isStart():
            return steps

        if not seek_start and point.getHeight() == 0:
            return steps

        connections = point.getConnectingPoints()

        for connection in connections:
            if not (connection in search_stack):
                search_stack.append(connection)
                steps_stack.append(steps + 1)

    return float("inf")

def part1():
    point_map = []
    search_stack = []

    height_map = [list(line.rstrip()) for line in file]
    # print("Height Map: ", height_map)

    for y in range(0, len(height_map)):
        point_map.append([])
        for x in range(0, len(height_map[y])):
            point = Point(y, x, height_map)
            point_map[y].append(point)
            if point.isEnd():
                search_stack.append(point)

    for y in range(0, len(point_map)):
        for x in range(0, len(point_map[y])):
            point_map[y][x].determineConnectingPoints(point_map)

    return findRoute(True, search_stack, [0])

def part2():
    file.seek(0)

    point_map = []
    search_stack = []

    height_map = [list(line.rstrip()) for line in file]

    for y in range(0, len(height_map)):
        point_map.append([])
        for x in range(0, len(height_map[y])):
            point = Point(y, x, height_map)
            point_map[y].append(point)
            if point.isEnd():
                search_stack.append(point)

    for y in range(0, len(point_map)):
        for x in range(0, len(point_map[y])):
            point_map[y][x].determineConnectingPoints(point_map)

    return findRoute(False, search_stack, [0])

if Testing:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
