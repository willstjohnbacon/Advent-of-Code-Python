import re
import sys

TESTING = True

ore_collecting_robots = 0
clay_collecting_robots = 0


class blueprint:
    __slots__ = ("id", "cost", "useful")
    def __init__(self, input_string: str) -> None:
        values = [int(i) for i in re.findall(r"\d+", input_string)]
        self.id = values[0]
        self.cost = {
            "ore": {"ore": values[1]},
            "clay": {"ore": values[2]},
            "obsidian": {"ore": values[3], "clay": values[4]},
            "geode": {"ore": values[5], "obsidian": values[6]}
        }
        self.useful = {
            "ore": max(self.cost["clay"]["ore"],
                       self.cost["obsidian"]["ore"],
                       self.cost["geode"]["ore"]),
            "clay": self.cost["obsidian"]["clay"],
            "obsidian": self.cost["geode"]["obsidian"],
            "geode": float("inf")
        }

class State:
    __slots__ = ("robots", "resources", "ignored")

    def __init__(self, robots: dict = None, resources: dict = None,
                 ignored: list = None):
        self.robots = robots.copy() if robots else {
            "ore": 1, "clay": 0, "obsidian": 0, "geode": 0
        }
        self.resources = resources.copy() if resources else {
            "ore": 0, "clay": 0, "obsidian": 0, "geode": 0
        }
        self.ignored = ignored.copy() if ignored else []

    def copy(self) -> "State":
        return
    def __gt__(self, other):
        return
    def __repr__(self):
        return

def part1():
    file.seek(0)
    return

def part2():
    file.seek(0)
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
