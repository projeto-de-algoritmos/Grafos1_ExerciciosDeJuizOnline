from collections import defaultdict, deque

class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.adj_list = defaultdict(list)

    def add_edge(self, u, v):
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def display(self):
        for vertex, neighbors in self.adj_list.items():
            print(f"Vertex {vertex}: {neighbors}")

    def bfs(self):
        if self.vertices < 2:
            return -1

        visited = [False] * (self.vertices + 1)
        steps = [0] * (self.vertices + 1)
        start_vertex = 1  # Start from the first vertex

        queue = deque([(start_vertex, 0)])
        visited[start_vertex] = True

        while queue:
            current_vertex, current_steps = queue.popleft()

            if current_vertex == self.vertices:
                return current_steps

            for neighbor in self.adj_list[current_vertex]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append((neighbor, current_steps + 1))
                    steps[neighbor] = current_steps + 1

        return -1

def create_graph(n, m):
    graph = Graph(n)

    for _ in range(m):
        u, v = map(int, input().split())
        graph.add_edge(u, v)

    return graph

if __name__ == "__main__":
    n, m = map(int, input().split())

    graph = create_graph(n, m)
    numSteps = graph.bfs()

    if numSteps == -1 or numSteps > 2:
        print("IMPOSSIBLE")
    else:
        print("POSSIBLE")
