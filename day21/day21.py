import re

TESTING = False

def calculate(monkey1, monkey2, operation):
    if operation == "+":
        return monkey1 + monkey2
    if operation == "-":
        return monkey1 - monkey2
    if operation == "*":
        return monkey1 * monkey2
    if operation == "/":
        return monkey1 / monkey2

    print(f"Something went wrong with: {monkey1} {operation} {monkey2}")
    exit(1)

def solve (y, monkey1, monkey2, operation, yells, jobs):
    monkey1_yell = yells.get(monkey1)
    monkey2_yell = yells.get(monkey2)

    #Doesn't handle situation where both sides of equation are dependent on humn
    if not monkey1_yell and not monkey2_yell:
        print(f"Both sides of equation are dependent on humn: {monkey1}, {monkey2}")
        exit(1)

    if monkey1_yell and monkey2_yell:
        return calculate(monkey1, monkey2, operation)

    if not monkey1_yell:
        known_monkey_yell = monkey2_yell

        if monkey1 == "humn":
            # print("Monkey 1 is me")
            match operation:
                case "+": return y - known_monkey_yell
                case "*": return y // known_monkey_yell
                case "-": return y + known_monkey_yell
                case "/": return y * known_monkey_yell

        # print("Monkey 1's yell not known")
        next_monkey = monkey1

        next_monkey_job = jobs.get(next_monkey)

        match operation:
            case "+": return solve(y - known_monkey_yell, next_monkey_job.get("monkey1"), next_monkey_job.get("monkey2"), next_monkey_job.get("operation"), yells, jobs)
            case "*": return solve(y // known_monkey_yell, next_monkey_job.get("monkey1"), next_monkey_job.get("monkey2"), next_monkey_job.get("operation"), yells, jobs)
            case "-": return solve(y + known_monkey_yell, next_monkey_job.get("monkey1"), next_monkey_job.get("monkey2"), next_monkey_job.get("operation"), yells, jobs)
            case "/": return solve(y * known_monkey_yell, next_monkey_job.get("monkey1"), next_monkey_job.get("monkey2"), next_monkey_job.get("operation"), yells, jobs)

    elif not monkey2_yell:
        known_monkey_yell = monkey1_yell

        if monkey2 == "humn":
            # print("Monkey 2 is me")
            match operation:
                case "+": return y - known_monkey_yell
                case "*": return y // known_monkey_yell
                case "-": return known_monkey_yell - y
                case "/": return known_monkey_yell // y

        # print("Monkey 2's yell not known")
        next_monkey = monkey2

        next_monkey_job = jobs.get(next_monkey)

        match operation:
            case "+": return solve(y - known_monkey_yell, next_monkey_job.get("monkey1"), next_monkey_job.get("monkey2"), next_monkey_job.get("operation"), yells, jobs)
            case "*": return solve(y // known_monkey_yell, next_monkey_job.get("monkey1"), next_monkey_job.get("monkey2"), next_monkey_job.get("operation"), yells, jobs)
            case "-": return solve(known_monkey_yell - y, next_monkey_job.get("monkey1"), next_monkey_job.get("monkey2"), next_monkey_job.get("operation"), yells, jobs)
            case "/": return solve(known_monkey_yell // y, next_monkey_job.get("monkey1"), next_monkey_job.get("monkey2"), next_monkey_job.get("operation"), yells, jobs)

def part1():
    file.seek(0)
    lines = [line.rstrip() for line in file]

    yells = {}
    jobs = {}

    for line in lines:
        monkey_data = re.match('(.*?): (.*?)$', line)
        monkey_name = monkey_data[1]

        yell_num = re.match('(\d*?)$', monkey_data[2])

        if (yell_num):
            # print(f"Monkey {monkey_name} yells {yell_num[1]}")
            yells.update({monkey_name: int(yell_num[1])})
        else:
            job_data = re.match('(.*?) ([+-/*]) (.*?)$', monkey_data[2])
            # print(f"Monkey {monkey_name} calculates {job_data[1]} {job_data[2]} {job_data[3]}")
            jobs.update({monkey_name: {"monkey1": job_data[1], "operation": job_data[2], "monkey2": job_data[3]}})

    # print(yells)
    # print(jobs)

    while (not "root" in yells):
        for monkey_name, job in jobs.items():
            monkey1 = job.get("monkey1")
            monkey2 = job.get("monkey2")
            operation = job.get("operation")

            if (monkey1 in yells) and (monkey2 in yells):
                monkey1_yell_num = yells.get(monkey1)
                monkey2_yell_num = yells.get(monkey2)
                yells.update({monkey_name: calculate(monkey1_yell_num, monkey2_yell_num, operation)})

    return yells.get("root")

def part2():
    file.seek(0)
    lines = [line.rstrip() for line in file]

    yells = {}
    jobs = {}

    for line in lines:
        monkey_data = re.match('(.*?): (.*?)$', line)
        monkey_name = monkey_data[1]

        yell_num = re.match('(\d*?)$', monkey_data[2])

        if (yell_num):
            # print(f"Monkey {monkey_name} yells {yell_num[1]}")
            yells.update({monkey_name: int(yell_num[1])})
        else:
            job_data = re.match('(.*?) ([+-/*]) (.*?)$', monkey_data[2])
            # print(f"Monkey {monkey_name} calculates {job_data[1]} {job_data[2]} {job_data[3]}")
            jobs.update({monkey_name: {"monkey1": job_data[1], "operation": job_data[2], "monkey2": job_data[3]}})

    yells.pop("humn")
    root_job = jobs.pop("root")
    root_monkey1 = root_job.get("monkey1")
    root_monkey2 = root_job.get("monkey2")

    resolved_yell_num = True

    while resolved_yell_num:
        resolved_yell_num = False

        for monkey_name, job in list(jobs.items()):
            monkey1 = job.get("monkey1")
            monkey2 = job.get("monkey2")
            operation = job.get("operation")

            if (monkey1 in yells) and (monkey2 in yells):
                resolved_yell_num = True
                jobs.pop(monkey_name)
                monkey1_yell_num = yells.get(monkey1)
                monkey2_yell_num = yells.get(monkey2)
                yells.update({monkey_name: calculate(monkey1_yell_num, monkey2_yell_num, operation)})

    first_operation = "-"
    if yells.get(root_monkey1):
        first_operation = "+"

    return solve(0, root_monkey1, root_monkey2, first_operation, yells, jobs)

if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
