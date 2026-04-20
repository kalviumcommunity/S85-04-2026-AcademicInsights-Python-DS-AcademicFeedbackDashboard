"""
Simple Examples for Function Parameters and Returns
These are focused examples perfect for demonstrating the core concepts.
"""

# Example 1: Basic parameter and return
def add_numbers(a, b):
    """Add two numbers and return the result."""
    return a + b

# Example 2: Function with string parameter
def create_username(first_name, last_name):
    """Create a username from first and last name."""
    return f"{first_name.lower()}.{last_name.lower()}"

# Example 3: Function that returns boolean
def is_adult(age):
    """Check if someone is an adult (18 or older)."""
    return age >= 18

# Example 4: Function with calculation
def calculate_tip(bill_amount, tip_percentage):
    """Calculate tip amount."""
    return bill_amount * (tip_percentage / 100)

# Example 5: Function that uses returned value
def calculate_total_with_tip(bill_amount, tip_percentage):
    """Calculate total bill including tip."""
    tip = calculate_tip(bill_amount, tip_percentage)
    return bill_amount + tip

# Demonstration of using these functions
def demonstrate_simple_examples():
    """Show how to use these simple functions."""
    
    # Example 1: Adding numbers
    result1 = add_numbers(5, 3)
    print(f"5 + 3 = {result1}")
    
    # Example 2: Creating username
    username = create_username("John", "Doe")
    print(f"Username: {username}")
    
    # Example 3: Checking age
    adult_check = is_adult(21)
    print(f"Is 21 an adult? {adult_check}")
    
    # Example 4: Calculating tip
    tip_amount = calculate_tip(50.00, 15)
    print(f"Tip on $50.00 (15%): ${tip_amount:.2f}")
    
    # Example 5: Total with tip
    total = calculate_total_with_tip(50.00, 15)
    print(f"Total with tip: ${total:.2f}")

if __name__ == "__main__":
    demonstrate_simple_examples()
