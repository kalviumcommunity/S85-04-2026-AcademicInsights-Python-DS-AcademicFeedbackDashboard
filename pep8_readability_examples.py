"""
PEP 8 Readability Examples: Variable Names and Comments
This file demonstrates proper PEP 8 naming conventions and effective commenting practices.
"""

# 1. Writing Readable Variable Names

# POOR EXAMPLES - Cryptic or unclear names
def poor_naming_example():
    x = 5
    y = 10
    z = x + y
    tmp = "John"
    val = tmp + " Doe"
    return val, z

# GOOD EXAMPLES - Clear, descriptive names
def good_naming_example():
    first_number = 5
    second_number = 10
    total_sum = first_number + second_number
    first_name = "John"
    full_name = first_name + " Doe"
    return full_name, total_sum

# 2. Following PEP 8 Naming Conventions

# POOR EXAMPLES - Inconsistent or incorrect naming styles
def poor_naming_conventions():
    userName = "alice"           # camelCase (should be snake_case)
    TotalPrice = 100.50          # PascalCase (should be snake_case)
    discount_rate = 0.1           # Good snake_case
    TAX_AMOUNT = 8.25            # Constant style (good for constants)
    num_of_items = 5             # Abbreviation (could be clearer)
    
    return userName, TotalPrice, discount_rate, TAX_AMOUNT, num_of_items

# GOOD EXAMPLES - Proper PEP 8 conventions
def good_naming_conventions():
    user_name = "alice"           # snake_case for variables
    total_price = 100.50          # snake_case for variables
    discount_rate = 0.1           # snake_case for variables
    TAX_RATE = 0.08               # UPPER_CASE for constants
    number_of_items = 5           # Full words, snake_case
    
    return user_name, total_price, discount_rate, TAX_RATE, number_of_items

# 3. Writing Useful Comments

# POOR EXAMPLES - Unnecessary or obvious comments
def poor_commenting_example():
    # Add two numbers together
    result = 5 + 3  # This adds 5 and 3
    
    # Create a list
    my_list = [1, 2, 3]  # Initialize list with three numbers
    
    # Loop through the list
    for item in my_list:  # Iterate over each item
        print(item)  # Print the item

# GOOD EXAMPLES - Comments that explain intent
def good_commenting_example():
    # Calculate the total including tax for an invoice
    result = 5 + 3
    
    # Store user preferences for dashboard customization
    user_preferences = [1, 2, 3]
    
    # Process each preference to apply user settings
    for preference in user_preferences:
        apply_user_setting(preference)

def apply_user_setting(preference):
    """Apply individual user preference to the dashboard."""
    pass  # Implementation would go here

# 4. Complex Examples with Good Practices

def calculate_monthly_expenses(daily_expenses, number_of_days):
    """
    Calculate total monthly expenses from daily spending data.
    
    Args:
        daily_expenses (list): List of daily expense amounts
        number_of_days (int): Number of days in the month
        
    Returns:
        float: Total monthly expenses
    """
    # Sum all daily expenses to get monthly total
    total_expenses = sum(daily_expenses)
    
    # Adjust for partial months (if fewer than 30 days)
    if number_of_days < 30:
        # Calculate daily average and multiply by standard 30-day month
        daily_average = total_expenses / number_of_days
        monthly_total = daily_average * 30
    else:
        monthly_total = total_expenses
    
    return monthly_total

def process_student_grades(student_records):
    """
    Process student grades and calculate statistics.
    
    Args:
        student_records (list): List of student grade records
        
    Returns:
        dict: Dictionary containing grade statistics
    """
    grade_statistics = {
        'total_students': 0,
        'average_grade': 0.0,
        'highest_grade': 0,
        'lowest_grade': 100
    }
    
    # Initialize list to store all grades for calculation
    all_grades = []
    
    # Process each student record
    for student in student_records:
        student_grade = student['grade']
        all_grades.append(student_grade)
        grade_statistics['total_students'] += 1
        
        # Track highest and lowest grades
        if student_grade > grade_statistics['highest_grade']:
            grade_statistics['highest_grade'] = student_grade
        if student_grade < grade_statistics['lowest_grade']:
            grade_statistics['lowest_grade'] = student_grade
    
    # Calculate average grade if we have data
    if all_grades:
        grade_statistics['average_grade'] = sum(all_grades) / len(all_grades)
    
    return grade_statistics

# 5. Common Readability Mistakes and Corrections

# MISTAKE 1: Using single-letter variables
def poor_single_letter_variables():
    x = [1, 2, 3, 4, 5]
    y = 0
    for i in x:
        y += i
    return y

def good_descriptive_variables():
    numbers = [1, 2, 3, 4, 5]
    total_sum = 0
    for number in numbers:
        total_sum += number
    return total_sum

# MISTAKE 2: Abbreviations that aren't clear
def poor_abbreviations():
    emp_nm = "John Smith"
    emp_age = 25
    emp_dept = "IT"
    emp_sal = 50000
    return emp_nm, emp_age, emp_dept, emp_sal

def good_full_names():
    employee_name = "John Smith"
    employee_age = 25
    employee_department = "IT"
    employee_salary = 50000
    return employee_name, employee_age, employee_department, employee_salary

# MISTAKE 3: Commented-out code that should be removed
def poor_commented_out_code():
    # Old implementation - remove this
    # result = x * y
    
    # New implementation
    result = x + y
    return result

def good_clean_code():
    # Calculate the sum instead of product for business logic
    result = x + y
    return result

# MISTAKE 4: Misleading comments
def poor_misleading_comments():
    # This function calculates the average
    result = max(numbers)  # Actually returns max, not average
    return result

def good_accurate_comments():
    # Find the maximum value in the list
    result = max(numbers)
    return result

# 6. Demonstration Functions for Video Walkthrough

def demonstrate_variable_naming():
    """Show the difference between poor and good variable names."""
    print("=== Variable Naming Demonstration ===")
    
    # Poor example
    print("POOR: Cryptic variable names")
    x = 25
    y = "John"
    z = x * 12
    print(f"x: {x}, y: {y}, z: {z}")
    
    # Good example
    print("\nGOOD: Descriptive variable names")
    employee_age = 25
    employee_name = "John"
    annual_salary = employee_age * 12
    print(f"employee_age: {employee_age}, employee_name: {employee_name}, annual_salary: {annual_salary}")

def demonstrate_naming_conventions():
    """Show proper PEP 8 naming conventions."""
    print("\n=== PEP 8 Naming Conventions ===")
    
    # Variables: snake_case
    user_name = "alice"
    total_amount = 100.50
    discount_percentage = 0.15
    
    # Constants: UPPER_CASE
    MAX_LOGIN_ATTEMPTS = 3
    DEFAULT_TIMEOUT = 30
    
    print(f"Variables: {user_name}, {total_amount}, {discount_percentage}")
    print(f"Constants: {MAX_LOGIN_ATTEMPTS}, {DEFAULT_TIMEOUT}")

def demonstrate_effective_comments():
    """Show the difference between poor and good comments."""
    print("\n=== Effective Comments ===")
    
    # Poor commenting
    print("POOR: Obvious comments")
    # Add two numbers
    result = 5 + 3  # This adds 5 and 3
    
    # Good commenting
    print("\nGOOD: Intent-explaining comments")
    # Calculate base price for standard product configuration
    base_price = 5 + 3
    
    print(f"Results: {result} vs {base_price}")

def demonstrate_common_mistakes():
    """Show common readability mistakes and their corrections."""
    print("\n=== Common Mistakes and Corrections ===")
    
    # Mistake: Single letters
    print("MISTAKE: Single-letter variables")
    x = [1, 2, 3]
    s = 0
    for i in x:
        s += i
    
    print("CORRECTION: Descriptive names")
    numbers = [1, 2, 3]
    sum_total = 0
    for number in numbers:
        sum_total += number
    
    print(f"Results: {s} vs {sum_total}")

# Main demonstration function
def main():
    """Run all readability demonstrations."""
    print("PEP 8 Readability: Variable Names and Comments")
    print("=" * 50)
    
    demonstrate_variable_naming()
    demonstrate_naming_conventions()
    demonstrate_effective_comments()
    demonstrate_common_mistakes()
    
    print("\n" + "=" * 50)
    print("Readability demonstration complete!")

if __name__ == "__main__":
    main()
