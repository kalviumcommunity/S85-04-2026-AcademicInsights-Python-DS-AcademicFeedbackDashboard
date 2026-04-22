"""
Simple NumPy Mathematical Operations Examples
Focused examples for demonstrating basic array arithmetic.
"""

import numpy as np

# 1. Element-Wise Operations
def simple_element_wise():
    """Simple element-wise operations."""
    print("=== Simple Element-Wise Operations ===")
    
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    
    print(f"A: {a}")
    print(f"B: {b}")
    print(f"A + B = {a + b}")
    print(f"A - B = {a - b}")
    print(f"A * B = {a * b}")
    print(f"B / A = {b / a}")

# 2. Scalar Operations
def simple_scalar_operations():
    """Simple scalar operations."""
    print("\n=== Simple Scalar Operations ===")
    
    arr = np.array([10, 20, 30])
    
    print(f"Array: {arr}")
    print(f"Add 5: {arr + 5}")
    print(f"Multiply by 2: {arr * 2}")
    print(f"Subtract 10: {arr - 10}")
    print(f"Divide by 5: {arr / 5}")

# 3. NumPy vs Lists
def simple_comparison():
    """Simple NumPy vs lists comparison."""
    print("\n=== NumPy vs Lists ===")
    
    # Lists
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    
    # Arrays
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([4, 5, 6])
    
    print(f"Lists: {list1} + {list2} = {list1 + list2}")
    print(f"Arrays: {arr1} + {arr2} = {arr1 + arr2}")
    
    print(f"Lists: {list1} * 2 = {list1 * 2}")
    print(f"Arrays: {arr1} * 2 = {arr1 * 2}")

# 4. Common Mistakes
def simple_mistakes():
    """Simple common mistakes."""
    print("\n=== Common Mistakes ===")
    
    # Shape mismatch
    try:
        a = np.array([1, 2, 3])
        b = np.array([4, 5])  # Different shape
        result = a + b
    except ValueError:
        print("Shape mismatch error - arrays must have same shape")
    
    # Correct way
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])  # Same shape
    print(f"Correct: {a} + {b} = {a + b}")

def main():
    """Run simple demonstrations."""
    print("Simple NumPy Mathematical Operations")
    print("=" * 40)
    
    simple_element_wise()
    simple_scalar_operations()
    simple_comparison()
    simple_mistakes()
    
    print("\n" + "=" * 40)
    print("Simple examples complete!")

if __name__ == "__main__":
    main()
