from collections import deque

TESTING = False

def readInput():
    blizzard_movement = {">": (0, 1), "<": (0, -1), "v": (1, 0), "^": (-1, 0)}

    file.seek(0)
    lines = [line.rstrip() for line in file]

    last_line = len(lines) - 1
    start_pos = (-1, lines[0].find(".") - 1)
    end_pos = (last_line - 1, lines[last_line].find(".") - 1)

    print(f"Start: {start_pos}, End: {end_pos}")

    vertical_blizzards = []
    horizontal_blizzards = []

    for x in range(1, len(lines[0]) - 1):
        vertical_blizzards.append([])

    for y in range(1, len(lines) - 1):
        horizontal_blizzards.append([])
        for x in range(1, len(lines[0]) - 1):
            pos = lines[y][x]
            if (pos != "."):
                movement = blizzard_movement[pos]
                match (pos):
                    case "^" | "v":
                        vertical_blizzards[x - 1].append(((y - 1, x - 1), movement))
                    case "<" | ">":
                        horizontal_blizzards[y - 1].append(((y - 1, x - 1), movement))

    return vertical_blizzards, horizontal_blizzards, \
        (len(lines) - 2), (len(lines[0]) - 2), start_pos, end_pos

def positionOnTurn(turn_num, blizzard, valley_length, valley_width):
    start, movement = blizzard
    startY, startX = start
    movementY, movementX = movement

    posOnTurnY = (startY + (turn_num * movementY)) % valley_length
    posOnTurnX = (startX + (turn_num * movementX)) % valley_width

    return (posOnTurnY, posOnTurnX)

def coincidentalBlizzardOrWall(turn_num, posY, posX, vertical_blizzards, horizontal_blizzards, valley_length, valley_width):
    if posY < 0 or posY >= valley_length or posX < 0 or posX >= valley_width:
        return True

    for blizzard in vertical_blizzards[posX] + horizontal_blizzards[posY]:
        if positionOnTurn(turn_num, blizzard, valley_length, valley_width) == (posY, posX):
            return True

    return False

# def getMinTurns(current_pos, destination, turn_num, vertical_blizzards, horizontal_blizzards, valley_length, valley_width):
#     if current_pos == destination:
#         return turn_num
#
#     currentY, currentX = current_pos
#
#     check_positions = [(1, 0), (0, 1), (0, -1), (-1, 0), (0, 0)]
#     potential_next_positions = []
#
#     for offsetY, offsetX in check_positions:
#         checkY = currentY + offsetY
#         checkX = currentX + offsetX
#
#         if coincidentalBlizzardOrWall(turn_num + 1, checkY, checkX, vertical_blizzards,
#                                       horizontal_blizzards, valley_length, valley_width):
#             continue
#
#         potential_next_positions.append((checkY, checkX))
#
#     min_turns = float('inf')
#     for position in potential_next_positions:
#         min_turns = min(min_turns, 1 + getMinTurns(position, destination, turn_num + 1, vertical_blizzards,
#                                                horizontal_blizzards, valley_length, valley_width))
#
#     return min_turns

def getMinTurns(positions, start_pos, end_pos, vertical_blizzards, horizontal_blizzards,
                valley_length, valley_width):
    check_positions = deque([(1, 0), (0, 1), (0, -1), (-1, 0), (0, 0)])

    turn_num = 0

    while positions and (turn_num < 1000):
        turn_num, current_pos = positions.popleft()
        print(f"Turn num {turn_num}, position {current_pos}")

        currentY, currentX = current_pos

        for offsetY, offsetX in check_positions:
            checkY = currentY + offsetY
            checkX = currentX + offsetX

            if (checkY, checkX) == end_pos:
                return turn_num + 1

            if ((checkY, checkX) != start_pos) and \
                    coincidentalBlizzardOrWall(turn_num + 1, checkY, checkX,
                                               vertical_blizzards, horizontal_blizzards,
                                               valley_length, valley_width):
                continue

            if (turn_num + 1, (checkY, checkX)) not in positions:
                positions.append((turn_num + 1, (checkY, checkX)))

        #Cycle check order to prevent bouncing back and forth between two squares
        #but keep "wait" as last option
        wait = check_positions.pop()
        check_positions.append(check_positions.popleft())
        check_positions.append(wait)

    return float('inf')

def part1():
    vertical_blizzards, horizontal_blizzards,\
        valley_length, valley_width, start_pos, end_pos = readInput()

    print(f"Valley is {valley_length} long by {valley_width} wide")

    positions = deque([(0, start_pos)])

    return getMinTurns(positions, start_pos, end_pos, vertical_blizzards, horizontal_blizzards, valley_length, valley_width)
    # return getMinTurns(start_pos, end_pos, 0, vertical_blizzards, horizontal_blizzards, valley_length, valley_width)

def part2():
    file.seek(0)
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
