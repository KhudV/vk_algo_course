import unittest
import timeit
import random
import string

# 1. Максимальная сумма подмассива фиксированной длины
def max_subarray_sum(arr, k):
    n = len(arr)
    if n < k or k <= 0:
        return None
    current_sum = sum(arr[:k])
    max_sum = current_sum
    for i in range(k, n):
        current_sum += arr[i] - arr[i - k]
        if current_sum > max_sum:
            max_sum = current_sum
    return max_sum

# 2. Subarray Sum Equals K
def subarray_sum(nums, k):
    prefix_sum = 0
    prefix_count = {0: 1}
    count = 0
    for num in nums:
        prefix_sum += num
        needed = prefix_sum - k
        count += prefix_count.get(needed, 0)
        prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1
    return count

# 3. Максимальная длина подмассива с равным числом нулей и единиц
def find_max_length(nums):
    prefix_sum = 0
    index_map = {0: -1}
    max_len = 0
    for i, num in enumerate(nums):
        if num == 0:
            prefix_sum -= 1
        else:
            prefix_sum += 1
        if prefix_sum in index_map:
            length = i - index_map[prefix_sum]
            if length > max_len:
                max_len = length
        else:
            index_map[prefix_sum] = i
    return max_len

# 4. Pivot Index of an Array
def pivot_index(nums):
    total_sum = sum(nums)
    left_sum = 0
    for i, num in enumerate(nums):
        if left_sum == total_sum - left_sum - num:
            return i
        left_sum += num
    return -1

# 5. Баланс скобок с разрешёнными удалениями
def can_make_valid_with_deletions(s, k):
    balance = 0
    extra_closed = 0
    for ch in s:
        if ch == '(':
            balance += 1
        else:
            if balance > 0:
                balance -= 1
            else:
                extra_closed += 1
    total_needed = balance + extra_closed
    return total_needed <= k

# Тесты
class TestSeminar4Algorithms(unittest.TestCase):

    def test_max_subarray_sum(self):
        self.assertEqual(max_subarray_sum([1,2,3,4,5], 2), 9)
        self.assertEqual(max_subarray_sum([5, -1, 5], 2), 4)
        self.assertEqual(max_subarray_sum([5, 1, 5], 2), 6)
        self.assertEqual(max_subarray_sum([1,2,3], 4), None)
        self.assertEqual(max_subarray_sum([], 1), None)

    def test_subarray_sum(self):
        self.assertEqual(subarray_sum([1,1,1], 2), 2)
        self.assertEqual(subarray_sum([1,2,3], 3), 2)
        self.assertEqual(subarray_sum([], 0), 0)
        self.assertEqual(subarray_sum([3,4,7,2,-3,1,4,2], 7), 4)

    def test_find_max_length(self):
        self.assertEqual(find_max_length([0,1]), 2)
        self.assertEqual(find_max_length([0,1,0]), 2)
        self.assertEqual(find_max_length([0,0,1,1,0,1,0,1]), 8)
        self.assertEqual(find_max_length([], ), 0)

    def test_pivot_index(self):
        self.assertEqual(pivot_index([1,7,3,6,5,6]), 3)
        self.assertEqual(pivot_index([1,2,3]), -1)
        self.assertEqual(pivot_index([2,1,-1]), 0)
        self.assertEqual(pivot_index([],), -1)

    def test_can_make_valid_with_deletions(self):
        self.assertTrue(can_make_valid_with_deletions("()()", 0))
        self.assertFalse(can_make_valid_with_deletions(")(()", 1))
        self.assertFalse(can_make_valid_with_deletions(")(((", 2))
        self.assertTrue(can_make_valid_with_deletions("", 0))
        self.assertTrue(can_make_valid_with_deletions("(()))(", 2))

# Бенчмарки
def benchmark():
    print("\n=== БЕНЧМАРКИ ===")
    setup = (
        "from __main__ import (max_subarray_sum, subarray_sum, find_max_length, pivot_index, can_make_valid_with_deletions);"
        "import random, string;"
        "arr = [random.randint(-1000,1000) for _ in range(10000)];"
        "nums = [random.randint(-10,10) for _ in range(10000)];"
        "binarr = [random.choice([0,1]) for _ in range(10000)];"
        "s = ''.join(random.choice('()') for _ in range(10000));"
    )
    tests = [
        ("max_subarray_sum(arr, 500)",               "Max subarray sum (fixed length)"),
        ("subarray_sum(nums, 0)",                    "Subarray sum equals K"),
        ("find_max_length(binarr)",                  "Max length equal zeros and ones"),
        ("pivot_index(arr)",                         "Pivot index"),
        ("can_make_valid_with_deletions(s, 100)",    "Bracket balance with deletions"),
    ]
    for stmt, desc in tests:
        t = timeit.timeit(stmt=stmt, setup=setup, number=200)
        print(f"{desc}: {t/200:.6f} сек")

if __name__ == "__main__":
    unittest.main(exit=False)
    benchmark()
