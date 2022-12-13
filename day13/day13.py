TESTING = False

def findEndOfNumeric(string, startPos):
    commaPos = string.find(',', startPos)
    bracketPos = string.find(']', startPos)

    if bracketPos == -1:
        print("ERROR: No terminating ']' in string", string)
        exit(1)

    if commaPos == -1:
        return bracketPos

    return commaPos if (commaPos < bracketPos) else bracketPos

def getNumeric(string, startPos):
    endPos = findEndOfNumeric(string, startPos)
    return int(string[startPos:endPos])

def insertChar(char, string, pos):
    return string[:pos] + char + string[pos:]

def highlightError(packets, charnum):
    packets[0] = insertChar('<', packets[0], charnum + 1)
    packets[0] = insertChar('>', packets[0], charnum)
    packets[1] = insertChar('<', packets[1], charnum + 1)
    packets[1] = insertChar('>', packets[1], charnum)

def isCorrectOrder(packets):
    for charnum in range(0, len(packets[0])):
        if packets[0][charnum] == '[':
            if packets[1][charnum] == '[':
                continue
            if packets[1][charnum] == ']':
                print("Right side ran out", packets)
                return False
            if packets[1][charnum] == ',':
                highlightError(packets, charnum)
                print ("ERROR: [ vs ,", packets)
                exit(-1)
            if packets[1][charnum].isnumeric():
                end_of_numeric = findEndOfNumeric(packets[1], charnum)
                packets[1] = insertChar(']', packets[1], end_of_numeric)
                packets[1] = insertChar('[', packets[1], charnum)
                continue
        if packets[0][charnum] == ']':
            if packets[1][charnum] == '[':
                print("Left side ran out", packets)
                return True
            if packets[1][charnum] == ']':
                continue
            if packets[1][charnum] == ',':
                print("Left side ran out", packets)
                return True
            if packets[1][charnum].isnumeric():
                print("Left side ran out", packets)
                return True
        if packets[0][charnum] == ',':
            if packets[1][charnum] == '[':
                highlightError(packets, charnum)
                print ("ERROR: , vs [", packets)
                exit(-1)
            if packets[1][charnum] == ']':
                print("Right side ran out", packets)
                return False
            if packets[1][charnum] == ',':
                continue
            if packets[1][charnum].isnumeric():
                highlightError(packets, charnum)
                print ("ERROR: , vs num", packets)
                exit(-1)
        if packets[0][charnum].isnumeric():
            end_of_numeric = findEndOfNumeric(packets[0], charnum)

            if packets[1][charnum] == '[':
                packets[0] = insertChar(']', packets[0], end_of_numeric)
                packets[0] = insertChar('[', packets[0], charnum)
                continue
            if packets[1][charnum] == ']':
                print("Right side ran out", packets)
                return False
            if packets[1][charnum] == ',':
                highlightError(packets, charnum)
                print ("ERROR: num vs ,", packets)
                exit(-1)
            if packets[1][charnum].isnumeric():
                numeric_0 = getNumeric(packets[0], charnum)
                numeric_1 = getNumeric(packets[1], charnum)
                if numeric_0 < numeric_1:
                    print("Left side smaller", packets)
                    return True
                if numeric_1 < numeric_0:
                    print("Right side smaller", packets)
                    return False

    if len(packets[1]) > len(packets[0]):
        print ("Left side ran out", packets)
        return True

    print ("Right side ran out", packets)
    return False

def part1():
    if TESTING:
        file = open("sampleInput.txt", "r")
    else:
        file = open("input.txt", "r")

    lines = file.readlines()

    pairnum = 0
    total = 0

    while pairnum < (len(lines) / 3):
        print ("Analysing pair", pairnum + 1)

        packets = [lines[pairnum * 3].rstrip(), lines[(pairnum * 3) + 1].rstrip()]
        if isCorrectOrder(packets):
            print (f"Pair {pairnum + 1} is correct")
            total += (pairnum + 1)
        else:
            print (f"Pair {pairnum + 1} is incorrect")

        pairnum += 1

    return total

def part2():
    if TESTING:
        file = open("sampleInput_part2.txt", "r")
    else:
        file = open("input_part2.txt", "r")

    file.seek(0)
    lines = [line.rstrip() for line in file if line != "\n"]
    print ("Starting lines:", lines)

    swap_made = False

    for i in range(0, len(lines) - 1):
        for j in range(0, len(lines) - i - 1): #The last i packets will be in the correct order
            if not isCorrectOrder([lines[j], lines[j+1]]):
                swap_made = True
                lines.insert(j, lines.pop(j + 1))

        if not swap_made: #Ran through without changing anything so must be sorted
            break

    print ("Sorted Lines:", lines)

    decoder_key = 1

    for linenum in range(0, len(lines)):
        if (lines[linenum] in ["[[2]]", "[[6]]"]):
            decoder_key *= (linenum + 1)

    return decoder_key

part1 = part1()
part2 = part2()

print("Part 1: ", part1)
print("Part 2: ", part2)
