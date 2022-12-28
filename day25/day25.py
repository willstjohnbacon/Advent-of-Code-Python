TESTING = False

def add(num1, num2):
    snafu_to_val = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}
    val_to_snafu = {-2: "=", -1: "-", 0: "0", 1: "1", 2: "2"}

    snafu_sum = ""
    carry = 0

    for digit_num in range(len(num1) - 1, -1, -1):
        digit1 = snafu_to_val[num1[digit_num]]
        digit2 = snafu_to_val[num2[digit_num]]

        sum_digit = (digit1 + digit2) + carry
        carry = 0

        if sum_digit > 2:
            carry = 1
            sum_digit -= 5
        elif sum_digit < -2:
            carry = -1
            sum_digit += 5

        snafu_sum = val_to_snafu[sum_digit] + snafu_sum

    if carry:
        snafu_sum = val_to_snafu[carry] + snafu_sum

    return snafu_sum

def part1():
    file.seek(0)
    nums = [line.rstrip().zfill(20) for line in file]

    snafu_sum = "00000000000000000000"

    for num in nums:
        snafu_sum = add(snafu_sum, num)

    # print(add("1=", "1="))
    # print(add("2=", "2="))
    # print(add("2=0=", "2=01"))
    return snafu_sum

def part2():
    file.seek(0)
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
