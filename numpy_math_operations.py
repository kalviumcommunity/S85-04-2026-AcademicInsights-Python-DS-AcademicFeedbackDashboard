"""
NumPy Mathematical Operations: Basic Array Arithmetic
This file demonstrates basic mathematical operations on NumPy arrays including
element-wise operations, scalar operations, and comparisons with Python lists.
"""

import numpy as np

# 1. Element-Wise Array Operations

def demonstrate_element_wise_operations():
    """Demonstrate basic element-wise operations on NumPy arrays."""
    print("=== Element-Wise Array Operations ===")
    
    # Create two arrays of the same shape
    array_a = np.array([1, 2, 3, 4, 5])
    array_b = np.array([10, 20, 30, 40, 50])
    
    print(f"Array A: {array_a}")
    print(f"Array B: {array_b}")
    
    # Addition (element-wise)
    addition_result = array_a + array_b
    print(f"\nAddition (A + B): {addition_result}")
    print("Explanation: 1+10=11, 2+20=22, 3+30=33, 4+40=44, 5+50=55")
    
    # Subtraction (element-wise)
    subtraction_result = array_b - array_a
    print(f"\nSubtraction (B - A): {subtraction_result}")
    print("Explanation: 10-1=9, 20-2=18, 30-3=27, 40-4=36, 50-5=45")
    
    # Multiplication (element-wise)
    multiplication_result = array_a * array_b
    print(f"\nMultiplication (A * B): {multiplication_result}")
    print("Explanation: 1*10=10, 2*20=40, 3*30=90, 4*40=160, 5*50=250")
    
    # Division (element-wise)
    division_result = array_b / array_a
    print(f"\nDivision (B / A): {division_result}")
    print("Explanation: 10/1=10, 20/2=10, 30/3=10, 40/4=10, 50/5=10")

def demonstrate_2d_array_operations():
    """Demonstrate element-wise operations on 2D arrays."""
    print("\n=== 2D Array Operations ===")
    
    # Create 2D arrays
    matrix_a = np.array([[1, 2], [3, 4]])
    matrix_b = np.array([[5, 6], [7, 8]])
    
    print(f"Matrix A:\n{matrix_a}")
    print(f"Matrix B:\n{matrix_b}")
    
    # Element-wise operations on 2D arrays
    sum_matrix = matrix_a + matrix_b
    print(f"\nSum (A + B):\n{sum_matrix}")
    
    product_matrix = matrix_a * matrix_b
    print(f"\nElement-wise product (A * B):\n{product_matrix}")

# 2. Scalar Operations on Arrays

def demonstrate_scalar_operations():
    """Demonstrate scalar operations on NumPy arrays."""
    print("\n=== Scalar Operations on Arrays ===")
    
    # Create an array
    numbers = np.array([1, 2, 3, 4, 5])
    print(f"Original array: {numbers}")
    
    # Add scalar to array
    addition_scalar = numbers + 10
    print(f"\nAdd 10 to each element: {addition_scalar}")
    print("Explanation: 1+10=11, 2+10=12, 3+10=13, 4+10=14, 5+10=15")
    
    # Multiply array by scalar
    multiplication_scalar = numbers * 3
    print(f"\nMultiply each element by 3: {multiplication_scalar}")
    print("Explanation: 1*3=3, 2*3=6, 3*3=9, 4*3=12, 5*3=15")
    
    # Subtract scalar from array
    subtraction_scalar = numbers - 2
    print(f"\nSubtract 2 from each element: {subtraction_scalar}")
    print("Explanation: 1-2=-1, 2-2=0, 3-2=1, 4-2=2, 5-2=3")
    
    # Divide array by scalar
    division_scalar = numbers / 2
    print(f"\nDivide each element by 2: {division_scalar}")
    print("Explanation: 1/2=0.5, 2/2=1.0, 3/2=1.5, 4/2=2.0, 5/2=2.5")

def demonstrate_scalar_2d_operations():
    """Demonstrate scalar operations on 2D arrays."""
    print("\n=== Scalar Operations on 2D Arrays ===")
    
    matrix = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"Original matrix:\n{matrix}")
    
    # Add scalar to matrix
    result = matrix + 10
    print(f"\nAdd 10 to matrix:\n{result}")

# 3. Comparing NumPy Arrays and Python Lists

def demonstrate_numpy_vs_lists():
    """Compare NumPy array behavior with Python list behavior."""
    print("\n=== NumPy Arrays vs Python Lists ===")
    
    # Python lists
    list_a = [1, 2, 3, 4, 5]
    list_b = [10, 20, 30, 40, 50]
    
    # NumPy arrays
    array_a = np.array([1, 2, 3, 4, 5])
    array_b = np.array([10, 20, 30, 40, 50])
    
    print("Python List Behavior:")
    print(f"List A: {list_a}")
    print(f"List B: {list_b}")
    
    # List addition (concatenation)
    list_sum = list_a + list_b
    print(f"List A + List B: {list_sum}")
    print("Result: Lists are concatenated, not element-wise added!")
    
    # Try list multiplication (repetition)
    list_mult = list_a * 2
    print(f"List A * 2: {list_mult}")
    print("Result: List is repeated, not element-wise multiplied!")
    
    print("\nNumPy Array Behavior:")
    print(f"Array A: {array_a}")
    print(f"Array B: {array_b}")
    
    # Array addition (element-wise)
    array_sum = array_a + array_b
    print(f"Array A + Array B: {array_sum}")
    print("Result: Arrays are added element-wise!")
    
    # Array multiplication (element-wise)
    array_mult = array_a * 2
    print(f"Array A * 2: {array_mult}")
    print("Result: Each element is multiplied!")

def demonstrate_performance_difference():
    """Show why NumPy is preferred for numerical operations."""
    print("\n=== Why NumPy is Preferred ===")
    
    # Large arrays for demonstration
    size = 1000000
    
    # Python list approach (conceptual - not actually running)
    print("Python List Approach:")
    print("- Would require loops for element-wise operations")
    print("- Much slower for large datasets")
    print("- Verbose code")
    
    # NumPy approach
    print("\nNumPy Array Approach:")
    large_array = np.arange(size)
    result = large_array * 2 + 10
    print(f"- Single operation on {size} elements: {large_array[:5]}... * 2 + 10")
    print(f"- Result sample: {result[:5]}...")
    print("- Fast and concise!")

# 4. Avoiding Common Mistakes

def demonstrate_common_mistakes():
    """Show common mistakes and how to avoid them."""
    print("\n=== Common Mistakes and Solutions ===")
    
    # Mistake 1: Incompatible shapes
    print("MISTAKE 1: Incompatible shapes")
    try:
        array1 = np.array([1, 2, 3])
        array2 = np.array([4, 5])  # Different length
        result = array1 + array2
    except ValueError as e:
        print(f"Error: {e}")
        print("Solution: Ensure arrays have compatible shapes")
    
    # Correct approach
    array1 = np.array([1, 2, 3])
    array2 = np.array([4, 5, 6])  # Same length
    result = array1 + array2
    print(f"Correct: {array1} + {array2} = {result}")
    
    # Mistake 2: Expecting list behavior from arrays
    print("\nMISTAKE 2: Expecting list concatenation")
    array1 = np.array([1, 2, 3])
    array2 = np.array([4, 5, 6])
    array_concat = array1 + array2
    print(f"Array 'concatenation': {array_concat}")
    print("This is element-wise addition, not concatenation!")
    print("For concatenation, use np.concatenate()")
    
    # Correct concatenation
    correct_concat = np.concatenate([array1, array2])
    print(f"Correct concatenation: {correct_concat}")
    
    # Mistake 3: Division by zero
    print("\nMISTAKE 3: Division by zero")
    try:
        array = np.array([1, 2, 0, 4])
        result = 10 / array
        print(f"10 / {array} = {result}")
        print("NumPy handles division by zero with 'inf' and warnings")
    except Exception as e:
        print(f"Error: {e}")

def demonstrate_shape_awareness():
    """Demonstrate the importance of shape awareness."""
    print("\n=== Shape Awareness ===")
    
    # 1D arrays
    array_1d = np.array([1, 2, 3, 4])
    print(f"1D array shape: {array_1d.shape}")
    
    # 2D arrays
    array_2d = np.array([[1, 2], [3, 4]])
    print(f"2D array shape: {array_2d.shape}")
    
    # Broadcasting example
    scalar = 5
    result = array_2d + scalar
    print(f"\nBroadcasting: {array_2d} + {scalar} =\n{result}")
    print("Scalar automatically expands to match array shape")

# 5. Demonstration Functions for Video Walkthrough

def demonstrate_basic_operations():
    """Show basic operations for video demonstration."""
    print("=== Basic NumPy Operations Demo ===")
    
    # Create arrays
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    
    print(f"Array A: {a}")
    print(f"Array B: {b}")
    
    # Show operations
    print(f"A + B = {a + b}")
    print(f"A - B = {a - b}")
    print(f"A * B = {a * b}")
    print(f"B / A = {b / a}")

def demonstrate_scalar_operations_demo():
    """Show scalar operations for video demonstration."""
    print("\n=== Scalar Operations Demo ===")
    
    arr = np.array([10, 20, 30, 40, 50])
    print(f"Original: {arr}")
    
    print(f"Add 5: {arr + 5}")
    print(f"Multiply by 2: {arr * 2}")
    print(f"Subtract 10: {arr - 10}")
    print(f"Divide by 5: {arr / 5}")

def demonstrate_comparison_demo():
    """Show NumPy vs Python lists comparison."""
    print("\n=== NumPy vs Lists Demo ===")
    
    # Lists
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    print(f"Lists: {list1} + {list2} = {list1 + list2}")
    
    # Arrays
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([4, 5, 6])
    print(f"Arrays: {arr1} + {arr2} = {arr1 + arr2}")

# Main demonstration function
def main():
    """Run all NumPy math demonstrations."""
    print("NumPy Mathematical Operations Demonstration")
    print("=" * 50)
    
    demonstrate_element_wise_operations()
    demonstrate_2d_array_operations()
    demonstrate_scalar_operations()
    demonstrate_scalar_2d_operations()
    demonstrate_numpy_vs_lists()
    demonstrate_performance_difference()
    demonstrate_common_mistakes()
    demonstrate_shape_awareness()
    
    print("\n" + "=" * 50)
    print("Video Walkthrough Summary:")
    demonstrate_basic_operations()
    demonstrate_scalar_operations_demo()
    demonstrate_comparison_demo()
    
    print("\n" + "=" * 50)
    print("NumPy math operations demonstration complete!")

if __name__ == "__main__":
    main()
