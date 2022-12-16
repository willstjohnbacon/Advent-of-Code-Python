import re
from dijkstra import *

TESTING = True

def readValves(lines, valves):
    for line in lines:
        raw_data = re.match('Valve (.*?) has flow rate=(.*?); tunnel[s]? lead[s]? to valve[s]? (.*?)$', line)
        name = raw_data[1]
        flow_rate = raw_data[2]
        connecting_valves = raw_data[3].split(", ")
        valves.update({name: {"flow_rate" : flow_rate, "connections" : connecting_valves}})
        print(f"Valve {name} flows at {flow_rate} and connects to {connecting_valves}")

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

def calcMaxValue(valve_name, valves, distances, open_valves, time_remaining):
    if (time_remaining == 0):
        return 0

    attributes = valves.get(valve_name)

    #Option 1 - Move immediately
    max_next_value = 0

    for next_valve_name in attributes.get("connections"):
        new_time_remaining = time_remaining - distances.get((valve_name, next_valve_name))

        if new_time_remaining > 0:
            max_next_value = max(max_next_value, calcMaxValue(next_valve_name, valves, distances, open_valves, new_time_remaining))

    # Option 2 - Open Valve then Move - only if not already open and flow_rate > 0
    flow_rate = attributes.get("flow_rate")

    if (valve_name in open_valves) or flow_rate == 0:
        return max_next_value

    new_open_valves = open_valves.copy()
    new_open_valves.append(valve_name)

    open_valve_value = int(flow_rate) * (time_remaining - 1)

    for next_valve_name in attributes.get("connections"):
        new_time_remaining = time_remaining - 1 - distances.get((valve_name, next_valve_name))

        if new_time_remaining > 0:
            max_next_value = max(max_next_value, open_valve_value + calcMaxValue(next_valve_name, valves, distances, new_open_valves, new_time_remaining))

    return max_next_value

def part1():
    file.seek(0)
    lines = [line.rstrip() for line in file]

    valves = {}
    paths = {}
    distances = {}

    readValves(lines, valves)

    graph = Graph()

    for valve_name, valve_attributes in valves.items():
        graph.add_vertex(valve_name)
        for connecting_valve in valve_attributes.get("connections"):
            graph.add_edge(valve_name, connecting_valve, 1)

    printGraph(graph)

    for source_name in valves.keys():
        for target_name in valves.keys():
            if (source_name != target_name):
                dijkstra(graph, graph.get_vertex(source_name), graph.get_vertex(target_name))

                target_vertex = graph.get_vertex(target_name)
                path = [target_vertex.get_id()]
                shortest(target_vertex, path)

                print('The shortest path : %s' % (path[::-1]))

                paths.update({(source_name, target_name) : path[::-1]})
                distances.update({(source_name, target_name) : len(path)})

    printPaths(paths, distances)

    return calcMaxValue("AA", valves, distances, [], 30)

def part2():
    file.seek(0)
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
