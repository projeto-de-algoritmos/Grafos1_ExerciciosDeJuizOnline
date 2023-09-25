class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_x] = root_y
            if self.rank[root_x] == self.rank[root_y]:
                self.rank[root_y] += 1

        return True

def calcularDias(m, n, roads):
    total_cost = sum(road[2] for road in roads)
    roads.sort(key=lambda road: road[2])
    min_span_tree_cost = 0
    union_find = UnionFind(m)

    for road in roads:
        x, y, z = road
        if union_find.union(x, y):
            min_span_tree_cost += z

    return total_cost - min_span_tree_cost

def main():
    while True:
        m, n = map(int, input().split())
        if m == 0 and n == 0:
            break

        estradas = [tuple(map(int, input().split())) for _ in range(n)]
        maxDias = calcularDias(m, n, estradas)
        print(maxDias)

if __name__ == "__main__":
    main()
