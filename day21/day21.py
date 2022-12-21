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
            print(f"Monkey {monkey_name} yells {yell_num[1]}")
            yells.update({monkey_name: int(yell_num[1])})
        else:
            job_data = re.match('(.*?) ([+-/*]) (.*?)$', monkey_data[2])
            print(f"Monkey {monkey_name} calculates {job_data[1]} {job_data[2]} {job_data[3]}")
            jobs.update({monkey_name: {"monkey1": job_data[1], "operation": job_data[2], "monkey2": job_data[3]}})

    print(yells)
    print(jobs)

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
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
