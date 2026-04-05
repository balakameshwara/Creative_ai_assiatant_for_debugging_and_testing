
import unittest

# --- Target Code ---

def add(a, b):
    return a + b

# -------------------

# --- Generated Tests ---
import pytest

# The function to be tested
def add(a, b):
    return a + b

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),               # Positive integers
    (-1, -1, -2),            # Negative integers
    (-1, 5, 4),              # Mixed signs
    (0, 0, 0),               # Zeroes
    (1000000, 2000000, 3000000), # Large integers
])
def test_add_integers(a, b, expected):
    """Test addition with various integer combinations."""
    assert add(a, b) == expected

def test_add_floats():
    """Test addition with floating point numbers using approximation."""
    # Using pytest.approx to handle floating point precision issues (e.g., 0.1 + 0.2)
    assert add(0.1, 0.2) == pytest.approx(0.3)
    assert add(-1.5, 2.5) == 1.0

def test_add_strings():
    """Test that the function correctly concatenates strings (polymorphism)."""
    assert add("hello", " world") == "hello world"

def test_add_lists():
    """Test that the function correctly merges lists."""
    assert add([1, 2], [3, 4]) == [1, 2, 3, 4]

def test_add_type_mismatch():
    """Test that adding incompatible types raises a TypeError."""
    with pytest.raises(TypeError):
        add(1, "string")

def test_add_none():
    """Test that passing None raises a TypeError."""
    with pytest.raises(TypeError):
        add(None, 5)
# -----------------------

if __name__ == '__main__':
    unittest.main()
