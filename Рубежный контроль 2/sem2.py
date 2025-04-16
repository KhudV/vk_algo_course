import unittest
import timeit
import random
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# 1. Восстановление бинарного дерева из массива
def build_tree(arr, i=0):
    if i >= len(arr):
        return None
    # Если в массиве могут быть None, то:
    if arr[i] is None:
        return None
    root = TreeNode(arr[i])
    root.left = build_tree(arr, 2 * i + 1)
    root.right = build_tree(arr, 2 * i + 2)
    return root

# 2. Проверка симметричности бинарного дерева (BFS)
def is_symmetric(root):
    if root is None:
        return True
    queue = deque([root])
    while queue:
        level_size = len(queue)
        # формируем список узлов текущего уровня (включая None)
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node)
            if node is not None:
                queue.append(node.left)
                queue.append(node.right)
        # проверяем, что список level симметричен
        left, right = 0, len(level) - 1
        while left < right:
            a = level[left]
            b = level[right]
            if a is None and b is None:
                left += 1
                right -= 1
                continue
            if a is None or b is None:
                return False
            if a.val != b.val:
                return False
            left += 1
            right -= 1
    return True

# 3. Проверка симметричности бинарного дерева
def dfs_inorder(node, res):
    if node is None:
        res.append(None)  # чтобы учитывать пропуски
        return res
    dfs_inorder(node.left, res)
    res.append(node.val)
    dfs_inorder(node.right, res)
    return res

def is_symmetric_dfs(root):
    if root is None:
        return True
    data = dfs_inorder(root, [])
    i, j = 0, len(data) - 1
    while i < j:
        if data[i] != data[j]:
            return False
        i += 1
        j -= 1
    return True

# 4. Поиск минимальной глубины бинарного дерева
def min_depth(root):
    if root is None:
        return 0
    if root.left is None and root.right is None:
        return 1
    if root.left is not None and root.right is not None:
        return 1 + min(min_depth(root.left), min_depth(root.right))
    if root.left is not None:
        return 1 + min_depth(root.left)
    return 1 + min_depth(root.right)

# 5. Произведение минимального и максимального элементов
def max_min_multiplication(data):
    if len(data) < 3:
        return -1
    min_index = 1
    max_index = 2
    i = 1
    while 2 * i + 1 < len(data):
        min_index = 2 * i + 1
        i = 2 * i + 1
    i = 0
    # Первоначально i = 0, правый потомок = 2
    while 2 * i + 2 < len(data):
        max_index = 2 * i + 2
        i = 2 * i + 2
    return data[min_index] * data[max_index]

# 6. Сравнение двух бинарных деревьев
def is_same_tree(a, b):
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    if a.val != b.val:
        return False
    return is_same_tree(a.left, b.left) and is_same_tree(a.right, b.right)

# 7. Является ли дерево B поддеревом дерева A
def is_subtree(A, B):
    if B is None:
        return True
    if A is None:
        return False
    if is_same_tree(A, B):
        return True
    return is_subtree(A.left, B) or is_subtree(A.right, B)

# 8. Подсчёт зеркальных узлов
def dfs_mirror(left, right):
    if left is None or right is None:
        return 0
    count = 1 if left.val == right.val else 0
    count += dfs_mirror(left.left, right.right)
    count += dfs_mirror(left.right, right.left)
    return count

def count_mirror_twins(root):
    if root is None:
        return 0
    return dfs_mirror(root.left, root.right)

# Тесты
class TestTreeAlgorithms(unittest.TestCase):

    def test_build_tree(self):
        # Для массива [1,2,3,4,5,6,7] ожидаем полное бинарное дерево:
        #           1
        #         /   \
        #       2       3
        #      / \     / \
        #     4   5   6   7
        arr = [1, 2, 3, 4, 5, 6, 7]
        root = build_tree(arr)
        self.assertEqual(root.val, 1)
        self.assertEqual(root.left.val, 2)
        self.assertEqual(root.right.val, 3)
        self.assertEqual(root.left.left.val, 4)
        self.assertEqual(root.left.right.val, 5)
        self.assertEqual(root.right.left.val, 6)
        self.assertEqual(root.right.right.val, 7)

    def test_is_symmetric(self):
        # Симметричное дерево:
        #         1
        #       /   \
        #      2     2
        #     / \   / \
        #    3  4  4   3
        symmetric_arr = [1,2,2,3,4,4,3]
        root = build_tree(symmetric_arr)
        self.assertTrue(is_symmetric(root))
        self.assertTrue(is_symmetric_dfs(root))
        # Несимметричное дерево:
        non_sym_arr = [1,2,2,None,3,None,3]
        root_non = build_tree(non_sym_arr)
        self.assertFalse(is_symmetric(root_non))
        self.assertFalse(is_symmetric_dfs(root_non))

    def test_min_depth(self):
        # Для дерева:
        #      1
        #     / \
        #    2   3
        #         \
        #          4
        # Минимальная глубина = 2 (1 -> 2)
        arr = [1, 2, 3, None, None, None, 4]
        root = build_tree(arr)
        self.assertEqual(min_depth(root), 2)
        # Для дерева из одного элемента:
        self.assertEqual(min_depth(TreeNode(10)), 1)
        # Пустое дерево:
        self.assertEqual(min_depth(None), 0)

    def test_max_min_multiplication(self):
        # Для представления дерева в виде массива,
        # например, полный бинарный дерево [10, 5, 20, 3, 7, 15, 25]
        # Ищем минимальный – идём по левым потомкам:
        #   i = 1 -> 5, затем 2*1+1 = 3 -> 3
        # Правый потомок: i = 2 -> 20, затем 2*2+2 = 6 -> 25
        # Произведение = 3 * 25 = 75
        arr = [10, 5, 20, 3, 7, 15, 25]
        self.assertEqual(max_min_multiplication(arr), 75)
        # Если массив слишком короткий:
        self.assertEqual(max_min_multiplication([1,2]), -1)

    def test_is_same_tree(self):
        # Два одинаковых дерева
        arr1 = [1,2,3,4,5]
        tree1 = build_tree(arr1)
        tree2 = build_tree(arr1)
        self.assertTrue(is_same_tree(tree1, tree2))
        # Изменим одно дерево
        tree2.left.val = 999
        self.assertFalse(is_same_tree(tree1, tree2))

    def test_is_subtree(self):
        # A = полное дерево
        A_arr = [1,2,3,4,5,6,7]
        A = build_tree(A_arr)
        # B – поддерево, содержащее вершину 3 и её потомков [3,6,7]
        B_arr = [3,6,7]
        B = build_tree(B_arr)
        self.assertTrue(is_subtree(A, B))
        # Изменим B: сделаем дерево, которого нет в A
        B2_arr = [2,4,999]
        B2 = build_tree(B2_arr)
        self.assertFalse(is_subtree(A, B2))
        # Если B пустое, оно считается поддеревом
        self.assertTrue(is_subtree(A, None))

    def test_count_mirror_twins(self):
        # Рассмотрим симметричное дерево:
        #           1
        #         /   \
        #        2     2
        #       / \   / \
        #      3   4 4   3
        arr = [1,2,2,3,4,4,3]
        root = build_tree(arr)
        # Зеркальные пары:
        # 2 и 2, 3 и 3, 4 и 4, итого 3 пары (если считать только пары, возникающие в dfs)
        self.assertEqual(count_mirror_twins(root), 3)
        # Для дерева без зеркальных пар:
        arr2 = [1,2,3]
        root2 = build_tree(arr2)
        self.assertEqual(count_mirror_twins(root2), 0)

# Бенчмарки
def benchmark():
    print("\n=== БЕНЧМАРКИ ===")
    
    setup_code = (
        "from __main__ import build_tree, is_symmetric, is_symmetric_dfs, min_depth, max_min_multiplication, "
        "is_same_tree, is_subtree, count_mirror_twins, TreeNode; "
        "import random; "
        "arr = [random.randint(1,1000) for _ in range(1023)]; "  # полное дерево с 1023 элементами
        "root = build_tree(arr); "
        "data = arr[:] "
    )
    
    tests = [
        ("build_tree(arr)", "Восстановление дерева из массива"),
        ("is_symmetric(root)", "Проверка симметричности (BFS)"),
        ("is_symmetric_dfs(root)", "Проверка симметричности (DFS)"),
        ("min_depth(root)", "Поиск минимальной глубины дерева"),
        ("max_min_multiplication(data)", "Произведение min и max элементов дерева в виде массива"),
        ("is_same_tree(root, root)", "Сравнение двух одинаковых деревьев"),
        ("is_subtree(root, build_tree(arr[:7]))", "Проверка, является ли одно дерево поддеревом другого"),
        ("count_mirror_twins(root)", "Подсчёт зеркальных узлов"),
    ]
    
    iterations = 1000
    for code_snip, desc in tests:
        t = timeit.timeit(stmt=code_snip, setup=setup_code, number=iterations)
        print(f"{desc}: {t / iterations:.8f} сек на запуск (среднее за {iterations} итераций)")


if __name__ == "__main__":
    unittest.main(exit=False)
    benchmark()
