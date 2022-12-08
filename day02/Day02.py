file = open("input.txt", "r")
strategy = file.read()

def part1():
    for round in strategy:
        players = round.split(' ')
        print (players[0], 'x', players[1])
    return 'Incomplete'

def part2():
    return 'Incomplete'


print("Part 1: ",part1())
print("Part 2: ",part2())
