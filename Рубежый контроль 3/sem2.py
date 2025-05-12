import unittest
import timeit
import random
import heapq
from collections import deque

# 1. Поиск компонент связности (DFS)
def find_connected_components(graph):
    visited = set()
    components = []

    def dfs(v, comp):
        visited.add(v)
        comp.append(v)
        for u in graph.get(v, []):
            if u not in visited:
                dfs(u, comp)

    for v in graph:
        if v not in visited:
            comp = []
            dfs(v, comp)
            components.append(comp)
    return components

# 2. Окраска компонент связности
def color_connected_components(graph):
    color = {}
    current_color = 0

    def dfs_color(v, c):
        color[v] = c
        for u in graph.get(v, []):
            if u not in color:
                dfs_color(u, c)

    for v in graph:
        if v not in color:
            current_color += 1
            dfs_color(v, current_color)
    return color

# 3. Проверка наличия цикла в неориентированном графе
def has_cycle(graph):
    visited = set()

    def dfs_cycle(v, parent):
        visited.add(v)
        for u in graph.get(v, []):
            if u not in visited:
                if dfs_cycle(u, v):
                    return True
            elif u != parent:
                return True
        return False

    for v in graph:
        if v not in visited:
            if dfs_cycle(v, None):
                return True
    return False

# 4. Проверка, является ли граф деревом
def is_tree(graph):
    if has_cycle(graph):
        return False
    comps = find_connected_components(graph)
    return len(comps) == 1

# 5. Алгоритм Дейкстры
def dijkstra(graph, start):
    dist = {v: float('inf') for v in graph}
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        d, v = heapq.heappop(heap)
        if d > dist[v]:
            continue
        for u, w in graph[v].items():
            nd = d + w
            if nd < dist[u]:
                dist[u] = nd
                heapq.heappush(heap, (nd, u))
    return dist

# 6a. Проверка двудольности (BFS)
def is_bipartite_bfs(graph):
    color = {}
    for v in graph:
        if v not in color:
            color[v] = 1
            queue = deque([v])
            while queue:
                x = queue.popleft()
                for u in graph[x]:
                    if u not in color:
                        color[u] = -color[x]
                        queue.append(u)
                    elif color[u] == color[x]:
                        return False
    return True

# 6b. Проверка двудольности (DFS)
def is_bipartite_dfs(graph):
    color = {}
    def dfs_color(v, c):
        color[v] = c
        for u in graph[v]:
            if u not in color:
                if not dfs_color(u, -c):
                    return False
            elif color[u] == c:
                return False
        return True

    for v in graph:
        if v not in color:
            if not dfs_color(v, 1):
                return False
    return True

# Тесты
class TestGraphAlgorithms(unittest.TestCase):

    def setUp(self):
        # простой неориентированный граф с двумя компонентами и циклом
        self.graph = {
            1: [2],
            2: [1, 3],
            3: [2],
            4: [5, 6],
            5: [4, 6],
            6: [4, 5]
        }
        # граф-дерево (линейный)
        self.tree = {i: [i+1] for i in range(1, 5)}
        self.tree[5] = []
        for i in range(2, 6):
            self.tree[i].append(i-1)
        # взвешенный ориентированный граф для Дейкстры
        self.wgraph = {
            'A': {'B': 1, 'C': 4},
            'B': {'C': 2, 'D': 5},
            'C': {'D': 1},
            'D': {}
        }
        # граф для двудольности
        self.bip = {1:[2,4],2:[1,3],3:[2,4],4:[1,3]}
        self.not_bip = {1:[2,3],2:[1,3],3:[1,2]}

    def test_find_connected_components(self):
        comps = find_connected_components(self.graph)
        # две компоненты: [1,2,3] и [4,5,6]
        self.assertEqual(sorted(map(sorted, comps)), [[1,2,3],[4,5,6]])

    def test_color_connected_components(self):
        colors = color_connected_components(self.graph)
        comp_ids = set(colors.values())
        self.assertEqual(len(comp_ids), 2)
        # вершины 1,2,3 одного цвета, 4,5,6 другого
        self.assertEqual(
            set(colors[v] for v in [1,2,3]),
            {colors[1]}
        )
        self.assertEqual(
            set(colors[v] for v in [4,5,6]),
            {colors[4]}
        )

    def test_has_cycle(self):
        self.assertTrue(has_cycle(self.graph))
        self.assertFalse(has_cycle(self.tree))

    def test_is_tree(self):
        self.assertFalse(is_tree(self.graph))
        self.assertTrue(is_tree(self.tree))

    def test_dijkstra(self):
        dist = dijkstra(self.wgraph, 'A')
        # A→B=1, A→C via B=3, A→D via C=4
        self.assertEqual(dist, {'A':0,'B':1,'C':3,'D':4})

    def test_is_bipartite_bfs(self):
        self.assertTrue(is_bipartite_bfs(self.bip))
        self.assertFalse(is_bipartite_bfs(self.not_bip))

    def test_is_bipartite_dfs(self):
        self.assertTrue(is_bipartite_dfs(self.bip))
        self.assertFalse(is_bipartite_dfs(self.not_bip))

# Бенчмарки
def benchmark():
    print("\n=== БЕНЧМАРКИ ===")
    # создаём случайный граф на 100 вершин, p=0.05
    N = 100
    rand_graph = {i:[] for i in range(N)}
    for i in range(N):
        for j in range(i+1, N):
            if random.random() < 0.05:
                rand_graph[i].append(j)
                rand_graph[j].append(i)
    # для Дейкстры ориентированный полный граф на 100 вершинах, p=0.1
    rand_wg = {i:{} for i in range(N)}
    for i in range(N):
        for j in range(N):
            if i!=j and random.random()<0.05:
                rand_wg[i][j] = random.randint(1,10)

    setup = (
        "from __main__ import (find_connected_components, color_connected_components, has_cycle, is_tree, dijkstra, "
        "is_bipartite_bfs, is_bipartite_dfs); "
        "import random; "
        f"rg = {rand_graph}; rw = {rand_wg}"
    )
    tests = [
        ("find_connected_components(rg)",   "Компоненты связности"),
        ("color_connected_components(rg)",  "Окраска компонент"),
        ("has_cycle(rg)",                   "Поиск цикла"),
        ("is_tree(rg)",                     "Проверка дерева"),
        ("dijkstra(rw, 0)",                 "Dijkstra"),
        ("is_bipartite_bfs(rg)",            "Двудольность BFS"),
        ("is_bipartite_dfs(rg)",            "Двудольность DFS"),
    ]
    for stmt, desc in tests:
        t = timeit.timeit(stmt=stmt, setup=setup, number=200)
        print(f"{desc}: {t/200:.6f} сек")

if __name__ == "__main__":
    unittest.main(exit=False)
    benchmark()
