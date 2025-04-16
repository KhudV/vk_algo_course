import unittest
import timeit
import random

# Реализация минимальной кучи
class MinHeap:
    def __init__(self):
        self.data = []
    
    def heappush(self, item):
        self.data.append(item)
        self._bubble_up(len(self.data) - 1)
    
    def heappop(self):
        if not self.data:
            raise IndexError("pop from empty heap")
        # меняем корень с последним элементом и удаляем последний
        self._swap(0, len(self.data) - 1)
        min_item = self.data.pop()
        self._bubble_down(0)
        return min_item
    
    def isEmpty(self):
        return len(self.data) == 0
    
    def __len__(self):
        return len(self.data)
    
    def _bubble_up(self, idx):
        while idx > 0:
            parent = (idx - 1) // 2
            if self.data[parent] <= self.data[idx]:
                break
            self._swap(parent, idx)
            idx = parent
    
    def _bubble_down(self, idx):
        n = len(self.data)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx
            if left < n and self.data[left] < self.data[smallest]:
                smallest = left
            if right < n and self.data[right] < self.data[smallest]:
                smallest = right
            if smallest == idx:
                break
            self._swap(idx, smallest)
            idx = smallest
            
    def _swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]


# Реализация двусторонней очереди с помощью двусвязного списка
class DequeNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class Deque:
    def __init__(self, iterable=None):
        self.head = None
        self.tail = None
        self._length = 0
        if iterable:
            for item in iterable:
                self.append(item)
    
    def append(self, value):
        node = DequeNode(value)
        if not self.tail:
            self.head = self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        self._length += 1
    
    def popleft(self):
        if not self.head:
            raise IndexError("pop from an empty deque")
        value = self.head.value
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self._length -= 1
        return value
    
    def appendleft(self, value):
        node = DequeNode(value)
        if not self.head:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self._length += 1
    
    def pop(self):
        if not self.tail:
            raise IndexError("pop from an empty deque")
        value = self.tail.value
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None
        else:
            self.head = None
        self._length -= 1
        return value
    
    def __len__(self):
        return self._length
    
    def __bool__(self):
        return self._length > 0

# Классы и вспомогательные функции для работы с деревьями
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self.balanceFactor = 0  # для функции расчёта balance factor

# Построение бинарного дерева из массива (None - отсутствующий узел)
def build_tree(arr, i=0):
    if i >= len(arr):
        return None
    if arr[i] is None:
        return None
    root = TreeNode(arr[i])
    root.left = build_tree(arr, 2 * i + 1)
    root.right = build_tree(arr, 2 * i + 2)
    return root

# 1. Проверка корректности max-кучи (массив)
def is_max_heap_arr(arr):
    n = len(arr)
    for i in range((n - 2) // 2 + 1):
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[i] < arr[left]:
            return False
        if right < n and arr[i] < arr[right]:
            return False
    return True

# 2. Проверка корректности max-кучи (BFS по дереву)
def is_max_heap_bfs(root):
    if not root:
        return True
    queue = Deque([root])
    should_be_leaf = False
    while len(queue):
        current = queue.popleft()
        if current.left:
            if should_be_leaf or current.left.val > current.val:
                return False
            queue.append(current.left)
        else:
            should_be_leaf = True
        if current.right:
            if should_be_leaf or current.right.val > current.val:
                return False
            queue.append(current.right)
        else:
            should_be_leaf = True
    return True

# 3. Проверка, является ли дерево полным
def is_complete_tree(root):
    if not root:
        return True
    queue = Deque([root])
    seen_null = False
    while len(queue):
        node = queue.popleft()
        if node is None:
            seen_null = True
        else:
            if seen_null:
                return False
            queue.append(node.left)
            queue.append(node.right)
    return True

# 4. Объединение K отсортированных массивов (наивный вариант)
def merge_k_sorted_arrays_naive(sorted_arrays):
    min_heap = MinHeap()
    for arr in sorted_arrays:
        for num in arr:
            min_heap.heappush(num)
    merged = []
    while not min_heap.isEmpty():
        merged.append(min_heap.heappop())
    return merged

# 5. Объединение K отсортированных массивов (оптимальный вариант)
def merge_k_sorted_arrays(sorted_arrays):
    merged = []
    min_heap = MinHeap()
    # Инициализируем кучу первым элементом каждого массива
    for i, arr in enumerate(sorted_arrays):
        if arr:  # если не пуст
            # Кладем кортеж: (значение, индекс массива, индекс элемента)
            min_heap.heappush((arr[0], i, 0))
    while not min_heap.isEmpty():
        val, arr_idx, el_idx = min_heap.heappop()
        merged.append(val)
        if el_idx + 1 < len(sorted_arrays[arr_idx]):
            next_val = sorted_arrays[arr_idx][el_idx + 1]
            min_heap.heappush((next_val, arr_idx, el_idx + 1))
    return merged

# 6. k‑й наименьший элемент в BST (итеративно, in-order обход)
def kth_smallest(root, k):
    stack = []
    count = 0
    current = root
    while stack or current:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        count += 1
        if count == k:
            return current.val
        current = current.right
    return None

# 7. Расчёт высот поддеревьев и проставление balance factor для каждого узла
def calculate_heights_and_balance(node):
    if not node:
        return 0
    left_height = calculate_heights_and_balance(node.left)
    right_height = calculate_heights_and_balance(node.right)
    node.balanceFactor = left_height - right_height
    return 1 + max(left_height, right_height)

# 8. Преобразование дерева в зеркальное (рекурсивно)
def mirror_tree(node):
    if node is None:
        return None
    node.left, node.right = node.right, node.left
    mirror_tree(node.left)
    mirror_tree(node.right)
    return node

# 9. Преобразование дерева в зеркальное (итеративно, BFS)
def mirror_tree_iterative(root):
    if root is None:
        return None
    queue = Deque([root])
    while len(queue):
        current = queue.popleft()
        current.left, current.right = current.right, current.left
        if current.left:
            queue.append(current.left)
        if current.right:
            queue.append(current.right)
    return root

# Тесты
class TestHeapAndTreeAlgorithms(unittest.TestCase):
    def test_is_max_heap_arr(self):
        self.assertTrue(is_max_heap_arr([21, 19, 18, 11, 12, 15, 16]))
        self.assertFalse(is_max_heap_arr([10, 15, 20, 30, 40]))
    
    def test_is_max_heap_bfs(self):
        # Создаем max-кучу вручную
        root = TreeNode(21)
        root.left = TreeNode(19)
        root.right = TreeNode(18)
        root.left.left = TreeNode(11)
        root.left.right = TreeNode(12)
        root.right.left = TreeNode(15)
        root.right.right = TreeNode(16)
        self.assertTrue(is_max_heap_bfs(root))
        # Нарушаем свойство – изменяем значение
        root.left.val = 25
        self.assertFalse(is_max_heap_bfs(root))
    
    def test_is_complete_tree(self):
        # Полное дерево:
        #           1
        #         /   \
        #        2     3
        #       / \   /
        #      4   5 6
        root = TreeNode(1)
        root.left = TreeNode(2, TreeNode(4), TreeNode(5))
        root.right = TreeNode(3, TreeNode(6), None)
        self.assertTrue(is_complete_tree(root))
        # Изменим дерево, чтобы оно не было полным
        root.right.left = None
        root.right.right = TreeNode(7)
        self.assertFalse(is_complete_tree(root))
    
    def test_merge_k_sorted_arrays(self):
        arrays = [[1, 3, 5, 7], [2, 4, 6], [0, 8, 9, 11]]
        expected = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11]
        self.assertEqual(merge_k_sorted_arrays(arrays), expected)
        self.assertEqual(merge_k_sorted_arrays_naive(arrays), expected)
    
    def test_kth_smallest(self):
        # Построим BST:
        #         5
        #        / \
        #       3   7
        #      / \ / \
        #     2  4 6  8
        root = TreeNode(5,
                        TreeNode(3, TreeNode(2), TreeNode(4)),
                        TreeNode(7, TreeNode(6), TreeNode(8)))
        self.assertEqual(kth_smallest(root, 1), 2)
        self.assertEqual(kth_smallest(root, 3), 4)
        self.assertEqual(kth_smallest(root, 5), 6)
        self.assertEqual(kth_smallest(root, 7), 8)
        self.assertIsNone(kth_smallest(root, 10))
    
    def test_calculate_heights_and_balance(self):
        # Для дерева:
        #        5
        #       / \
        #      3   7
        #     / \
        #    2   4
        root = TreeNode(5,
                        TreeNode(3, TreeNode(2), TreeNode(4)),
                        TreeNode(7))
        height = calculate_heights_and_balance(root)
        self.assertEqual(height, 3)
        self.assertEqual(root.left.balanceFactor, 0)
        self.assertEqual(root.balanceFactor, 1)
    
    def test_mirror_tree(self):
        # Исходное дерево:
        #       1
        #      / \
        #     2   3
        #    / \
        #   4   5
        root = TreeNode(1,
                        TreeNode(2, TreeNode(4), TreeNode(5)),
                        TreeNode(3))
        mirrored = mirror_tree(root)
        self.assertEqual(mirrored.val, 1)
        self.assertEqual(mirrored.left.val, 3)
        self.assertEqual(mirrored.right.val, 2)
        self.assertEqual(mirrored.right.left.val, 5)
        self.assertEqual(mirrored.right.right.val, 4)
    
    def test_mirror_tree_iterative(self):
        # Исходное дерево:
        #       1
        #      / \
        #     2   3
        #    / \
        #   4   5
        root = TreeNode(1,
                        TreeNode(2, TreeNode(4), TreeNode(5)),
                        TreeNode(3))
        mirrored = mirror_tree_iterative(root)
        self.assertEqual(mirrored.val, 1)
        self.assertEqual(mirrored.left.val, 3)
        self.assertEqual(mirrored.right.val, 2)
        self.assertEqual(mirrored.right.left.val, 5)
        self.assertEqual(mirrored.right.right.val, 4)

# Бенчмарки
def benchmark():
    print("\n=== БЕНЧМАРКИ ===")
    setup_code = (
        "from __main__ import (is_max_heap_arr, is_max_heap_bfs, is_complete_tree, merge_k_sorted_arrays, "
        "merge_k_sorted_arrays_naive, kth_smallest, calculate_heights_and_balance, mirror_tree, mirror_tree_iterative, "
        "TreeNode, build_tree, MinHeap, Deque); "
        "import random; "
        "arr_heap = [random.randint(1, 1000) for _ in range(1023)]; "
        "nodes = [TreeNode(x) for x in arr_heap]; "
        "for i in range(len(arr_heap)):\n"
        "    left = 2 * i + 1\n"
        "    right = 2 * i + 2\n"
        "    if left < len(arr_heap): nodes[i].left = nodes[left]\n"
        "    if right < len(arr_heap): nodes[i].right = nodes[right]\n"
        "root_heap = nodes[0]; "
        "sorted_arrays = [[random.randint(0, 1000) for _ in range(100)] for _ in range(10)]; "
        "bst_nodes = [TreeNode(x) for x in sorted(range(1, 1024))]; "
        "for i in range(len(bst_nodes)):\n"
        "    left = 2 * i + 1\n"
        "    right = 2 * i + 2\n"
        "    if left < len(bst_nodes): bst_nodes[i].left = bst_nodes[left]\n"
        "    if right < len(bst_nodes): bst_nodes[i].right = bst_nodes[right]\n"
        "bst_root = bst_nodes[0]; "
    )
    tests = [
        ("is_max_heap_arr(arr_heap)", "Проверка корректности max-кучи (массив)"),
        ("is_max_heap_bfs(root_heap)", "Проверка корректности max-кучи (BFS)"),
        ("is_complete_tree(root_heap)", "Проверка, является ли дерево полным"),
        ("merge_k_sorted_arrays(sorted_arrays)", "Объединение K отсортированных массивов (оптимально)"),
        ("merge_k_sorted_arrays_naive(sorted_arrays)", "Объединение K отсортированных массивов (наивно)"),
        ("kth_smallest(bst_root, 100)", "Нахождение 100-го наименьшего элемента в BST"),
        ("calculate_heights_and_balance(bst_root)", "Вычисление высот и balance factor"),
        ("mirror_tree(bst_root)", "Преобразование дерева в зеркальное (рекурсивно)"),
        ("mirror_tree_iterative(bst_root)", "Преобразование дерева в зеркальное (итеративно)"),
    ]
    iterations = 1000
    for code_snip, desc in tests:
        t = timeit.timeit(stmt=code_snip, setup=setup_code, number=iterations)
        print(f"{desc}: {t / iterations:.8f} сек на запуск (среднее за {iterations} итераций)")

if __name__ == "__main__":
    unittest.main(exit=False)
    benchmark()

