# A = Rock, B = Paper, C = Scissors
# Response: X = Rock, Y = Paper, Z = Scissors
# Winner: A beats Z, C beats Y, B beats X

result_cheatsheet = {'A X': 4, 'A Y': 8, 'A Z': 3, 'B X': 1, 'B Y': 5, 'B Z': 9, 'C X': 7, 'C Y': 2, 'C Z': 6}

# type_scores = {'A': 1, 'X': 1, 'B': 2, 'Y': 2, 'C': 3, 'Z': 3}
# win_score = {'win':6, 'draw':3, 'loss':0}

def part1():
    total_score = 0
    for line in file.readlines():
        total_score += result_cheatsheet.get(line.rstrip())
        # Opponent = line.split()[0]
        # Player = line.split()[1]
        # round_score = type_scores[Player]
        # if (Opponent == 'A'):
        #     if (Player == 'X'):
        #         round_score += win_score['draw']
        #     elif (Player == 'Y'):
        #         round_score += win_score['win']
        #     elif (Player == 'Z'):
        #         round_score += win_score['loss']
        # elif (Opponent == 'B'):
        #     if (Player == 'X'):
        #         round_score += win_score['loss']
        #     elif (Player == 'Y'):
        #         round_score += win_score['draw']
        #     elif (Player == 'Z'):
        #         round_score += win_score['win']
        # elif (Opponent == 'C'):
        #     if (Player == 'X'):
        #         round_score += win_score['win']
        #     elif (Player == 'Y'):
        #         round_score += win_score['loss']
        #     elif (Player == 'Z'):
        #         round_score += win_score['draw']
        # total_score += round_score
    return total_score

def part2():
    file.seek(0)

    total_score = 0
    for line in file.readlines():
        Opponent = line.split()[0]
        Outcome = line.split()[1]
        round_score = 0
        if (Opponent == 'A'):
            if (Outcome == 'X'):
                total_score += result_cheatsheet.get('A Z')
                # round_score += type_scores['C']
                # round_score += win_score['loss']
            elif (Outcome == 'Y'):
                total_score += result_cheatsheet.get('A X')
                # round_score += type_scores[Opponent]
                # round_score += win_score['draw']
            elif (Outcome == 'Z'):
                total_score += result_cheatsheet.get('A Y')
                # round_score += type_scores['B']
                # round_score += win_score['win']
        elif (Opponent == 'B'):
            if (Outcome == 'X'):
                total_score += result_cheatsheet.get('B X')
                # round_score += type_scores['A']
                # round_score += win_score['loss']
            elif (Outcome == 'Y'):
                total_score += result_cheatsheet.get('B Y')
                # round_score += type_scores[Opponent]
                # round_score += win_score['draw']
            elif (Outcome == 'Z'):
                total_score += result_cheatsheet.get('B Z')
                # round_score += type_scores['C']
                # round_score += win_score['win']
        elif (Opponent == 'C'):
            if (Outcome == 'X'):
                total_score += result_cheatsheet.get('C Y')
                # round_score += type_scores['B']
                # round_score += win_score['loss']
            elif (Outcome == 'Y'):
                total_score += result_cheatsheet.get('C Z')
                # round_score += type_scores[Opponent]
                # round_score += win_score['draw']
            elif (Outcome == 'Z'):
                total_score += result_cheatsheet.get('C X')
                # round_score += type_scores['A']
                # round_score += win_score['win']
        # total_score += round_score
    return total_score


Testing = False
if Testing:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
