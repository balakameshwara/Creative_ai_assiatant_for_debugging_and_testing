import json

dsa_debugger_snippets = [
    {
        "id": i + 11,
        "buggy_code": f"def bubble_sort_{i}(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] < arr[j+1]: # BUG: should be >\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr",
        "error_message": "AssertionError: lists differ",
        "expected_behavior": "Sort the array in ascending order using bubble sort logic.",
        "unit_test": f"from target_module import bubble_sort_{i}\ndef test_sort_{i}():\n    assert bubble_sort_{i}([64, 34, 25, 12, 22, 11, 90]) == [11, 12, 22, 25, 34, 64, 90]"
    } for i in range(10)
] + [
    {
        "id": i + 21,
        "buggy_code": f"def binary_search_{i}(arr, x):\n    low, high = 0, len(arr)\n    while low <= high:\n        mid = (high + low) // 2\n        if arr[mid] < x:\n            low = mid + 1\n        elif arr[mid] > x:\n            high = mid - 1\n        else:\n            return mid\n    return -1",
        "error_message": "IndexError: list index out of range",
        "expected_behavior": "Perform binary search. High should be initialized to len(arr) - 1.",
        "unit_test": f"from target_module import binary_search_{i}\ndef test_bs_{i}():\n    assert binary_search_{i}([2, 3, 4, 10, 40], 10) == 3\n    assert binary_search_{i}([2, 3, 4, 10, 40], 50) == -1"
    } for i in range(10)
] + [
     {
        "id": i + 31,
        "buggy_code": f"def dfs_{i}(graph, start, visited=None):\n    if visited is None: visited = set()\n    visited.add(start)\n    for next in graph[start] - visited:\n        dfs_{i}(graph, next, visited)\n    return visited",
        "error_message": "TypeError: unsupported operand type(s) for -: 'list' and 'set'",
        "expected_behavior": "Perform Depth First Search. The graph edges are represented as lists, not sets.",
        "unit_test": f"from target_module import dfs_{i}\ndef test_dfs_{i}():\n    graph = {{'0': ['1', '2'], '1': ['2'], '2': ['0', '3'], '3': ['3']}}\n    result = dfs_{i}(graph, '2')\n    assert '3' in result\n    assert '0' in result"
    } for i in range(10)
] + [
    {
        "id": i + 41,
        "buggy_code": f"def fib_dp_{i}(n):\n    if n <= 1: return n\n    dp = [0] * n\n    dp[0] = 0\n    dp[1] = 1\n    for i in range(2, n+1):\n        dp[i] = dp[i-1] + dp[i-2]\n    return dp[n]",
        "error_message": "IndexError: list assignment index out of range",
        "expected_behavior": "Return the nth Fibonacci number taking O(n) space. Ensure array allocation handles size n+1 properly.",
        "unit_test": f"from target_module import fib_dp_{i}\ndef test_fib_{i}():\n    assert fib_dp_{i}(9) == 34\n    assert fib_dp_{i}(0) == 0"
    } for i in range(10)
] + [
    {
        "id": i + 51,
        "buggy_code": f"class Node:\n    def __init__(self, data): self.data = data; self.next = None\nclass LinkedList_{i}:\n    def __init__(self): self.head = None\n    def push(self, data):\n        new_node = Node(data)\n        new_node.next = self.head\n        self.head = new_node\n    def pop(self):\n        if not self.head: return None\n        val = self.head.data\n        self.head = None # BUG: should be self.head.next\n        return val",
        "error_message": "AssertionError: list broken",
        "expected_behavior": "Pop the top element from the Linked List correctly by moving the head to head.next.",
        "unit_test": f"from target_module import LinkedList_{i}\ndef test_ll_{i}():\n    ll = LinkedList_{i}()\n    ll.push(1); ll.push(2); ll.push(3)\n    assert ll.pop() == 3\n    assert ll.pop() == 2"
    } for i in range(10)
]

with open('eval_dataset.json', 'r') as f:
    existing = json.load(f)

existing.extend(dsa_debugger_snippets)

with open('eval_dataset.json', 'w') as f:
    json.dump(existing, f, indent=4)

print(f"Debugger dataset expanded. Total items now: {len(existing)}")
