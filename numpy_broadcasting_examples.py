"""NumPy broadcasting simple examples for Kalvium A8 assignment.

Includes:
- scalar-to-array
- 1D with 1D (compatible/incompatible)
- 2D with 1D (row/column)

Each example prints shapes and results and contains simple asserts.
"""
import numpy as np


def scalar_broadcast():
    a = np.array([1, 2, 3])
    s = 5
    print("scalar_broadcast: a.shape=", a.shape)
    print("scalar_broadcast: s=", s)
    r = a + s
    print("result:", r)
    assert np.all(r == np.array([6, 7, 8]))


def one_d_broadcast():
    x = np.array([1, 2, 3])
    y = np.array([10])  # length-1 can broadcast
    print("one_d_broadcast: x.shape=", x.shape, "y.shape=", y.shape)
    r = x + y
    print("result:", r)
    assert r.shape == x.shape

    # incompatible shapes example (will raise ValueError if uncommented)
    # z = np.array([1,2])
    # x + z  # shapes (3,) and (2,) incompatible


def two_d_with_1d():
    M = np.array([[1, 2, 3], [4, 5, 6]])  # shape (2,3)
    v_row = np.array([10, 20, 30])  # shape (3,) aligns to columns
    print("two_d_with_1d: M.shape=", M.shape, "v_row.shape=", v_row.shape)
    r1 = M + v_row
    print("row-wise result:\n", r1)
    assert r1.shape == M.shape

    v_col = np.array([[100], [200]])  # shape (2,1) aligns to rows
    print("v_col.shape=", v_col.shape)
    r2 = M + v_col
    print("column-wise result:\n", r2)
    assert r2.shape == M.shape


def explain_rules():
    # Rightmost-first alignment and size 1 is expandable
    a = np.zeros((4, 1, 3))
    b = np.ones((    5, 3))  # treated as (1,5,3)
    print("explain_rules: a.shape=", a.shape, "b.shape=", b.shape)
    # result will be (4,5,3)
    r = a + b
    print("broadcasted shape:", r.shape)
    assert r.shape == (4, 5, 3)


def run_all():
    print("Running NumPy broadcasting examples...\n")
    scalar_broadcast()
    print()
    one_d_broadcast()
    print()
    two_d_with_1d()
    print()
    explain_rules()
    print("\nAll examples completed successfully.")


if __name__ == "__main__":
    run_all()
