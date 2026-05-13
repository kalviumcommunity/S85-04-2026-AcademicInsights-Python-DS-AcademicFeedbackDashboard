"""NumPy Broadcasting Examples

Simple, small examples demonstrating scalar, 1D-1D, and 2D-1D broadcasting.
Run this file to print shapes and results for inspection.
"""
import numpy as np


def scalar_broadcast():
    a = np.array([1, 2, 3])
    s = 5
    print("scalar_broadcast: a.shape=", a.shape)
    print("scalar_broadcast: s=", s)
    print("a + s ->", a + s)


def one_d_broadcast():
    x = np.array([1, 2, 3])        # shape (3,)
    y = np.array([10])             # shape (1,) can expand to (3,)
    print("one_d_broadcast: x.shape=", x.shape)
    print("one_d_broadcast: y.shape=", y.shape)
    print("x + y ->", x + y)

    # incompatible example
    z = np.array([1, 2])           # shape (2,) incompatible with (3,)
    print("z.shape=", z.shape)
    try:
        _ = x + z
    except ValueError as e:
        print("Expected error for incompatible shapes:", e)


def two_d_one_d_broadcast():
    M = np.array([[1, 2, 3], [4, 5, 6]])   # shape (2, 3)
    v_row = np.array([10, 20, 30])         # shape (3,) -> broadcast across rows
    v_col = np.array([100, 200])           # shape (2,) -> broadcast across columns

    print("two_d_one_d_broadcast: M.shape=", M.shape)
    print("v_row.shape=", v_row.shape)
    print("M + v_row ->")
    print(M + v_row)

    print("v_col.shape=", v_col.shape)
    print("M + v_col[:, None] -> broadcast v_col as column")
    print(M + v_col[:, None])


def broadcasting_rules_demo():
    examples = [
        ((3, 4), (4,), True),    # compatible: (3,4) with (4,) -> (3,4)
        ((3, 1), (3,), True),    # compatible: (3,1) with (3,) -> (3,3) after alignment
        ((2, 3), (3, 1), True),  # compatible via trailing dims and size-1
        ((2, 3), (2,), False),   # incompatible example
    ]
    for a_shape, b_shape, expected in examples:
        print(f"Shapes: {a_shape} vs {b_shape}, expected compatible={expected}")
        try:
            a = np.zeros(a_shape)
            b = np.zeros(b_shape)
            res = a + b
            print(" OK -> result.shape=", res.shape)
        except ValueError as e:
            print(" Error ->", e)


def main():
    print("--- Scalar broadcasting ---")
    scalar_broadcast()
    print()
    print("--- 1D broadcasting ---")
    one_d_broadcast()
    print()
    print("--- 2D and 1D broadcasting ---")
    two_d_one_d_broadcast()
    print()
    print("--- Rules demo ---")
    broadcasting_rules_demo()


if __name__ == '__main__':
    main()
