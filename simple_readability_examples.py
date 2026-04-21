"""
Simple PEP 8 Readability Examples
Focused examples for demonstrating variable naming and commenting best practices.
"""

# POOR: Cryptic variable names
def poor_example():
    x = 25
    n = "Alice"
    a = x * 12
    return n, a

# GOOD: Descriptive variable names
def good_example():
    employee_age = 25
    employee_name = "Alice"
    annual_salary = employee_age * 12
    return employee_name, annual_salary

# POOR: Wrong naming conventions
def poor_conventions():
    userName = "bob"      # camelCase
    TotalPrice = 99.99    # PascalCase
    numItems = 5          # Abbreviation
    return userName, TotalPrice, numItems

# GOOD: Proper PEP 8 conventions
def good_conventions():
    user_name = "bob"      # snake_case
    total_price = 99.99    # snake_case
    number_of_items = 5    # Full words, snake_case
    return user_name, total_price, number_of_items

# POOR: Unnecessary comments
def poor_comments():
    # Add two numbers
    result = 5 + 3  # This adds 5 and 3
    return result

# GOOD: Useful comments
def good_comments():
    # Calculate base price for standard configuration
    base_price = 5 + 3
    return base_price

# Constants should be UPPER_CASE
MAX_LOGIN_ATTEMPTS = 3
DEFAULT_TIMEOUT = 30
TAX_RATE = 0.08

def demonstrate_simple_examples():
    """Show simple readability examples."""
    print("=== Simple Readability Examples ===")
    
    # Variable naming
    print("POOR: x, n, a")
    print("GOOD: employee_age, employee_name, annual_salary")
    
    # Naming conventions
    print("\nPOOR: userName, TotalPrice, numItems")
    print("GOOD: user_name, total_price, number_of_items")
    
    # Comments
    print("\nPOOR: # Add two numbers")
    print("GOOD: # Calculate base price for standard configuration")
    
    # Constants
    print(f"\nConstants: MAX_LOGIN_ATTEMPTS = {MAX_LOGIN_ATTEMPTS}")

if __name__ == "__main__":
    demonstrate_simple_examples()
