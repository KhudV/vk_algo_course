import timeit
import unittest
from collections import deque


# Проверка, является ли связный список циклическим
class ListNode:
    def __init__(self, val=0):
        self.val = val
        self.next = None


def has_cycle(head):
    if not head or not head.next:
        return False
    slow, fast = head, head.next
    while slow != fast:
        if not fast or not fast.next:
            return False
        slow = slow.next
        fast = fast.next.next
    return True


# Разворот односвязного списка
def reverse_linked_list(head):
    prev, current = None, head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev


# Поиск середины списка
def middle_node(head):
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


# Удаление элемента из односвязного списка
def remove_elements(head, val):
    dummy = ListNode()
    dummy.next = head
    prev, cur = dummy, head
    while cur:
        if cur.val == val:
            prev.next = cur.next
        else:
            prev = cur
        cur = cur.next
    return dummy.next


# Проверка, является ли одна строка подстрокой другой
def is_subsequence_queue(a, b):
    q = deque(a)
    for char in b:
        if q and q[0] == char:
            q.popleft()
    return not q


def is_subsequence_pointers(a, b):
    i, j = 0, 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1
        j += 1
    return i == len(a)


# Проверка, является ли слово палиндромом
def is_palindrome_stack(s):
    stack = list(s)
    for char in s:
        if char != stack.pop():
            return False
    return True


def is_palindrome_pointers(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True


# Слияние двух отсортированных списков
def merge_two_lists(l1, l2):
    dummy = ListNode()
    cur = dummy
    while l1 and l2:
        if l1.val < l2.val:
            cur.next = l1
            l1 = l1.next
        else:
            cur.next = l2
            l2 = l2.next
        cur = cur.next
    cur.next = l1 if l1 else l2
    return dummy.next


# Тесты
class TestAlgorithms(unittest.TestCase):

    def test_has_cycle(self):
        head = ListNode(1)
        head.next = ListNode(2)
        head.next.next = head  # Цикл
        self.assertTrue(has_cycle(head))

        head = ListNode(1)
        head.next = ListNode(2)
        self.assertFalse(has_cycle(head))

    def test_reverse_linked_list(self):
        head = ListNode(1)
        head.next = ListNode(2)
        head.next.next = ListNode(3)
        new_head = reverse_linked_list(head)
        self.assertEqual(new_head.val, 3)
        self.assertEqual(new_head.next.val, 2)

    def test_middle_node(self):
        head = ListNode(1)
        head.next = ListNode(2)
        head.next.next = ListNode(3)
        self.assertEqual(middle_node(head).val, 2)

    def test_remove_elements(self):
        head = ListNode(1)
        head.next = ListNode(2)
        head.next.next = ListNode(6)
        head = remove_elements(head, 6)
        self.assertEqual(head.next.next, None)

    def test_is_subsequence(self):
        self.assertTrue(is_subsequence_queue("abc", "ahbgdc"))
        self.assertFalse(is_subsequence_queue("axc", "ahbgdc"))
        self.assertTrue(is_subsequence_pointers("abc", "ahbgdc"))
        self.assertFalse(is_subsequence_pointers("axc", "ahbgdc"))

    def test_is_palindrome(self):
        self.assertTrue(is_palindrome_stack("racecar"))
        self.assertFalse(is_palindrome_stack("hello"))
        self.assertTrue(is_palindrome_pointers("racecar"))
        self.assertFalse(is_palindrome_pointers("hello"))

    def test_merge_two_lists(self):
        l1 = ListNode(1)
        l1.next = ListNode(3)
        l2 = ListNode(2)
        l2.next = ListNode(4)
        merged = merge_two_lists(l1, l2)
        self.assertEqual(merged.val, 1)
        self.assertEqual(merged.next.val, 2)
        self.assertEqual(merged.next.next.val, 3)


# Бенчмарки
def benchmark():
    setup_code = """
from __main__ import (
    ListNode, has_cycle, reverse_linked_list, middle_node, remove_elements, 
    is_subsequence_queue, is_subsequence_pointers, 
    is_palindrome_stack, is_palindrome_pointers, merge_two_lists
)"""

    test_cases = [
        ("has_cycle(ListNode(1))", "Проверка цикла в списке"),
        ("reverse_linked_list(ListNode(1))", "Разворот списка"),
        ("middle_node(ListNode(1))", "Поиск середины списка"),
        ("remove_elements(ListNode(1), 1)", "Удаление элемента из списка"),
        ("is_subsequence_queue('abcdef', 'aebdfc')", "Подстрока (очередь)"),
        ("is_subsequence_pointers('abcdef', 'aebdfc')", "Подстрока (указатели)"),
        ("is_palindrome_stack('racecar')", "Палиндром (стек)"),
        ("is_palindrome_pointers('racecar')", "Палиндром (указатели)")
    ]

    for code, desc in test_cases:
        time = timeit.timeit(stmt=code, setup=setup_code, number=10000)
        print(f"{desc}: {time:.5f} сек")


if __name__ == "__main__":
    unittest.main(exit=False)
    benchmark()
