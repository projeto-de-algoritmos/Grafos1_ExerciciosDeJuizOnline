from collections import defaultdict, deque

def find_minimum_points(points_count, links_data):
    adjacency_list = defaultdict(list)
    for link in links_data:
        start, end = link.split()
        adjacency_list[start].append(end)
        adjacency_list[end].append(start)

    def bfs(start, target):
        visited = set()
        queue = deque([(start, 0)])  # (point, steps)

        while queue:
            point, steps = queue.popleft()
            if point == target:
                return steps

            for neighbor in adjacency_list[point]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, steps + 1))

        return float('inf')  # If no path is found

    entrance_to_cheese = bfs('Entrada', '*')

    cheese_to_exit = bfs('*', 'Saida')

    total_points = entrance_to_cheese + cheese_to_exit

    return total_points

points_count, links_count = map(int, input().split())

links_data = []
for _ in range(links_count):
    link = input().strip()
    links_data.append(link)

min_points = find_minimum_points(points_count, links_data)
print(min_points)  