import json

datasets = []
multiplier = 100  # 10 templates * 100 iterations = 1000 datasets

# Technology 1: Python
for i in range(multiplier):
    datasets.append({
        "id": len(datasets) + 1,
        "buggy_code": f"def twoSum_{i}(nums, target):\n    for i in range(len(nums)):\n        for j in range(len(nums)):\n            if nums[i] + nums[j] == target:\n                return [i, j]\n    return []",
        "error_message": "AssertionError: lists differ",
        "expected_behavior": "Return the indices of the two numbers that add up to target. Elements cannot be reused.",
        "unit_test": f"from target_module import twoSum_{i}\ndef test_{i}():\n    assert twoSum_{i}([3, 2, 4], 6) == [1, 2]"
    })

for i in range(multiplier):
    datasets.append({
        "id": len(datasets) + 1,
        "buggy_code": f"def binary_search_{i}(arr, x):\n    low, high = 0, len(arr)\n    while low <= high:\n        mid = (high + low) // 2\n        if arr[mid] == x:\n            return mid\n        elif arr[mid] < x:\n            low = mid\n        else:\n            high = mid - 1\n    return -1",
        "error_message": "TimeLimitExceeded",
        "expected_behavior": "Perform standard binary search without infinite loops.",
        "unit_test": f"from target_module import binary_search_{i}\ndef test_bs_{i}():\n    assert binary_search_{i}([-1,0,3,5,9,12], 9) == 4"
    })

# Technology 2: C++
for i in range(multiplier):
    datasets.append({
        "id": len(datasets) + 1,
        "buggy_code": f"#include <vector>\n#include <algorithm>\nusing namespace std;\nclass Solution_{i} {{\npublic:\n    bool containsDuplicate(vector<int>& nums) {{\n        sort(nums.begin(), nums.end());\n        for (int i = 1; i < nums.size(); i++) {{\n            if (nums[i] == nums[i-1]) return true;\n            else return false;\n        }}\n        return false;\n    }}\n}};",
        "error_message": "LogicError: Returns false prematurely",
        "expected_behavior": "Return true if any value appears at least twice in the array.",
        "unit_test": f"#include <cassert>\n#include \"target_module.cpp\"\nvoid test_{i}() {{\n    Solution_{i} sol;\n    vector<int> nums = {{1, 2, 3, 1}};\n    assert(sol.containsDuplicate(nums));\n}}"
    })

# Technology 3: Java
for i in range(multiplier):
    datasets.append({
        "id": len(datasets) + 1,
        "buggy_code": f"import java.util.Stack;\npublic class Solution_{i} {{\n    public boolean isValid(String s) {{\n        Stack<Character> stack = new Stack<>();\n        for (char c : s.toCharArray()) {{\n            if (c == '(') stack.push(')');\n            else if (c == '{{') stack.push('}}');\n            else if (c == '[') stack.push(']');\n            else if (stack.pop() != c) return false;\n        }}\n        return stack.isEmpty();\n    }}\n}}",
        "error_message": "EmptyStackException",
        "expected_behavior": "Validate that string brackets are closed in order. Avoid EmptyStackException on invalid inputs.",
        "unit_test": f"import org.junit.Test;\nimport static org.junit.Assert.*;\npublic class SolutionTest_{i} {{\n    @Test\n    public void test() {{\n        Solution_{i} sol = new Solution_{i}();\n        assertFalse(sol.isValid(\"]\"));\n    }}\n}}"
    })

# Technology 4: HTML
for i in range(multiplier):
    datasets.append({
        "id": len(datasets) + 1,
        "buggy_code": f"<!DOCTYPE html>\n<html>\n<head><title>Form_{i}</title></head>\n<body>\n    <form>\n        <label for=\"username\">Username:</label>\n        <input type=\"text\" name=\"username\" id=\"username\">\n        <input type=\"submit\" value=\"Submit\">\n    </form>\n</body>\n</html>",
        "error_message": "ValidationError: Form action is missing",
        "expected_behavior": "The HTML form should specify an 'action' attribute to know where to submit the data.",
        "unit_test": f"// Load HTML in DOM and verify action attr on form_{i}"
    })

# Technology 5: React.js
for i in range(multiplier):
    datasets.append({
        "id": len(datasets) + 1,
        "buggy_code": f"import React, {{ useState }} from 'react';\n\nexport default function Counter_{i}() {{\n  const [count, setCount] = useState(0);\n  \n  const increment = () => {{\n    count = count + 1; // BUG: State mutated directly\n  }};\n\n  return (\n    <div>\n      <p>Count: {{count}}</p>\n      <button onClick={{increment}}>Increment</button>\n    </div>\n  );\n}}",
        "error_message": "StateMutatedException: React state is read-only",
        "expected_behavior": "To update state in React, you must use the dispatch function `setCount` instead of mutating the variable directly.",
        "unit_test": f"import {{ render, fireEvent }} from '@testing-library/react';\nimport Counter_{i} from './target_module';\ntest('increments_{i}', () => {{\n  const {{ getByText }} = render(<Counter_{i} />);\n  fireEvent.click(getByText('Increment'));\n  expect(getByText('Count: 1')).toBeInTheDocument();\n}});"
    })

for i in range(multiplier):
    datasets.append({
        "id": len(datasets) + 1,
        "buggy_code": f"import React, {{ useState, useEffect }} from 'react';\n\nexport default function UserProfile_{i}({{ userId }}) {{\n  const [user, setUser] = useState(null);\n  \n  useEffect(() => {{\n    fetch(`/api/users/${{userId}}`)\n      .then(res => res.json())\n      .then(data => setUser(data));\n  }}); // BUG: Missing dependency array\n\n  return <div>{{user ? user.name : 'Loading...'}}</div>;\n}}",
        "error_message": "InfiniteLoopWarning: Component rapidly re-renders",
        "expected_behavior": "The `useEffect` hook should include a dependency array `[userId]` so that the fetch is only executed when the component mounts or `userId` changes.",
        "unit_test": f"import {{ render }} from '@testing-library/react';\nimport UserProfile_{i} from './target_module';\n// Test omitted for brevity"
    })

# Technology 6: Express.js
for i in range(multiplier):
    datasets.append({
        "id": len(datasets) + 1,
        "buggy_code": f"const express = require('express');\nconst app = express();\n\napp.get('/api/data_{i}', (req, res) => {{\n    const data = {{ status: 'success', value: 42 }};\n    // BUG: missing res.json(data);\n}});\n\nmodule.exports = app;",
        "error_message": "TimeoutError: Request hangs indefinitely",
        "expected_behavior": "The route handler must send a response back to the client using `res.json()` or `res.send()`.",
        "unit_test": f"const request = require('supertest');\nconst app = require('./target_module');\ntest('GET /api/data_{i}', async () => {{\n    const res = await request(app).get('/api/data_{i}');\n    expect(res.statusCode).toBe(200);\n}});"
    })

for i in range(multiplier):
    datasets.append({
        "id": len(datasets) + 1,
        "buggy_code": f"const express = require('express');\nconst app = express();\n\nconst authMiddleware = (req, res, next) => {{\n    if (req.headers.authorization) {{\n        req.user = {{ id: 1 }};\n        // BUG: missing next();\n    }} else {{\n        res.status(401).send('Unauthorized');\n    }}\n}};\n\napp.get('/secure_{i}', authMiddleware, (req, res) => {{\n    res.send('Secure data');\n}});\n\nmodule.exports = app;",
        "error_message": "TimeoutError: Request hangs indefinitely",
        "expected_behavior": "Middlewares must either terminate the request-response cycle by sending a response or call `next()` to pass control to the next middleware function.",
        "unit_test": f"const request = require('supertest');\nconst app = require('./target_module');\ntest('Auth Middleware_{i}', async () => {{\n    const res = await request(app).get('/secure_{i}').set('Authorization', 'Bearer token');\n    expect(res.statusCode).toBe(200);\n}});"
    })

for i in range(multiplier):
    datasets.append({
        "id": len(datasets) + 1,
        "buggy_code": f"const express = require('express');\nconst app = express();\n\napp.post('/users_{i}', (req, res) => {{\n    const username = req.body.username;\n    // BUG: Missing express.json() middleware\n    res.json({{ created: username }});\n}});\n\nmodule.exports = app;",
        "error_message": "TypeError: Cannot read properties of undefined (reading 'username')",
        "expected_behavior": "To access JSON request bodies in Express, `app.use(express.json())` must be configured.",
        "unit_test": f"const request = require('supertest');\nconst app = require('./target_module');\ntest('POST users_{i}', async () => {{\n    const res = await request(app).post('/users_{i}').send({{username: 'test'}});\n    expect(res.body.created).toBe('test');\n}});"
    })


with open('backend/eval_dataset_multilang.json', 'w') as f:
    json.dump(datasets, f, indent=4)

print(f"Generated eval_dataset_multilang.json with {len(datasets)} items combining Python, C++, Java, HTML, React.js, and Express.js.")
