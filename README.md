# Running, Restarting, and Interrupting Jupyter Kernels

This milestone focuses on understanding how Jupyter kernels work and how to control them safely. Many notebook issues are not caused by code errors, but by kernel state—cells running out of order, stale variables, or long-running executions that were never interrupted.

Learning how to run, restart, and interrupt kernels correctly is essential for debugging, reproducibility, and sanity during the Data Science sprint.

This lesson is to help you:
- Understand what a Jupyter kernel is and why it matters
- Run notebook cells in a controlled way
- Restart kernels to reset notebook state
- Interrupt long-running or stuck executions safely

By completing this milestone, you will be able to:
- Identify when a kernel is running, idle, or stuck
- Restart a kernel intentionally and rerun cells
- Interrupt execution without breaking the notebook
- Maintain a clean, predictable notebook state

## Why This Matters

Common notebook problems include:
- Code working once but failing later
- Variables mysteriously changing values
- Cells depending on hidden execution order
- Kernels freezing during execution

These issues usually come from poor kernel management, not bad logic.

This milestone ensures that:
- Your notebooks behave consistently
- You can debug issues systematically
- Reviewers and teammates can reproduce your results

Think of the kernel as the engine of your notebook—this lesson teaches you how to control it.

## What You Are Expected to Do

This is a kernel control and debugging milestone, not a data analysis task.

You are expected to:
- Run cells in sequence
- Restart the kernel and observe effects
- Interrupt a running cell
- Understand when and why to use each action

No datasets or analysis are required.

## 1. Running Cells and Understanding Execution Order

Run notebook cells deliberately.

You should:
- Execute cells one by one
- Observe how outputs depend on execution order
- Understand that the kernel remembers variables until restarted

This builds awareness of hidden state in notebooks.

## 2. Restarting Kernel

Restart the kernel to reset notebook state.

You should:
- Use restart option from Jupyter menu
- Observe that variables and memory are cleared
- Rerun cells from top to restore state

This is essential for testing notebook reproducibility.

## 3. Interrupting Execution

Interrupt a running cell safely.

You should:
- Start a deliberately long-running or infinite operation
- Interrupt execution using the interrupt option
- Confirm that the notebook remains responsive afterward

This skill prevents frozen notebooks and wasted time.

## 4. Recognizing When to Restart vs Interrupt

Understand the difference between restarting and interrupting.

You should:
- Identify scenarios where interrupting is sufficient
- Identify scenarios where a full restart is safer
- Explain trade-offs between the two actions

This helps you respond correctly to notebook issues.

## 5. Video Walkthrough (~2 Minutes)

Record a short screen-capture video demonstrating kernel control.

Your video must include:
- Running cells normally
- Interrupting a running cell
- Restarting the kernel
- Rerunning cells after restart
- Brief explanation of why each action is used

## Submission Guidelines

- Submit your work as a Pull Request (if required)
- Submit video link as instructed
- Video should be approximately 2 minutes
- Video must be screen-facing and clearly visible

## Important Notes

- This milestone is about control and predictability
- Do not perform EDA or data loading
- Keep examples simple and intentional
- Always restart and rerun before final submission in real projects

Knowing how to manage kernels prevents subtle, hard-to-debug errors. This milestone ensures you can control notebook execution confidently throughout the Data Science sprint.

## Bonus Content

This section is optional, and learners who want to explore the topics covered so far can utilize the materials provided below.

- Stop Jupyter Kernel if Kernel is not responding
- Kernel Keeps dying and restarting
- Kernel Restarting

## Assignment

Complete this assignment to show your understanding of the concepts you've learned.

**Target**: Get 60% or more
**Time Limit**: 180 minutes

### Related Learning Milestones
- Understanding Notebook Cells: Code vs Markdown
- Writing Markdown for Headings, Lists, and Code Blocks in Notebooks
