import json

dsa_tester_snippets = [
    {
        "id": i + 6, # Tester dataset ended at 5
        "code": f"def quicksort_{i}(arr):\n    if len(arr) <= 1: return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort_{i}(left) + middle + quicksort_{i}(right)",
        "context": "Implement standard QuickSort on an array of integers. Expected O(N log N) performance."
    } for i in range(10)
] + [
    {
        "id": i + 16,
        "code": f"def kruskal_mst_{i}(graph_edges, num_vertices):\n    parent = list(range(num_vertices))\n    def find(i):\n        if parent[i] == i: return i\n        return find(parent[i])\n    def union(i, j):\n        root_i = find(i)\n        root_j = find(j)\n        parent[root_i] = root_j\n    mst, w_sum = [], 0\n    graph_edges.sort(key=lambda item: item[2])\n    for u, v, weight in graph_edges:\n        if find(u) != find(v):\n            union(u, v)\n            mst.append((u, v, weight))\n            w_sum += weight\n    return mst, w_sum",
        "context": "Implement Kruskal's Algorithm to find the Minimum Spanning Tree given an edge list [(u,v,w)] and number of vertices."
    } for i in range(10)
] + [
    {
        "id": i + 26,
        "code": f"def longest_common_subsequence_{i}(X, Y):\n    m, n = len(X), len(Y)\n    L = [[0]*(n+1) for i in range(m+1)]\n    for i in range(1, m+1):\n        for j in range(1, n+1):\n            if X[i-1] == Y[j-1]:\n                L[i][j] = L[i-1][j-1] + 1\n            else:\n                L[i][j] = max(L[i-1][j], L[i][j-1])\n    return L[m][n]",
        "context": "Find the length of the Longest Common Subsequence of two strings X and Y using Dynamic Programming."
    } for i in range(10)
] + [
    {
        "id": i + 36,
        "code": f"class TrieNode_{i}:\n    def __init__(self): self.children = {{}}; self.is_end = False\nclass Trie_{i}:\n    def __init__(self): self.root = TrieNode_{i}()\n    def insert(self, word):\n        node = self.root\n        for char in word:\n            if char not in node.children:\n                node.children[char] = TrieNode_{i}()\n            node = node.children[char]\n        node.is_end = True\n    def search(self, word):\n        node = self.root\n        for char in word:\n            if char not in node.children: return False\n            node = node.children[char]\n        return node.is_end",
        "context": "A standard Trie (Prefix Tree) implementation with insert and search methods for strings."
    } for i in range(10)
] + [
     {
        "id": i + 46,
        "code": f"def knapsack_01_{i}(W, wt, val, n):\n    K = [[0 for w in range(W + 1)] for i in range(n + 1)]\n    for i in range(n + 1):\n        for w in range(W + 1):\n            if i == 0 or w == 0:\n                K[i][w] = 0\n            elif wt[i-1] <= w:\n                K[i][w] = max(val[i-1] + K[i-1][w-wt[i-1]],  K[i-1][w])\n            else:\n                K[i][w] = K[i-1][w]\n    return K[n][W]",
        "context": "Standard 0/1 Knapsack dynamic programming algorithm to find the maximum value of items that can be packed within a weight limit W."
    } for i in range(10)
]

with open('eval_tester_dataset.json', 'r') as f:
    existing = json.load(f)

existing.extend(dsa_tester_snippets)

with open('eval_tester_dataset.json', 'w') as f:
    json.dump(existing, f, indent=4)

print(f"Tester dataset expanded. Total items now: {len(existing)}")
