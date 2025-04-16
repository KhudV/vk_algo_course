import unittest
import timeit
import random

# 1. Нахождение корня числа (ближайшее целое) с помощью бинарного поиска
def binary_search_sqrt(target):
    l = 0
    r = target
    while l <= r:
        mid = (l + r) // 2
        if mid * mid > target:
            r = mid - 1
        elif mid * mid < target:
            l = mid + 1
        else:
            return mid
    return r

# 2. Очень лёгкая задача: вычисление минимального времени для копирования N документов двумя ксероксами с заданными скоростями
def copy_time(n, x, y):
    if n <= 0:
        return 0
    if n == 1:
        return min(x, y)
    l = 0
    r = (n - 1) * max(x, y)
    while l + 1 < r:
        mid = (l + r) // 2
        copies = mid // x + mid // y
        if copies < n - 1:
            l = mid
        else:
            r = mid
    return r + min(x, y)

# 3. Кормление животных
def feed_animals(animals, food):
    if not animals or not food:
        return 0
    animals_sorted = sorted(animals)
    food_sorted = sorted(food)
    count = 0
    for f in food_sorted:
        if count < len(animals_sorted) and f >= animals_sorted[count]:
            count += 1
        if count == len(animals_sorted):
            break
    return count

# 4. Нахождение разницы между строками
def extra_letter(a, b):
    hash_map = {}
    for ch in b:
        hash_map[ch] = hash_map.get(ch, 0) + 1
    for ch in a:
        if ch in hash_map:
            hash_map[ch] -= 1
            if hash_map[ch] == 0:
                del hash_map[ch]
    for ch, count in hash_map.items():
        if count > 0:
            return ch
    return ""

# 5. Сумма двух элементов
def two_sum(data, target):
    cache = {}
    for i, num in enumerate(data):
        diff = target - num
        if diff in cache:
            return [cache[diff], i]
        cache[num] = i
    return []

# 6. Сортировка Шелла
def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            j = i
            while j >= gap and arr[j] < arr[j - gap]:
                arr[j], arr[j - gap] = arr[j - gap], arr[j]
                j -= gap
        gap //= 2
    return arr

# 7. Группировка анаграмм: группирует слова, являющиеся анаграммами друг друга
def group_anagrams(strs):
    groups = {}
    for word in strs:
        key = ''.join(sorted(word))
        if key not in groups:
            groups[key] = []
        groups[key].append(word)
    return list(groups.values())

# Тесты
class TestSeminarAlgorithms(unittest.TestCase):

    def test_binary_search_sqrt(self):
        self.assertEqual(binary_search_sqrt(0), 0)
        self.assertEqual(binary_search_sqrt(1), 1)
        self.assertEqual(binary_search_sqrt(4), 2)
        self.assertEqual(binary_search_sqrt(8), 2)   # sqrt(8) округляется вниз до 2
        self.assertEqual(binary_search_sqrt(9), 3)
        self.assertEqual(binary_search_sqrt(10), 3)

    def test_copy_time(self):
        self.assertEqual(copy_time(4, 1, 3), 4)       # 5 копий, x=1, y=2
        self.assertEqual(copy_time(1, 3, 5), 3)         # для 1 копии возвращаем min(x,y)
        self.assertEqual(copy_time(10, 1, 1), 6)

    def test_feed_animals(self):
        self.assertEqual(feed_animals([3, 4, 7], [8, 1, 2]), 1)
        self.assertEqual(feed_animals([3, 8, 1, 4], [1, 1, 2]), 1)
        self.assertEqual(feed_animals([1, 2, 2], [7, 1]), 2)
        self.assertEqual(feed_animals([8, 2, 3, 2], [1, 4, 3, 8]), 3)
        self.assertEqual(feed_animals([], [1, 4]), 0)
        self.assertEqual(feed_animals([1, 2], []), 0)

    def test_extra_letter(self):
        self.assertEqual(extra_letter("uio", "oeiu"), "e")
        self.assertEqual(extra_letter("fe", "efo"), "o")
        self.assertEqual(extra_letter("ab", "ab"), "")
        self.assertEqual(extra_letter("bbb", "bbbb"), "b")

    def test_two_sum(self):
        self.assertEqual(two_sum([1, 2, 3, 4, 5, 6, 7], 12), [4, 6])
        self.assertEqual(two_sum([3, 2, 4], 6), [1, 2])
        self.assertEqual(two_sum([1, 2, 3, 4, 5], 100), [])
        self.assertEqual(two_sum([], 10), [])

    def test_shell_sort(self):
        self.assertEqual(shell_sort([12, 3, 18, 1, 5]), [1, 3, 5, 12, 18])
        self.assertEqual(shell_sort([]), [])
        self.assertEqual(shell_sort([1]), [1])
        self.assertEqual(shell_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_group_anagrams(self):
        input_data = ["eat", "tea", "tan", "ate", "nat", "bat"]
        result = group_anagrams(input_data)
        # Сортируем внутренние списки и затем внешний список для сравнения
        def normalize(groups):
            return sorted([sorted(group) for group in groups])
        expected_groups = [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
        self.assertEqual(normalize(result), normalize(expected_groups))
        
        input_data2 = ["won", "now", "aaa", "ooo", "ooo"]
        result2 = group_anagrams(input_data2)
        expected_groups2 = [["aaa"], ["ooo", "ooo"], ["now", "won"]]
        self.assertEqual(normalize(result2), normalize(expected_groups2))

# Бенчмарки
def benchmark():
    print("\n=== БЕНЧМАРКИ ===")
    
    setup_code = (
        "from __main__ import binary_search_sqrt, copy_time, feed_animals, extra_letter, two_sum, shell_sort, group_anagrams; "
        "import random"
    )
    
    tests = [
        ("binary_search_sqrt(10**6)", "Нахождение корня числа (binary search sqrt)"),
        ("copy_time(1000, 3, 5)", "Подсчёт времени копирования документов"),
        ("feed_animals([random.randint(1,10) for _ in range(10000)], [random.randint(1,10) for _ in range(10000)])", "Кормление животных"),
        ("extra_letter('abcdef', 'fabcdeg')", "Нахождение дополнительной буквы"),
        ("two_sum([random.randint(1,1000) for _ in range(10000)], 1500)", "Поиск двух чисел с заданной суммой"),
        ("shell_sort([random.randint(1,10000) for _ in range(1000)])", "Сортировка Шелла"),
        ("group_anagrams([''.join(random.sample('abcdef', 6)) for _ in range(1000)])", "Группировка анаграмм"),
    ]
    
    iterations = 1000
    for code, desc in tests:
        t = timeit.timeit(stmt=code, setup=setup_code, number=iterations)
        print(f"{desc}: {t / iterations:.8f} сек на запуск (среднее за {iterations} итераций)")

if __name__ == "__main__":
    unittest.main(exit=False)
    benchmark()

