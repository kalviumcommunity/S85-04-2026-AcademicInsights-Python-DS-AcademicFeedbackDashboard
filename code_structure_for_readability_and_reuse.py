"""
Milestone: Structuring Python Code for Readability and Reuse

This script demonstrates:
1) Clear code sections
2) Reusable helper functions
3) Separation of setup, logic, and execution
4) Readable, maintainable structure
"""

from statistics import mean

# ============================================================
# 1. Configuration and Sample Data
# ============================================================

ASSIGNMENT_WEIGHT = 0.40
EXAM_WEIGHT = 0.60
PASSING_SCORE = 60

STUDENT_RECORDS = [
    {"name": "Aarav", "assignment_score": 78, "exam_score": 84},
    {"name": "Diya", "assignment_score": 92, "exam_score": 88},
    {"name": "Kabir", "assignment_score": 60, "exam_score": 55},
    {"name": "Meera", "assignment_score": 85, "exam_score": 79},
]


# ============================================================
# 2. Reusable Helper Functions
# ============================================================


def calculate_weighted_score(assignment_score, exam_score):
    """Return the weighted final score for one student."""
    return (assignment_score * ASSIGNMENT_WEIGHT) + (exam_score * EXAM_WEIGHT)



def get_letter_grade(score):
    """Return a letter grade for a numeric score."""
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"



def has_passed(score):
    """Return True if a student meets the passing threshold."""
    return score >= PASSING_SCORE



def format_student_line(student_summary):
    """Return one formatted output line for the report."""
    status = "PASS" if student_summary["passed"] else "FAIL"
    return (
        f"{student_summary['name']:<10} | "
        f"Final: {student_summary['final_score']:>6.2f} | "
        f"Grade: {student_summary['grade']} | "
        f"Status: {status}"
    )


# ============================================================
# 3. Core Business Logic
# ============================================================


def build_student_summary(student_record):
    """Transform raw student record into a reusable summary dictionary."""
    final_score = calculate_weighted_score(
        student_record["assignment_score"],
        student_record["exam_score"],
    )

    return {
        "name": student_record["name"],
        "final_score": final_score,
        "grade": get_letter_grade(final_score),
        "passed": has_passed(final_score),
    }



def build_all_student_summaries(student_records):
    """Create summaries for every student using reusable logic."""
    return [build_student_summary(record) for record in student_records]



def build_class_summary(student_summaries):
    """Return overall class metrics from student summaries."""
    final_scores = [student["final_score"] for student in student_summaries]
    passing_count = sum(1 for student in student_summaries if student["passed"])

    return {
        "student_count": len(student_summaries),
        "average_score": mean(final_scores) if final_scores else 0,
        "highest_score": max(final_scores) if final_scores else 0,
        "lowest_score": min(final_scores) if final_scores else 0,
        "pass_rate": (passing_count / len(student_summaries) * 100)
        if student_summaries
        else 0,
    }


# ============================================================
# 4. Presentation / Output Logic
# ============================================================


def print_report(student_summaries, class_summary):
    """Print a readable report with student and class level sections."""
    print("=" * 66)
    print("CLASS PERFORMANCE REPORT")
    print("=" * 66)

    print("\nStudent Results")
    print("-" * 66)
    for student in student_summaries:
        print(format_student_line(student))

    print("\nClass Summary")
    print("-" * 66)
    print(f"Total Students : {class_summary['student_count']}")
    print(f"Average Score  : {class_summary['average_score']:.2f}")
    print(f"Highest Score  : {class_summary['highest_score']:.2f}")
    print(f"Lowest Score   : {class_summary['lowest_score']:.2f}")
    print(f"Pass Rate      : {class_summary['pass_rate']:.2f}%")


# ============================================================
# 5. Minimal Execution Entry Point
# ============================================================


def main():
    """Run the script with clean top-level execution."""
    student_summaries = build_all_student_summaries(STUDENT_RECORDS)
    class_summary = build_class_summary(student_summaries)
    print_report(student_summaries, class_summary)


if __name__ == "__main__":
    main()
