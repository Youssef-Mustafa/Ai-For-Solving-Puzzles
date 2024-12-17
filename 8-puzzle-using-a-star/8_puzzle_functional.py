import tkinter as tk
from tkinter import messagebox


def compose(f, g):
    return lambda *args: f(g(*args))


def is_solvable(puzzle):
    """
    Check if the 8-puzzle is solvable based on the number of inversions.
    A puzzle is solvable if the number of inversions is even.
    """

    def flatten(puzzle, i=0, j=0, acc=()):
        if i == len(puzzle):
            return acc
        if j == len(puzzle[i]):
            return flatten(puzzle, i + 1, 0, acc)
        if puzzle[i][j] != "_":
            acc += (puzzle[i][j],)
        return flatten(puzzle, i, j + 1, acc)

    def count_inversions(arr, index=0, count=0):
        if index == len(arr):
            return count

        def inner(index_inner, count_inner):
            if index_inner == len(arr):
                return count_inner
            return inner(
                index_inner + 1,
                count_inner + (1 if arr[index] > arr[index_inner] else 0),
            )

        return count_inversions(arr, index + 1, count + inner(index + 1, 0))

    flat_puzzle = flatten(puzzle)
    inversions = count_inversions(flat_puzzle)
    return inversions % 2 == 0


def find_blank(puz, x="_"):
    if not puz:
        return None
    try:
        j = puz[0].index(x)
        return 0, j
    except ValueError:
        result = find_blank(puz[1:], x)
        if result:
            i, j = result
            return i + 1, j
    print(f"Error: Blank space '{x}' not found in puzzle: {puz}")
    return None


def swap_recursive(puzzle, a, b, row=0, col=0, current_row=()):
    """Recursive function to swap two positions in an immutable tuple with bounds check."""
    if row == len(puzzle):
        return ()
    if col == len(puzzle[0]):
        return (current_row,) + swap_recursive(puzzle, a, b, row + 1, 0)

    a_value = (
        puzzle[a[0]][a[1]]
        if 0 <= a[0] < len(puzzle) and 0 <= a[1] < len(puzzle[0])
        else None
    )
    b_value = (
        puzzle[b[0]][b[1]]
        if 0 <= b[0] < len(puzzle) and 0 <= b[1] < len(puzzle[0])
        else None
    )

    current_value = (
        b_value if (row, col) == a else a_value if (row, col) == b else puzzle[row][col]
    )
    return swap_recursive(puzzle, a, b, row, col + 1, current_row + (current_value,))


def state_transition(puz, x1, y1, x2, y2):
    """Move the blank space to a new position if valid using composition."""
    validate_move = lambda: 0 <= x2 < len(puz) and 0 <= y2 < len(puz[0])
    return compose(
        lambda _: swap_recursive(puz, (x1, y1), (x2, y2)),
        lambda _: validate_move() or None,
    )(puz)


def generate_children(puz, level, fval, goal, heuristic):
    """Generate child nodes recursively without mutable state."""
    x, y = find_blank(puz)
    if (x, y) is None:
        return ()  # Handle invalid state

    moves = ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y))

    def process_moves(moves, acc=()):
        if not moves:
            return acc
        i, j = moves[0]
        new_state = state_transition(puz, x, y, i, j)
        if new_state:
            new_node = {
                "data": new_state,
                "level": level + 1,
                "fval": heuristic(new_state, goal) + level + 1,
            }
            return process_moves(moves[1:], acc + (new_node,))
        return process_moves(moves[1:], acc)

    return process_moves(moves)


def heuristic(start, goal):
    """Functional heuristic: count misplaced tiles recursively."""

    def count_misplaced(s, g, i=0, j=0):
        if i == len(s):
            return 0
        if j == len(s[i]):
            return count_misplaced(s, g, i + 1, 0)
        return int(s[i][j] != g[i][j] and s[i][j] != "_") + count_misplaced(
            s, g, i, j + 1
        )

    return count_misplaced(start, goal)


def solve_puzzle(start, goal, heuristic_func):
    def process(open_list, closed_list):
        if not open_list:
            return closed_list
        open_list = tuple(sorted(open_list, key=lambda x: x["fval"]))
        current = open_list[0]
        closed_list += (current,)
        if heuristic_func(current["data"], goal) == 0:
            return closed_list
        children = generate_children(
            current["data"], current["level"], current["fval"], goal, heuristic_func
        )
        new_open_list = open_list[1:] + children
        return process(new_open_list, closed_list)

    if not is_solvable(start):
        raise ValueError("Puzzle is unsolvable.")
    start_node = {"data": start, "level": 0, "fval": heuristic_func(start, goal)}
    return process((start_node,), ())


def print_solution(solution):
    """Print the sequence of steps from start to goal recursively."""

    def print_step(steps):
        if not steps:
            return
        step = steps[0]
        print(f"Level: {step['level']}")

        def print_row(data, idx=0):
            if idx == len(data):
                return
            print(data[idx])
            print_row(data, idx + 1)

        print_row(step["data"])
        print()
        print_step(steps[1:])

    print_step(solution)


def get_user_input():
    print("Enter the 3x3 puzzle row by row, use '_' for the blank space:")

    def input_row(n=3, rows=()):
        if n == 0:
            return rows
        row = tuple(input(f"Row {len(rows) + 1}: ").split())
        if len(row) != 3:
            print("Each row must have exactly 3 elements. Try again.")
            return input_row(n, rows)
        return input_row(n - 1, rows + (row,))

    return input_row()


# if __name__ == "__main__":
#     # print("Enter the start state:")
#     # start_state = get_user_input()
#     # print("Enter the goal state:")
#     # goal_state = get_user_input()
#     start_state = (("2", "5", "4"), ("1", "_", "6"), ("3", "7", "8"))
#     goal_state = (("1", "2", "3"), ("4", "5", "6"), ("7", "8", "_"))
#     try:
#         print("\nSteps to solve the puzzle:")
#         solution = solve_puzzle(start_state, goal_state, heuristic)
#         print_solution(solution)
#     except ValueError as e:
#         print(e)


class PuzzleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("8-Puzzle Solver")
        self.master.geometry("500x800")  # Adjust the window size
        self.master.config(bg="#f7f0e5")

        self.grid_size = 3
        self.steps = []
        self.current_step = 0

        self.create_widgets()

    def create_widgets(self):
        # Input Frames
        self.frame_input = tk.Frame(self.master, bg="#f7f0e5")
        self.frame_input.pack(pady=20)

        self.start_label = tk.Label(
            self.frame_input,
            text="Enter Start State:",
            font=("Helvetica", 14, "bold"),
            bg="#f7f0e5",
            fg="#58554e",
        )
        self.start_label.grid(row=0, column=0, columnspan=self.grid_size, pady=5)

        self.goal_label = tk.Label(
            self.frame_input,
            text="Enter Goal State:",
            font=("Helvetica", 14, "bold"),
            bg="#f7f0e5",
            fg="#58554e",
        )
        self.goal_label.grid(
            row=self.grid_size + 1, column=0, columnspan=self.grid_size, pady=5
        )

        # Start and Goal Entries
        self.start_entries = self.create_entry_grid(1)
        self.goal_entries = self.create_entry_grid(self.grid_size + 2)

        # Buttons
        self.solve_button = tk.Button(
            self.master,
            text="Solve Puzzle Step by Step",
            font=("Helvetica", 14, "bold"),
            bg="#b6d4c5",
            fg="#58554e",
            relief="flat",
            height=2,
            command=self.solve_puzzle,
            width=25,
        )
        self.solve_button.pack(pady=15)

        self.next_button = tk.Button(
            self.master,
            text="Next Step",
            font=("Helvetica", 14, "bold"),
            bg="#58554e",
            fg="white",
            relief="flat",
            height=2,
            state="disabled",
            command=self.next_step,
            width=25,
        )
        self.next_button.pack(pady=10)

        # Puzzle Display
        self.puzzle_label = tk.Label(
            self.master,
            text="Puzzle State will be displayed here",
            font=("Courier", 16, "bold"),
            bg="#f7f0e5",
            fg="#333333",
            width=20,
            height=5,
            anchor="center",
            justify="center",
        )
        self.puzzle_label.pack(pady=10, padx=10, fill="both", expand=True)

    def create_entry_grid(self, start_row):
        entries = tuple(
            tuple(
                tk.Entry(
                    self.frame_input,
                    width=5,
                    font=("Arial", 16),
                    bd=2,
                    relief="solid",
                    justify="center",
                )
                for _ in range(self.grid_size)
            )
            for _ in range(self.grid_size)
        )
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                entries[i][j].grid(row=start_row + i, column=j, padx=10, pady=5)
        return entries

    def solve_puzzle(self):
        start = tuple(tuple(e.get() for e in row) for row in self.start_entries)
        goal = tuple(tuple(e.get() for e in row) for row in self.goal_entries)

        try:
            solution = solve_puzzle(start, goal, heuristic)
            self.steps = solution
            self.current_step = 0

            if self.steps:
                self.update_puzzle_display(self.steps[self.current_step]["data"])
                self.next_button.config(state="normal")
            else:
                messagebox.showerror("Error", "No solution found for the given puzzle.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def next_step(self):
        self.current_step += 1
        if self.current_step < len(self.steps):
            self.update_puzzle_display(self.steps[self.current_step]["data"])
        else:
            messagebox.showinfo("Puzzle Solved", "The puzzle has been solved!")
            self.next_button.config(state="disabled")

    def update_puzzle_display(self, data):
        display_text = "\n".join(" ".join(row) for row in data)
        self.puzzle_label.config(text=display_text)


# # ! if you wan run gui run this
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = PuzzleGUI(root)
#     root.mainloop()
