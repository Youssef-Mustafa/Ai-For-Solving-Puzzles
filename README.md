# N-Queen and 8-Puzzle Solver

![Project Overview](https://github.com/user-attachments/assets/cdc0600f-19b0-4026-a7bc-aeb6a324c1fd)
![Project OverView](https://github.com/user-attachments/assets/7aad3bc0-ca42-446a-8c0e-de8034eedf01)

This project demonstrates solutions for two classic problems in computer science: the N-Queen problem and the 8-Puzzle problem. The project is implemented in Python as part of the **Concept of Programming Languages** course and explores two programming paradigms: **Imperative** and **Functional**.

---

## Table of Contents
- [Project Description](#project-description)
- [Technologies Used](#technologies-used)
- [Solutions Implemented](#solutions-implemented)

---

## Project Description

### N-Queen Problem
The N-Queen problem involves placing N queens on an N × N chessboard such that no two queens threaten each other. This project uses the **backtracking algorithm** to solve this problem.

### 8-Puzzle Problem
The 8-Puzzle problem involves sliding tiles on a 3 × 3 grid to reach a goal configuration. This project uses the **A* search algorithm** to solve the puzzle efficiently.

### Paradigms Explored
1. **Imperative Programming**: Focuses on explicit instructions, state changes, and step-by-step computations.
2. **Functional Programming**: Emphasizes immutability, higher-order functions, and declarative programming styles.

---

## Technologies Used
- **Programming Language**: Python 3.10+
- **GUI Library**: `tkinter` for building a graphical interface to visualize solutions.

---

## Solutions Implemented

### N-Queen Problem
1. **Imperative Paradigm**: 
   - Uses loops and conditionals to implement the backtracking algorithm.
   - State changes and explicit steps are logged for debugging.

2. **Functional Paradigm**:
   - Uses recursive functions and functional constructs (e.g., `map`, `filter`) to achieve the same goal.

### 8-Puzzle Problem
1. **Imperative Paradigm**:
   - Implements A* algorithm with priority queues and explicit state transitions.

2. **Functional Paradigm**:
   - Employs recursive evaluation of states, prioritization using functional constructs, and immutable data structures.

---

### Customization
- Modify the N size for N-Queen problem in `nqueen_solver.py`.
- Change the start and goal configurations for 8-Puzzle in `eight_puzzle_solver.py`.


