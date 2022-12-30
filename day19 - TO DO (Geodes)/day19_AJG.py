import re

TESTING = False

MINING_MINS = 24
ORE, CLAY, OBSIDIAN, GEODE = 0, 1, 2, 3
RESOURCE_NAMES = ["ore", "clay", "obsidian", "geode"]
BOT_NAMES = ["ore-collecting", "clay-collecting", "obsidian-collecting", "geode-cracking"]

def readBlueprints():
    file.seek(0)
    lines = [line.rstrip() for line in file]

    blueprints = []

    for line in lines:
        nums = re.findall('[0-9]+', line)
        blueprints.append([int(nums[1]), int(nums[2]), (int(nums[3]), int(nums[4])), (int(nums[5]), 0, int(nums[6]))])

    print(blueprints)
    return blueprints

def determineMaxBotsRequired(blueprint):
    max_bots_required = [0, 0, 0]

    max_bots_required[ORE] = max(blueprint[ORE], blueprint[CLAY], blueprint[OBSIDIAN][ORE], blueprint[GEODE][ORE])
    max_bots_required[CLAY] = blueprint[OBSIDIAN][CLAY]
    max_bots_required[OBSIDIAN] = blueprint[GEODE][OBSIDIAN]

    return max_bots_required

def buildableBots(blueprint, resources):
    bots_available = []

    if resources[ORE] >= blueprint[ORE]:
        bots_available.append(ORE)

    if resources[ORE] >= blueprint[CLAY]:
        bots_available.append(CLAY)

    if resources[ORE] >= blueprint[OBSIDIAN][ORE] and \
            resources[CLAY] >= blueprint[OBSIDIAN][CLAY]:
            bots_available.append(OBSIDIAN)

    if resources[ORE] >= blueprint[GEODE][ORE] and \
            resources[OBSIDIAN] >= blueprint[GEODE][OBSIDIAN]:
            bots_available.append(GEODE)

    return bots_available

def buildBot(blueprint, bot_type, resources, log):
    new_resources = resources.copy()

    bot_name = BOT_NAMES[bot_type]
    cost = ""

    if bot_type == ORE:
        new_resources[ORE] -= blueprint[ORE]
        cost = f"{blueprint[ORE]} ore"
    elif bot_type == CLAY:
        new_resources[ORE] -= blueprint[CLAY]
        cost = f"{blueprint[CLAY]} ore"
    elif bot_type == OBSIDIAN:
        new_resources[ORE] -= blueprint[OBSIDIAN][ORE]
        new_resources[CLAY] -= blueprint[OBSIDIAN][CLAY]
        cost = f"{blueprint[OBSIDIAN][ORE]} ore and {blueprint[OBSIDIAN][CLAY]} clay"
    elif bot_type == GEODE:
        new_resources[ORE] -= blueprint[GEODE][ORE]
        new_resources[OBSIDIAN] -= blueprint[GEODE][OBSIDIAN]
        cost = f"{blueprint[GEODE][ORE]} ore and {blueprint[GEODE][OBSIDIAN]} obsidian"

    a = "an" if bot_type in [ORE, OBSIDIAN] else "a"
    log.append(f"Spend {cost} to start building {a} {bot_name} robot.")

    return new_resources, log

def addResources(resources, bots, log):
    new_resources = resources.copy()

    for resource_type in [ORE, CLAY, OBSIDIAN, GEODE]:
        if bots[resource_type] > 0:
            new_resources[resource_type] += bots[resource_type]

            bot_name = BOT_NAMES[resource_type]
            robot = "robot" if bots[resource_type] == 1 else "robots"
            collect = "collects" if bots[resource_type] == 1 else "collect"
            if resource_type == GEODE:
                collect = "cracks" if bots[resource_type] == 1 else "crack"
            resource_name = RESOURCE_NAMES[resource_type]
            if resource_name == "geode" and bots[resource_type] > 1:
                resource_name = "geodes"
            log.append(f"{bots[resource_type]} {bot_name} {robot} {collect} {bots[resource_type]} {resource_name}; you now have {new_resources[resource_type]} {resource_name}.")

    return new_resources, log

def theoreticalAdditionalGeodes(mins_remaining):
    geodes = 0
    num_bots = 1

    for mins in range(mins_remaining, 0, -1):
        geodes += num_bots * mins

    return geodes

def maxGeodes(blueprint, mins_remaining, max_geodes, bots, resources, max_bots_required, not_bought_last_round, log):
    new_log = log.copy()
    new_log.append("")
    new_log.append(f"== Minute {MINING_MINS - mins_remaining + 1} ==")

    #If this is the last minute, do nothing
    if mins_remaining == 1:
        new_resources, new_log = addResources(resources, bots, new_log)
        return new_resources[GEODE], new_log

    bots_available = buildableBots(blueprint, resources)

    #If possible, build a Geode bot
    if GEODE in bots_available:
        new_bots = bots.copy()
        new_bots[GEODE] = bots[GEODE] + 1
        new_resources, new_log = buildBot(blueprint, GEODE, resources, new_log)
        new_resources, new_log = addResources(new_resources, bots, new_log)
        new_log.append(f"The new {BOT_NAMES[GEODE]} robot is ready; you now have {new_bots[GEODE]} of them.")

        return maxGeodes(blueprint, mins_remaining - 1, max_geodes, new_bots, new_resources, max_bots_required, [], new_log)

    #Work out what the most geodes would be, assuming we were able to build an additional geode bot on every turn after this one
    theoretical_max_geodes = resources[GEODE] + (bots[GEODE] * mins_remaining) + theoreticalAdditionalGeodes(mins_remaining - 1)

    #If the most we could possibly produce is less than we already know we can produce via another path, don't bother with this path
    if theoretical_max_geodes <= max_geodes:
        return 0, ""

    #Now we need to try the various other options and select the one that produces the most geodes...

    not_bought_bots = []  #If we could buy a bot but choose instead to wait on this turn, we should not buy it on the next turn
    max_geodes_log = ""

    #If mins >= 3 and number of ore bots < max ore required for a bot and can build an ore bot, do so
    if mins_remaining >= 3 and \
            ORE not in not_bought_last_round and \
            bots[ORE] < max_bots_required[ORE] and \
            ORE in bots_available:
        path_log = new_log.copy()
        new_bots = bots.copy()
        new_bots[ORE] = bots[ORE] + 1
        new_resources, path_log = buildBot(blueprint, ORE, resources, path_log)
        new_resources, path_log = addResources(new_resources, bots, path_log)
        path_log.append(f"The new {BOT_NAMES[ORE]} robot is ready; you now have {new_bots[ORE]} of them.")

        path_max_geodes, path_log = maxGeodes(blueprint, mins_remaining - 1, max_geodes, new_bots, new_resources, max_bots_required, [], path_log)
        if path_max_geodes > max_geodes:
            max_geodes = path_max_geodes
            max_geodes_log = path_log

    if bots[ORE] >= max_bots_required[ORE] or ORE in bots_available:
        not_bought_bots = [ORE]

    #If mins >= 3 and number of obsidian bots < max obsidian required for a bot and can build an obsidian bot, do so
    if mins_remaining >= 3 and \
            OBSIDIAN not in not_bought_last_round and \
            bots[OBSIDIAN] < max_bots_required[OBSIDIAN] and \
            OBSIDIAN in bots_available:
        path_log = new_log.copy()
        new_bots = bots.copy()
        new_bots[OBSIDIAN] = bots[OBSIDIAN] + 1
        new_resources, path_log = buildBot(blueprint, OBSIDIAN, resources, path_log)
        new_resources, path_log = addResources(new_resources, bots, path_log)
        path_log.append(f"The new {BOT_NAMES[OBSIDIAN]} robot is ready; you now have {new_bots[OBSIDIAN]} of them.")

        path_max_geodes, path_log = maxGeodes(blueprint, mins_remaining - 1, max_geodes, new_bots, new_resources, max_bots_required, [], path_log)
        if path_max_geodes > max_geodes:
            max_geodes = path_max_geodes
            max_geodes_log = path_log

    if bots[OBSIDIAN] >= max_bots_required[OBSIDIAN] or OBSIDIAN in bots_available:
        not_bought_bots.append(OBSIDIAN)

    #If mins >= 4 and number of clay bots < max clay required for a bot and can build a clay bot, do so
    if mins_remaining >= 4 and \
            CLAY not in not_bought_last_round and \
            bots[CLAY] < max_bots_required[CLAY] and \
            CLAY in bots_available:
        path_log = new_log.copy()
        new_bots = bots.copy()
        new_bots[CLAY] = bots[CLAY] + 1
        new_resources, path_log = buildBot(blueprint, CLAY, resources, path_log)
        new_resources, path_log = addResources(new_resources, bots, path_log)
        path_log.append(f"The new {BOT_NAMES[CLAY]} robot is ready; you now have {new_bots[CLAY]} of them.")

        path_max_geodes, path_log = maxGeodes(blueprint, mins_remaining - 1, max_geodes, new_bots, new_resources, max_bots_required, [], path_log)
        if path_max_geodes > max_geodes:
            max_geodes = path_max_geodes
            max_geodes_log = path_log

    if bots[CLAY] >= max_bots_required[CLAY] or CLAY in bots_available:
        not_bought_bots.append(CLAY)

    #Wait
    path_log = new_log.copy()
    new_resources, path_log = addResources(resources, bots, path_log)
    path_max_geodes, path_log = maxGeodes(blueprint, mins_remaining - 1, max_geodes, bots, new_resources, max_bots_required, not_bought_bots, path_log)
    if path_max_geodes > max_geodes:
        max_geodes = path_max_geodes
        max_geodes_log = path_log

    return max_geodes, max_geodes_log

def printLog(log):
    for line in log:
        print(line)

    print()

def part1():
    blueprints = readBlueprints()

    quality_levels = []

    for blueprint_num, blueprint in enumerate(blueprints):
        max_bots_required = determineMaxBotsRequired(blueprint)
        bots = [1, 0, 0, 0]
        resources = [0, 0, 0, 0]

        max_geodes, log = maxGeodes(blueprint, MINING_MINS, 0, bots, resources, max_bots_required, [], [])

        # printLog(log)
        print(f"Blueprint {blueprint_num + 1} can produce {max_geodes} geodes")

        quality_levels.append((blueprint_num + 1) * max_geodes)

    return sum(quality_levels)

def part2():
    file.seek(0)
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
