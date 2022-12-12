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
        self.steps_to_end = 999999999999999999999999999999999999999999999999
        self.visited = False

    def __str__(self):
        return f"Point {self.y}, {self.x}: {len(self.connecting_points)} connections"

    def getHeight(self):
        return self.height

    def isVisited(self):
        return self.visited
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
                                    if (point_map[y][x].getHeight() - self.height) <= 1:
                                        self.connecting_points.append(point_map[y][x])

        # self.connecting_points.sort(key=lambda p: p.height, reverse=True)

    def stepsToEnd(self):
        if self.visited:
            return self.steps_to_end

        self.visited = True

        if self.height == 26:
            self.steps_to_end = 0
        else:
            for point in self.connecting_points:
                subpath_length = point.stepsToEnd()

                if (subpath_length + 1) < self.steps_to_end:
                    self.steps_to_end = 1 + subpath_length

        return self.steps_to_end

def startPos(height_map):
    for y in range(0, len(height_map)):
        for x in range(0, len(height_map[y])):
            if height_map[y][x] == 'S':
                return y, x


def part1():
    point_map = []

    height_map = [list(line.rstrip()) for line in file]
    print("Height Map: ", height_map)

    currentY, currentX = startPos(height_map)
    print("Starting at", currentY, ",", currentX)

    for y in range(0, len(height_map)):
        point_map.append([])
        for x in range(0, len(height_map[y])):
            point_map[y].append(Point(y, x, height_map))

    for y in range(0, len(point_map)):
        for x in range(0, len(point_map[y])):
            point_map[y][x].determineConnectingPoints(point_map)

    return point_map[currentY][currentX].stepsToEnd()

def part2():
    file.seek(0)
    return

sys.setrecursionlimit(10000)

if Testing:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
