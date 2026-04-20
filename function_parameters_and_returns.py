"""
Python Functions: Parameters and Returns
This file demonstrates proper parameter passing and return values in Python functions.
"""

# 1. Understanding Parameters and Arguments

def greet_user(name):
    """
    Function that accepts a parameter and returns a greeting.
    
    Args:
        name (str): The name of the user to greet
        
    Returns:
        str: A personalized greeting message
    """
    return f"Hello, {name}! Welcome to Python functions."

def calculate_rectangle_area(length, width):
    """
    Function with multiple parameters.
    
    Args:
        length (float): The length of the rectangle
        width (float): The width of the rectangle
        
    Returns:
        float: The area of the rectangle
    """
    return length * width

def calculate_cylinder_volume(radius, height):
    """
    Function that uses mathematical operations and returns a result.
    
    Args:
        radius (float): The radius of the cylinder
        height (float): The height of the cylinder
        
    Returns:
        float: The volume of the cylinder
    """
    import math
    return math.pi * radius ** 2 * height

# 2. Returning Values from Functions

def is_even(number):
    """
    Function that returns a boolean value.
    
    Args:
        number (int): The number to check
        
    Returns:
        bool: True if the number is even, False otherwise
    """
    return number % 2 == 0

def get_grade_score(score):
    """
    Function that returns different values based on conditions.
    
    Args:
        score (int): The numerical score (0-100)
        
    Returns:
        str: The letter grade
    """
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

def find_maximum(numbers):
    """
    Function that returns the maximum value from a list.
    
    Args:
        numbers (list): List of numbers
        
    Returns:
        int/float: The maximum value in the list
    """
    if not numbers:
        return None
    
    max_value = numbers[0]
    for num in numbers:
        if num > max_value:
            max_value = num
    return max_value

# 3. Using Returned Results

def calculate_discounted_price(original_price, discount_percentage):
    """
    Function that calculates discounted price.
    
    Args:
        original_price (float): The original price
        discount_percentage (float): Discount percentage (0-100)
        
    Returns:
        float: The discounted price
    """
    discount_amount = original_price * (discount_percentage / 100)
    return original_price - discount_amount

def calculate_tax_amount(price, tax_rate):
    """
    Function that calculates tax amount.
    
    Args:
        price (float): The price before tax
        tax_rate (float): Tax rate as a decimal (e.g., 0.08 for 8%)
        
    Returns:
        float: The tax amount
    """
    return price * tax_rate

def calculate_final_price(original_price, discount_percentage, tax_rate):
    """
    Function that uses other functions to calculate final price.
    
    Args:
        original_price (float): The original price
        discount_percentage (float): Discount percentage (0-100)
        tax_rate (float): Tax rate as a decimal
        
    Returns:
        float: The final price after discount and tax
    """
    # Use returned values from other functions
    discounted_price = calculate_discounted_price(original_price, discount_percentage)
    tax_amount = calculate_tax_amount(discounted_price, tax_rate)
    final_price = discounted_price + tax_amount
    return final_price

# 4. Avoiding Common Function Mistakes

# BAD EXAMPLE - Hardcoded values and printing instead of returning
def bad_calculate_area():
    """Bad example: hardcoded values and prints instead of returning."""
    length = 5  # Hardcoded
    width = 3   # Hardcoded
    area = length * width
    print(f"The area is: {area}")  # Printing instead of returning

# GOOD EXAMPLE - Flexible parameters and return values
def good_calculate_area(length, width):
    """Good example: uses parameters and returns value."""
    return length * width

# BAD EXAMPLE - Mixing print and return incorrectly
def bad_check_number(number):
    """Bad example: mixes print and return."""
    if number > 0:
        print("Positive number")
        return True
    else:
        print("Negative or zero")
        # Missing return statement here!

# GOOD EXAMPLE - Clear return behavior
def good_check_number(number):
    """Good example: consistent return behavior."""
    if number > 0:
        return True
    else:
        return False

# 5. Demonstration Functions for Video Walkthrough

def demonstrate_basic_parameters():
    """Demonstrate basic parameter passing."""
    print("=== Basic Parameter Demonstration ===")
    
    # Call function with different arguments
    message1 = greet_user("Alice")
    message2 = greet_user("Bob")
    
    print(message1)
    print(message2)

def demonstrate_multiple_parameters():
    """Demonstrate functions with multiple parameters."""
    print("\n=== Multiple Parameters Demonstration ===")
    
    # Calculate areas with different dimensions
    area1 = calculate_rectangle_area(5, 3)
    area2 = calculate_rectangle_area(10, 4)
    
    print(f"Rectangle 1 area: {area1}")
    print(f"Rectangle 2 area: {area2}")
    
    # Calculate cylinder volume
    volume = calculate_cylinder_volume(2, 5)
    print(f"Cylinder volume: {volume:.2f}")

def demonstrate_returned_values():
    """Demonstrate using returned values."""
    print("\n=== Using Returned Values Demonstration ===")
    
    # Store and use returned values
    numbers = [15, 42, 8, 23, 67]
    max_num = find_maximum(numbers)
    print(f"Maximum number in {numbers}: {max_num}")
    
    # Check if numbers are even
    for num in numbers[:3]:
        even_check = is_even(num)
        print(f"Is {num} even? {even_check}")
    
    # Get grades
    scores = [95, 82, 74, 58]
    for score in scores:
        grade = get_grade_score(score)
        print(f"Score {score} gets grade: {grade}")

def demonstrate_function_composition():
    """Demonstrate composing functions together."""
    print("\n=== Function Composition Demonstration ===")
    
    # Calculate final price using multiple functions
    original_price = 100.0
    discount = 10  # 10%
    tax_rate = 0.08  # 8%
    
    final_price = calculate_final_price(original_price, discount, tax_rate)
    
    print(f"Original price: ${original_price:.2f}")
    print(f"Discount: {discount}%")
    print(f"Tax rate: {tax_rate * 100:.0f}%")
    print(f"Final price: ${final_price:.2f}")

def demonstrate_common_mistakes():
    """Demonstrate common mistakes and their solutions."""
    print("\n=== Common Mistakes Demonstration ===")
    
    print("BAD: Hardcoded function")
    print("This function always calculates area for 5x3:")
    bad_calculate_area()  # Always the same result
    
    print("\nGOOD: Flexible function")
    area1 = good_calculate_area(5, 3)
    area2 = good_calculate_area(10, 4)
    print(f"Area 1: {area1}, Area 2: {area2}")
    
    print("\nBAD: Inconsistent return behavior")
    result1 = bad_check_number(5)
    print(f"Bad check result for positive: {result1}")
    result2 = bad_check_number(-3)  # This returns None!
    print(f"Bad check result for negative: {result2}")
    
    print("\nGOOD: Consistent return behavior")
    result3 = good_check_number(5)
    print(f"Good check result for positive: {result3}")
    result4 = good_check_number(-3)
    print(f"Good check result for negative: {result4}")

# Main demonstration function
def main():
    """Run all demonstrations."""
    print("Python Functions: Parameters and Returns Demonstration")
    print("=" * 60)
    
    demonstrate_basic_parameters()
    demonstrate_multiple_parameters()
    demonstrate_returned_values()
    demonstrate_function_composition()
    demonstrate_common_mistakes()
    
    print("\n" + "=" * 60)
    print("Demonstration complete!")

if __name__ == "__main__":
    main()
