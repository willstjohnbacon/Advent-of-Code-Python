file = open("input.txt", "r")

currentDirectory = ['root']

directorySizes = {}

def cd(directory):
    global currentDirectory
    if (directory == "..") and (len(currentDirectory) > 1):
        currentDirectory.pop()
    elif directory == '/':
        currentDirectory = ['root']
    else:
        currentDirectory.append(directory)

    # print('Change directory to', currentDirectory)
    return

def ls():
    # print('ls')
    return True

def dir():
    # print('dir')
    return True

def part1():
    lineNum = 1

    for line in (file.readlines()):
        # print ("Line ", lineNum, ": ", line)

        if line[0] == '$':
            if line[2] == 'c':
                cd(line[5:len(line)-1])
            elif line[2] == 'l':
                ls()
        elif line[0] == 'd':
            dir()
        else:
            currentDirectoryStr = '/'.join(currentDirectory)
            fileSize = int(line.split(' ')[0])
            if (currentDirectorySize := directorySizes.get(currentDirectoryStr)):
                currentDirectorySize += fileSize
                # print(currentDirectorySize)
            else:
                currentDirectorySize = fileSize
            directorySizes[currentDirectoryStr] = currentDirectorySize

            parentDirs = currentDirectory.copy()

            for i in range(1, len(currentDirectory)):
                parentDirs.pop()
                parentDirectoryStr = '/'.join(parentDirs)
                # print ("Adding ", fileSize, " to ", parentDirectoryStr)

                if (directorySizes.get(parentDirectoryStr)):
                    directorySizes[parentDirectoryStr] += fileSize
                else:
                    directorySizes[parentDirectoryStr] = fileSize


    # print(directorySizes)

    smallDirSize = 0
    for key in directorySizes.keys():
        if directorySizes[key] <= 100000:
            smallDirSize += directorySizes[key]
    return smallDirSize


def part2():
    storage = 70000000
    usedStorage = directorySizes['root']
    unusedStorage = storage - usedStorage
    spaceToDelete = 30000000 - unusedStorage
    currentSmallestDirectory = storage

    for key in directorySizes.keys():
        if directorySizes[key] >= spaceToDelete and directorySizes[key] < currentSmallestDirectory:
            currentSmallestDirectory = directorySizes[key]
    return currentSmallestDirectory


print("Part 1: ", part1())
print("Part 2: ", part2())
