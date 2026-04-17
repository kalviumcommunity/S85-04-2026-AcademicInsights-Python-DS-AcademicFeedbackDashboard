"""Milestone: Python loop iteration examples.

This script demonstrates for loops, while loops, break, continue, and safe loop termination.
"""

from typing import List


def display_for_range() -> None:
    print("1. for loop over range")
    for number in range(1, 6):
        print(f"  Step {number}: square = {number ** 2}")
    print()


def display_for_list(fruits: List[str]) -> None:
    print("2. for loop over a list")
    for index, fruit in enumerate(fruits, start=1):
        print(f"  Item {index}: {fruit}")
    print()


def display_while_counter() -> None:
    print("3. while loop with condition-based repetition")
    counter = 0
    while counter < 5:
        print(f"  Counter is {counter}")
        counter += 1
    print("  Loop finished cleanly when counter reached 5")
    print()


def display_break_continue() -> None:
    print("4. controlling loop flow with break and continue")
    numbers = list(range(10))

    print("  Using continue to skip odd numbers:")
    for n in numbers:
        if n % 2 != 0:
            continue
        print(f"    even number: {n}")

    print("  Using break to stop early when 7 is reached:")
    for n in numbers:
        if n == 7:
            print("    found 7, breaking out of loop")
            break
        print(f"    checking {n}")
    print()


def main() -> None:
    display_for_range()
    display_for_list(["apple", "banana", "cherry"])
    display_while_counter()
    display_break_continue()


if __name__ == "__main__":
    main()
