import tkinter as tk
from tkinter import messagebox


class Node:
    """
    This class represents a node in the puzzle search tree for solving problems like the 8-puzzle.
    Each node contains a configuration of the puzzle, the depth of the node (level),
    and a heuristic value (fval), which helps in guiding the search towards the goal.
    """

    def __init__(self, data, level, fval):
        """
        Initializes the node with a given puzzle configuration, its level in the search tree,
        and the associated heuristic value.

        Args:
            data (list of list): 2D list representing the puzzle configuration.
            level (int): The depth of the current node in the search tree.
            fval (int or float): The heuristic value (or cost) of the node, used in search algorithms like A*.
        """
        self.data = data  # Current puzzle configuration (2D list)
        self.level = level  # Depth in the search tree (number of moves from root)
        self.fval = fval  # Heuristic value or cost (typically 0 for non-leaf nodes)

    def generate_child(self):
        """
        Generates child nodes by moving the blank space ('_') in the four possible directions: up, down, left, right.

        Returns:
            list: A list of child Node objects representing new puzzle configurations.
        """
        x, y = self.find(self.data, "_")  # Find the position of the blank space ('_')

        # List of possible moves (up, down, left, right)
        val_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        children = []

        # For each possible move, generate a child node if the move is valid
        for i in val_list:
            child = self.state_transition(
                self.data, x, y, i[0], i[1]
            )  # Try to shuffle the puzzle
            if child is not None:
                # Create a new node with the updated puzzle configuration, incremented level, and fval set to 0
                child_node = Node(child, self.level + 1, 0)
                children.append(child_node)

        return children

    def state_transition(self, puz, x1, y1, x2, y2):
        """
        Attempts to move the blank space in the puzzle from position (x1, y1) to (x2, y2).
        Returns a new puzzle configuration if the move is valid, or None if the move is out of bounds.

        Args:
            puz (list of list): The current puzzle configuration.
            x1 (int): The current row of the blank space.
            y1 (int): The current column of the blank space.
            x2 (int): The target row for the blank space.
            y2 (int): The target column for the blank space.

        Returns:
            list of list or None: A new puzzle configuration after the move, or None if the move is invalid.
        """
        if x2 >= 0 and x2 < len(puz) and y2 >= 0 and y2 < len(puz[0]):
            # Valid move: Create a deep copy of the puzzle and perform the swap
            temp_puz = self.copy(puz)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            # Invalid move: Out of bounds
            return None

    def copy(self, root):
        """
        Creates a deep copy of the given puzzle (2D list) to avoid modifying the original puzzle.

        Args:
            root (list of list): The puzzle to copy.

        Returns:
            list of list: A deep copy of the puzzle.
        """
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)  # Copy each element
            temp.append(t)  # Append copied row to the new puzzle
        return temp

    def find(self, puz, x):
        """
        Finds the position of a given element (typically the blank space '_') in the puzzle.

        Args:
            puz (list of list): The puzzle configuration to search through.
            x (str): The element to search for (usually '_').

        Returns:
            tuple: A tuple (i, j) representing the row and column index of the element x in the puzzle.
        """
        for i in range(len(puz)):
            for j in range(len(puz[i])):
                if puz[i][j] == x:
                    return i, j  # Return the row and column index of the blank space


class Puzzle:
    """
    This class represents a puzzle-solving problem using a heuristic search algorithm (such as A*).
    It manages the puzzle state, processes the algorithm step by step, and calculates the heuristic values.
    """

    def __init__(self, size):
        """
        Initializes the puzzle with the specified size and prepares empty lists for open and closed nodes.

        Args:
            size (int): The size of the puzzle grid (e.g., 3 for a 3x3 puzzle).
        """
        self.n = size  # Puzzle size (n x n)
        self.open = []  # List of open nodes (nodes to be explored)
        self.closed = []  # List of closed nodes (nodes already explored)

    def total_cost(self, start, goal):
        """
        Calculates the f-value (total cost) for the current node using the heuristic function.

        f(x) = h(x) + g(x)
        Where:
            h(x) is the heuristic value (estimated cost to reach the goal from x)
            g(x) is the actual cost (or depth) to reach node x from the start (level)

        Args:
            start (Node): The current node being evaluated.
            goal (list of list): The goal state of the puzzle.

        Returns:
            int: The total cost (f-value) of the current node.
        """
        return (
            self.heuristic(start.data, goal) + start.level
        )  # Heuristic value + depth (level)

    def heuristic(self, start, goal):
        """
        Heuristic function that calculates the difference (misplaced tiles) between the current state
        and the goal state of the puzzle.

        This heuristic counts the number of tiles that are in the wrong position, excluding the blank space ('_').

        Args:
            start (list of list): The current puzzle configuration.
            goal (list of list): The goal puzzle configuration.

        Returns:
            int: The number of misplaced tiles (excluding the blank space).
        """
        temp = 0  # Initialize the count of misplaced tiles
        for i in range(self.n):
            for j in range(self.n):
                # Increment the count if the tile is misplaced and not the blank space
                if start[i][j] != goal[i][j] and start[i][j] != "_":
                    temp += 1
        return temp

    def process(self, start, goal, puzzle_display, next_step_callback):
        """
        Solves the puzzle step by step using a search algorithm (like A*) and updates the state at each step.

        The algorithm processes the puzzle by exploring nodes in the open list and generating child nodes
        until it reaches the goal configuration. After each step, the next step is shown via the callback.

        Args:
            start (list of list): The initial puzzle configuration.
            goal (list of list): The goal puzzle configuration.
            puzzle_display (function): Function to display the puzzle state (not used in this method but passed for integration).
            next_step_callback (function): A callback function to call at each step, passing the puzzle states for display.

        Returns:
            list: A list of Node objects representing the sequence of puzzle states from start to goal.
        """
        # Initialize the start node with the initial configuration, level 0, and f-value set to 0
        start_node = Node(start, 0, 0)
        start_node.fval = self.total_cost(
            start_node, goal
        )  # Calculate the f-value of the start node
        self.open.append(start_node)  # Add the start node to the open list

        steps = []  # List to store the sequence of steps (nodes)

        # Start the puzzle-solving loop
        while True:
            # Get the current node from the open list (the node with the lowest f-value)
            cur = self.open[0]
            steps.append(cur)  # Add current node to the steps list

            # Check if the goal is reached (no misplaced tiles)
            if self.heuristic(cur.data, goal) == 0:
                break  # Goal reached, stop the loop

            # Generate child nodes from the current node
            for i in cur.generate_child():
                i.fval = self.total_cost(
                    i, goal
                )  # Calculate the f-value for each child
                self.open.append(i)  # Add the child node to the open list

            # Move the current node to the closed list (explored nodes)
            self.closed.append(cur)
            del self.open[0]  # Remove the current node from the open list

            # Sort the open list based on f-value (lowest f-value first)
            self.open.sort(key=lambda x: x.fval, reverse=False)

        # Call the callback function to process the next step and display the puzzle state
        next_step_callback(steps)

        # Return the sequence of steps taken to solve the puzzle
        return steps


def is_solvable(puzzle):
    """
    Checks if the given puzzle is solvable.
    Solvable condition: Count inversions. If odd, unsolvable; if even, solvable.

    Args:
        puzzle (list of list): 2D list representing the puzzle configuration.

    Returns:
        bool: True if solvable, False otherwise.
    """
    flat_puzzle = [num for row in puzzle for num in row if num != "_"]
    inversions = 0

    # Count inversions in the flattened puzzle
    for i in range(len(flat_puzzle)):
        for j in range(i + 1, len(flat_puzzle)):
            if flat_puzzle[i] > flat_puzzle[j]:
                inversions += 1

    return inversions % 2 == 0


class PuzzleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("8-Puzzle Solver")
        self.master.geometry("500x800")  # Adjust the window size
        self.master.config(bg="#f7f0e5")  # Set background color for the whole window

        # Initialize the puzzle grid size (3x3 for this example)
        self.grid_size = 3
        self.puzzle = Puzzle(self.grid_size)
        self.steps = []
        self.current_step = 0

        self.create_widgets()

    def create_widgets(self):
        # Frame for the input section with padding and background color
        self.frame_input = tk.Frame(self.master, bg="#f7f0e5")
        self.frame_input.pack(pady=20)

        # Title labels with modern font and new color palette
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

        # Entry widgets for start state puzzle with modern design
        self.start_entries = [
            [
                tk.Entry(
                    self.frame_input,
                    width=5,
                    font=("Arial", 16),
                    bd=2,
                    relief="solid",
                    justify="center",
                    highlightbackground="#000000",
                    highlightthickness=2,
                )
                for _ in range(self.grid_size)
            ]
            for _ in range(self.grid_size)
        ]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.start_entries[i][j].grid(row=i + 1, column=j, padx=10, pady=5)

        # Entry widgets for goal state puzzle
        self.goal_entries = [
            [
                tk.Entry(
                    self.frame_input,
                    width=5,
                    font=("Arial", 16),
                    bd=2,
                    relief="solid",
                    justify="center",
                    highlightbackground="#000000",
                    highlightthickness=2,
                )
                for _ in range(self.grid_size)
            ]
            for _ in range(self.grid_size)
        ]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.goal_entries[i][j].grid(
                    row=i + self.grid_size + 2, column=j, padx=10, pady=5
                )

        # Solve button with flat style, light greenish background
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

        # Next step button with flat style, dark olive green background
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

        # Label to display the puzzle with grid-style layout and light cream background
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

    def solve_puzzle(self):
        """Solve the puzzle when button is pressed"""
        start = self.get_puzzle_state(self.start_entries)
        goal = self.get_puzzle_state(self.goal_entries)

        # Validate if the puzzle is solvable
        if not is_solvable(start):
            messagebox.showerror("Unsolvable Puzzle", "The puzzle cannot be solved!")
            return

        self.steps = self.puzzle.process(
            start, goal, self.update_puzzle_display, self.prepare_next_step
        )
        self.update_puzzle_display(self.steps[self.current_step])
        self.next_button.config(state="normal")

    def get_puzzle_state(self, entries):
        """Get the puzzle state from the entry widgets"""
        state = []
        for i in range(self.grid_size):
            row = [entries[i][j].get() for j in range(self.grid_size)]
            state.append(row)
        return state

    def update_puzzle_display(self, step):
        """Update the puzzle display with the current step"""
        display_text = "\n".join([" ".join(row) for row in step.data])
        self.puzzle_label.config(text=display_text)

    def prepare_next_step(self, steps):
        """Prepare the next step to show in the GUI"""
        self.steps = steps

    def next_step(self):
        """Move to the next step in the puzzle solving"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.update_puzzle_display(self.steps[self.current_step])
        else:
            messagebox.showinfo("Puzzle Solved", "The puzzle has been solved!")


root = tk.Tk()
app = PuzzleGUI(root)
root.mainloop()
