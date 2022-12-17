import re
from dijkstra import *

TESTING = False

def readValves(lines, valves):
    for line in lines:
        raw_data = re.match('Valve (.*?) has flow rate=(.*?); tunnel[s]? lead[s]? to valve[s]? (.*?)$', line)
        name = raw_data[1]
        flow_rate = int(raw_data[2])
        connecting_valves = raw_data[3].split(", ")
        valves.update({name: {"flow_rate" : flow_rate, "connections" : connecting_valves}})
        # print(f"Valve {name} flows at {flow_rate} and connects to {connecting_valves}")

def printGraph(graph):
    print('Graph data:')
    for v in graph:
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()
            print('( %s, %s, %3d)' % (vid, wid, v.get_weight(w)))

def printPaths(paths, distances):
    for route, path in paths.items():
        print(f"{route[0]} -> {route[1]} = {path} [Dist {distances.get(route)}]")

def calcMaxValue(valve_name, openable_valves, distances, time_remaining, followed_paths, current_path, pressure_released):
    if (time_remaining <= 0):
        followed_paths.update({tuple(current_path): pressure_released})
        return 0

    new_path = current_path.copy()
    new_path.append(valve_name)

    attributes = openable_valves.get(valve_name)
    flow_rate = attributes.get("flow_rate")

    new_openable_valves = openable_valves.copy()
    new_openable_valves.pop(valve_name)

    max_next_value = 0
    pressure_released_from_this_valve = flow_rate * (time_remaining - 1)

    for next_valve_name in new_openable_valves.keys():
        new_time_remaining = (time_remaining - 1) - distances.get((valve_name, next_valve_name))
        max_next_value = max(max_next_value, calcMaxValue(next_valve_name, new_openable_valves, distances,
            new_time_remaining, followed_paths, new_path, (pressure_released + pressure_released_from_this_valve)))

    return max_next_value + pressure_released_from_this_valve

def intersection(tuple1, tuple2):
    return tuple(set(tuple1) & set(tuple2))

def part1():
    file.seek(0)
    lines = [line.rstrip() for line in file]

    valves = {}
    paths = {}
    distances = {}

    readValves(lines, valves)

    for source_name in valves.keys():
        for target_name in valves.keys():
            if (source_name != target_name):
                graph = Graph()

                for valve_name, valve_attributes in valves.items():
                    graph.add_vertex(valve_name)
                    for connecting_valve in valve_attributes.get("connections"):
                        graph.add_edge(valve_name, connecting_valve, 1)

                dijkstra(graph, graph.get_vertex(source_name), graph.get_vertex(target_name))

                target_vertex = graph.get_vertex(target_name)
                path = [target_vertex.get_id()]
                shortest(target_vertex, path)

                # print('The shortest path : %s' % (path[::-1]))

                paths.update({(source_name, target_name): path[::-1]})
                distances.update({(source_name, target_name): len(path) - 1})

    # printPaths(paths, distances)

    openable_valves = {}
    for valve_name, attributes in valves.items():
        if (valve_name == "AA") or (attributes.get("flow_rate") > 0):
            openable_valves.update({valve_name: attributes})

    # openable_valves.pop("DD")
    # openable_valves.pop("BB")
    # openable_valves.pop("JJ")
    # openable_valves.pop("HH")
    # openable_valves.pop("EE")

    # return calcMaxValue("CC", openable_valves, distances, 7)
    # return calcMaxValue("EE", openable_valves, distances, 10)
    # return calcMaxValue("HH", openable_valves, distances, 14)
    # return calcMaxValue("JJ", openable_valves, distances, 22)
    # return calcMaxValue("BB", openable_valves, distances, 26)
    # return calcMaxValue("DD", openable_valves, distances, 29)
    return calcMaxValue("AA", openable_valves, distances, 31, {}, [], 0)
def part2():
    file.seek(0)
    lines = [line.rstrip() for line in file]

    valves = {}
    paths = {}
    distances = {}

    readValves(lines, valves)

    for source_name in valves.keys():
        for target_name in valves.keys():
            if (source_name != target_name):
                graph = Graph()

                for valve_name, valve_attributes in valves.items():
                    graph.add_vertex(valve_name)
                    for connecting_valve in valve_attributes.get("connections"):
                        graph.add_edge(valve_name, connecting_valve, 1)

                dijkstra(graph, graph.get_vertex(source_name), graph.get_vertex(target_name))

                target_vertex = graph.get_vertex(target_name)
                path = [target_vertex.get_id()]
                shortest(target_vertex, path)

                # print('The shortest path : %s' % (path[::-1]))

                paths.update({(source_name, target_name): path[::-1]})
                distances.update({(source_name, target_name): len(path) - 1})

    # printPaths(paths, distances)

    openable_valves = {}
    for valve_name, attributes in valves.items():
        if (valve_name == "AA") or (attributes.get("flow_rate") > 0):
            openable_valves.update({valve_name: attributes})

    #Run calcMaxValue up to 26 secs and capture all paths.  Then find the pair with the largest sum
    #where their intersection is just "AA" and return the total

    followed_paths = {}

    # openable_valves.pop("DD")
    # openable_valves.pop("BB")
    # openable_valves.pop("JJ")
    # openable_valves.pop("HH")
    # openable_valves.pop("EE")

    # return calcMaxValue("CC", openable_valves, distances, 7)
    # return calcMaxValue("EE", openable_valves, distances, 10)
    # return calcMaxValue("HH", openable_valves, distances, 14)
    # return calcMaxValue("JJ", openable_valves, distances, 22)
    # return calcMaxValue("BB", openable_valves, distances, 26)
    # return calcMaxValue("DD", openable_valves, distances, 29)
    calcMaxValue("AA", openable_valves, distances, 27, followed_paths, [], 0)

    ascending_followed_paths = dict(sorted(followed_paths.items(), key=lambda item: item[1]))
    descending_followed_paths = dict(sorted(followed_paths.items(), key=lambda item: item[1], reverse=True))

    # print(sorted_followed_paths)

    while len(ascending_followed_paths):
        my_path, my_released_pressure = ascending_followed_paths.popitem()
        descending_followed_paths.pop(my_path)

        for elephant_path, elephant_released_pressure in descending_followed_paths.items():
            intersect = intersection(my_path, elephant_path)
            print(f"Me: {my_path} [{my_released_pressure}]  Elephant: {elephant_path} [{elephant_released_pressure}]  Intersect: {intersect}")

            if intersection(my_path, elephant_path) == ("AA",):
                print(f"Me: {my_path} [{my_released_pressure}]  Elephant: {elephant_path} [{elephant_released_pressure}]")
                return my_released_pressure + elephant_released_pressure

    return "Can not find non-intersecting pair"


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

# print("Part 1: ", part1())
print("Part 2: ", part2())
