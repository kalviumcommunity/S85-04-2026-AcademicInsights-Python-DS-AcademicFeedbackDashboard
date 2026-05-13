**NumPy Broadcasting — Assignment Support**

- **Files added:** `numpy_broadcasting.py`
- **What to run:**

```bash
python numpy_broadcasting.py
```

- **Video guidance:** Record a ~2 minute screen capture that includes:
  - Running the script to show shapes and outputs
  - A scalar-to-array example
  - A 1D-to-2D example
  - A 10–20 second explanation of why broadcasting works (shape alignment and size-1 expansion)

- **Git / PR steps (local):**

```bash
# create and switch to the branch
git checkout -b feature/numpy-broadcasting

# add and commit the new files
git add numpy_broadcasting.py README_broadcasting.md
git commit -m "Add NumPy broadcasting examples and README"

# if you have a remote named 'origin', push the branch
git push -u origin feature/numpy-broadcasting

# Create a PR using GitHub web or the CLI (if installed):
# With GitHub CLI:
gh pr create --fill --title "NumPy broadcasting examples" --body "Adds small examples and README for assignment"
```

- **If I should create and push the branch now, reply and I will attempt to run the git commands.**
