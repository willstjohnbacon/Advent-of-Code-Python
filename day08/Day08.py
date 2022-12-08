with open("input.txt") as inputFile:
    treeGrid = [list(row.rstrip()) for row in inputFile]

print (treeGrid)

columns = len(treeGrid[0])
rows = len(treeGrid)

print("Grid is ", rows, " by ", columns
      )

def isVisibleFromLeft(x, y):
    height = treeGrid[y][x]
    for testX in range(0,x):
        if treeGrid[y][testX] >= height:
            return False
    return True


def isVisibleFromRight(x, y):
    height = treeGrid[y][x]
    for testX in range(x+1, columns):
        if treeGrid[y][testX] >= height:
            return False
    return True

def isVisibleFromTop(x, y):
    height = treeGrid[y][x]
    for testY in range(0, y):
        if treeGrid[testY][x] >= height:
            return False
    return True

def isVisibleFromBottom(x, y):
    height = treeGrid[y][x]
    for testY in range(y+1, rows):
        if treeGrid[testY][x] >= height:
            return False
    return True

def treesVisibleLeft(x, y):
    height = treeGrid[y][x]
    score = 1
    for testX in range(x-1, 0, -1):
        if treeGrid[y][testX] >= height:
            return score
        else:
            score += 1
    return score

def treesVisibleRight(x, y):
    height = treeGrid[y][x]
    score = 1
    for testX in range(x+1, columns-1):
        if treeGrid[y][testX] >= height:
            return score
        else:
            score += 1
    return score

def treesVisibleUp(x, y):
    height = treeGrid[y][x]
    score = 1
    for testY in range(y-1, 0, -1):
        if treeGrid[testY][x] >= height:
            return score
        else:
            score += 1
    return score

def treesVisibleDown(x, y):
    height = treeGrid[y][x]
    score = 1
    for testY in range(y+1, rows-1):
        if treeGrid[testY][x] >= height:
            return score
        else:
            score += 1
    return score

def part1():
    visibleTrees = ((rows-1) * 2) + ((columns-1) * 2)

    for x in range(1, columns-1):
        for y in range(1, rows-1):
            if isVisibleFromTop(x,y) or isVisibleFromBottom(x,y) or isVisibleFromLeft(x,y) or isVisibleFromRight(x,y):
                visibleTrees += 1
    return visibleTrees

def part2():
    highestScenicScore = 0

    for x in range(1, columns - 1):
        for y in range(1, rows - 1):
            scenicScore = treesVisibleLeft(x, y) * treesVisibleRight(x, y) * treesVisibleUp(x, y) * treesVisibleDown(x, y)
            if scenicScore > highestScenicScore:
                highestScenicScore = scenicScore
    return highestScenicScore


print(treesVisibleLeft(2,1))
print(treesVisibleRight(2,1))
print(treesVisibleUp(2,1))
print(treesVisibleDown(2,1))

print("Part 1: ",part1())
print("Part 2: ",part2())
