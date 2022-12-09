def sign(num):
    if num < 0:
        return -1
    return 1
def moveKnot(thisKnot, priorKnot, track, visitedPositions):
        if (priorKnot[0] - thisKnot[0]) > 1 and (priorKnot[1] - thisKnot[1]) > 1:
            thisKnot[0] += 1
            thisKnot[1] += 1

        elif (priorKnot[0] - thisKnot[0]) > 1 and (priorKnot[1] - thisKnot[1]) < -1:
            thisKnot[0] += 1
            thisKnot[1] -= 1

        elif (priorKnot[0] - thisKnot[0]) < -1 and (priorKnot[1] - thisKnot[1]) > 1:
            thisKnot[0] -= 1
            thisKnot[1] += 1

        elif (priorKnot[0] - thisKnot[0]) < -1 and (priorKnot[1] - thisKnot[1]) < -1:
            thisKnot[0] -= 1
            thisKnot[1] -= 1

        elif (priorKnot[0] - thisKnot[0]) > 1:
            thisKnot[0] += 1
            thisKnot[1] = priorKnot[1]

        elif (priorKnot[0] - thisKnot[0]) < -1:
            thisKnot[0] -= 1
            thisKnot[1] = priorKnot[1]

        elif (priorKnot[1] - thisKnot[1]) > 1:
            thisKnot[1] += 1
            thisKnot[0] = priorKnot[0]

        elif (priorKnot[1] - thisKnot[1]) < -1:
            thisKnot[1] -= 1
            thisKnot[0] = priorKnot[0]

        if track:
            visitedPositions.add(tuple(thisKnot))

def part1():
    headPos = [0,0]
    tailPos = [0,0]
    visitedPositions = {tuple([0,0])}

    dirMap = {"R": [1,0], "L": [-1,0], "U": [0,-1], "D": [0, 1]}

    for line in file.readlines():
        print("Input Line: ", line)

        moveCommand = line.split()
        moveDir = moveCommand[0]
        moveDist = int(moveCommand[1])

        increments = dirMap.get(moveDir)
        xIncrement = increments[0]
        yIncrement = increments[1]

        print("Moving head", moveDist, "positions with increments: [", xIncrement, ",", yIncrement, "]")

        for moveNum in range(0, moveDist):
            headPos[0] += xIncrement
            headPos[1] += yIncrement

            moveKnot(tailPos, headPos, True, visitedPositions)

            # print("headPos:", headPos, ", tailPos:", tailPos, "Visited: ", visitedPositions)

    return len(visitedPositions)

def part2():
    knots = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]
    visitedPositions = {tuple([0,0])}

    dirMap = {"R": [1,0], "L": [-1,0], "U": [0,-1], "D": [0,1]}

    file.seek(0)
    for line in file.readlines():
        # print("Input Line: ", line)

        moveCommand = line.split()
        moveDir = moveCommand[0]
        moveDist = int(moveCommand[1])

        increments = dirMap.get(moveDir)
        xIncrement = increments[0]
        yIncrement = increments[1]

        print("Moving head", moveDist, "positions with increments: [", xIncrement, ",", yIncrement, "]")

        for moveNum in range(0, moveDist):
            knots[0][0] += xIncrement
            knots[0][1] += yIncrement

            for knotNum in range(1, len(knots)):
                track = (knotNum == (len(knots) - 1))
                moveKnot(knots[knotNum], knots[knotNum-1], track, visitedPositions)

    print("headPos:", knots[0], ", tailPos:", knots[9], "Visited: ", visitedPositions)

    return len(visitedPositions)


Testing = False
if Testing:
    file = open("sampleInput2.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
