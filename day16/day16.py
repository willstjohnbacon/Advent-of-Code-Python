import re
from dijkstra import *

TESTING = False

def readValves(lines, valves):
    for line in lines:
        raw_data = re.match('Valve (.*?) has flow rate=(.*?); tunnel[s]? lead[s]? to valve[s]? (.*?)$', line)
        name = raw_data[1]
        flow_rate = raw_data[2]
        connecting_valves = raw_data[3].split(", ")
        valves.append({"name" : name, "flow_rate" : flow_rate, "connections" : connecting_valves})
        print(f"Valve {name} flows at {flow_rate} and connects to {connecting_valves}")

def printGraph(graph):
    print('Graph data:')
    for v in graph:
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()
            print('( %s, %s, %3d)' % (vid, wid, v.get_weight(w)))

def printPaths(paths):
    for route, path in paths.items():
        print(f"{route[0]} -> {route[1]} = {path}")

def part1():
    file.seek(0)
    lines = [line.rstrip() for line in file]

    valves = []
    paths = {}

    readValves(lines, valves)

    graph = Graph()

    for valve in valves:
        graph.add_vertex(valve.get("name"))
        for connecting_valve in valve.get("connections"):
            graph.add_edge(valve.get("name"), connecting_valve, 1)

    printGraph(graph)

    for source in valves:
        source_name = source.get("name")

        for target in valves:
            target_name = target.get("name")

            if (source_name != target_name):
                dijkstra(graph, graph.get_vertex(source_name), graph.get_vertex(target_name))

                target_vertex = graph.get_vertex(target_name)
                path = [target_vertex.get_id()]
                shortest(target_vertex, path)

                print('The shortest path : %s' % (path[::-1]))

                paths.update({(source_name, target_name) : path[::-1]})

    printPaths(paths)
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
