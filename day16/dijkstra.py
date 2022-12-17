import heapq

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = float('inf')
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist=float('inf')):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, previous=None):
        self.previous = previous

    def set_visited(self, visited=True):
        self.visited = visited

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([adjacent.id for adjacent in self.adjacent])

    def __lt__(self, other):
        return self.distance < other.get_distance()

class Graph:
    def __init__(self):
        self.vertices = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vertices.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vertices[node] = new_vertex
        return new_vertex

    def get_vertex(self, node):
        if node in self.vertices:
            return self.vertices[node]
        else:
            return None

    def add_edge(self, source, destination, cost=0):
        if source not in self.vertices:
            self.add_vertex(source)
        if destination not in self.vertices:
            self.add_vertex(destination)

        self.vertices[source].add_neighbor(self.vertices[destination], cost)
        self.vertices[destination].add_neighbor(self.vertices[source], cost)

    def get_vertices(self):
        return self.vertices.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous

def shortest(vertex, path):
    if vertex.previous:
        path.append(vertex.previous.get_id())
        shortest(vertex.previous, path)
    return

def reset_graph(graph):
    for vertex in graph:
        vertex.set_visited(False)
        vertex.set_distance()
        vertex.set_previous()

def printGraph(graph):
    print('Graph data:')
    for vertex in graph:
        for connection in vertex.get_connections():
            vertex_id = vertex.get_id()
            connection_id = connection.get_id()
            print('( %s, %s, %3d)' % (vertex_id, connection_id, vertex.get_weight(connection)))

def dijkstra(graph, start, target):
    reset_graph(graph)

    # print("Dijkstra's Shortest Path Algorithm")
    # Set the distance for the start node to zero
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(vertex.get_distance(), vertex) for vertex in graph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance
        unvisited_vertex = heapq.heappop(unvisited_queue)
        current = unvisited_vertex[1]
        current.set_visited()

        # Repeat for each adjacent vertex
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue

            new_distance = current.get_distance() + current.get_weight(next)

            if new_distance < next.get_distance():
                next.set_distance(new_distance)
                next.set_previous(current)
                # print('updated : current = %s next = %s new_distance = %s' \
                # % (current.get_id(), next.get_id(), next.get_distance()))
            # else:
                # print('not updated : current = %s next = %s new_distance = %s' \
                # % (current.get_id(), next.get_id(), next.get_distance()))

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)

        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(vertex.get_distance(), vertex) for vertex in graph if not vertex.visited]
        heapq.heapify(unvisited_queue)


if __name__ == '__main__':

    g = Graph()

    g.add_vertex('a')
    g.add_vertex('b')
    g.add_vertex('c')
    g.add_vertex('d')
    g.add_vertex('e')
    g.add_vertex('f')

    g.add_edge('a', 'b', 7)
    g.add_edge('a', 'c', 9)
    g.add_edge('a', 'f', 14)
    g.add_edge('b', 'c', 10)
    g.add_edge('b', 'd', 15)
    g.add_edge('c', 'd', 11)
    g.add_edge('c', 'f', 2)
    g.add_edge('d', 'e', 6)
    g.add_edge('e', 'f', 9)

    printGraph(g)

    dijkstra(g, g.get_vertex('a'), g.get_vertex('e'))

    target = g.get_vertex('e')
    path = [target.get_id()]
    shortest(target, path)
    print('The shortest path : %s' % (path[::-1]))
