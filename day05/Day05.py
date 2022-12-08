file = open("input.txt", "r")

# dockStacks = [['Z','N'],['M','C','D'],['P']]
craneStack = []
dockStacks = [['N','D','M','Q','B','P','Z'],['C','L','Z','Q','M','D','H','V'],['Q','H','R','D','V','F','Z','G'],['H','G','D','F','N'],['N','F','Q'],['D','Q','V','Z','F','B','T'],['Q','M','T','Z','D','V','S','H'],['M','G','F','P','N','Q'],['B','W','R','M']]

def lift(numToLift, stackNum):
    for crate in range(0, numToLift):
        craneStack.append(dockStacks[stackNum].pop());
    return

def drop(numToDrop, stackNum):
    for crate in range(0, numToDrop):
        dockStacks[stackNum].append(craneStack.pop());
    return

def part1():
    moveOps = file.readlines()

    print(dockStacks)

    for op in moveOps:
        command = op.split()
        print(command)

        numToMove = int(command[1])
        fromStack = int(command[3]) - 1
        toStack = int(command [5]) - 1

        for crate in range(0, numToMove):
            lift(1, fromStack)
            drop(1, toStack)

        print (dockStacks)

    answer = ''

    for stack in range(0, len(dockStacks)):
        answer += dockStacks[stack][len(dockStacks[stack])-1]
    return answer


def part2():
    file.seek(0)
    moveOps = file.readlines()

    print(dockStacks)
    print(moveOps)

    for op in moveOps:
        command = op.split()
        print(command)

        numToMove = int(command[1])
        fromStack = int(command[3]) - 1
        toStack = int(command[5]) - 1


        lift(numToMove, fromStack)
        drop(numToMove, toStack)

        print(dockStacks)

    answer = ''

    for stack in range(0, len(dockStacks)):
        answer += dockStacks[stack][len(dockStacks[stack]) - 1]

    return answer


# print("Part 1: ",part1())
print("Part 2: ",part2())
