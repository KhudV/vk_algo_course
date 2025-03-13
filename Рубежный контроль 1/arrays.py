import unittest
import timeit

# Функции

def twoSum(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
    return []

def reverseArray(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr

def reverseArrayHelper(arr, left, right):
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1

def rotateArray(arr, k):
    n = len(arr)
    if n == 0:
        return arr
    k %= n
    reverseArray(arr)
    reverseArrayHelper(arr, 0, k - 1)
    reverseArrayHelper(arr, k, n - 1)
    return arr

def rotateArray_cyclic(arr, k):
    n = len(arr)
    k %= n
    count = 0  # Считаем количество перемещённых элементов
    start = 0
    while count < n:
        current = start
        prev = arr[start]
        while True:
            next_idx = (current + k) % n
            arr[next_idx], prev = prev, arr[next_idx]
            current = next_idx
            count += 1
            if start == current:  # Цикл замкнулся
                break
        start += 1
    return arr

def merge_sorted_arrays(arr1, arr2):
    merged = []
    i, j = 0, 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            merged.append(arr1[i])
            i += 1
        else:
            merged.append(arr2[j])
            j += 1
    merged.extend(arr1[i:])
    merged.extend(arr2[j:])
    return merged

def merge(arr1, arr2):
    m = len(arr1) - len(arr2)
    i = m - 1
    j = len(arr2) - 1
    k = len(arr1) - 1
    while j >= 0:
        if i >= 0 and arr1[i] > arr2[j]:
            arr1[k] = arr1[i]
            i -= 1
        else:
            arr1[k] = arr2[j]
            j -= 1
        k -= 1
    return arr1

def sort_binary_array(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        if arr[left] == 0:
            left += 1
        elif arr[right] == 1:
            right -= 1
        else:
            arr[left], arr[right] = arr[right], arr[left]
            left += 1
            right -= 1
    return arr

def sortColors(nums):
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
    return nums

def evenFirst(arr):
    evenIndex = 0
    for i in range(len(arr)):
        if arr[i] % 2 == 0:
            arr[i], arr[evenIndex] = arr[evenIndex], arr[i]
            evenIndex += 1
    return arr

def moveZerosToEnd(arr):
    nonZeroIndex = 0
    for i in range(len(arr)):
        if arr[i] != 0:
            arr[i], arr[nonZeroIndex] = arr[nonZeroIndex], arr[i]
            nonZeroIndex += 1
    return arr

# Тесты для каждого алгоритма

class TestAlgorithms(unittest.TestCase):

    def test_twoSum(self):
        self.assertEqual(twoSum([1, 2, 3, 4, 5, 6, 7], 9), [1, 6])  # 2 + 7 = 9
        self.assertEqual(twoSum([1, 3, 5, 7], 8), [0, 3])              # 1 + 7 = 8
        self.assertEqual(twoSum([1, 2, 3, 4, 5], 100), [])
        self.assertEqual(twoSum([], 10), [])

    def test_reverseArray(self):
        self.assertEqual(reverseArray([1, 2, 3, 4, 5]), [5, 4, 3, 2, 1])
        self.assertEqual(reverseArray([]), [])
        self.assertEqual(reverseArray([1]), [1])

    def test_rotateArray(self):
        self.assertEqual(rotateArray([1, 2, 3, 4, 5, 6, 7], 3), [5, 6, 7, 1, 2, 3, 4])
        # Сдвиг на 0 должен вернуть исходный массив
        self.assertEqual(rotateArray([1, 2, 3], 0), [1, 2, 3])
        # Сдвиг на длину массива (или кратное длине) — массив не меняется
        self.assertEqual(rotateArray([1, 2, 3, 4], 4), [1, 2, 3, 4])
        # Если k больше длины массива (используется операция mod)
        self.assertEqual(rotateArray([1, 2, 3, 4], 5), [4, 1, 2, 3])

        self.assertEqual(rotateArray_cyclic([1, 2, 3, 4, 5, 6, 7], 3), [5, 6, 7, 1, 2, 3, 4])
        # Сдвиг на 0 должен вернуть исходный массив
        self.assertEqual(rotateArray_cyclic([1, 2, 3], 0), [1, 2, 3])
        # Сдвиг на длину массива (или кратное длине) — массив не меняется
        self.assertEqual(rotateArray_cyclic([1, 2, 3, 4], 4), [1, 2, 3, 4])
        # Если k больше длины массива (используется операция mod)
        self.assertEqual(rotateArray_cyclic([1, 2, 3, 4], 5), [4, 1, 2, 3])

    def test_merge_sorted_arrays(self):
        self.assertEqual(merge_sorted_arrays([1, 3, 5], [2, 4, 6]), [1, 2, 3, 4, 5, 6])
        self.assertEqual(merge_sorted_arrays([], [1, 2]), [1, 2])
        self.assertEqual(merge_sorted_arrays([1, 2], []), [1, 2])
        self.assertEqual(merge_sorted_arrays([1, 3], [2, 4, 5, 6]), [1, 2, 3, 4, 5, 6])

    def test_merge(self):
        # arr1 имеет достаточный запас (последние элементы — 0)
        self.assertEqual(merge([1, 3, 5, 0, 0, 0], [2, 4, 6]), [1, 2, 3, 4, 5, 6])
        self.assertEqual(merge([2, 0], [1]), [1, 2])
        # Дополнительный тест: если в arr1 уже есть ноль как действительное число
        self.assertEqual(merge([1, 2, 3, 0, 0], [0, 4]), [0, 1, 2, 3, 4])

    def test_sort_binary_array(self):
        self.assertEqual(sort_binary_array([0, 1, 0, 1, 1, 0]), [0, 0, 0, 1, 1, 1])
        self.assertEqual(sort_binary_array([1, 1, 1, 0, 0]), [0, 0, 1, 1, 1])
        self.assertEqual(sort_binary_array([0, 0, 0]), [0, 0, 0])
        self.assertEqual(sort_binary_array([1, 1, 1]), [1, 1, 1])
        self.assertEqual(sort_binary_array([]), [])

    def test_sortColors(self):
        self.assertEqual(sortColors([2, 0, 2, 1, 1, 0]), [0, 0, 1, 1, 2, 2])
        self.assertEqual(sortColors([0]), [0])
        self.assertEqual(sortColors([1, 2, 0]), [0, 1, 2])
        self.assertEqual(sortColors([]), [])

    def test_evenFirst(self):
        self.assertEqual(evenFirst([7, 3, 2, 4, 1, 11, 8, 9]), [2, 4, 8, 3, 1, 11, 7, 9])
        self.assertEqual(evenFirst([2, 4, 6, 1, 3, 5]), [2, 4, 6, 1, 3, 5])
        self.assertEqual(evenFirst([1, 3, 5]), [1, 3, 5])
        self.assertEqual(evenFirst([]), [])

    def test_moveZerosToEnd(self):
        self.assertEqual(moveZerosToEnd([0, 0, 1, 0, 3, 12]), [1, 3, 12, 0, 0, 0])
        self.assertEqual(moveZerosToEnd([0, 33, 57, 88, 60, 0, 0, 80, 99]), [33, 57, 88, 60, 80, 99, 0, 0, 0])
        self.assertEqual(moveZerosToEnd([0, 0, 0, 18, 16, 0, 0, 77, 99]), [18, 16, 77, 99, 0, 0, 0, 0, 0])
        self.assertEqual(moveZerosToEnd([1, 2, 3]), [1, 2, 3])
        self.assertEqual(moveZerosToEnd([]), [])

# Бенчмарки

def benchmark():
    print("\n=== БЕНЧМАРКИ ===")

    setup_code = """
from __main__ import (twoSum, reverseArray, rotateArray, rotateArray_cyclic, merge_sorted_arrays, 
merge, sort_binary_array, sortColors, evenFirst, moveZerosToEnd)
import random
arr = list(range(10000))
target = arr[5000] + arr[5001]
arr2 = list(range(5000, 10000))
"""

    tests = [
        ("twoSum(arr, target)", "Поиск двух чисел в отсортированном массиве"),
        ("reverseArray(arr)", "Разворот массива"),
        ("rotateArray(arr, 1234)", "Развернуть часть массива"),
        ("rotateArray_cyclic(arr, 1234)", "Развернуть часть массива (второй способ)"),
        ("merge_sorted_arrays(arr, arr2)", "Слияние отсортированных массивов"),
        ("merge(arr, arr2)", "Слияние отсортированных массивов (второй способ)"),
        ("sort_binary_array([random.choice([0, 1]) for _ in range(10000)])", "Сортировка бинарного массива"),
        ("sortColors([random.choice([0, 1, 2]) for _ in range(10000)])", "Сортировка массива цветов"),
        ("evenFirst([random.randint(1, 100) for _ in range(10000)])", "Чётные числа в начало массива"),
        ("moveZerosToEnd([0 if random.random() < 0.2 else random.randint(1, 100) for _ in range(10000)])", "Перемещение нулей в конец"),
    ]

    iterations = 10000

    for code, desc in tests:
        time = timeit.timeit(stmt=code, setup=setup_code, number=iterations)
        print(f"{desc}: {time / iterations:.8f} сек на запуск (среднее за {iterations} итераций)")



if __name__ == "__main__":
    unittest.main(exit=False)
    benchmark()
