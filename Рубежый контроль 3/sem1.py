import unittest
import timeit
import random
import string

# 1. Последовательности из 0 и 1 без двух единиц подряд
def count_no_adjacent_ones(n):
    if n == 0:
        return 1
    if n == 1:
        return 2
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 2
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

# 2. Последовательности из 0 и 1 без трёх единиц подряд
def count_no_three_ones(n):
    if n == 0:
        return 1
    if n == 1:
        return 2
    if n == 2:
        return 4
    dp = [0] * (n + 1)
    dp[0], dp[1], dp[2] = 1, 2, 4
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2] + dp[i - 3]
    return dp[n]

# 3. Наибольшая непрерывная возрастающая подпоследовательность
def longest_continuous_lis(nums):
    if not nums:
        return 0
    max_len = 1
    curr_len = 1
    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:
            curr_len += 1
            if curr_len > max_len:
                max_len = curr_len
        else:
            curr_len = 1
    return max_len

# 4. Треугольник Паскаля
def build_pascal_triangle(n):
    dp = []
    for row in range(n):
        current = [1] * (row + 1)
        for col in range(1, row):
            current[col] = dp[row - 1][col - 1] + dp[row - 1][col]
        dp.append(current)
    return dp

# 5. Максимальная выгода от торговли акциями
def max_profit(prices):
    if not prices:
        return 0
    min_price = prices[0]
    best = 0
    for price in prices[1:]:
        profit = price - min_price
        if profit > best:
            best = profit
        if price < min_price:
            min_price = price
    return best

# 6. Размен монет
def coin_change(coins, amount):
    INF = amount + 1
    dp = [INF] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for c in coins:
            if c <= i:
                dp[i] = min(dp[i], dp[i - c] + 1)
    return dp[amount] if dp[amount] != INF else -1

# 7a. Длина максимального палиндрома-подстроки (расширение от центра)
def longest_palindrome(s):
    if not s:
        return ""
    start, end = 0, 0

    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return r - l - 1

    for i in range(len(s)):
        len1 = expand(i, i)
        len2 = expand(i, i + 1)
        mlen = max(len1, len2)
        if mlen > end - start + 1:
            start = i - (mlen - 1) // 2
            end = i + mlen // 2
    return s[start:end + 1]

# 7b. Длина максимального палиндрома-подстроки (DP)
def longest_palindrome_dp(s):
    n = len(s)
    if n == 0:
        return ""
    dp = [[False] * n for _ in range(n)]
    max_len = 1
    start = 0
    for i in range(n):
        dp[i][i] = True
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and (length == 2 or dp[i + 1][j - 1]):
                dp[i][j] = True
                if length > max_len:
                    max_len = length
                    start = i
    return s[start:start + max_len]

# Тесты
class TestDPSeminar(unittest.TestCase):

    def test_count_no_adjacent_ones(self):
        self.assertEqual(count_no_adjacent_ones(0), 1)
        self.assertEqual(count_no_adjacent_ones(1), 2)
        self.assertEqual(count_no_adjacent_ones(2), 3)
        self.assertEqual(count_no_adjacent_ones(3), 5)
        self.assertEqual(count_no_adjacent_ones(5), 13)

    def test_count_no_three_ones(self):
        self.assertEqual(count_no_three_ones(0), 1)
        self.assertEqual(count_no_three_ones(1), 2)
        self.assertEqual(count_no_three_ones(2), 4)
        self.assertEqual(count_no_three_ones(3), 7)
        self.assertEqual(count_no_three_ones(4), 13)

    def test_longest_continuous_lis(self):
        self.assertEqual(longest_continuous_lis([]), 0)
        self.assertEqual(longest_continuous_lis([1]), 1)
        self.assertEqual(longest_continuous_lis([1,2,2,3,4,1,2,3]), 3)
        self.assertEqual(longest_continuous_lis([5,4,3,2,1]), 1)

    def test_build_pascal_triangle(self):
        self.assertEqual(build_pascal_triangle(0), [])
        self.assertEqual(build_pascal_triangle(1), [[1]])
        self.assertEqual(build_pascal_triangle(5), [
            [1],
            [1,1],
            [1,2,1],
            [1,3,3,1],
            [1,4,6,4,1]
        ])

    def test_max_profit(self):
        self.assertEqual(max_profit([]), 0)
        self.assertEqual(max_profit([7,1,5,3,6,4]), 5)
        self.assertEqual(max_profit([7,6,4,3,1]), 0)

    def test_coin_change(self):
        self.assertEqual(coin_change([1,2,5], 11), 3)
        self.assertEqual(coin_change([2], 3), -1)
        self.assertEqual(coin_change([1], 0), 0)
        self.assertEqual(coin_change([1,3,4], 6), 2)

    def test_longest_palindrome(self):
        self.assertEqual(longest_palindrome(""), "")
        self.assertEqual(longest_palindrome("a"), "a")
        self.assertIn(longest_palindrome("babad"), ["bab","aba"])
        self.assertEqual(longest_palindrome("cbbd"), "bb")

    def test_longest_palindrome_dp(self):
        self.assertEqual(longest_palindrome_dp(""), "")
        self.assertEqual(longest_palindrome_dp("a"), "a")
        self.assertIn(longest_palindrome_dp("babad"), ["bab","aba"])
        self.assertEqual(longest_palindrome_dp("cbbd"), "bb")

# Бенчмарки
def benchmark():
    print("\n=== БЕНЧМАРКИ ===")
    setup = (
        "from __main__ import (count_no_adjacent_ones, count_no_three_ones, longest_continuous_lis, "
        "build_pascal_triangle, max_profit, coin_change, longest_palindrome, longest_palindrome_dp);"
        "import random, string;"
        "arr = [random.randint(0,1) for _ in range(1000)];"
        "prices = [random.randint(1,1000) for _ in range(1000)];"
        "coins = [1,5,10,25];"
        "s_long = ''.join(random.choices(string.ascii_lowercase, k=1000));"
    )
    tests = [
        ("count_no_adjacent_ones(30)",                            "DP без двух единиц подряд"),
        ("count_no_three_ones(30)",                               "DP без трёх единиц подряд"),
        ("longest_continuous_lis(arr)",                           "Непрерывная возрастающая подпоследовательность"),
        ("build_pascal_triangle(100)",                            "Треугольник Паскаля"),
        ("max_profit(prices)",                                    "Макс. прибыль от акций"),
        ("coin_change(coins, 1000)",                              "Размен монет"),
        ("longest_palindrome(s_long)",                            "Палиндром центр. расширение"),
        ("longest_palindrome_dp(s_long)",                         "Палиндром DP"),
    ]
    for code, desc in tests:
        t = timeit.timeit(stmt=code, setup=setup, number=500)
        print(f"{desc}: {t/500:.8f} сек")

if __name__ == "__main__":
    unittest.main(exit=False)
    benchmark()
